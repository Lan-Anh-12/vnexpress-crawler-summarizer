import requests
from bs4 import BeautifulSoup
import config
import time

from db_service import supabase, is_url_exists, export_to_json
from ai_service import summarize_text

# Trả về danh sách ALL TIÊU ĐỀ, LINK bài viết của 1 thể loại
def get_articles_from_rss(rss_url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    articles = []
    try:
        response = requests.get(rss_url, headers=headers, timeout=10)
        if response.status_code != 200:
            return articles     
        # Đọc cấu trúc XML của RSS Feed bằng lxml parser
        soup = BeautifulSoup(response.content, 'xml')
        items = soup.find_all('item')
        
        for item in items:
            title_tag = item.find('title')
            link_tag = item.find('link')
            
            if title_tag and link_tag:
                articles.append({
                    "title": title_tag.text.strip(),
                    "url": link_tag.text.strip()
                })
        return articles
    except Exception as e:
        print(f" Lỗi khi đọc dữ liệu từ RSS: {e}")
        return articles

# lấy nội dung của 1 bài viết cụ thể từ link 
def crawl_full_content(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    try:
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code != 200: 
            return None
        
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # Thẻ chứa nội dung bài viết chính của VnExpress
        content_div = soup.find('article', class_='fck_detail')
        if not content_div: 
            return None
        
        paragraphs = content_div.find_all('p')
        full_text = "\n".join([p.text.strip() for p in paragraphs])
        
        if len(full_text) < 150: 
            return None # Bỏ qua bài viết quá ngắn hoặc bài video/ảnh
            
        return full_text
    except Exception as e:
        print(f" Lỗi khi bóc tách chữ từ bài báo: {e}")
        return None

# HÀM MAIN CỦA CHƯƠNG TRÌNH
def main():
    print("========================================")
    print("HỆ THỐNG CÀO BÁO VÀ TÓM TẮT AI BẮT ĐẦU CHẠY")
    print("========================================\n")

    total_errors = 0 

    # Duyệt qua các danh mục được bật trong file config.py
    for cat_name, cat_url in config.TARGET_CATEGORIES.items():
        print(f"ĐANG XỬ LÝ THỂ LOẠI: [{cat_name}]")
        
        raw_articles = get_articles_from_rss(cat_url)
        print(f"-> Tìm thấy {len(raw_articles)} bài viết từ thể loại {cat_name.upper()}.")
        count = 0 # Biến đếm số lượng bài xử lý thành công
        
        for article in raw_articles:
            # check số lượng bài lỗi
            if total_errors >= 3:
                print(f"Phát hiện hệ thống lỗi quá {total_errors} bài.Tự động dừng chương trình.")
                break

            # Giới hạn số lượng bài cào cho mỗi danh mục theo config
            if count >= config.MAX_ARTICLES_PER_CATEGORY:
                print(f" -> Đã đạt giới hạn {config.MAX_ARTICLES_PER_CATEGORY} bài cho chuyên mục này.")
                break
                
            url = article['url']
            title = article['title']
            
            # 1. Gọi hàm is_url_exists từ db_service để kiểm tra trùng lặp
            try:
                check_db = supabase.table('article_summary').select('id').eq("url", url).execute()
                if len(check_db.data) > 0:
                    continue
            except Exception:
                if is_url_exists(url): 
                    continue 
            print(f"Đang xử lý bài: {title}")
            
            # 2. Cào nội dung chi tiết
            full_content = crawl_full_content(url)
            if not full_content:
                print("Bài viết có nội dung chữ quá ít or không thể cào, bỏ qua.")
                continue
                
            # 3. Gọi hàm tóm tắt từ ai_service (Bản Gemini 3.5 Flash)
            summary_result = summarize_text(full_content)
            if not summary_result:
                print("Không lấy được tóm tắt từ AI, bỏ qua.")
                total_errors += 1
                time.sleep(6)
                continue
                
            # 4. Thực hiện chèn dữ liệu trực tiếp vào bảng article_summary của bạn
            try:
                final_data = {
                    "url": url,
                    "title": title,
                    "category": cat_name,
                    "summary": summary_result
                }
                supabase.table("article_summary").insert(final_data).execute()
                print(" Đã lưu bài viết vào Supabase Database!")
                count += 1
                time.sleep(8)
            except Exception as e:
                print(f" Lỗi khi lưu bài viết vào database: {e}")
                
    # 5. Gọi hàm xuất file JSON từ db_service sau khi hoàn thành quy trình cào
    export_to_json()
    
    print("\n========================================")
    print("HOÀN THÀNH TOÀN BỘ QUY TRÌNH")
    print("========================================")

if __name__ == "__main__":
    main()
