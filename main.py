from AudioCoverMerger import AudioCoverMerger
from NetEaseMusicPlaylist import NetEaseMusicPlaylist
from NetEaseMusicDownloader import NetEaseMusicDownloader
from ImageFetcher import ImageFetcher
from LyricFetcher import LyricFetcher

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
    'NMTID': '00OUtoKEfn5GdT7HEkNmOcp0zYKxPIAAAGaXsDdug',
    'WNMCID': 'joybak.1762526290735.01.0',
    'sDeviceId': 'YD-pI4WY76lXmxEU1QRAEOQ%2BHMs%2B8rjT8X4',
    '__snaker__id': 'qmYpS5lxKP3kpNya',
    'P_INFO': '13368984287|1762603866|1|music|00&99|null&null&null#bej&null#10#0|&0|null|13368984287',
    'ntes_utid': 'tid._.8rtEadkQJRNAUlAUVRLQ%252BCYp%252F8vmW5Db._.0.%2C.edd._.._.0',
    'timing_user_id': 'time_HuNoQfGPhk',
    '_ga_C6TGHFPQ1H': 'GS2.1.s1762845822$o3$g0$t1762845822$j60$l0$h0',
    '_clck': '1wr32hr%5E2%5Eg0x%5E0%5E2058',
    '__csrf': 'c5cd456ec98c25bb9dc7715091ed424c',
    'MUSIC_U': '003D93FBACDB079D087C3AB373721E1DC4776F1AE04119EAFD7CED34E5815D34EA2B5C133F6ADA5C2BCD66F9296A6C2E4FA03E8F8400B251EC1326707148872AED49F75E441F30419128BE10847C59B15420C268AEDC0607DA94EEC25A115ED3E425A2A0DDDB4564F381B9F2B11B61F745E78D6A79C9A7BBF7E96C4DAA443289DED7F9A685EDA06B9637755193D51AB011B4F5430995A77ADE4E04B8350F53773715DADFE3EBA6F56D16D3E4DE298B77CA1D9DBE91FC3FB67679769277A576D425DEFCE8C11D894AB46BEF7A050C40DDF6FA2FCF5812585A56F99C0AA690D8D06BE60ABD607AA9D36BDC36C5109AA9337EB224A0850F874C0B6E1125564FBDECE1A197C1E8D46BD44CFF2908BDC2D97164F73D665D06EA72E59963621FD62B706ED9C7492BCD3A943690992F06BEF5B29DF55AF13A1532A6F14560E5BB13590322001062BC0815FC17877D8A044E836D3A0F35D4266B439808016610A22AAC8CC1FD71B9ED5D0C89C6F534E512F99AF8E2177695A63A444960730059F61E21B4D785434D4A6A1BFA20D80303476024E1C6',
    '__remember_me': 'true',
    'gdxidpyhxdE': 'Ovb%2B%2BuQB2bxPhBl7xYnyhh%2Fd5Z9ijXcseXzlJDM9nc5xWtklYZQWb%5C8Ty4vfyS2cPuECJ0ahYH3y8P5k3z%2Bo2YGZ2p%2FEC5%5ChfBEwGfgmaP2KljuCqgqgy1iUUfXMZvNJA3A9f%5C%2FV5r7l9tMtI%2Fc3zva7niYlSrGjeCvDr6NnV0KzH%5CDs%3A1763916367683',
    'JSESSIONID-WYYY': 'fDouqB%5CI%2FvKr%5CCwWlMG2C0koW2ngeUmRwRBmy6Clqi3%2F89zco0F8S98bx7a%5CzQy0ym8hQQ9XvSu08pynMkYhpc19Qd3Ba3S0V92o4dDr6o%2BFaBeddKWHAO6F%2F3PTIdT%5CmsrXFmC1fQDxrHJCFdA0InoG7lp%5Ci%2BXNQPaveAVyAaXTJyMn%3A1763990738036',
    'WM_NI': 'bF7aGBflvYXVw9j2%2B%2F%2BKD2fHY0pIdANC8x%2BiIaDPkuPr1MxkVRsaKT%2B6LeKNTGoZsK%2F0Jk1SmiXFNUxUMCJGMX3FR1rp9g2WWdMCI1CeuFrDjDudsHllYnZPz8KkbooLcko%3D',
    'WM_NIKE': '9ca17ae2e6ffcda170e2e6ee9bd76fa390a2aebc50f5e78ba3d84e978b8ab1c63a8eb1b7d7d380948e00b3f72af0fea7c3b92aa29af982c64aa6b4babadb5eb5e7a6d3aa25e9958cd3e5449bf0c0aae74b8e9df899aa638bbf8cb1ea7f94aeffaefb61968ebd82ca60e9ea8486ca469899a1bbf241edf0868cb459afb798a7cd5fbc8b83a4c94d8f88fda7d13bb2b0f788b15d95bc83a4cc3b81bbbba7f150aa9cbb85f244b0b4978fd95cbae8858ce165ad94ad8cee37e2a3',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=0, i',
    'referer': 'https://music.163.com/',
    'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'iframe',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
    # 'cookie': '_iuqxldmzr_=32; _ntes_nuid=3b1c0fc15c337315c7fff08a919ffab9; WEVNSM=1.0.0; WM_TID=WheyCB61HcVFFEBUAAKE%2FXN9u5%2FjUVMv; ntes_kaola_ad=1; _ga=GA1.1.1013376860.1722333820; _ntes_nnid=3b1c0fc15c337315c7fff08a919ffab9,1743451927144; _ga_EPDQHDTJH5=GS2.1.s1755358963$o1$g0$t1755358963$j60$l0$h0; NTES_P_UTID=df16zZIVzyOI0nRoElzQVtO5el5IRdqE|1762264992; nts_mail_user=13368984287@163.com:-1:1; NMTID=00OUtoKEfn5GdT7HEkNmOcp0zYKxPIAAAGaXsDdug; WNMCID=joybak.1762526290735.01.0; sDeviceId=YD-pI4WY76lXmxEU1QRAEOQ%2BHMs%2B8rjT8X4; __snaker__id=qmYpS5lxKP3kpNya; P_INFO=13368984287|1762603866|1|music|00&99|null&null&null#bej&null#10#0|&0|null|13368984287; ntes_utid=tid._.8rtEadkQJRNAUlAUVRLQ%252BCYp%252F8vmW5Db._.0.%2C.edd._.._.0; timing_user_id=time_HuNoQfGPhk; _ga_C6TGHFPQ1H=GS2.1.s1762845822$o3$g0$t1762845822$j60$l0$h0; _clck=1wr32hr%5E2%5Eg0x%5E0%5E2058; __csrf=c5cd456ec98c25bb9dc7715091ed424c; MUSIC_U=003D93FBACDB079D087C3AB373721E1DC4776F1AE04119EAFD7CED34E5815D34EA2B5C133F6ADA5C2BCD66F9296A6C2E4FA03E8F8400B251EC1326707148872AED49F75E441F30419128BE10847C59B15420C268AEDC0607DA94EEC25A115ED3E425A2A0DDDB4564F381B9F2B11B61F745E78D6A79C9A7BBF7E96C4DAA443289DED7F9A685EDA06B9637755193D51AB011B4F5430995A77ADE4E04B8350F53773715DADFE3EBA6F56D16D3E4DE298B77CA1D9DBE91FC3FB67679769277A576D425DEFCE8C11D894AB46BEF7A050C40DDF6FA2FCF5812585A56F99C0AA690D8D06BE60ABD607AA9D36BDC36C5109AA9337EB224A0850F874C0B6E1125564FBDECE1A197C1E8D46BD44CFF2908BDC2D97164F73D665D06EA72E59963621FD62B706ED9C7492BCD3A943690992F06BEF5B29DF55AF13A1532A6F14560E5BB13590322001062BC0815FC17877D8A044E836D3A0F35D4266B439808016610A22AAC8CC1FD71B9ED5D0C89C6F534E512F99AF8E2177695A63A444960730059F61E21B4D785434D4A6A1BFA20D80303476024E1C6; __remember_me=true; gdxidpyhxdE=Ovb%2B%2BuQB2bxPhBl7xYnyhh%2Fd5Z9ijXcseXzlJDM9nc5xWtklYZQWb%5C8Ty4vfyS2cPuECJ0ahYH3y8P5k3z%2Bo2YGZ2p%2FEC5%5ChfBEwGfgmaP2KljuCqgqgy1iUUfXMZvNJA3A9f%5C%2FV5r7l9tMtI%2Fc3zva7niYlSrGjeCvDr6NnV0KzH%5CDs%3A1763916367683; JSESSIONID-WYYY=fDouqB%5CI%2FvKr%5CCwWlMG2C0koW2ngeUmRwRBmy6Clqi3%2F89zco0F8S98bx7a%5CzQy0ym8hQQ9XvSu08pynMkYhpc19Qd3Ba3S0V92o4dDr6o%2BFaBeddKWHAO6F%2F3PTIdT%5CmsrXFmC1fQDxrHJCFdA0InoG7lp%5Ci%2BXNQPaveAVyAaXTJyMn%3A1763990738036; WM_NI=bF7aGBflvYXVw9j2%2B%2F%2BKD2fHY0pIdANC8x%2BiIaDPkuPr1MxkVRsaKT%2B6LeKNTGoZsK%2F0Jk1SmiXFNUxUMCJGMX3FR1rp9g2WWdMCI1CeuFrDjDudsHllYnZPz8KkbooLcko%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6ee9bd76fa390a2aebc50f5e78ba3d84e978b8ab1c63a8eb1b7d7d380948e00b3f72af0fea7c3b92aa29af982c64aa6b4babadb5eb5e7a6d3aa25e9958cd3e5449bf0c0aae74b8e9df899aa638bbf8cb1ea7f94aeffaefb61968ebd82ca60e9ea8486ca469899a1bbf241edf0868cb459afb798a7cd5fbc8b83a4c94d8f88fda7d13bb2b0f788b15d95bc83a4cc3b81bbbba7f150aa9cbb85f244b0b4978fd95cbae8858ce165ad94ad8cee37e2a3',
}

