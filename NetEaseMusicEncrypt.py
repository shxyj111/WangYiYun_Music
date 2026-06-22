# 从.js文件获取加密过的data数据
import execjs


class NetEaseMusicEncrypt:
    """
    网易云音乐加密参数获取类
    """

    def __init__(self, js_file_path='demo_0.js'):
        """
        初始化类，加载JavaScript加密代码

        Args:
            js_file_path: JavaScript文件路径，默认为'demo_0.js'
        """
        self.js_file_path = js_file_path
        self.ctx = None
        self._load_js_code()

    def _load_js_code(self):
        """加载并编译JavaScript代码"""
        try:
            with open(self.js_file_path, 'r', encoding='utf-8') as f:
                js_code = f.read()
            self.ctx = execjs.compile(js_code)
        except Exception as e:
            print(f"加载JavaScript文件出错: {e}")
            raise

    def get_song_lyric_data(self, song_id):
        """
        获取歌曲歌词数据的加密参数

        Args:
            song_id: 歌曲ID

        Returns:
            dict: 包含加密参数params和encSecKey的字典
        """
        try:
            result = self.ctx.call('song_lyric_data', song_id)
            return result
        except Exception as e:
            print(f"获取歌曲歌词数据加密参数出错: {e}")
            return None

    def get_song_download_data(self, song_id):
        """
        获取歌曲下载数据的加密参数

        Args:
            song_id: 歌曲ID

        Returns:
            dict: 包含加密参数params和encSecKey的字典
        """
        try:
            result = self.ctx.call('song_download_data', song_id)
            return result
        except Exception as e:
            print(f"获取歌曲下载数据加密参数出错: {e}")
            return None

    def get_song_comment_data(self, song_id, pageNo = "1", pageSize = "20"):
        """
        获取最新评论数据的加密参数

        Args:
            song_id: 歌曲ID/歌单ID
            pageNo: 页码
            pageSize: 每页大小

        Returns:
            dict: 包含加密参数params和encSecKey的字典
        """

        try:
            result = self.ctx.call('song_list_comment_data', song_id, pageNo, pageSize)
            return result
        except Exception as e:
            print(f"获取最新评论数据加密参数出错: {e}")
            return None

    def get_song_all_data(self, song_id,  pageNo = "1", pageSize = "20"):
        """
        同时获取歌曲评论和下载数据的加密参数

        Args:
            song_id: 歌曲ID

        Returns:
            dict: 包含评论数据和下载数据加密参数的字典
        """
        lyric_data = self.get_song_lyric_data(song_id)
        download_data = self.get_song_download_data(song_id)
        comment_data = self.get_song_comment_data(song_id, pageNo, pageSize)

        return {
            'lyric_data': lyric_data,
            'download_data': download_data,
            'comment_data': comment_data
        }


# 使用示例
if __name__ == "__main__":
    # 创建加密类实例
    music_encrypt = NetEaseMusicEncrypt()

    # 测试歌曲ID
    song_id = 5271858

    # 测试评论页数
    pageNo = 1

    # 测试评论条数
    pageSize = 20

    # 获取所有数据
    all_data = music_encrypt.get_song_all_data(song_id)
    if all_data:
        print("歌词数据加密值:", all_data['lyric_data'])
        print("下载数据加密值:", all_data['download_data'])

    print("\n" + "=" * 50 + "\n")

    # 单独获取歌曲歌词数据
    lyric_data = music_encrypt.get_song_lyric_data(song_id)
    print("单独获得歌词数据:", lyric_data)

    print("\n" + "=" * 50 + "\n")

    # 单独获取歌曲下载数据
    download_data = music_encrypt.get_song_download_data(song_id)
    print("单独获取下载数据:", download_data)

    print("\n" + "=" * 50 + "\n")

    # 单独获取最新评论数据
    comment_data = music_encrypt.get_song_comment_data(song_id, pageNo, pageSize)
    print("单独获取最新评论数据:", comment_data)
