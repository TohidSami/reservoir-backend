from sqlalchemy import create_engine, text

# --- اطلاعات اتصال ---
# !!! این بخش خیلی مهم است !!!
# "postgres" نام کاربری پیش‌فرض است.
# "YOUR_PASSWORD" را با پسوردی که هنگام نصب PostgreSQL گذاشتید، عوض کنید.
# "localhost:5432" آدرس سرور دیتابیس روی کامپیوتر شماست.
# "reservoir_db" نام دیتابیسی است که در فاز ۱ ساختید.

DB_URL = "postgresql://postgres:123salam@localhost:5432/test1"

try:
    # 1. ساخت "موتور" اتصال
    engine = create_engine(DB_URL)

    # 2. برقراری اتصال
    with engine.connect() as connection:
        print("--- اتصال به دیتابیس PostgreSQL موفقیت‌آمیز بود! ---")

        # 3. آماده‌سازی دستور SQL
        # (این دقیقا همان دستوری است که در pgAdmin زدید)
        sql_query = text("SELECT well_name, field_name FROM WellHeader")

        # 4. اجرای دستور
        result = connection.execute(sql_query)

        print("لیست چاه‌های موجود در دیتابیس:")

        # 5. نمایش نتایج
        for row in result:
            # row یک شیء است که می‌توانید با نام ستون به آن دسترسی داشته باشید
            print(f"  > نام چاه: {row.well_name} (میدان: {row.field_name})")

except Exception as e:
    print(f"!!! خطا: نتوانستیم به دیتابیس وصل شویم. !!!")
    print(f"جزئیات خطا: {e}")