params = {
    'csrf_token': 'b394367d854d672cc86a21b5fe5de014',
}

num = input('歌单id还是歌曲id?(歌单id输入1,歌曲id输入0):')

playlist = NetEaseMusicPlaylist(cookies, headers)
img_fetcher = ImageFetcher(cookies, headers)
downloader = NetEaseMusicDownloader(params, cookies, headers)
lyrics = LyricFetcher(params, cookies, headers)
merger = AudioCoverMerger()

location = './my_music'

if num == '1':
    id = input('输入歌单id:')
    # 获取歌单信息并批量获得歌单中歌曲id
    html = playlist.fetch_playlist(id)
    data = playlist.extract_song_info(html)

    # 开始获取歌曲信息
    for item in data:
        song_id = item['id']
        # 开始获取歌曲信息
        html_data = img_fetcher.get_song_img_data(song_id)
        # 提取歌曲信息
        song_info = img_fetcher.extract_song_info(html_data)
        print(f"提取到的歌曲信息: {song_info}")
        # 格式化输出
        formatted_output = f"[id: {song_info['id']}, song_name: {song_info['song']}, singer: {song_info['singer']}]"
        print(f"格式化结果: {formatted_output}")

        # 提取并下载图片
        downloaded_path = None
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

        # 下载歌曲
        file_path = None
        try:
            response_json = downloader.get_song_download_url(song_id)
            download_url = downloader.extract_and_convert_url(response_json)

            # if download_url:
            #     file_path = downloader.download_song_with_custom_name(
            #         download_url,
            #         "我的自定义歌曲名",
            #         "自定义歌手名",  # 新增：设置歌手名称
            #         "./my_music"
            #     )
            #     print(f"文件已保存到: {file_path}")
            # else:
            #     print("无法获取下载链接")
            if download_url:
                file_path = downloader.download_song_with_custom_name(
                    download_url,
                    f"{song_info['song']}",
                    f"{song_info['singer']}",
                    f"{location}"
                )
                print(f"文件已保存到: {file_path}")
            else:
                print("无法获取下载链接")
        except Exception as e:
            print(f"下载失败: {e}")

        # 下载歌词
        re_text = lyrics.get_song_lyrics_data(song_id)
        print("原始JSON响应:")
        print(re_text)
        # # 保存为LRC文件
        # lrc_file = lyrics.save_lyric_as_lrc(
        #     re_text,
        #     output_file="米津玄師 - Lemon.lrc",
        #     song_title="Lemon",
        #     artist="米津玄師"
        # )
        # 保存为LRC文件
        lrc_file = lyrics.save_lyric_as_lrc(
            re_text,
            output_file=f"{song_info['song']}",
            song_title=f"{song_info['song']}",
            artist=f"{song_info['singer']}",
            output_dir=f"{location}"
        )

        # 单个文件处理图片+歌曲文件
        merger.set_audio_cover(
            audio_path=f"{file_path}",
            cover_path=f"{downloaded_path}",
            title=f"{song_info['song']}",
            artist=f"{song_info['singer']}",
            album=f"{song_info['album']}"
        )


