# 私人电台项目

该项目是一个私人电台，利用 `chattts` 进行文本转语音转换。项目通过自定义的网页爬虫抓取新闻文章，使用 `kimi` 进行总结，并生成 MP3 音频文件。

## 功能特点

- **网页爬虫**：目前实现了36kr和新浪新闻的爬虫。
- **摘要生成**：使用 `kimi` 对文章生成简洁摘要。
- **文本转语音**：使用 `chattts` 将摘要转换为音频。
- **背景音乐生成**：调用 sunoapi 生成背景音乐。
- **音频生成**：生成便于收听的 MP3 文件。

## 前置条件

- Python 3.10
- `FFMPEG` 
- `kimi` api key
- `suno` session cookie


## 安装步骤

1. 克隆该仓库：

    ```bash
    git clone https://github.com/yourusername/personal-radio-station.git
    cd audionews
    ```

2. 安装所需依赖：

    ```bash
    pip install -r requirements.txt
    ```

3. 确保系统已安装 `ffmpeg`。该工具用于音频文件转换。

    - 在 macOS 上：

        ```bash
        brew install ffmpeg
        ```

    - 在 Ubuntu 上：

        ```bash
        sudo apt-get install ffmpeg
        ```

    - 在 Windows 上：

        从 [FFmpeg 网站](https://ffmpeg.org/download.html)下载并安装。

## 使用方法

1. **配置来源**：编辑 `const.py` 设置 kimi 的 apikey，suno 的相关参数。

2. **运行项目**：进行抓取文章，生成音频，合并音频

    ```bash
    python main.py 36kr #或normal(执行不同的爬虫获取不同的新闻来源)
    ```

3. **收听私人电台**：在 `tmp` 目录中找到生成的 MP3 文件。

## 致谢

- 感谢 [chattts](https://github.com/2noise/ChatTTS) 和 `kimi` 的开发者。