# Küresel Siber Güvenlik Etkinlikleri ve Yarışmaları İçin Bütünleşik Takip Platformu
## Kapsamlı Teknik Mimari ve Güvenlik Araştırma Raporu

---

## 1. Yönetici Özeti

Siber güvenlik alanı, bilginin yarılanma ömrünün son derece kısa olduğu ve sürekli öğrenmenin bir zorunluluk haline geldiği dinamik bir ekosistemdir. Bu ekosistemin can damarlarını, teknik yetkinliklerin sınandığı "Capture The Flag" (CTF) yarışmaları ve en güncel zafiyetlerin tartışıldığı BlackHat, DEFCON, FOSDEM gibi prestijli konferanslar oluşturmaktadır. Ancak, bu etkinliklerin duyurulduğu, yönetildiği ve arşivlendiği platformların dağınıklığı, profesyoneller ve araştırmacılar için ciddi bir veri asimetrisi ve takip zorluğu yaratmaktadır. Mevcut durumda, bir güvenlik uzmanının küresel etkinlikleri takip edebilmesi için onlarca farklı RSS kaynağını, GitHub deposunu, Twitter akışını ve kapalı devre mobil uygulama bildirimlerini izlemesi gerekmektedir. Bu fragmante yapı, kritik eğitim fırsatlarının kaçırılmasına, yanlış zaman planlamalarına ve bilgi kirliliğine yol açmaktadır.

Bu rapor, söz konusu problemi çözmek amacıyla tasarlanan; dünya genelindeki tüm siber güvenlik yarışmalarını, konferansları, çalıştayları ve bildiri çağrılarını (CFP) tek bir çatı altında toplayan, ölçeklenebilir, güvenli ve kişiselleştirilebilir bir "Siber Güvenlik Etkinlik Takip ve Yönetim Platformu"nun teknik fizibilitesini, mimari tasarımını ve güvenlik gereksinimlerini en ince detayına kadar incelemektedir. Rapor, veri toplama (ingestion) katmanından kullanıcı arayüzüne, güvenlik sıkılaştırmasından (hardening) veri normalizasyonuna kadar uçtan uca bir teknik yol haritası sunmaktadır.

Analiz sürecinde, CTFtime gibi sektör standardı otoritelerin API yapıları, Chaos Computer Club (CCC) ve FOSDEM tarafından geliştirilen Frab ve Pentabarf gibi açık kaynak konferans yönetim protokolleri, ve BlackHat/DEFCON gibi ticari etkinliklerin kapalı devre veri yapıları derinlemesine incelenmiştir. Ayrıca, heterojen veri kaynaklarının entegrasyonu sırasında ortaya çıkabilecek Server-Side Request Forgery (SSRF), XML External Entity (XXE) ve iCalendar Injection gibi kritik güvenlik riskleri tehdit modellemesi ile ele alınmış ve savunma mimarileri geliştirilmiştir. Raporun temel çıktısı, siber güvenlik topluluğunun ihtiyaçlarına yanıt veren, "Security by Design" prensibiyle geliştirilmiş, merkezi ve akıllı bir platformun teknik tasarım dokümanıdır.

---

## 2. Giriş ve Problem Uzayı Analizi

### 2.1. Siber Güvenlik Ekosisteminde Veri Entropisi
Siber güvenlik sektörü, diğer bilişim disiplinlerinden farklı olarak, son derece topluluk odaklı ve merkeziyetsiz bir yapı sergiler. Bilgi üretimi ve paylaşımı, akademik kurumlardan ziyade, bağımsız araştırma grupları, hacker kolektifleri ve endüstriyel konferanslar aracılığıyla gerçekleşir. Bu durum, etkinlik verilerinin de standart bir formatta ve tek bir merkezde toplanmasını imkansız hale getirmiştir.

Mevcut manzarada bir güvenlik araştırmacısı veya CTF oyuncusu şu veri kaynaklarını manuel olarak korele etmek zorundadır:

