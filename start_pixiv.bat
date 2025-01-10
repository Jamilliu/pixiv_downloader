@echo off
:: 设置编码为UTF-8
chcp 65001
cls

echo 正在启动Pixiv下载器...

:: 检查Python环境
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python未安装！请先安装Python后再运行。
    pause
    exit
)

:: 检查必要的库
echo 正在检查并安装必要的库...
pip install requests -q

:: 检查文件是否存在
if not exist "pixiv_crawler_gui.py" (
    echo 错误：找不到 pixiv_crawler_gui.py 文件！
    echo 请确保该文件与批处理文件在同一目录。
    pause
    exit
)

:: 运行Python脚本
python pixiv_crawler_gui.py

if %errorlevel% neq 0 (
    echo 程序运行出错！
    pause
)

exit