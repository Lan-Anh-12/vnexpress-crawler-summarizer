from google import genai
import config

# Khởi tạo kết nối tới trợ lý AI
ai_client = genai.Client(api_key=config.GEMINI_API_KEY)

def summarize_text(full_text):
    try:
        prompt = f"""
        Bạn là một trợ lý biên tập báo chí chuyên nghiệp. 
        Hãy tóm tắt bài báo dưới đây thành đúng 3 gạch đầu dòng ngắn gọn, cô đọng bằng tiếng Việt.
        Tuyệt đối không thêm lời mở đầu hay kết luận, chỉ trả về đúng 3 gạch đầu dòng.

        Nội dung bài báo:
        {full_text}
        """
        response = ai_client.models.generate_content(
            model= config.GEMINI_MODEL, 
            contents=prompt
        )
        return response.text.strip()

    except Exception as e:
        print(f"Lỗi khi tóm tắt: {e}")
        return None