* **CTF Yarışmaları:** Ağırlıklı olarak CTFtime.org üzerinden takip edilse de, birçok yerel veya üniversite tabanlı yarışma sadece Discord sunucularında veya Twitter (X) duyurularında yer almaktadır. CTFtime verileri dahi, organizatörlerin manuel girişine dayandığı için zaman zaman tutarsızlıklar içerebilmektedir.
* **Akademik ve Sektörel Konferanslar:** BlackHat, RSA, DEFCON gibi devasa organizasyonlar kendi özel mobil uygulamalarını (Swapcard, Cvent) kullanırken; BSides, FOSDEM, CCC gibi topluluk etkinlikleri XML tabanlı açık kaynak sistemleri (Frab, Pretalx) tercih etmektedir. Akademik konferanslar (USENIX Security, ACM CCS) ise genellikle statik HTML sayfaları veya WikiCFP gibi eski nesil platformları kullanır.
* **Yerel Buluşmalar ve Eğitimler:** Meetup.com, Eventbrite veya GitHub üzerindeki "Awesome" listeleri üzerinden duyurulan bu etkinlikler, genellikle standart bir veri şemasına sahip değildir ve takibi en zor olan gruptur.

Bu veri dağınıklığı, "Information Noise" (Bilgi Gürültüsü) yaratarak, kullanıcının kendi ilgi alanına (örneğin sadece "Binary Exploitation" veya "Android Security") uygun etkinlikleri filtrelemesini zorlaştırmaktadır. Kullanıcılar, yüzlerce alakasız etkinlik arasında kaybolmakta ve manuel takvim yönetimi (Notion şablonları, Excel tabloları) ile vakit kaybetmektedir.

### 2.2. Çözüm Vizyonu: Birleşik Tehdit ve Etkinlik İstihbaratı
Önerilen platformun temel vizyonu, siber güvenlik etkinlik verilerini bir tür "Tehdit İstihbaratı" (Threat Intelligence) verisi gibi ele alıp; toplayan, zenginleştiren, normalize eden ve kullanıcıya sunan bir "Event Intelligence" sistemi kurmaktır. Bu sistem sadece "ne zaman ve nerede" sorularına değil, "kimler katılıyor", "hangi konular işlenecek", "benim yetkinlik setime uygun mu" sorularına da yanıt verebilmelidir.

Platformun teknik kapsamı şu ana sütunlar üzerine inşa edilmiştir:
1.  **Çok Modlu Veri Toplama (Multi-modal Ingestion):** REST API, GraphQL, XML Feed, iCal Aboneliği ve Web Scraping tekniklerinin hibrit kullanımı.
2.  **Semantik Analiz ve Etiketleme:** Etkinlik açıklamalarının NLP (Doğal Dil İşleme) ile analiz edilerek otomatik etiketlenmesi (örn. "heap spraying" geçen bir konuşmanın otomatik olarak "Exploit Development" kategorisine alınması).
3.  **Güvenli Entegrasyon:** Platformun kendisinin bir saldırı vektörü haline gelmemesi için, dış kaynaklardan gelen verilerin sıkı güvenlik denetimlerinden geçirilmesi.

---

## 3. Veri Kaynakları Mimarisi ve Entegrasyon Stratejileri

Platformun başarısı, beslendiği veri kaynaklarının çeşitliliğine, doğruluğuna ve güncelliğine doğrudan bağlıdır. Ancak her veri kaynağı farklı bir teknolojik altyapı, veri formatı ve erişim kısıtlaması sunmaktadır. Bu bölümde, siber güvenlik dünyasının ana veri kaynakları ve bunlarla entegrasyonun teknik detayları incelenmiştir.

### 3.1. CTFtime ve Yarışma Verileri
CTFtime, küresel CTF ekosisteminin de facto otoritesidir ve yarışma takvimi, takım sıralamaları ve yarışma sonuçları (scoreboard) için birincil kaynaktır. Ancak CTFtime verilerine erişim, basit bir API entegrasyonundan daha fazlasını gerektirir.

