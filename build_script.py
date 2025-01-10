import os
import shutil
import subprocess

def build_pixiv_crawler():
    """构建Pixiv爬虫的独立可执行文件"""
    # 安装必要的包
    print("Installing required packages...")
    subprocess.run(['pip', 'install', 'pyinstaller', 'requests'], check=True)
    
    # 创建build目录
    if not os.path.exists('build'):
        os.makedirs('build')
    
    # 复制文件到build目录
    print("Copying files to build directory...")
    files_to_copy = ['pixiv_crawler.py', 'pixiv_crawler_gui.py']
    for file in files_to_copy:
        shutil.copy(file, 'build/')
    
    # 创建启动脚本
    print("Creating launcher script...")
    with open('build/start_pixiv.bat', 'w', encoding='utf-8') as f:
        f.write('@echo off\n')
        f.write('chcp 65001\n')
        f.write('cls\n\n')
        f.write('echo Starting Pixiv Crawler...\n\n')
        f.write('start "" "pixiv_crawler.exe"\n')
        f.write('exit\n')
    
    # 使用PyInstaller打包
    print("Building executable with PyInstaller...")
    subprocess.run([
        'pyinstaller',
        '--noconfirm',
        '--clean',
        '--windowed',
        '--name=pixiv_crawler',
        '--icon=favicon.ico',  # 使用你的图标
        '--add-data=build/pixiv_crawler.py;.',
        '--hidden-import=requests',
        '--hidden-import=tkinter',
        '--hidden-import=threading',
        'build/pixiv_crawler_gui.py'
    ])
    
    # 移动启动脚本到dist目录
    print("Moving files to distribution directory...")
    shutil.copy('build/start_pixiv.bat', 'dist/pixiv_crawler/')
    
    print("\nBuild completed successfully!")
    print("The packaged application can be found in the 'dist/pixiv_crawler' directory")
    print("Users can run the application by executing 'start_pixiv.bat'")

if __name__ == '__main__':
    build_pixiv_crawler()