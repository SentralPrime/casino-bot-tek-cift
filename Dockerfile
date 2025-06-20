# Railway için optimize edilmiş Dockerfile
FROM python:3.11-slim

# Sistem bağımlılıklarını yükle
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

# Google Chrome'u yükle (güncel versiyon)
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# ChromeDriver'ı manuel yükle - sabit versiyon kullan
RUN CHROME_VERSION=$(google-chrome --version | cut -d' ' -f3 | cut -d'.' -f1) \
    && echo "Chrome major version: $CHROME_VERSION" \
    && wget -O /tmp/chromedriver.zip "https://storage.googleapis.com/chrome-for-testing-public/137.0.7151.119/linux64/chromedriver-linux64.zip" \
    && unzip /tmp/chromedriver.zip -d /tmp/ \
    && mv /tmp/chromedriver-linux64/chromedriver /usr/local/bin/ \
    && chmod +x /usr/local/bin/chromedriver \
    && rm -rf /tmp/chromedriver.zip /tmp/chromedriver-linux64 \
    && chromedriver --version

# Çalışma dizini oluştur
WORKDIR /app

# Python bağımlılıklarını kopyala ve yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama dosyalarını kopyala
COPY . .

# Railway ortam değişkenlerini ayarla
ENV RAILWAY_ENVIRONMENT=true
ENV DISPLAY=:99
ENV PORT=8080

# Port ayarla (Railway için)
EXPOSE 8080

# Flask uygulamasını başlat (deneme1.py değil app.py!)
CMD ["python", "app.py"] 