#### 3.1.1. CTFtime API Yapısı ve Kısıtlamaları
CTFtime, veriye erişim için halka açık bir REST API sunmaktadır. Bu API, JSON formatında yanıt döndürür ve temel olarak `/api/v1/events/` endpoint'i üzerinden belirli bir zaman aralığındaki yarışmaları listeler. Bir yarışma objesi şu kritik verileri içerir:
* **ID ve Metadata:** CTFtime üzerindeki benzersiz ID, yarışma başlığı, logosu ve formatı (Jeopardy vs Attack-Defense).
* **Zaman Bilgisi:** `start` ve `finish` alanları ISO 8601 formatında veya Unix Timestamp olarak verilir. Zaman dilimi yönetimi burada kritiktir, çünkü yarışmalar küreseldir ve genellikle UTC baz alınır.
* **Organizatör ve Erişim:** Organizatör takımın ID'si, yarışmanın resmi web sitesi (`url`) ve CTFtime üzerindeki sayfası (`ctftime_url`).
* **Ağırlık (Weight):** Yarışmanın zorluk derecesini ve prestijini belirleyen puan katsayısı. Bu veri, kullanıcıların "sadece yüksek prestijli yarışmaları göster" filtresi için hayati önem taşır.

Ancak CTFtime, verilerinin "clone" siteler oluşturmak amacıyla kullanılmasına karşı katı politikalara sahiptir. API dokümantasyonu, verilerin mobil uygulamalar ve veri analizi için kullanılabileceğini belirtse de, agresif veri çekme işlemleri (scraping) IP engellemeleriyle sonuçlanabilir. Rate limiting (istek sınırlaması) mekanizmaları, platformun tasarımında "Lazy Synchronization" ve "Caching Proxy" stratejilerini zorunlu kılar.

#### 3.1.2. Akıllı Senkronizasyon Stratejisi
CTFtime sunucularını yormamak ve platformun performansını artırmak için şu mimari uygulanmalıdır:
* **Incremental Fetching (Artımlı Çekme):** Sadece `finish_date` değeri gelecekte olan veya son 48 saat içinde güncellenmiş etkinlikler sorgulanmalıdır. Geçmiş etkinlik verileri (arşiv), platformun kendi veritabanında saklanmalı ve tekrar tekrar CTFtime'dan istenmemelidir.
* **Redis Caching:** API yanıtları, Redis gibi bir in-memory veritabanında önbelleğe alınmalıdır. Örneğin, `/api/v1/top/` endpoint'i (takım sıralamaları) günde sadece bir kez değişebileceği için, bu verinin TTL (Time-to-Live) süresi 24 saat olarak ayarlanabilir. Etkinlik listesi ise daha dinamik olduğu için 1-2 saatlik bir TTL yeterlidir.
* **User-Agent Yönetimi:** İsteklerde kullanılan User-Agent başlığı, platformun kimliğini açıkça belirtmeli ve iletişim bilgisi içermelidir (örn. `SecEventTracker/1.0 (+https://platform.com/contact)`). Bu, şeffaflık sağlar ve olası engellemelerin önüne geçer.

### 3.2. Açık Kaynak Konferans Yönetim Sistemleri (Frab, Pentabarf, Pretalx)
Topluluk odaklı siber güvenlik konferansları (CCC, FOSDEM, FrOSCon, DebConf), ticari kaygılardan uzak oldukları için verilerini açık standartlarla paylaşırlar. Bu standartların başında Pentabarf XML ve onun modern türevleri olan Frab ve Pretalx gelir.

#### 3.2.1. Pentabarf XML Şeması Analizi
Pentabarf formatı, bir konferansın tüm programını hiyerarşik bir XML yapısında sunar. Platformun bu veriyi işlemesi için özel bir "XML Ingestion Engine" geliştirmesi gerekir. Tipik bir Pentabarf/Frab XML dosyası (`schedule.xml`) şu hiyerarşiyi izler:
* `<schedule>`: Kök element.
* `<conference>`: Konferans metadata'sı (başlık, kısaltma, şehir).
* `<day index="1" date="2025-08-16">`: Gün bazlı ayrım.
* `<room name="Main Hall">`: Salon bazlı ayrım.
* `<event id="1234">`: Tekil etkinlik/konuşma.
* `<start>`, `<duration>`: Zamanlama.
* `<title>`, `<abstract>`, `<description>`: İçerik detayları.
* `<persons>`: Konuşmacı listesi.
* `<links>`: Sunum dosyaları veya ilgili linkler.

