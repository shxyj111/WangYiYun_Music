# 获得歌曲图片和歌名和歌手和歌曲专辑
import re
import requests
import os
from urllib.parse import urlparse


class ImageFetcher:
    def __init__(self, cookies, headers):
        self.params = None
        self.cookies = cookies
        self.headers = headers

    def get_song_img_data(self, song_id):
        self.params = {
            'id': f'{song_id}'
        }
        response = requests.get(
            'https://music.163.com/song',
            params=self.params,
            cookies=self.cookies,
            headers=self.headers,
        )
        return response.text

    def extract_song_info(self, html_text):
        """
        从HTML中提取歌名和歌手信息

        Args:
            html_text: HTML文本内容

        Returns:
            dict: 包含歌曲信息的字典
        """
        song_info = {
            'id': self.params['id'],
            'song': '',
            'singer': ''
        }

        try:
            # 提取歌名 - 从title标签中获取
            title_pattern = r'<title>(.*?) - (.*?) - 单曲 - 网易云音乐</title>'
            title_match = re.search(title_pattern, html_text)
            # 提取专辑信息 - 新增正则表达式
            # 方法1：从meta标签中提取
            album_meta_pattern = r'<meta property="og:music:album" content="(.*?)"/>'
            album_meta_match = re.search(album_meta_pattern, html_text)

            if title_match and album_meta_match:
                song_info['song'] = title_match.group(1)
                song_info['singer'] = title_match.group(2)
                song_info['album'] = album_meta_match.group(1)
            else:
                # 备用方法：从页面内容中提取
                song_pattern = r'<em class="f-ff2">(.*?)</em>'
                artist_pattern = r'歌手：<span title="(.*?)"><a class="s-fc7"'
                album_pattern = r'所属专辑：<a[^>]*>(.*?)</a>'

                song_match = re.search(song_pattern, html_text)
                artist_match = re.search(artist_pattern, html_text)
                album_match = re.search(album_pattern, html_text)

                if song_match:
                    song_info['song'] = song_match.group(1)
                if artist_match:
                    song_info['singer'] = artist_match.group(1)
                if album_match:
                    song_info['album'] = album_match.group(1)


        except Exception as e:
            print(f"提取歌曲信息时出错: {e}")

        return song_info

    def extract_and_convert_image_url(self, html_text):
        """
        从HTML中提取图片链接并转换为HTTPS
        """
        pattern = r'<img[^>]*src="(http://[^"]+)"[^>]*>'
        match = re.search(pattern, html_text)

        if match:
            original_url = match.group(1)
            https_url = re.sub(r'^http://', 'https://', original_url)
            return https_url
        return None

    def download_image(self, img_url, save_folder='song_images', filename=None):
        """
        下载图片到本地
        """
        try:
            if not os.path.exists(save_folder):
                os.makedirs(save_folder)

            if filename is None:
                parsed_url = urlparse(img_url)
                url_filename = os.path.basename(parsed_url.path)
                if not url_filename or url_filename == 'null':
                    filename = f"song_{self.params['id']}.jpg"
                else:
                    filename = url_filename
            else:
                if not filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                    filename += '.jpg'

            filepath = os.path.join(save_folder, filename)

            response = requests.get(img_url, stream=True, timeout=30)
            response.raise_for_status()

            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            print(f"✅ 图片下载成功: {filepath}")
            return filepath

        except Exception as e:
            print(f"❌ 图片下载失败: {e}")
            return None


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

    # 测试不同的歌曲ID
    test_ids = ['536622304','411314659']  # 你可以添加更多ID

    for song_id in test_ids:
        print(f"\n=== 处理歌曲ID: {song_id} ===")

        img_fetcher = ImageFetcher(cookies, headers)
        html_data = img_fetcher.get_song_img_data(song_id)
        # print(html_data)

        # 提取歌曲信息
        song_info = img_fetcher.extract_song_info(html_data)
        print(f"提取到的歌曲信息: {song_info}")

        # 格式化输出
        formatted_output = f"[id: {song_info['id']}, song_name: {song_info['song']}, singer: {song_info['singer']}, album: {song_info['album']}]"
        print(f"格式化结果: {formatted_output}")

        # 提取并下载图片
        img_url = img_fetcher.extract_and_convert_image_url(html_data)
        print(f"获取到的图片链接: {img_url}")

        if img_url:
            downloaded_path = img_fetcher.download_image(img_url)
            if downloaded_path:
                print(f"图片已保存到: {downloaded_path}")
            else:
                print("图片下载失败")
        else:
            print("未能获取到图片链接")