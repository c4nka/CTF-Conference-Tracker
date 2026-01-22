# Küresel Siber Güvenlik Etkinlik Takip ve CTF Aggregator Platformlarının Mimari Analizi

## Giriş
Siber güvenlik alanı, bilginin ve tehdit aktörlerinin devasa bir hızla evrildiği dinamik bir ekosistemdir. Bu ekosistemin en kritik bileşenlerini **Capture The Flag (CTF)** yarışmaları ve **BlackHat, DEFCON, BSides** gibi prestijli konferanslar oluşturmaktadır. Bu rapor, merkezi etkinlik takip platformlarının mimari yapılarını, veri mühendisliği süreçlerini ve güvenlik standartlarını siber güvenlik mühendisliği perspektifiyle ele almaktadır.

---

## 1. Teknolojinin Temel Çalışma Prensipleri ve Mimari Temelleri

Modern bir siber güvenlik etkinlik aggregator platformu, heterojen veri kaynaklarından beslenen ve bu verileri anlamlı istihbarata dönüştüren bir boru hattı (pipeline) olarak işlev görür.

### 1.1. Veri Edinimi ve Çoklu Kaynak Senkronizasyonu
Sistem; yapılandırılmış (API) ve yapılandırılmamış (Web Scraping) kaynaklardan beslenir.

| Kaynak Türü | Veri Yapısı | Entegrasyon Yöntemi | Örnek Platformlar |
| :--- | :--- | :--- | :--- |
| **Yapılandırılmış API** | JSON / REST | HTTP GET / Webhooks | CTFtime, MajorLeagueCyber |
| **Yapılandırılmamış Web** | HTML / DOM | Scraper (BeautifulSoup/Selenium) | BlackHat, DEFCON Official Pages |
| **Topluluk Odaklı** | Metin / Form | Manuel Giriş / Admin Onay | BSides, Local Meetups |
| **Sosyal Medya** | Akış / Feed | RSS / Social Media API | X (Twitter), LinkedIn Updates |

### 1.2. Olay Güdümlü Mimari (EDA) ve Asenkron Süreçler
Siber güvenlik etkinlikleri doğası gereği zaman duyarlıdır. Bu durum, sistemin **Olay Güdümlü Mimari (Event-Driven Architecture - EDA)** ile tasarlanmasını zorunlu kılar.



* **Producers (Üreticiler):** Veritabanındaki bir kaydın değişmesi veya yeni verinin çekilmesiyle olayı tetikler.
* **Brokers (Aracılar):** AWS EventBridge veya Google Eventarc gibi araçlar olayları filtreler ve yönlendirir.
* **Consumers (Tüketiciler):** Mobil bildirim servisleri veya e-posta motorları gibi uç noktalar.

### 1.3. Veri Normalizasyonu ve Şema Eşleme
Farklı kaynaklardan gelen tutarsız veriler (Örn: "Vegas" vs "Las Vegas"), merkezi bir şemaya oturtulur. Veri bütünlüğünü korumak için **1NF, 2NF ve 3NF** normal formları uygulanarak veri tekrarları önlenir.

---

## 2. En İyi Uygulama Yöntemleri ve Endüstri Standartları

### 2.1. Olay İzleme ve İsimlendirme Konvansiyonları
Karmaşıklığı önlemek için **"Nesne-Eylem" (Object-Action)** çerçevesi benimsenmelidir:
* `ctf_registered`
* `conference_bookmarked`

### 2.2. Kullanıcı Deneyimi ve Kayıt Süreçleri
Kişiselleştirme önemlidir ancak kayıt sırasında kullanıcıya çok fazla soru sormak (25+ soru), form tamamlama oranlarını **%5.7**'ye kadar düşürebilir.

### 2.3. Etik Web Kazıma ve robots.txt Uyumluluğu
* **robots.txt:** Hedef sitenin yönergelerine tam uyum sağlanmalıdır.
* **Rate Limiting:** Hedef sunucunun aşırı yüklenmesini önlemek için hız sınırlama uygulanmalıdır.
* **User-Agent:** Platform adı ve iletişim bilgileri şeffafça belirtilmelidir.

---

## 3. Benzer Açık Kaynak Projeler ve Rakip Analizi

* **CTFd:** Python (Flask) tabanlı en yaygın açık kaynak CTF çerçevesi.
* **CTFtime:** Global veri kaynağı ve puanlama standardı (JSON API sunar).
* **Hack The Box (HTB):** Oyunlaştırılmış eğitim ve yetenek değerlendirme platformu.
* **OpenCTI:** STIX2 standartlarına göre veri organize etme yeteneğine sahip tehdit istihbaratı odaklı platform.

---

## 4. Kritik Yapılandırma Dosyaları ve Parametreleri

Modern yazılım prensiplerine göre, yapılandırmalar koddan ayrılmalı ve ortam değişkenleri (`.env`) üzerinden yönetilmelidir.

### Örnek Docker Konfigürasyonu (`docker-compose.yml`)
```yaml
services:
  app:
    environment:
      - SECRET_KEY=${APP_SECRET_KEY}
      - DATABASE_URL=postgres://${DB_USER}:${DB_PASS}@db:5432/${DB_NAME}
    depends_on:
      - db
      - redis
  worker:
    command: celery -A eventpilot worker --loglevel=info
  db:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data