Bu yapının parse edilmesi sırasında karşılaşılan en büyük zorluk, veri alanlarının opsiyonel olmasıdır (örn. her konuşmanın bir abstract'ı olmayabilir). Ayrıca XML parsing işlemi, siber güvenlik açısından XML External Entity (XXE) riski taşır. Platform, güvenilmeyen kaynaklardan gelen bu XML dosyalarını işlerken standart parserlar yerine güvenli kütüphaneler kullanmalıdır (Detaylar Bölüm 6.1'de).

#### 3.2.2. Pretalx ve JSON Desteği
Modern konferanslar giderek artan oranda Pretalx sistemine geçiş yapmaktadır. Pretalx, Pentabarf XML formatını desteklemekle birlikte, geliştiriciler için daha dostane olan JSON export seçeneği de sunar. JSON formatı, veri boyutu (payload size) açısından daha verimlidir ve XML'e özgü güvenlik zafiyetlerinin çoğundan muaftır. Platformun entegrasyon modülü, hedef URL'in content-type başlığını kontrol ederek (`application/xml` vs `application/json`) uygun parser'ı dinamik olarak seçmelidir.

### 3.3. Kapalı Devre Ekosistemler: BlackHat ve DEFCON
Sektörün devleri olan BlackHat ve DEFCON, verilerini açık bir API ile sunmazlar. Bu etkinlikler genellikle Swapcard, Cvent veya kendi geliştirdikleri özel mobil uygulamalar üzerinden katılımcılara ulaşır. Bu durum, veri toplama sürecini "Entegrasyon"dan "Tersine Mühendislik" (Reverse Engineering) boyutuna taşır.

#### 3.3.1. Mobil Uygulama API'lerinin Analizi ve Tersine Mühendislik
BlackHat ve DEFCON'un resmi mobil uygulamaları, arka planda sunucularla veri alışverişi yapan zengin istemcilerdir. Bu veriye erişmek için Traffic Interception teknikleri kullanılmalıdır:
* **Proxy Kurulumu:** Burp Suite veya MITMProxy kullanılarak, mobil cihazın trafiği izlenir. Uygulamanın sunucuyla konuşurken kullandığı endpoint'ler (örn. `https://api.swapcard.com/graphql` veya `https://blackhat.mobile-api.net/v1/schedule`) tespit edilir.
* **Certificate Pinning Bypass:** Modern uygulamalar, trafiğin araya girilerek (Man-in-the-Middle) izlenmesini önlemek için SSL Pinning kullanır. Frida veya Objection gibi araçlar kullanılarak, uygulamanın çalışma zamanında (runtime) bu kontrolleri aşması sağlanabilir. Bu sayede şifreli trafik çözülerek JSON veri yapısı ortaya çıkarılır.
* **API Token Analizi:** Uygulamanın kimlik doğrulama mekanizması analiz edilmelidir. Genellikle bir "Bearer Token" veya "API Key" kullanılır. Eğer bu anahtarlar statik ise (hardcoded), platform tarafından veri çekmek için kullanılabilir. Ancak dinamik ve kullanıcı bazlı ise, anonim bir "dummy" hesap oluşturularak bu hesabın token'ı üzerinden veri çekilmelidir.

