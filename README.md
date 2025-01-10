# Pixiv Downloader / Pixiv作品下载器

[English](#english) | [中文](#chinese)

<a name="chinese"></a>
## 中文

# Pixiv 作品下载器

这是一个使用Cookie认证方式的Pixiv作品下载工具。本应用提供了图形界面，可以便捷地下载指定Pixiv画师的所有作品。

## 主要功能

- 简单直观的图形用户界面
- 使用Cookie认证方式，稳定可靠
- 自动下载指定画师的所有作品
- 实时显示下载进度和状态
- 支持断点续传功能
- 将下载的作品按文件夹分类存储
- 内置下载完整性验证功能
- 清晰的日志系统，方便监控下载过程

## 系统要求

- Python 3.10 或更高版本
- 需要的Python包（会自动安装）：
  - requests
  - tkinter（Python通常自带）
  - PyInstaller（仅在打包时需要）

## 安装说明

1. 克隆仓库：
```bash
git clone https://github.com/your-username/pixiv_downloader.git
cd pixiv_downloader
```

2. 运行方式（两种选择）：

   方式一：使用批处理文件（Windows系统）：
   - 直接双击运行 `start_pixiv.bat`
   - 脚本会自动检查Python环境和所需依赖

   方式二：生成独立执行文件：
   - 运行构建脚本：
   ```bash
   python build_script.py
   ```
   - 在 `dist/pixiv_crawler/pixiv_crawler.exe` 目录下找到生成的程序

## 使用说明

1. 使用上述任一方式启动程序
2. 获取Pixiv的Cookie：
   - 用Chrome浏览器登录Pixiv网站
   - 按F12键打开开发者工具
   - 切换到"网络/Network"标签
   - 刷新页面
   - 点击任意一个pixiv.net的请求
   - 在请求头中找到Cookie值
   - 复制整个Cookie字符串
3. 将Cookie粘贴到应用程序中
4. 输入要下载的画师ID
5. 选择保存目录（默认为D:\dairi）
6. 点击"验证Cookie"测试登录状态
7. 点击"开始下载"开始下载作品

## 项目结构

- `pixiv_crawler_gui.py`：主要的图形界面程序
- `pixiv_crawler.py`：核心下载功能模块
- `build_script.py`：用于构建独立执行文件的脚本
- `start_pixiv.bat`：快速启动批处理文件

## 参与贡献

欢迎提交贡献！如果您想进行重大更改，请先开一个issue讨论您想要改变的内容。

## 安全与法律提示

- 本工具仅供个人使用
- 请尊重画师的权利和Pixiv的服务条款
- 请妥善保管您的Cookie信息，不要分享给他人
- 未经授权，请勿传播下载的作品

## 开源协议

本项目采用[MIT许可证](LICENSE)。您可以自由使用和修改代码，但请注明出处。

## 致谢

感谢所有在Pixiv上分享作品的画师，是他们让这个平台变得精彩纷呈。

## 常见问题解答

### 1. 为什么下载速度较慢？
为了避免对Pixiv服务器造成过大压力，程序设置了下载间隔。每下载一个作品后会等待2-5秒再下载下一个。

### 2. Cookie无法验证成功怎么办？
- 确保您已经成功登录Pixiv
- 检查复制的Cookie是否完整
- Cookie可能已过期，请重新获取

### 3. 下载中断后如何继续？
程序会自动记录已下载的作品，重新启动后会自动跳过这些作品，只下载未完成的部分。

### 4. 找不到画师ID怎么办？
打开画师的主页，网址中的数字部分就是画师ID。例如：`https://www.pixiv.net/users/XXXXXX` 中的XXXXXX就是画师ID。

<a name="english"></a>
## English

# Pixiv Downloader

A user-friendly tool for downloading artwork from Pixiv using cookie-based authentication. This application provides a graphical interface for easily downloading all artworks from a specified Pixiv artist.

## Features

- Simple and intuitive graphical user interface
- Cookie-based authentication for reliable access
- Automatic download of all artworks from a specified artist
- Progress tracking with real-time status updates
- Support for resuming interrupted downloads
- Organized storage of downloaded artwork in separate folders
- Built-in verification of download completeness
- Clear logging system for monitoring download progress

## Requirements

- Python 3.10 or higher
- Required Python packages (automatically installed):
  - requests
  - tkinter (usually comes with Python)
  - PyInstaller (for building executable)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/pixiv_downloader.git
cd pixiv_downloader
```

2. You can run the application in two ways:

   a. Using the batch file (Windows):
   - Simply double-click `start_pixiv.bat`
   - The script will automatically check for Python and required dependencies

   b. Building an executable:
   - Run the build script:
   ```bash
   python build_script.py
   ```
   - Find the executable in `dist/pixiv_crawler/pixiv_crawler.exe`

## Usage

1. Launch the application using either method described above
2. Obtain your Pixiv cookie:
   - Log into Pixiv in Chrome
   - Press F12 to open Developer Tools
   - Go to the Network tab
   - Refresh the page
   - Click on any pixiv.net request
   - Find the Cookie value in the request headers
   - Copy the entire cookie string
3. Paste the cookie into the application
4. Enter the Pixiv artist ID
5. Choose a save directory (defaults to D:\dairi)
6. Click "Verify Cookie" to test your login
7. Click "Start Download" to begin downloading artworks

## Project Structure

- `pixiv_crawler_gui.py`: Main GUI application
- `pixiv_crawler.py`: Core downloading functionality
- `build_script.py`: Script for building standalone executable
- `start_pixiv.bat`: Batch file for easy launching

## Contributing

Contributions are welcome! Please feel free to submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## Safety and Legal Notes

- This tool is for personal use only
- Please respect artists' rights and Pixiv's terms of service
- Keep your cookie information private and secure
- Do not distribute downloaded artworks without permission

## License

[MIT License](LICENSE) - feel free to use and modify the code, but please provide attribution.

## Acknowledgments

Thanks to all the artists sharing their work on Pixiv and making the platform what it is today.