import random
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import threading
from datetime import datetime
import os
import logging
import time
from pixiv_crawler import PixivCookieCrawler
import sys
def resource_path(relative_path):
    """获取资源的绝对路径"""
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller 创建临时目录，将路径写入 _MEIPASS
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class PixivCrawlerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Pixiv爬虫 - Cookie登录版")
        self.root.geometry("800x750")  # 增加窗口高度以容纳新内容
        
        # 创建主框架
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置框架
        self.setup_guide_frame()  # 新增用户指引区域
        self.setup_input_frame()
        self.setup_progress_frame()  # 新增进度条区域
        self.setup_log_frame()
        self.setup_control_frame()
        
        # 初始化变量
        self.is_running = False
        self.current_thread = None
        self.download_start_time = None
        self.total_works = 0
        self.completed_works = 0
        
    def setup_guide_frame(self):
        guide_frame = ttk.LabelFrame(self.main_frame, text="获取Cookie教程", padding="5")
        guide_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        guide_text = """如何获取Pixiv的Cookie：
1. 使用Chrome打开pixiv.net并登录你的账号
2. 按F12键打开开发者工具
3. 点击"网络/Network"标签
4. 刷新页面
5. 在Network找到pixiv.net的请求（一般是第一个）
6. 在右侧的请求详情中找到"请求标头/Headers"部分
7. 向下滚动找到"Cookie:"开头的行
8. 右键点击Cookie行，选择"复制值"
9. 将复制的内容粘贴到下方的Cookie输入框中
注意事项：
- Cookie的有效期一般很长，但不是永久的
- 如果下载时提示Cookie失效，请重新获取
- Cookie是你的登录凭证，请勿分享给他人"""
        
        guide_label = ttk.Label(guide_frame, text=guide_text, justify=tk.LEFT, wraplength=750)
        guide_label.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
    def setup_input_frame(self):
        input_frame = ttk.LabelFrame(self.main_frame, text="登录信息", padding="5")
        input_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Cookie输入
        ttk.Label(input_frame, text="Cookie:").grid(row=0, column=0, sticky=tk.W)
        self.cookie_input = scrolledtext.ScrolledText(input_frame, width=60, height=4)
        self.cookie_input.grid(row=0, column=1, columnspan=2, sticky=tk.W)
        
        # 作者ID输入
        ttk.Label(input_frame, text="作者ID:").grid(row=1, column=0, sticky=tk.W)
        self.author_id = ttk.Entry(input_frame, width=20)
        self.author_id.grid(row=1, column=1, sticky=tk.W)
        
        # 保存目录选择
        ttk.Label(input_frame, text="保存目录:").grid(row=2, column=0, sticky=tk.W)
        self.save_dir = ttk.Entry(input_frame, width=50)
        self.save_dir.grid(row=2, column=1, sticky=tk.W)
        self.save_dir.insert(0, "D:\\dairi")
        
        ttk.Button(input_frame, text="选择目录", command=self.choose_directory).grid(
            row=2, column=2, sticky=tk.W)
    
    def setup_progress_frame(self):
        progress_frame = ttk.LabelFrame(self.main_frame, text="下载进度", padding="5")
        progress_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # 总体进度条
        ttk.Label(progress_frame, text="总体进度:").grid(row=0, column=0, sticky=tk.W)
        self.progress_bar = ttk.Progressbar(progress_frame, mode='determinate', length=400)
        self.progress_bar.grid(row=0, column=1, sticky=(tk.W, tk.E))
        
        # 下载速度和进度信息
        self.progress_info = ttk.Label(progress_frame, text="等待开始下载...")
        self.progress_info.grid(row=1, column=0, columnspan=2, sticky=tk.W)
            
    def setup_log_frame(self):
        log_frame = ttk.LabelFrame(self.main_frame, text="运行日志", padding="5")
        log_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, width=80)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.log_text.configure(state='disabled')
        
        log_handler = LogHandler(self.log_text)
        log_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logging.getLogger().addHandler(log_handler)
        logging.getLogger().setLevel(logging.INFO)
        
    def setup_control_frame(self):
        control_frame = ttk.Frame(self.main_frame)
        control_frame.grid(row=4, column=0, columnspan=2, pady=5)
        
        self.verify_button = ttk.Button(control_frame, text="验证Cookie", command=self.verify_cookie)
        self.verify_button.grid(row=0, column=0, padx=5)
        
        self.start_button = ttk.Button(control_frame, text="开始下载", command=self.start_download)
        self.start_button.grid(row=0, column=1, padx=5)
        self.start_button.state(['disabled'])
        
        self.stop_button = ttk.Button(control_frame, text="停止下载", command=self.stop_download)
        self.stop_button.grid(row=0, column=2, padx=5)
        self.stop_button.state(['disabled'])
        
        ttk.Button(control_frame, text="清空日志", command=self.clear_log).grid(row=0, column=3, padx=5)

    def update_progress(self, work_id):
        self.completed_works += 1
        progress = (self.completed_works / self.total_works * 100) if self.total_works > 0 else 0
        self.progress_bar['value'] = progress
        
        # 计算下载速度
        if self.download_start_time:
            elapsed_time = time.time() - self.download_start_time
            speed = self.completed_works / elapsed_time if elapsed_time > 0 else 0
            
            # 更新进度信息
            info_text = f"已完成: {self.completed_works}/{self.total_works} 作品 "
            info_text += f"({progress:.1f}%) - 平均速度: {speed:.2f} 作品/秒"
            self.progress_info['text'] = info_text
        
        self.root.update_idletasks()

    def verify_cookie(self):
        cookie = self.cookie_input.get('1.0', tk.END).strip()
        if not cookie:
            messagebox.showerror("错误", "请输入Cookie！")
            return
            
        self.verify_button.state(['disabled'])
        threading.Thread(target=self.verify_cookie_task, args=(cookie,)).start()
        
    def verify_cookie_task(self, cookie):
        try:
            logging.info("正在验证Cookie...")
            crawler = PixivCookieCrawler(cookie)
            if crawler.verify_login():
                logging.info("Cookie验证成功！")
                self.root.after(0, self.enable_download)
            else:
                logging.error("Cookie验证失败！")
        except Exception as e:
            logging.error(f"验证过程出错: {str(e)}")
        finally:
            self.root.after(0, lambda: self.verify_button.state(['!disabled']))
            
    def enable_download(self):
        self.start_button.state(['!disabled'])
            
    def choose_directory(self):
        dir_path = filedialog.askdirectory()
        if dir_path:
            self.save_dir.delete(0, tk.END)
            self.save_dir.insert(0, dir_path)
            
    def clear_log(self):
        self.log_text.configure(state='normal')
        self.log_text.delete(1.0, tk.END)
        self.log_text.configure(state='disabled')
    
    def start_download(self):
        if self.is_running:
            return
            
        cookie = self.cookie_input.get('1.0', tk.END).strip()
        author_id = self.author_id.get().strip()
        save_dir = self.save_dir.get().strip()
        
        if not all([cookie, author_id, save_dir]):
            messagebox.showerror("错误", "请填写所有必要信息！")
            return
            
        self.is_running = True
        self.start_button.state(['disabled'])
        self.stop_button.state(['!disabled'])
        
        # 重置进度相关变量
        self.completed_works = 0
        self.progress_bar['value'] = 0
        self.progress_info['text'] = "正在获取作品列表..."
        self.download_start_time = None
        
        self.current_thread = threading.Thread(
            target=self.download_task,
            args=(cookie, author_id, save_dir)
        )
        self.current_thread.start()
        
    def stop_download(self):
        if self.is_running:
            self.is_running = False
            logging.info("正在停止下载...")
            self.stop_button.state(['disabled'])
    
    def download_task(self, cookie, author_id, save_dir):
        try:
            crawler = PixivCookieCrawler(cookie, save_dir)
            
            # 获取作品列表
            works = crawler.get_author_works(author_id)
            existing_works = crawler.get_existing_work_ids()
            new_works = [work_id for work_id in works if work_id not in existing_works]
            
            self.total_works = len(new_works)
            self.download_start_time = time.time()
            
            # 更新进度信息
            self.root.after(0, lambda: self.progress_info.config(
                text=f"开始下载 {self.total_works} 个作品..."
            ))
            
            # 下载每个作品
            for i, work_id in enumerate(new_works, 1):
                if not self.is_running:
                    break
                logging.info(f"正在下载第 {i}/{self.total_works} 个作品 (ID: {work_id})")
                crawler.download_work(work_id)
                self.root.after(0, lambda: self.update_progress(work_id))
                time.sleep(random.uniform(2, 5))
                
        except Exception as e:
            logging.error(f"下载过程中出错: {str(e)}")
        finally:
            self.is_running = False
            self.root.after(0, self.reset_buttons)
            if not self.is_running:  # 如果是正常完成而不是手动停止
                self.root.after(0, lambda: self.progress_info.config(text="下载完成！"))
    
    def reset_buttons(self):
        self.start_button.state(['!disabled'])
        self.stop_button.state(['disabled'])

class LogHandler(logging.Handler):
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget

    def emit(self, record):
        msg = self.format(record)
        def append():
            self.text_widget.configure(state='normal')
            self.text_widget.insert('end', msg + '\n')
            self.text_widget.see('end')
            self.text_widget.configure(state='disabled')
        self.text_widget.after(0, append)

def main():
    try:
        root = tk.Tk()
        app = PixivCrawlerGUI(root)
        root.mainloop()
    except Exception as e:
        # 在打包环境中捕获并显示错误
        messagebox.showerror("Error", f"发生错误：{str(e)}")
        logging.error(f"程序发生错误: {str(e)}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        # 确保错误信息不会静默消失
        with open("error_log.txt", "w", encoding="utf-8") as f:
            f.write(f"程序启动错误: {str(e)}")
        messagebox.showerror("Error", f"程序启动失败：{str(e)}")