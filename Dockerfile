# 1. انتخاب تصویر پایه (Base Image)
# ما از یک نسخه سبک پایتون (Slim) استفاده می‌کنیم تا حجم کانتینر کم باشد
FROM python:3.9-slim

# 2. تنظیم پوشه کاری داخل کانتینر
# یعنی: "هر دستوری که بعد از این می‌دهم، داخل پوشه /app اجرا کن"
WORKDIR /app

# 3. نصب پیش‌نیازهای سیستم (برای کتابخانه Psycopg2)
# پستگرس برای وصل شدن به فایل‌های سیستمی لینوکس نیاز دارد
RUN apt-get update && apt-get install -y libpq-dev gcc

# 4. کپی کردن لیست خرید (Requirements)
# ما اول فقط فایل requirements.txt را کپی می‌کنیم (برای استفاده از Cache داکر)
COPY req.txt .

# 5. نصب کتابخانه‌ها
RUN pip install --no-cache-dir -r req.txt
RUN python -c "import flask; print('Flask is installed')"
# 6. کپی کردن کل کد پروژه به داخل کانتینر
COPY . .

# 7. دستوری که موقع روشن شدن کانتینر اجرا می‌شود
CMD ["python", "run.py"]