**Uyarı:** Bu yöntemler teknik olarak mümkün olsa da, etkinlik organizatörlerinin Kullanım Koşulları'na (Terms of Service) aykırı olabilir. Platform geliştiricileri, bu yöntemleri kullanmadan önce yasal riskleri değerlendirmeli veya organizatörlerden resmi veri erişim izni talep etmelidir. Alternatif olarak, topluluk tarafından oluşturulan ve gönüllülerce güncellenen HackerTracker gibi açık kaynak projelerin veri setleri (JSON formatında) kullanılabilir. HackerTracker, DEFCON ve yan etkinliklerin verilerini GitHub üzerinde barındırdığı JSON dosyalarıyla sunar, bu da scraping ihtiyacını ortadan kaldıran güvenli ve etik bir alternatiftir.

### 3.4. Dağınık Veri Kaynakları: GitHub ve Statik Siteler
Küçük ölçekli etkinlikler, yerel BSides organizasyonları veya akademik çalıştaylar genellikle bir veritabanı yönetim sistemine sahip değildir. Bu etkinliklerin verileri GitHub üzerindeki Markdown dosyalarında (`README.md`) veya statik HTML sayfalarında bulunur.
* **GitHub Awesome Listeleri:** `infosec-conferences` gibi popüler repolar, etkinlikleri yıllara ve aylara göre ayrılmış Markdown dosyalarında tutar. Platform, GitHub API'sini kullanarak bu dosyaların "Raw" içeriğini çekmeli ve Regular Expression (RegEx) veya Markdown AST (Abstract Syntax Tree) parser'lar kullanarak tablo yapısını (`| Event | Date | Location |`) anlamlandırmalıdır. Bu yöntem, binlerce küçük etkinliğin tek seferde sisteme dahil edilmesini sağlar.
* **HTML Scraping:** Yapısal olmayan web siteleri için BeautifulSoup veya Scrapy gibi Python kütüphaneleri kullanılarak özel "Scraper"lar yazılmalıdır. Ancak web sitesi tasarımları sık değiştiği için bu yöntem bakım maliyeti yüksek (fragile) bir yöntemdir ve sadece başka alternatifi olmayan yüksek değerli etkinlikler için kullanılmalıdır.

---

## 4. Veri Normalizasyonu ve Birleşik Etkinlik Modeli (Unified Event Model)

Farklı kaynaklardan, farklı formatlarda (JSON, XML, iCal, Markdown) ve farklı dillerde gelen verilerin tek bir potada eritilmesi, platformun en kritik mühendislik problemidir. Kullanıcıya tutarlı bir deneyim sunmak için tüm veriler Birleşik Etkinlik Modeli (Unified Event Model) adı verilen standart bir şemaya dönüştürülmelidir.

### 4.1. Veri Ontolojisi ve Şema Tasarımı
Siber güvenlik etkinlikleri hiyerarşik ve ilişkisel bir yapıya sahiptir. Tasarlanacak veri modeli hem bir CTF yarışmasının puanlama detaylarını hem de bir konferansın konuşmacı biyografisini kapsayacak esneklikte olmalıdır. Önerilen veri modeli şu temel varlıkları (entities) içerir:
* **EventSeries (Etkinlik Serisi):** Etkinliğin üst kimliğidir. Örn. "DEF CON", "Google CTF". Logo, web sitesi ve genel açıklama burada tutulur.
* **EventInstance (Etkinlik Örneği):** Serinin belirli bir zamandaki tezahürüdür. Örn. "DEF CON 33", "Google CTF 2025 Quals". Başlangıç-bitiş tarihleri, lokasyon (fiziksel/sanal) ve format bilgisi buradadır.
* **Session (Oturum/Aktivite):** Etkinliğin en küçük yapı taşıdır.
    * Bir konferans için: "Keynote Konuşması", "Workshop", "Panel".
    * Bir CTF için: "Challenge (Soru)", "Kategori".
    * Özellikleri: Başlık, Özet (Abstract), Başlangıç/Bitiş Saati, Salon/Oda, Konuşmacılar, Etiketler (Tags).
* **Person (Kişi):** Konuşmacılar, eğitmenler veya CTF organizatörleri. Ad, Biyografi, Sosyal Medya Linkleri, Bağlı Olduğu Kurum.

**Normalizasyon Tablosu:**

