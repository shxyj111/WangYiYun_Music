# 获得歌曲歌词链接
import re
import json
import requests
import os  # 添加这行导入
from NetEaseMusicEncrypt import NetEaseMusicEncrypt


class LyricFetcher():
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

    # 在这里添加 _sanitize_filename 方法
    def _sanitize_filename(self, filename):
        """
        清理文件名，移除或替换非法字符

        Args:
            filename: 原始文件名

        Returns:
            str: 清理后的文件名
        """
        # 替换路径分隔符和其他可能的问题字符
        invalid_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
        for char in invalid_chars:
            filename = filename.replace(char, '_')

        # 移除多余的空格和点
        filename = filename.strip().rstrip('.')

        return filename

    def get_song_lyrics_data(self, song_id):
        """
        获取歌曲下载链接

        Args:
            song_id: 歌曲ID，如果提供则动态生成加密参数

        Returns:
            str: API响应文本
        """
        # 如果提供了song_id，动态生成加密参数
        encryptor = NetEaseMusicEncrypt()
        encrypted_data = encryptor.get_song_lyric_data(song_id)  # 假设encrypt模块有这个方法
        self.data = encrypted_data

        response = requests.post(
            'https://music.163.com/weapi/song/lyric',
            params=self.params,
            cookies=self.cookies,
            headers=self.headers,
            data=self.data,
        )

        return response.text

    def save_lyric_as_lrc(self, json_data, output_file=None, song_title="", artist="", output_dir="./my_music"):
        """
        将网易云音乐歌词JSON数据保存为LRC文件

        Args:
            json_data: 网易云音乐API返回的歌词JSON数据
            output_file: 输出LRC文件名，如果为None则自动生成
            song_title: 歌曲标题
            artist: 歌手名
            output_dir: 输出目录，默认为"./my_music"

        Returns:
            str: 生成的LRC文件路径
        """
        # 如果输入是字符串，则解析JSON
        if isinstance(json_data, str):
            data = json.loads(json_data)
        else:
            data = json_data

        # 提取歌词信息
        original_lrc = data.get('lrc', {}).get('lyric', '')
        translated_lrc = data.get('tlyric', {}).get('lyric', '')

        # 解析原歌词和翻译歌词
        original_lines = self._parse_lrc_text(original_lrc)
        translated_lines = self._parse_lrc_text(translated_lrc)

        # 创建时间戳到歌词的映射
        original_dict = {line['timestamp']: line['text'] for line in original_lines if line['text'].strip()}
        translated_dict = {line['timestamp']: line['text'] for line in translated_lines if line['text'].strip()}

        # 合并歌词
        merged_lines = self._merge_lyrics(original_dict, translated_dict)

        # 生成LRC内容
        lrc_content = self._generate_lrc_content(merged_lines, song_title, artist, data)

        # 确定输出文件名
        if output_file is None:
            if song_title and artist:
                output_file = f"{artist} - {song_title}.lrc"
            else:
                output_file = f"song_{data.get('id', 'unknown')}.lrc"

        # 确保文件扩展名为.lrc
        if not output_file.endswith('.lrc'):
            output_file += '.lrc'

        # 清理文件名中的非法字符
        output_file = self._sanitize_filename(output_file)

        # 确保输出目录存在
        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)

        # 构建完整的文件路径
        full_output_path = os.path.join(output_dir, output_file)

        # 保存文件
        with open(full_output_path, 'w', encoding='utf-8') as f:
            f.write(lrc_content)

        print(f"LRC文件已保存: {full_output_path}")
        return full_output_path

    def _parse_lrc_text(self, lrc_text):
        """
        解析LRC格式文本

        Args:
            lrc_text: LRC格式的文本

        Returns:
            list: 包含时间戳和歌词的字典列表
        """
        lines = []

        # 正则表达式匹配时间戳和歌词
        pattern = r'\[(\d+):(\d+)\.(\d+)\](.*)'

        for line in lrc_text.split('\n'):
            match = re.match(pattern, line.strip())
            if match:
                minutes, seconds, milliseconds, text = match.groups()

                # 计算总毫秒数
                total_ms = (int(minutes) * 60 + int(seconds)) * 1000 + int(milliseconds.ljust(3, '0')[:3])

                lines.append({
                    'timestamp': total_ms,
                    'text': text.strip()
                })

        return lines

    def _merge_lyrics(self, original_dict, translated_dict):
        """
        合并原歌词和翻译歌词

        Args:
            original_dict: 原歌词字典 {时间戳: 歌词}
            translated_dict: 翻译歌词字典 {时间戳: 歌词}

        Returns:
            list: 合并后的歌词列表，每个元素为(时间戳, 原歌词, 翻译歌词)
        """
        # 获取所有时间戳并排序
        all_timestamps = sorted(set(original_dict.keys()) | set(translated_dict.keys()))

        merged = []
        for timestamp in all_timestamps:
            original = original_dict.get(timestamp, '')
            translation = translated_dict.get(timestamp, '')

            # 如果原歌词或翻译歌词为空，跳过
            if original or translation:
                merged.append((timestamp, original, translation))

        return merged

    def _format_timestamp(self, milliseconds):
        """
        将毫秒数格式化为LRC时间戳

        Args:
            milliseconds: 毫秒数

        Returns:
            str: 格式化的时间戳 [MM:SS.xx]
        """
        total_seconds = milliseconds / 1000
        minutes = int(total_seconds // 60)
        seconds = int(total_seconds % 60)
        centiseconds = int((milliseconds % 1000) / 10)

        return f"[{minutes:02d}:{seconds:02d}.{centiseconds:02d}]"

    def _generate_lrc_content(self, merged_lines, song_title, artist, original_data):
        """
        生成LRC文件内容

        Args:
            merged_lines: 合并后的歌词列表
            song_title: 歌曲标题
            artist: 歌手名
            original_data: 原始数据

        Returns:
            str: LRC文件内容
        """
        lines = []

        # 添加元数据
        if song_title:
            lines.append(f"[ti:{song_title}]")
        if artist:
            lines.append(f"[ar:{artist}]")

        # 从原始数据中提取编辑者信息
        lyric_user = original_data.get('lyricUser', {})
        if lyric_user.get('nickname'):
            lines.append(f"[by:{lyric_user['nickname']}]")

        lines.append("[offset:0]")
        lines.append("")  # 空行分隔元数据和歌词

        # 添加歌词内容
        for timestamp, original, translation in merged_lines:
            time_str = self._format_timestamp(timestamp)

            # 添加原歌词
            if original:
                lines.append(f"{time_str} {original}")

            # 添加翻译歌词（使用相同的时间戳）
            if translation:
                lines.append(f"{time_str} {translation}")

        return '\n'.join(lines)

    def get_and_save_lyric(self, song_id, output_file=None, song_title="", artist="", output_dir="./my_music"):
        """
        获取歌词并保存为LRC文件的便捷方法

        Args:
            song_id: 歌曲ID
            output_file: 输出文件名
            song_title: 歌曲标题
            artist: 歌手名
            output_dir: 输出目录，默认为"./my_music"

        Returns:
            str: 生成的LRC文件路径
        """
        # 获取歌词数据
        lyric_data = self.get_song_lyrics_data(song_id)

        # 保存为LRC文件
        return self.save_lyric_as_lrc(lyric_data, output_file, song_title, artist, output_dir)


if __name__ == '__main__':
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
        'JSESSIONID-WYYY': 'u2rQ1GzahTCm0PhdNQ3oDdE%2Fei6%2B6Ixy4gwoKpGAFwU4%2F2aMzRw6bmnnla8ZapAe%2FjoKUbDaC5aex0q3Xw9eK%5CzXoPm9cU%2F41aE4OlQzCK1aut04WdFgN5KOzDeCCi9uyuDVXp1cApwrgTc0%2BlhCRBIIKDr8rgSOHFxF%2BPTWBEC%2Bpprh%3A1763275351420',
        'WM_NI': '%2F4vivyIOV%2BHgC5hTHSMzoPtzQOcHxLc9l19QoRKHr7fViZ3tTPLvAPgyFDfCek9gwz6%2BVxGJPpGJmKo7UIANWgWzy8RSu%2Bs7%2BnjvpUvhkkb%2F9igYln24aKZKhPUXP8EcY3A%3D',
        'WM_NIKE': '9ca17ae2e6ffcda170e2e6eea5b259929a8e88b67ae9b48ba6c15a929f9eb1c73aa19c85abc9348d92a4abfc2af0fea7c3b92aedecba8af5738b919acccb6d81eba8b5cb598fa6a1b1f7729391ada9fb48a1e7a4d2bc5bad8e85a9f13da68aa7bbb28098908497c45ca5a78aa5e549a7b5f788f672f6f59a99c64294b089abf041ade99baac44695b9999bfc34928dbbccf23de9b2a697f35fb6b8a58ce125fbb7a9baef66f2ecafacd941ac909bb9d33487bd97d4c437e2a3',
        'MUSIC_U': '000D80B0B0A7C9093BBDD0CEB9A2A5952AFC0FA2C05AAE68CE92E3DBF056C8112749BED1FE0DE315C1C505931556FDD368FBE2645CC3399B45F59370B0AF6A62C6DE362AC5A4DF4BADFEE5C3E78B9919BB7318D475A7680577E155E2E23D98C296722FB3F2114A9D13C713CE60C42DDB44AE43C93228ACE216C4285F87174C60407591C23B2ADA747CD21C58BF51BAD30FB6978AAF147E751E910691694DEE7857695F5E235484C8F65E1C3A8B9E29437486D0F65152868D85E9432FA9B817D3A8367262317496F4027560DB3590B0BDD49EEAF0D30ABC41D7E1C7EE305F07114F643FE138DBDA607ECFF310E3173E837803EE2518B029F6E75243F24BC23DB3009CB58DBDD77537159307EB7665B465FE975ADF96F4F5DABEA0BC2CB7DB981BFBB5A1C0688FB7DF16D95A3152320B3C8D1B3F1A93A049602722560DEB00E3EEE6CE698F098CDD98DA6B4B18E0CA704913B690F7AFCE78CF524E7A857944FBF805823D34B3832080F5DDC352EC12A994C9D083CCADBBD3A47396D9831D962DD3D02581BB3CF6130FF255F15958035A4A9E',
        '__csrf': '31772756571df4b2b0b354852f7f421e',
        'gdxidpyhxdE': 'ENHAsWddrT335yVBeGyw56R3Z65QRDqZ%2FqiamkPH7cQKutcTtG2btqJ83EaYUzbduQwX5DcB2%5CG%2Bhzi3K%2FtGwaEPTNpts8Akm2btA3i3VubgwxOKySK4nyZwGmRu0%2FtwHt2L%2Bh27JubmCEiO5MulygHPXBjplLIkX1UQW2RTyP%2FNhNmi%3A1763275311182',
        'playerid': '22237740',
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
    }

    params = {
        'csrf_token': 'b394367d854d672cc86a21b5fe5de014',
    }

    song_id = '496869422'

    lyrics = LyricFetcher(params, cookies, headers)

    # 方法1：获取歌词数据并手动保存
    re_text = lyrics.get_song_lyrics_data(song_id)
    print("原始JSON响应:")
    print(re_text)

    # 保存为LRC文件，保存到./my_music目录
    lrc_file = lyrics.save_lyric_as_lrc(
        re_text,
        output_file="Lemon.lrc",
        song_title="Lemon",
        artist="米津玄師",
        output_dir="./my_music"  # 指定保存目录
    )

    # 方法2：使用便捷方法一次性完成
    # lrc_file = lyrics.get_and_save_lyric(
    #     song_id,
    #     output_file="米津玄師 - Lemon.lrc",
    #     song_title="Lemon",
    #     artist="米津玄師",
    #     output_dir="./my_music"  # 指定保存目录
    # )

    print(f"LRC文件已生成: {lrc_file}")