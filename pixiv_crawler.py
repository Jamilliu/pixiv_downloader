import requests
import json
import time
import random
import os
import logging
import re

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PixivCookieCrawler:
    def __init__(self, cookie, save_dir='D:\\dairi'):
        self.save_dir = save_dir
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': 'https://www.pixiv.net/',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Cookie': cookie
        }
        
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

    def check_work_completeness(self, work_id):
        """检查作品是否完整下载
        
        Args:
            work_id (str): 作品ID
            
        Returns:
            tuple: (是否完整下载, 作品总页数, 已下载页数)
        """
        try:
            # 获取作品详情以了解总页数
            url = f'https://www.pixiv.net/ajax/illust/{work_id}'
            response = self.session.get(url, headers=self.headers)
            
            if response.status_code != 200:
                logger.error(f"获取作品 {work_id} 详情失败")
                return False, 0, 0
                
            data = response.json()
            if data.get('error'):
                logger.error(f"获取作品 {work_id} 详情出错")
                return False, 0, 0
            
            # 获取作品应有的总页数
            total_pages = data['body']['pageCount']
            
            # 在本地查找这个作品的文件夹
            for folder_name in os.listdir(self.save_dir):
                if folder_name.startswith(f"{work_id}_"):
                    folder_path = os.path.join(self.save_dir, folder_name)
                    # 统计实际下载的图片数量
                    downloaded_pages = len([f for f in os.listdir(folder_path) 
                                         if f.startswith(f"{work_id}_p") and f.endswith('.jpg')])
                    
                    return downloaded_pages >= total_pages, total_pages, downloaded_pages
                    
            return False, 0, 0
            
        except Exception as e:
            logger.error(f"检查作品 {work_id} 完整性时出错: {str(e)}")
            return False, 0, 0

    def get_existing_work_ids(self):
        """获取已下载的作品ID列表，并检查最后一个作品的完整性"""
        existing_ids = set()
        last_work_id = None
        
        try:
            # 获取所有作品文件夹，并按时间排序（最新的最后）
            folders = sorted(os.listdir(self.save_dir), 
                           key=lambda x: os.path.getctime(os.path.join(self.save_dir, x)))
            
            # 遍历除最后一个以外的所有文件夹
            for folder_name in folders[:-1]:
                match = re.match(r'^(\d+)_', folder_name)
                if match:
                    existing_ids.add(match.group(1))
            
            # 特殊处理最后一个文件夹
            if folders:
                match = re.match(r'^(\d+)_', folders[-1])
                if match:
                    last_work_id = match.group(1)
                    # 检查最后一个作品的完整性
                    is_complete, total_pages, downloaded_pages = self.check_work_completeness(last_work_id)
                    
                    if is_complete:
                        existing_ids.add(last_work_id)
                        logger.info(f"最后一个作品 {last_work_id} 已完整下载 ({downloaded_pages}/{total_pages} 页)")
                    else:
                        logger.info(f"最后一个作品 {last_work_id} 下载不完整 ({downloaded_pages}/{total_pages} 页)，将重新下载")
            
            logger.info(f"找到 {len(existing_ids)} 个已完整下载的作品")
            
        except Exception as e:
            logger.error(f"获取已下载作品列表时出错: {str(e)}")
        
        return existing_ids

    def verify_login(self):
        """验证登录状态"""
        try:
            verify_url = 'https://www.pixiv.net/ajax/user/extra'
            response = self.session.get(verify_url, headers=self.headers)
            
            if response.status_code == 200 and not response.json().get('error'):
                logger.info("Cookie 有效，已成功登录！")
                return True
            else:
                logger.error("Cookie 无效或已过期！")
                return False
                
        except Exception as e:
            logger.error(f"验证登录状态时出错: {str(e)}")
            return False

    def get_author_works(self, author_id):
        """获取作者的所有作品ID"""
        works = []
        try:
            url = f'https://www.pixiv.net/ajax/user/{author_id}/profile/all'
            response = self.session.get(url, headers=self.headers)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('error') == False:
                    illustrations = data['body']['illusts']
                    works.extend(list(illustrations.keys()))
                    logger.info(f"获取到 {len(works)} 个作品ID")
            
        except Exception as e:
            logger.error(f"获取作品列表出错: {str(e)}")

        return works

    def download_work(self, work_id):
        """下载单个作品的所有图片到独立文件夹"""
        try:
            # 获取作品详情
            url = f'https://www.pixiv.net/ajax/illust/{work_id}'
            response = self.session.get(url, headers=self.headers)
            
            if response.status_code != 200:
                logger.error(f"获取作品 {work_id} 详情失败")
                return
                
            data = response.json()
            if data.get('error'):
                logger.error(f"获取作品 {work_id} 详情出错")
                return
                
            # 获取作品信息
            pages = data['body']['pageCount']
            urls = data['body']['urls']
            title = data['body']['title']
            
            # 创建作品文件夹（使用作品ID和标题）
            safe_title = "".join(c for c in title if c not in r'<>:"/\|?*')
            folder_name = f"{work_id}_{safe_title}"
            work_dir = os.path.join(self.save_dir, folder_name)
            
            if not os.path.exists(work_dir):
                os.makedirs(work_dir)
                logger.info(f"创建文件夹: {folder_name}")
            
            # 下载所有页面到该文件夹
            for page in range(pages):
                image_url = urls['regular'].replace('_p0', f'_p{page}')
                filename = f'{work_id}_p{page}.jpg'
                save_path = os.path.join(work_dir, filename)
                
                if os.path.exists(save_path):
                    logger.info(f"文件 {filename} 已存在，跳过")
                    continue
                
                headers = self.headers.copy()
                headers['Referer'] = f'https://www.pixiv.net/artworks/{work_id}'
                
                response = self.session.get(image_url, headers=headers)
                if response.status_code == 200:
                    with open(save_path, 'wb') as f:
                        f.write(response.content)
                    logger.info(f"下载成功: {filename}")
                    time.sleep(random.uniform(1, 3))
                else:
                    logger.error(f"下载失败: {filename}")
                
        except Exception as e:
            logger.error(f"下载作品 {work_id} 时出错: {str(e)}")

    def download_all_works(self, author_id):
        """下载作者的所有作品"""
        if not self.verify_login():
            return
            
        # 获取作者的所有作品ID
        works = self.get_author_works(author_id)
        logger.info(f"共找到 {len(works)} 个作品")
        
        # 获取已下载的作品ID（会自动检查最后一个作品的完整性）
        existing_works = self.get_existing_work_ids()
        
        # 过滤出未下载的作品
        new_works = [work_id for work_id in works if work_id not in existing_works]
        logger.info(f"其中 {len(existing_works)} 个作品已完整下载，{len(new_works)} 个作品待下载")
        
        # 下载新作品
        for i, work_id in enumerate(new_works, 1):
            logger.info(f"正在下载第 {i}/{len(new_works)} 个作品 (ID: {work_id})")
            self.download_work(work_id)
            time.sleep(random.uniform(2, 5))

if __name__ == '__main__':
    try:
        COOKIE = ''  # 从GUI界面获取cookie
        AUTHOR_ID = ''  # 从GUI界面获取作者ID
        
        crawler = PixivCookieCrawler(COOKIE)
        crawler.download_all_works(AUTHOR_ID)
        
    except KeyboardInterrupt:
        logger.info("\n用户中断下载")
    except Exception as e:
        logger.error(f"程序遇到错误: {str(e)}")