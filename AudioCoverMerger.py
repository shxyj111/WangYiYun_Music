# 负责将专辑图片和音乐文件合并
import os
import re

from mutagen import File
from mutagen.id3 import ID3, APIC, TIT2, TPE1, TALB
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4, MP4Cover
from mutagen.flac import FLAC, Picture
from pathlib import Path


class AudioCoverMerger:
    def __init__(self):
        pass

    def set_audio_cover(self, audio_path, cover_path, title=None, artist=None, album=None):
        """
        为音频文件添加封面图片和元数据

        Args:
            audio_path: 音频文件路径
            cover_path: 封面图片路径
            title: 歌曲标题
            artist: 歌手
            album: 专辑名称
        """
        try:
            # 获取文件扩展名
            audio_ext = Path(audio_path).suffix.lower()
            cover_ext = Path(cover_path).suffix.lower()

            # 读取封面图片数据
            with open(cover_path, 'rb') as f:
                cover_data = f.read()

            # 根据音频格式处理
            if audio_ext in ['.mp3', '.m4a', '.aac']:
                return self._set_cover_mp3_m4a(audio_path, cover_data, cover_ext, title, artist, album)
            elif audio_ext == '.flac':
                return self._set_cover_flac(audio_path, cover_data, cover_ext, title, artist, album)
            else:
                print(f"不支持的音频格式: {audio_ext}")
                return False

        except Exception as e:
            print(f"设置封面失败: {e}")
            return False

    def _set_cover_mp3_m4a(self, audio_path, cover_data, cover_ext, title, artist, album):
        """为MP3/M4A文件设置封面"""
        try:
            # 确定MIME类型
            if cover_ext in ['.jpg', '.jpeg']:
                mime_type = 'image/jpeg'
            elif cover_ext == '.png':
                mime_type = 'image/png'
            else:
                mime_type = 'image/jpeg'  # 默认

            # 处理MP3文件
            if audio_path.lower().endswith('.mp3'):
                audio = MP3(audio_path, ID3=ID3)

                # 确保有ID3标签
                try:
                    audio.add_tags()
                except:
                    pass

                # 添加封面
                audio.tags.add(APIC(
                    encoding=3,  # UTF-8
                    mime=mime_type,
                    type=3,  # 封面图片
                    desc='Cover',
                    data=cover_data
                ))

                # 设置其他元数据
                if title:
                    audio.tags.add(TIT2(encoding=3, text=title))
                if artist:
                    audio.tags.add(TPE1(encoding=3, text=artist))
                if album:
                    audio.tags.add(TALB(encoding=3, text=album))

                audio.save()

            # 处理M4A文件
            elif audio_path.lower().endswith(('.m4a', '.mp4')):
                audio = MP4(audio_path)

                # 添加封面
                if cover_ext in ['.jpg', '.jpeg']:
                    audio['covr'] = [MP4Cover(cover_data, imageformat=MP4Cover.FORMAT_JPEG)]
                elif cover_ext == '.png':
                    audio['covr'] = [MP4Cover(cover_data, imageformat=MP4Cover.FORMAT_PNG)]

                # 设置其他元数据
                if title:
                    audio['\xa9nam'] = [title]
                if artist:
                    audio['\xa9ART'] = [artist]
                if album:
                    audio['\xa9alb'] = [album]

                audio.save()

            print(f"✅ 封面设置成功: {audio_path}")
            return True

        except Exception as e:
            print(f"设置MP3/M4A封面失败: {e}")
            return False

    def _set_cover_flac(self, audio_path, cover_data, cover_ext, title, artist, album):
        """为FLAC文件设置封面"""
        try:
            audio = FLAC(audio_path)

            # 创建图片对象
            picture = Picture()
            picture.data = cover_data

            if cover_ext in ['.jpg', '.jpeg']:
                picture.mime = 'image/jpeg'
                picture.type = 3  # 封面图片
            elif cover_ext == '.png':
                picture.mime = 'image/png'
                picture.type = 3

            # 添加图片
            audio.clear_pictures()
            audio.add_picture(picture)

            # 设置其他元数据
            if title:
                audio['title'] = [title]
            if artist:
                audio['artist'] = [artist]
            if album:
                audio['album'] = [album]

            audio.save()
            print(f"✅ FLAC封面设置成功: {audio_path}")
            return True

        except Exception as e:
            print(f"设置FLAC封面失败: {e}")
            return False

    def batch_set_covers(self, audio_folder, cover_folder, output_folder=None):
        """
        批量设置封面

        Args:
            audio_folder: 音频文件文件夹
            cover_folder: 封面图片文件夹
            output_folder: 输出文件夹（如果为None则覆盖原文件）
        """
        if output_folder and not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # 获取音频文件列表
        audio_files = []
        for ext in ['.mp3', '.m4a', '.flac', '.aac']:
            audio_files.extend(list(Path(audio_folder).glob(f'*{ext}')))

        success_count = 0
        for audio_file in audio_files:
            try:
                # 查找对应的封面文件
                cover_file = Path(cover_folder) / f"{audio_file.stem}.jpg"
                if not cover_file.exists():
                    cover_file = Path(cover_folder) / f"{audio_file.stem}.png"
                    if not cover_file.exists():
                        print(f"❌ 未找到封面文件: {audio_file.stem}")
                        continue

                # 确定输出路径
                if output_folder:
                    output_path = Path(output_folder) / audio_file.name
                    # 复制原文件到输出目录
                    import shutil
                    shutil.copy2(audio_file, output_path)
                    target_file = output_path
                else:
                    target_file = audio_file

                # 设置封面
                if self.set_audio_cover(str(target_file), str(cover_file)):
                    success_count += 1

            except Exception as e:
                print(f"❌ 处理失败 {audio_file.name}: {e}")

        print(f"🎉 批量处理完成: {success_count}/{len(audio_files)} 个文件成功")
        return success_count


# 使用示例
if __name__ == "__main__":
    merger = AudioCoverMerger()

    # 单个文件处理
    merger.set_audio_cover(
        audio_path="./my_music/歌曲名.m4a",
        cover_path="./song_images/歌曲封面.jpg",
        title="歌曲名",
        artist="歌手名",
        album="专辑名"
    )

    # 批量处理
    # merger.batch_set_covers(
    #     audio_folder="./my_music",
    #     cover_folder="./song_images",
    #     output_folder="./my_music_with_covers"
    # )