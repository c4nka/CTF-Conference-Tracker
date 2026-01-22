<div align="center">
<img src="docs/logo.png" width="500" height="500">
</div>

# 🛡️ CyberSec Event Tracker

![Project Status](https://img.shields.io/badge/Status-Geliştirme_Aşamasında-orange)
![License](https://img.shields.io/badge/License-MIT-blue)

> **Dünya genelindeki siber güvenlik yarışmalarını (CTF) ve prestijli konferansları (BlackHat, DEFCON) tek bir çatı altında toplayan, kişiselleştirilebilir etkinlik takip platformu.**

## 🎯 Proje Amacı

Siber güvenlik dünyasındaki dinamizmi yakalamak zor olabilir. Bu proje, dağınık haldeki etkinlik verilerini **CTFtime** ve konferans sitelerinden otomatik olarak çeker, kullanıcının teknik ilgi alanlarına (Web, Crypto, Pwn vb.) göre filtreler ve kişiselleştirilmiş bir takvim sunar.

---

## 🚀 Beklenen Özellikler

| Özellik | Açıklama |
| :--- | :--- |
| **📅 Etkinlik Takvimi** | Yaklaşan CTF ve konferansları interaktif bir takvim üzerinde gösterme. |
| **🤖 Otomatik Veri Çekme** | `CTFtime` ve resmi konferans web sitelerinden düzenli veri kazıma (Web Scraping). |
| **🔔 Kişiselleştirme** | Kullanıcı ilgi alanlarına (Örn: *Web Security, Cryptography*) göre özel bildirimler. |
| **📚 Arşiv Sistemi** | Geçmiş etkinliklere ait *Write-up* (çözüm) ve sunum dosyalarına erişim. |

---

## 🛠️ Teknik Odak ve Yöntemler

Bu proje geliştirilirken aşağıdaki temel yöntemler hedeflenmiştir:

- **Veri Toplama (Web Scraping):** Hedef sitelerden (CTFtime, Konferanslar) veri çekilmesi.
- **Takvim Entegrasyonu (Calendar Integration):** Etkinliklerin kullanıcı takvimleri ile senkronizasyonu.
- **Filtreleme Algoritması:** İlgi alanına dayalı içerik ayrıştırma.

---

### 🤝 Katkıda Bulunma

Projeye katkıda bulunmak isterseniz lütfen bir `Issue` açın veya `Pull Request` gönderin.

1. Bu repoyu forklayın
2. Yeni bir branch oluşturun (`git checkout -b feature/YeniOzellik`)
3. Değişikliklerinizi commit edin (`git commit -m 'Yeni özellik eklendi'`)
4. Branch'inizi pushlayın (`git push origin feature/YeniOzellik`)
5. Pull Request oluşturun

## 🛠️ Gereksinimler (Prerequisites)

Projenin sorunsuz çalışabilmesi için bilgisayarınızda aşağıdaki yazılımların kurulu olması gerekmektedir:

* **Python 3.8 veya üzeri** (Python'u [buradan](https://www.python.org/downloads/) indirebilirsiniz).
* **pip** (Python paket yöneticisi - Python ile birlikte gelir).

---

## 📦 Kurulum ve Çalıştırma Talimatları

Projeyi kendi bilgisayarınızda ayağa kaldırmak için aşağıdaki adımları sırasıyla uygulayın.

### Adım 1: Gerekli Kütüphanelerin Yüklenmesi

Terminalinizi (veya Komut İstemi'ni) proje klasöründe açın ve gerekli Python kütüphanelerini yükleyin:

```bash

pip install flask requests

## Dosya Yapısının Kontrolü

siber_etkinlik_takip/
│
├── app.py                # Ana sunucu dosyası (Backend)
├── project_info.json     # Proje meta veri dosyası
├── README.md             # Proje dokümantasyonu (Bu dosya)
│
├── static/
│   └── logo.png          # Proje logosu
│
└── templates/
    └── index.html        # Arayüz dosyası (Frontend)

## Uygulamanın Başlatılması

python app.py
Başarılı olduğunda şu çıktıyı göreceksiniz: Running on http://127.0.0.1:5000

## Erişim

Web tarayıcınızı açın ve adres çubuğuna şunu yazın: http://127.0.0.1:5000

## 👤 Hazırlayan

- **Ad Soyad:** Raşit ÇANKAYA
- **Öğrenci No:** 2420191006
- **Üniversite:** İstinye Üniversitesi
- **Bölüm:** Bilişim Güvenliği Teknolojisi (İÖ)
