# 网易云音乐批量下载器

一个基于 Python 的网易云音乐批量下载工具，支持根据歌单 ID 或歌曲 ID 下载音乐，自动获取封面图片、歌词，并将封面嵌入音频文件。

## 功能特性

- **歌单批量下载**：输入歌单 ID，自动解析并下载歌单内所有歌曲
- **单曲下载**：输入歌曲 ID，下载指定歌曲
- **封面获取与嵌入**：自动下载歌曲封面图片并嵌入到 MP3/M4A/FLAC 音频文件中
- **歌词下载**：自动获取歌词并保存为标准 LRC 格式文件（支持原歌词+翻译歌词合并）
- **音频元数据设置**：自动为下载的音频文件设置歌名、歌手、专辑等元数据

## 项目结构

```
WangYiYun_Music/
├── main.py                      # 主入口程序，协调各模块完成下载流程
├── NetEaseMusicDownloader.py    # 歌曲下载模块，获取下载链接并下载音频文件
├── NetEaseMusicEncrypt.py       # 加密参数生成模块，调用 JS 生成 API 加密参数
├── NetEaseMusicPlaylist.py      # 歌单解析模块，获取歌单中的歌曲 ID 列表
├── LyricFetcher.py              # 歌词获取模块，获取并保存 LRC 歌词文件
├── ImageFetcher.py              # 歌曲信息与封面获取模块
├── AudioCoverMerger.py          # 音频封面合并模块，将封面嵌入音频文件
├── demo_0.js                    # 网易云音乐前端加密核心代码（AES+RSA）
├── 请求头中的请求参数.txt         # 请求参数说明文档
└── README.md
```

## 环境依赖

### Python 版本

Python 3.7+

### Python 依赖库

```bash
pip install requests PyExecJS mutagen
```

### 外部依赖

需要安装 **Node.js**，因为 `PyExecJS` 需要通过 Node.js 来执行 `demo_0.js` 中的加密代码。

## 快速开始

### 1. 配置认证信息

在 `main.py` 中配置你的 cookies 和 headers（从浏览器中获取）：

```python
cookies = {
    "MUSIC_U": "your_music_u",
    "__csrf": "your_csrf_token",
    # ...
}

headers = {
    "User-Agent": "your_user_agent",
    # ...
}
```

> **注意**：认证信息具有时效性，过期后需要从浏览器重新抓取。

### 2. 运行程序

```bash
python main.py
```

### 3. 选择下载模式

- 输入 `1`：进入歌单下载模式，输入网易云歌单 ID
- 输入 `0`：进入单曲下载模式，输入歌曲 ID

### 4. 查看结果

下载的文件默认保存在 `./my_music` 目录下，包含：
- 音频文件（.m4a / .mp3 / .flac，已嵌入封面和元数据）
- 歌词文件（.lrc）
- 封面图片（临时保存在 `./song_images` 目录）

## 工作原理

```
用户输入（歌单ID 或 歌曲ID）
    │
    ├── 歌单模式 → 解析歌单页面 → 获取所有歌曲ID
    │
    └── 单曲模式 → 直接使用歌曲ID
            │
            ▼
    获取歌曲页面 → 提取歌名、歌手、专辑、封面URL
            │
    ┌───────┼───────┐
    ▼       ▼       ▼
 下载封面  生成加密参数  获取歌词
    │       │       │
    │       ▼       ▼
    │   获取下载链接  保存LRC文件
    │       │
    │       ▼
    │   下载音频文件
    │       │
    └───────┼───────┘
            ▼
    将封面嵌入音频 + 设置元数据
            │
            ▼
       ./my_music/
```

## API 端点

| API | 方法 | 用途 |
|-----|------|------|
| `https://music.163.com/playlist?id={id}` | GET | 获取歌单页面 |
| `https://music.163.com/song?id={id}` | GET | 获取歌曲页面 |
| `https://music.163.com/weapi/song/enhance/player/url/v1` | POST | 获取歌曲下载链接（需加密参数） |
| `https://music.163.com/weapi/song/lyric` | POST | 获取歌曲歌词（需加密参数） |

## 支持的音频格式

- **MP3** (.mp3) — 使用 ID3 标签嵌入封面
- **M4A/AAC** (.m4a) — 使用 MP4 标签嵌入封面
- **FLAC** (.flac) — 使用 Vorbis Comment + Picture 嵌入封面

## 注意事项

- 本项目仅供学习交流使用，请勿用于商业用途
- 请遵守网易云音乐的服务条款
- 下载的音乐版权归网易云音乐及相关权利人所有
- 认证信息（cookies/headers）过期后需重新获取并更新配置
- 需要稳定的网络连接才能正常下载

## 许可证

本项目仅供学习研究使用。
