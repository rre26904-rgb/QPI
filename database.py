import psycopg2
import os

# هذا الرابط بيقراه ريندر تلقائياً من المتغيرات
DATABASE_URL = os.getenv("DATABASE_URL")

def init_db():
    """هذه الدالة تصنع جدول النقاط إذا ما كان موجود"""
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id VARCHAR(50) PRIMARY KEY,
            points INT DEFAULT 0
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

def load_scores():
    """هذه الدالة تحل محل قراءة ملف الـ JSON"""
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, points FROM users")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        
        # تحويل البيانات إلى شكل مشابه للـ JSON (Dictionary)
        return {row[0]: row[1] for row in rows}
    except Exception as e:
        print(f"Database error: {e}")
        return {}

def save_scores(scores_dict):
    """هذه الدالة تحل محل حفظ ملف الـ JSON"""
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    
    # تحديث كل النقاط اللي تعدلت في الألعاب
    for user_id, points in scores_dict.items():
        cursor.execute("""
            INSERT INTO users (user_id, points) VALUES (%s, %s)
            ON CONFLICT (user_id) DO UPDATE SET points = EXCLUDED.points
        """, (str(user_id), points))
        
    conn.commit()
    cursor.close()
    conn.close()