# 1. Bazaviy rasm
FROM python:3.10-slim-buster

# 2. Ishchi papkani belgilaymiz
WORKDIR /app

# 3. System paketlarini (agar kerak bo‘lsa) va pip upgrade
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       libpq-dev \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --upgrade pip

# 4. requirements.txt ni konteynerga nusxa qilish va paketlarni o‘rnatish
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Loyiha fayllarini konteynerga nusxa ko‘chirib olish
COPY . .

# 6. Django statik fayllar uchun papka (agar kerak bo‘lsa)
#    (Masalan, collectstatic ishlashini xohlasangiz, keyinroq ishlatishingiz mumkin)
# RUN python manage.py collectstatic --noinput

# 7. Konteyner ishga tushganda bajariladigan buyruq:
#    Django serverni 0.0.0.0:8000 da ishga tushiramiz
CMD ["python", "manage.py", "runserver", "0.0.0.0:8010"]
