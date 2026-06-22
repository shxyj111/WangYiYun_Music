# 获取歌曲本体链接
import requests
import json
import re
import os
from urllib.parse import urlparse
from pathlib import Path

from NetEaseMusicEncrypt import NetEaseMusicEncrypt


class NetEaseMusicDownloader:
    def __init__(self, params, cookies, headers):
        """
        初始化NetEaseMusicDownloader类

        Args:
            params: 请求参数
            cookies: 网站cookies
            headers: 请求头信息
            data: 请求数据，如果为None则使用默认数据
        """
        self.params = params
        self.cookies = cookies
        self.headers = headers
        self.data = None

    def get_song_download_url(self, song_id):
        """
        获取歌曲下载链接

        Args:
            song_id: 歌曲ID，如果提供则动态生成加密参数

        Returns:
            str: API响应文本
        """
        # 如果提供了song_id，动态生成加密参数
        encryptor = NetEaseMusicEncrypt()
        encrypted_data = encryptor.get_song_download_data(song_id)  # 假设encrypt模块有这个方法
        self.data = encrypted_data

        response = requests.post(
            'https://music.163.com/weapi/song/enhance/player/url/v1',
            params=self.params,
            cookies=self.cookies,
            headers=self.headers,
            data=self.data,
        )

        return response.text

    @staticmethod
    def extract_and_convert_url(json_response):
        """
        从网易云音乐API响应中提取歌曲URL并转换为HTTPS

        Args:
            json_response: API响应文本

        Returns:
            str: 转换后的HTTPS URL
        """
        try:
            data = json.loads(json_response)
            if data and 'data' in data and len(data['data']) > 0:
                original_url = data['data'][0].get('url')
                if original_url:
                    # 将http替换为https
                    https_url = re.sub(r'^http://', 'https://', original_url)
                    return https_url
        except Exception as e:
            print(f"提取URL时出错: {e}")

        return None

    def set_audio_metadata(self, file_path, title, artist, album=None):
        """
        设置音频文件的元数据（歌名、歌手等）
        需要安装mutagen库: pip install mutagen

        Args:
            file_path: 音频文件路径
            title: 歌曲名称
            artist: 歌手名称
            album: 专辑名称（可选）
        """
        try:
            from mutagen import File
            from mutagen.id3 import ID3, TIT2, TPE1, TALB
            from mutagen.mp4 import MP4, MP4Cover

            audio = File(file_path, easy=True)

            if audio is None:
                print("无法读取音频文件元数据")
                return False

            # 设置基本元数据
            audio['title'] = title
            audio['artist'] = artist
            if album:
                audio['album'] = album

            # 保存元数据
            audio.save()
            print(f"已设置元数据: {artist} - {title}")
            return True

        except ImportError:
            print("请安装mutagen库: pip install mutagen")
            return False
        except Exception as e:
            print(f"设置元数据时出错: {e}")
            return False

    def download_song_with_custom_name(self, download_url, file_name, artist_name=None, output_dir='./downloads',
                                       set_metadata=True):
        """
        下载歌曲并重命名文件，可设置歌手名称

        Args:
            download_url: 歌曲下载链接
            file_name: 自定义文件名（不含扩展名）
            artist_name: 歌手名称（可选）
            output_dir: 输出目录
            set_metadata: 是否设置音频元数据

        Returns:
            str: 下载的文件路径
        """
        # 确保输出目录存在
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        # 从URL中提取文件扩展名
        parsed_url = urlparse(download_url)
        file_extension = Path(parsed_url.path).suffix or '.m4a'

        # 清理文件名中的非法字符
        file_name = self._sanitize_filename(file_name)
        # 构建完整的文件路径
        full_file_name = f"{file_name}{file_extension}"
        file_path = os.path.join(output_dir, full_file_name)

        print(f"开始下载: {file_name}")
        if artist_name:
            print(f"歌手: {artist_name}")
        print(f"下载链接: {download_url}")

        try:
            # 发送请求
            response = requests.get(download_url, stream=True)
            response.raise_for_status()

            # 获取文件大小
            total_size = int(response.headers.get('content-length', 0))
            downloaded_size = 0

            # 写入文件
            with open(file_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
                        downloaded_size += len(chunk)

                        # 显示进度
                        if total_size > 0:
                            progress = (downloaded_size / total_size) * 100
                            print(f"\r下载进度: {progress:.2f}%", end='', flush=True)

            print(f"\n下载完成: {full_file_name}")

            # 设置音频元数据
            if set_metadata and artist_name:
                self.set_audio_metadata(file_path, file_name, artist_name)

            return file_path

        except requests.exceptions.RequestException as e:
            # 如果下载失败，删除不完整的文件
            if os.path.exists(file_path):
                os.remove(file_path)
            raise Exception(f"下载失败: {str(e)}")

    def _sanitize_filename(self, filename):
        """
        清理文件名，移除或替换非法字符

        Args:
            filename: 原始文件名

        Returns:
            str: 清理后的文件名
        """
        if not filename:
            return "unknown"

        # 替换路径分隔符和其他可能的问题字符
        invalid_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|', '\0']
        for char in invalid_chars:
            filename = filename.replace(char, '_')

        # 移除多余的空格和点
        filename = filename.strip().rstrip('.')

        # 如果文件名太长，截断
        if len(filename) > 100:
            filename = filename[:100]

        # 如果文件名为空，使用默认值
        if not filename:
            filename = "unknown_song"

        return filename

    def download_song_by_id(self, song_id, file_name, artist_name=None, output_dir='./downloads', set_metadata=True):
        """
        根据歌曲ID下载歌曲并重命名，可设置歌手名称

        Args:
            song_id: 歌曲ID
            file_name: 自定义文件名
            artist_name: 歌手名称（可选）
            output_dir: 输出目录
            set_metadata: 是否设置音频元数据

        Returns:
            str: 下载的文件路径
        """
        # 获取下载链接
        response_json = self.get_song_download_url(song_id)
        download_url = self.extract_and_convert_url(response_json)

        if download_url:
            # 下载歌曲
            return self.download_song_with_custom_name(download_url, file_name, artist_name, output_dir, set_metadata)
        else:
            raise Exception("无法获取歌曲下载链接")

    def batch_download_songs(self, song_list, output_dir='./downloads', set_metadata=True):
        """
        批量下载多首歌曲，支持设置歌手名称

        Args:
            song_list: 歌曲列表，格式为 [(song_id, file_name), ...] 或 [(song_id, file_name, artist_name), ...]
            output_dir: 输出目录
            set_metadata: 是否设置音频元数据

        Returns:
            list: 成功下载的文件路径列表
        """
        success_files = []
        for song_info in song_list:
            try:
                if len(song_info) == 2:
                    song_id, file_name = song_info
                    artist_name = None
                elif len(song_info) == 3:
                    song_id, file_name, artist_name = song_info
                else:
                    print(f"无效的歌曲信息格式: {song_info}")
                    continue

                file_path = self.download_song_by_id(song_id, file_name, artist_name, output_dir, set_metadata)
                success_files.append(file_path)
                print(f"成功下载: {file_name}" + (f" - {artist_name}" if artist_name else ""))
            except Exception as e:
                print(f"下载失败 {file_name}: {e}")

        return success_files


if __name__ == '__main__':
    # 使用示例
    cookies = {
        '_iuqxldmzr_': '32',
        '_ntes_nuid': '3b1c0fc15c337315c7fff08a919ffab9',
        'WEVNSM': '1.0.0',
        'WM_TID': 'WheyCB61HcVFFEBUAAKE%2FXN9u5%2FjUVMv',
        'ntes_kaola_ad': '1',
        '_ga': 'GA1.1.1013376860.1722333820',
        '_ntes_nnid': '3b1c0fc15c337315c7fff08a919ffab9,1743451927144',
        '_ga_EPDQHDTJH5': 'GS2.1.s1755358963$o1$g0$t1755358963$j60$l0$h0',
        'NTES_P_UTID': 'df16zZIVzyOI0nRoElzQVtO5el5IRdqE|1762264992',
        'nts_mail_user': '13368984287@163.com:-1:1',
        '__csrf': 'b394367d854d672cc86a21b5fe5de014',
        'NMTID': '00OUtoKEfn5GdT7HEkNmOcp0zYKxPIAAAGaXsDdug',
        'WNMCID': 'joybak.1762526290735.01.0',
        'sDeviceId': 'YD-pI4WY76lXmxEU1QRAEOQ%2BHMs%2B8rjT8X4',
        '__snaker__id': 'qmYpS5lxKP3kpNya',
        'P_INFO': '13368984287|1762603866|1|music|00&99|null&null&null#bej&null#10#0|&0|null|13368984287',
        'ntes_utid': 'tid._.8rtEadkQJRNAUlAUVRLQ%252BCYp%252F8vmW5Db._.0.%2C.edd._.._.0',
        'timing_user_id': 'time_HuNoQfGPhk',
        '_ga_C6TGHFPQ1H': 'GS2.1.s1762845822$o3$g0$t1762845822$j60$l0$h0',
        '_clck': '1wr32hr%5E2%5Eg0x%5E0%5E2058',
        'WM_NI': '%2F4vivyIOV%2BHgC5hTHSMzoPtzQOcHxLc9l19QoRKHr7fViZ3tTPLvAPgyFDfCek9gwz6%2BVxGJPpGJmKo7UIANWgWzy8RSu%2Bs7%2BnjvpUvhkkb%2F9igYln24aKZKhPUXP8EcY3A%3D',
        'WM_NIKE': '9ca17ae2e6ffcda170e2e6eea5b259929a8e88b67ae9b48ba6c15a929f9eb1c73aa19c85abc9348d92a4abfc2af0fea7c3b92aedecba8af5738b919acccb6d81eba8b5cb598fa6a1b1f7729391ada9fb48a1e7a4d2bc5bad8e85a9f13da68aa7bbb28098908497c45ca5a78aa5e549a7b5f788f672f6f59a99c64294b089abf041ade99baac44695b9999bfc34928dbbccf23de9b2a697f35fb6b8a58ce125fbb7a9baef66f2ecafacd941ac909bb9d33487bd97d4c437e2a3',
        'MUSIC_U': '000D80B0B0A7C9093BBDD0CEB9A2A5952AFC0FA2C05AAE68CE92E3DBF056C8112749BED1FE0DE315C1C505931556FDD368FBE2645CC3399B45F59370B0AF6A62C6DE362AC5A4DF4BADFEE5C3E78B9919BB7318D475A7680577E155E2E23D98C296722FB3F2114A9D13C713CE60C42DDB44AE43C93228ACE216C4285F87174C60407591C23B2ADA747CD21C58BF51BAD30FB6978AAF147E751E910691694DEE7857695F5E235484C8F65E1C3A8B9E29437486D0F65152868D85E9432FA9B817D3A8367262317496F4027560DB3590B0BDD49EEAF0D30ABC41D7E1C7EE305F07114F643FE138DBDA607ECFF310E3173E837803EE2518B029F6E75243F24BC23DB3009CB58DBDD77537159307EB7665B465FE975ADF96F4F5DABEA0BC2CB7DB981BFBB5A1C0688FB7DF16D95A3152320B3C8D1B3F1A93A049602722560DEB00E3EEE6CE698F098CDD98DA6B4B18E0CA704913B690F7AFCE78CF524E7A857944FBF805823D34B3832080F5DDC352EC12A994C9D083CCADBBD3A47396D9831D962DD3D02581BB3CF6130FF255F15958035A4A9E',
        '__csrf': '31772756571df4b2b0b354852f7f421e',
        'gdxidpyhxdE': 'ENHAsWddrT335yVBeGyw56R3Z65QRDqZ%2FqiamkPH7cQKutcTtG2btqJ83EaYUzbduQwX5DcB2%5CG%2Bhzi3K%2FtGwaEPTNpts8Akm2btA3i3VubgwxOKySK4nyZwGmRu0%2FtwHt2L%2Bh27JubmCEiO5MulygHPXBjplLIkX1UQW2RTyP%2FNhNmi%3A1763275311182',
        'JSESSIONID-WYYY': 'owVvWXbunBn9e832ut1P6W0ujNBJ3MG7AjrygeC9NdsgD2OdVeDC0oIHQgnJTah4oXS4%2BHxujp63HAq4ebVWgOrwpx7UDc3jx5Qs6XjdJa2TsNTHjqk2%5Cw%5C8PCOo58l%2FuvaHHhF4ow09%2Bgmmwx%2FoYzacnPHPk5TMEm1Jj8fzK4%2FRGWDi%3A1763301465204',
        'playerid': '42424108',
    }

    headers = {
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'cache-control': 'no-cache',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://music.163.com',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://music.163.com/',
        'sec-ch-ua': '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
        # 'cookie': '_iuqxldmzr_=32; _ntes_nuid=3b1c0fc15c337315c7fff08a919ffab9; WEVNSM=1.0.0; WM_TID=WheyCB61HcVFFEBUAAKE%2FXN9u5%2FjUVMv; ntes_kaola_ad=1; _ga=GA1.1.1013376860.1722333820; _ntes_nnid=3b1c0fc15c337315c7fff08a919ffab9,1743451927144; _ga_EPDQHDTJH5=GS2.1.s1755358963$o1$g0$t1755358963$j60$l0$h0; NTES_P_UTID=df16zZIVzyOI0nRoElzQVtO5el5IRdqE|1762264992; nts_mail_user=13368984287@163.com:-1:1; __csrf=b394367d854d672cc86a21b5fe5de014; NMTID=00OUtoKEfn5GdT7HEkNmOcp0zYKxPIAAAGaXsDdug; WNMCID=joybak.1762526290735.01.0; sDeviceId=YD-pI4WY76lXmxEU1QRAEOQ%2BHMs%2B8rjT8X4; __snaker__id=qmYpS5lxKP3kpNya; P_INFO=13368984287|1762603866|1|music|00&99|null&null&null#bej&null#10#0|&0|null|13368984287; ntes_utid=tid._.8rtEadkQJRNAUlAUVRLQ%252BCYp%252F8vmW5Db._.0.%2C.edd._.._.0; timing_user_id=time_HuNoQfGPhk; _ga_C6TGHFPQ1H=GS2.1.s1762845822$o3$g0$t1762845822$j60$l0$h0; _clck=1wr32hr%5E2%5Eg0x%5E0%5E2058; WM_NI=%2F4vivyIOV%2BHgC5hTHSMzoPtzQOcHxLc9l19QoRKHr7fViZ3tTPLvAPgyFDfCek9gwz6%2BVxGJPpGJmKo7UIANWgWzy8RSu%2Bs7%2BnjvpUvhkkb%2F9igYln24aKZKhPUXP8EcY3A%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eea5b259929a8e88b67ae9b48ba6c15a929f9eb1c73aa19c85abc9348d92a4abfc2af0fea7c3b92aedecba8af5738b919acccb6d81eba8b5cb598fa6a1b1f7729391ada9fb48a1e7a4d2bc5bad8e85a9f13da68aa7bbb28098908497c45ca5a78aa5e549a7b5f788f672f6f59a99c64294b089abf041ade99baac44695b9999bfc34928dbbccf23de9b2a697f35fb6b8a58ce125fbb7a9baef66f2ecafacd941ac909bb9d33487bd97d4c437e2a3; MUSIC_U=000D80B0B0A7C9093BBDD0CEB9A2A5952AFC0FA2C05AAE68CE92E3DBF056C8112749BED1FE0DE315C1C505931556FDD368FBE2645CC3399B45F59370B0AF6A62C6DE362AC5A4DF4BADFEE5C3E78B9919BB7318D475A7680577E155E2E23D98C296722FB3F2114A9D13C713CE60C42DDB44AE43C93228ACE216C4285F87174C60407591C23B2ADA747CD21C58BF51BAD30FB6978AAF147E751E910691694DEE7857695F5E235484C8F65E1C3A8B9E29437486D0F65152868D85E9432FA9B817D3A8367262317496F4027560DB3590B0BDD49EEAF0D30ABC41D7E1C7EE305F07114F643FE138DBDA607ECFF310E3173E837803EE2518B029F6E75243F24BC23DB3009CB58DBDD77537159307EB7665B465FE975ADF96F4F5DABEA0BC2CB7DB981BFBB5A1C0688FB7DF16D95A3152320B3C8D1B3F1A93A049602722560DEB00E3EEE6CE698F098CDD98DA6B4B18E0CA704913B690F7AFCE78CF524E7A857944FBF805823D34B3832080F5DDC352EC12A994C9D083CCADBBD3A47396D9831D962DD3D02581BB3CF6130FF255F15958035A4A9E; __csrf=31772756571df4b2b0b354852f7f421e; gdxidpyhxdE=ENHAsWddrT335yVBeGyw56R3Z65QRDqZ%2FqiamkPH7cQKutcTtG2btqJ83EaYUzbduQwX5DcB2%5CG%2Bhzi3K%2FtGwaEPTNpts8Akm2btA3i3VubgwxOKySK4nyZwGmRu0%2FtwHt2L%2Bh27JubmCEiO5MulygHPXBjplLIkX1UQW2RTyP%2FNhNmi%3A1763275311182; JSESSIONID-WYYY=owVvWXbunBn9e832ut1P6W0ujNBJ3MG7AjrygeC9NdsgD2OdVeDC0oIHQgnJTah4oXS4%2BHxujp63HAq4ebVWgOrwpx7UDc3jx5Qs6XjdJa2TsNTHjqk2%5Cw%5C8PCOo58l%2FuvaHHhF4ow09%2Bgmmwx%2FoYzacnPHPk5TMEm1Jj8fzK4%2FRGWDi%3A1763301465204; playerid=42424108',
    }

    params = {
        'csrf_token': 'b394367d854d672cc86a21b5fe5de014',
    }

    song_id = '496869422'

    # 创建下载器实例
    downloader = NetEaseMusicDownloader(params, cookies, headers)

    # 方法1: 使用固定数据下载，包含歌手名称
    try:
        response_json = downloader.get_song_download_url(song_id)
        download_url = downloader.extract_and_convert_url(response_json)

        if download_url:
            file_path = downloader.download_song_with_custom_name(
                download_url,
                "我的自定义歌曲名",
                "自定义歌手名",  # 新增：设置歌手名称
                "./my_music"
            )
            print(f"文件已保存到: {file_path}")
        else:
            print("无法获取下载链接")

    except Exception as e:
        print(f"下载失败: {e}")

    # print("\n" + "=" * 50 + "\n")
    #
    # # 方法2: 根据歌曲ID下载（需要动态生成加密参数），包含歌手名称
    # try:
    #     # 假设我们有歌曲ID和对应的文件名
    #     song_id = "1961500054"  # 替换为实际歌曲ID
    #     file_name = "七里香"
    #     artist_name = "周杰伦"  # 新增：设置歌手名称
    #
    #     file_path = downloader.download_song_by_id(song_id, file_name, artist_name, "./my_music")
    #     print(f"文件已保存到: {file_path}")
    #
    # except Exception as e:
    #     print(f"根据ID下载失败: {e}")
    #
    # print("\n" + "=" * 50 + "\n")
    #
    # # 方法3: 批量下载，包含歌手名称
    # try:
    #     song_list = [
    #         ("1961500054", "七里香", "周杰伦"),
    #         ("123456", "江南", "林俊杰"),
    #         ("789012", "富士山下", "陈奕迅")
    #     ]
    #
    #     success_files = downloader.batch_download_songs(song_list, "./batch_downloads")
    #     print(f"成功下载 {len(success_files)} 首歌曲")
    #
    # except Exception as e:
    #     print(f"批量下载失败: {e}")