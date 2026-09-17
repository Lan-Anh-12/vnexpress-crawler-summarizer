import config
import json 
from supabase import create_client, Client


supabase: Client = create_client(config.SUPABASE_URL, config.SUPABASE_KEY)

# check url đã tồn tại hay chưa
def is_url_exists(url):
    try:
        check_db = supabase.table('article_summary').select('id').eq("url",url).execute()
        if check_db.data:
            return True
        else:
            return False
    except Exception as e:
        print(f"Lỗi khi chèn dữ liệu vào database: {e}")
        return False

#Truy vấn dữ liệu từ Supabase và xuất ra file data.json tĩnh.
def export_to_json():
    print(f'Truy vấn tối đa {config.MAX_ARTICLES_TO_EXPORT} bài')

    try:
        db_data = supabase.table("article_summary")\
            .select("*")\
            .order("id", desc=True)\
            .limit(config.MAX_ARTICLES_TO_EXPORT)\
            .execute()

        with open("data.json","w",encoding="utf-8") as f:
            json.dump(db_data.data, f, ensure_ascii=False, indent=4)
        print(" Đã cập nhật xong file data.json mới nhất")
    except Exception as e:
        print(f"Lỗi khi xuất file JSON dữ liệu: {e}")

