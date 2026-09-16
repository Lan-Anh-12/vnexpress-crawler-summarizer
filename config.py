import os
from dotenv import load_dotenv

# nạp file .env 
load_dotenv()

# lấy key của database và al
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("PUBLISHABLE_KEY")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

GEMINI_MODEL = "gemini-3.1-flash-lite"

# số lượng bài tối đa của mỗi danh mục/ngày 
MAX_ARTICLES_PER_CATEGORY = 3 

# số lượng bài viết tối đa nạp vào file data.json
MAX_ARTICLES_TO_EXPORT = 30

# tối đa số lần tóm tắt hỏng bài
error_count = 3

# Hệ thống link API công khai (RSS Feed) của VnExpress
TARGET_CATEGORIES = {

    "Giáo dục":"https://vnexpress.net/rss/giao-duc.rss" ,
    "Khoa học công nghệ":"https://vnexpress.net/rss/khoa-hoc-cong-nghe.rss",
    "Du lịch":"https://vnexpress.net/rss/du-lich.rss",
    "Thế giới": "https://vnexpress.net/rss/the-gioi.rss",
    "Kinh doanh": "https://vnexpress.net/rss/kinh-doanh.rss",
    "Bất động sản":"https://vnexpress.net/rss/bat-dong-san.rss",
    "Giải trí":"https://vnexpress.net/rss/giai-tri.rss",
    "Pháp luật":"https://vnexpress.net/rss/phap-luat.rss"
    

}