| Alan | CTFtime Karşılığı | Frab/Pentabarf Karşılığı | HackerTracker (DEFCON) Karşılığı | Unified Model Hedefi |
| :--- | :--- | :--- | :--- | :--- |
| **Başlık** | title | event/title | title | title |
| **Özet** | description | event/abstract + description | description | description (Markdown) |
| **Zaman** | start (ISO8601) | date + start (HH:MM) | begin (ISO8601) | start_time (UTC DateTime) |
| **Konum** | location / onsite | room | location/name | location JSON `{lat, long, name}` |
| **Kategori** | format (Jeopardy) | track (Security) | type (Talk, Party) | tags Array |

### 4.2. Zaman Dilimi Mühendisliği (Timezone Engineering)
Küresel etkinliklerde en sık yapılan hata, zaman dilimlerinin yanlış yönetilmesidir. Bir kullanıcı İstanbul'da iken Las Vegas'taki DEFCON programını görüntülüyorsa, saatlerin doğru çevrilmesi gerekir.
* **Depolama:** Veritabanında tüm zaman verileri istisnasız olarak UTC (Coordinated Universal Time) formatında saklanmalıdır.
* **Dönüşüm:** iCalendar dosyaları (.ics) parse edilirken TZID (Time Zone ID) parametresi dikkatle incelenmelidir. "America/Los_Angeles" gibi IANA zaman dilimi tanımları `pytz` veya `zoneinfo` kütüphaneleri ile UTC'ye çevrilmelidir.
* **Gösterim:** Kullanıcı arayüzünde (Frontend), tarayıcının yerel zaman dilimi algılanarak veya kullanıcının profil ayarlarındaki tercihine göre dinamik dönüşüm yapılmalıdır.

### 4.3. İçerik Zenginleştirme ve Otomatik Etiketleme
Ham veriler genellikle eksik veya düzensiz etiketlenmiştir. Platform, veriyi sadece saklamakla kalmamalı, zenginleştirmelidir.
* **NLP ile Kategorizasyon:** Etkinlik başlığı ve özet metni üzerinde Anahtar Kelime Çıkarımı (Keyword Extraction) uygulanmalıdır. Örneğin, metin içinde "ROP", "Heap", "Stack", "Buffer Overflow" kelimeleri geçiyorsa, sistem bu etkinliği otomatik olarak "Binary Exploitation" ve "Pwn" etiketleriyle işaretlemelidir. Benzer şekilde "K8s", "Docker", "Container" kelimeleri "Cloud Security" etiketini tetiklemelidir.
* **Coğrafi Zenginleştirme:** "Las Vegas" verisi, Google Maps veya OpenStreetMap API'leri kullanılarak koordinatlara (Enlem/Boylam) çevrilmeli, böylece harita üzerinde gösterim mümkün kılınmalıdır.

---

## 5. Platform Güvenlik Mimarisi ve Tehdit Modellemesi

Bir siber güvenlik platformu geliştirirken, güvenlik "eklenen bir özellik" değil, tasarımın temel taşı (Foundation) olmalıdır. Platform, dış dünyadan kontrolsüz ve güvenilmeyen verileri (Untrusted Input) sürekli olarak işlediği için, saldırganlar için cazip bir hedeftir. Aşağıda, platforma yönelik spesifik tehditler ve bunlara karşı geliştirilen savunma mimarisi detaylandırılmıştır.

### 5.1. XML External Entity (XXE) Saldırılarına Karşı Savunma
Konferans verilerini (Pentabarf/Frab) XML formatında işlerken en büyük risk XXE saldırılarıdır. Saldırgan, zararlı bir XML dosyası hazırlayarak (veya meşru bir konferans sitesini hackleyip dosyasını değiştirerek) platform sunucusunun yerel dosyalarını okuyabilir veya sunucuyu bir DoS saldırısına maruz bırakabilir.

**Tehdit Senaryosu:**
Saldırgan şu içeriğe sahip bir XML dosyasını platforma besler:

```xml
<!DOCTYPE foo>
<schedule>
  <conference>
    <title>&xxe;</title>
  </conference>
</schedule>