else:
    song_id = input('输入歌曲id:')
    # 开始获取歌曲信息
    html_data = img_fetcher.get_song_img_data(song_id)
    # 提取歌曲信息
    song_info = img_fetcher.extract_song_info(html_data)
    print(f"提取到的歌曲信息: {song_info}")
    # 格式化输出
    formatted_output = f"[id: {song_info['id']}, song_name: {song_info['song']}, singer: {song_info['singer']}]"
    print(f"格式化结果: {formatted_output}")

    # 提取并下载图片
    downloaded_path = None
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

    # 下载歌曲
    file_path = None
    try:
        response_json = downloader.get_song_download_url(song_id)
        # print('1')
        download_url = downloader.extract_and_convert_url(response_json)
        # print('2')

        # if download_url:
        #     file_path = downloader.download_song_with_custom_name(
        #         download_url,
        #         "我的自定义歌曲名",
        #         "自定义歌手名",  # 新增：设置歌手名称
        #         "./my_music"
        #     )
        #     print(f"文件已保存到: {file_path}")
        # else:
        #     print("无法获取下载链接")
        if download_url:
            file_path = downloader.download_song_with_custom_name(
                download_url,
                f"{song_info['song']}",
                f"{song_info['singer']}",
                f"{location}"
            )
            print(f"文件已保存到: {file_path}")
        else:
            print("无法获取下载链接")
    except Exception as e:
        print(f"下载失败: {e}")

    # 下载歌词
    re_text = lyrics.get_song_lyrics_data(song_id)
    print("原始JSON响应:")
    print(re_text)
    # # 保存为LRC文件
    # lrc_file = lyrics.save_lyric_as_lrc(
    #     re_text,
    #     output_file="米津玄師 - Lemon.lrc",
    #     song_title="Lemon",
    #     artist="米津玄師"
    # )
    # 保存为LRC文件
    lrc_file = lyrics.save_lyric_as_lrc(
        re_text,
        output_file=f"{song_info['song']}",
        song_title=f"{song_info['song']}",
        artist=f"{song_info['singer']}",
        output_dir=f"{location}"
    )

    # 单个文件处理图片+歌曲文件
    merger.set_audio_cover(
        audio_path=f"{file_path}",
        cover_path=f"{downloaded_path}",
        title=f"{song_info['song']}",
        artist=f"{song_info['singer']}",
        album=f"{song_info['album']}"
    )

