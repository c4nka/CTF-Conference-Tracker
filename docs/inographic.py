import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx
import seaborn as sns
from matplotlib.patches import FancyBboxPatch

# Grafik stili
plt.style.use('seaborn-v0_8-whitegrid')

# ---------------------------------------------------------
# GÖRSEL 1: VERİ KAYNAKLARI VE ZORLUK ANALİZİ (Tablo 1 Bazlı)
# ---------------------------------------------------------
def plot_data_sources():
    data = {
        'Kaynak': ['CTFtime', 'FOSDEM/CCC', 'BlackHat/DEFCON', 'GitHub Listeleri', 'Meetup/Eventbrite'],
        'Format': ['JSON (API)', 'XML (Pentabarf)', 'Mobile API', 'Markdown', 'HTML (Scraping)'],
        'Zorluk Seviyesi': [2, 1, 3, 2, 3],  # 1: Düşük, 2: Orta, 3: Yüksek
        'Risk': [1, 1, 3, 1, 2] # 1: Düşük, 2: Orta, 3: Yüksek
    }
    df = pd.DataFrame(data)

    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Renk paleti
    colors = ['#4CAF50' if x == 1 else '#FFC107' if x == 2 else '#F44336' for x in df['Zorluk Seviyesi']]
    
    bars = ax.barh(df['Kaynak'], df['Zorluk Seviyesi'], color=colors, alpha=0.8)
    
    # Etiketler
    ax.set_xlabel('Entegrasyon Zorluk Derecesi (1: Kolay - 3: Tersine Müh.)', fontsize=12)
    ax.set_title('Siber Güvenlik Veri Kaynakları: Entegrasyon Zorluk Analizi', fontsize=14, fontweight='bold')
    ax.set_xticks([1, 2, 3])
    ax.set_xticklabels(['Düşük\n(Standart API)', 'Orta\n(Parsing/Rate Limit)', 'Yüksek\n(Reverse Eng./Scraping)'])
    
    # Barların içine format bilgisini yazalım
    for bar, format_txt in zip(bars, df['Format']):
        width = bar.get_width()
        ax.text(width - 0.1, bar.get_y() + bar.get_height()/2, 
                format_txt, 
                ha='right', va='center', color='white', fontweight='bold')

    plt.tight_layout()
    plt.savefig('visual_1_data_sources.png')
    plt.close()

# ---------------------------------------------------------
# GÖRSEL 2: PLATFORM MİMARİ AKIŞI (Network Graph)
# ---------------------------------------------------------
def plot_architecture():
    G = nx.DiGraph()
    
    # Düğümler
    nodes = {
        'Sources': 'Veri Kaynakları\n(CTFtime, Frab, iCal)',
        'Ingestion': 'Ingestion Engine\n(Python/Go Workers)',
        'Security': 'Güvenlik Katmanı\n(DefusedXML, SSRF Guard)',
        'Normalize': 'Unified Event Model\n(Standardizasyon)',
        'DB': 'Veritabanı\n(PostgreSQL + JSONB)',
        'UI': 'Kullanıcı Arayüzü\n(Akıllı Filtreler, Takvim)'
    }
    
    for k, v in nodes.items():
        G.add_node(k, label=v)
        
    # Kenarlar (Akış)
    edges = [
        ('Sources', 'Ingestion'),
        ('Ingestion', 'Security'),
        ('Security', 'Normalize'),
        ('Normalize', 'DB'),
        ('DB', 'UI')
    ]
    G.add_edges_from(edges)
    
    pos = {
        'Sources': (0, 0),
        'Ingestion': (1, 0),
        'Security': (2, 0),
        'Normalize': (3, 0),
        'DB': (4, 0),
        'UI': (5, 0)
    }
    
    plt.figure(figsize=(12, 5))
    
    # Çizim
    nx.draw_networkx_nodes(G, pos, node_size=6000, node_color='#2196F3', alpha=0.9, node_shape='s')
    nx.draw_networkx_edges(G, pos, width=3, edge_color='gray', arrowsize=20)
    
    labels = nx.get_node_attributes(G, 'label')
    nx.draw_networkx_labels(G, pos, labels, font_size=9, font_color='white', font_weight='bold')
    
    plt.title("Siber Güvenlik Etkinlik Takip Platformu: Mimari Akış Şeması", fontsize=14, fontweight='bold')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig('visual_2_architecture.png')
    plt.close()

# ---------------------------------------------------------
# GÖRSEL 3: TEHDİT MODELLEMESİ (Tablo 2 Bazlı)
# ---------------------------------------------------------
def plot_threat_matrix():
    # Tehditler, Vektörler ve Çözümler
    threats = ['XXE Injection', 'SSRF', 'Calendar Injection', 'Deserialization']
    mitigations = ['DefusedXML & DTD Disable', 'URL Whitelist & Network Isolation', 'HTML Sanitization (Bleach)', 'JSON Only & Depth Limit']
    impacts = ['Dosya Okuma / DoS', 'İç Ağ Tarama / Cloud Metadata', 'Phishing / XSS', 'RCE / DoS']
    
    y_pos = range(len(threats))
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Basit bir tablo-grafik karışımı
    ax.barh(y_pos, [1]*len(threats), color='#e0e0e0', edgecolor='white') # Arka plan barları
    
    # Metinleri yerleştirme
    for i, (t, m, imp) in enumerate(zip(threats, mitigations, impacts)):
        # Tehdit
        ax.text(0.02, i, f"TEHDİT: {t}", fontsize=11, fontweight='bold', color='#D32F2F', va='center')
        # Etki
        ax.text(0.4, i, f"ETKİ: {imp}", fontsize=10, color='#333', va='center')
        # Çözüm (Kutucuk içinde gibi)
        ax.text(0.98, i, f"ÇÖZÜM: {m}", fontsize=10, fontweight='bold', color='#2E7D32', ha='right', va='center')

    ax.set_yticks([])
    ax.set_xticks([])
    ax.set_title('Güvenlik Odaklı Tasarım: Tehdit ve Savunma Matrisi', fontsize=14, fontweight='bold')
    
    # Sınırları kaldırma
    for spine in ax.spines.values():
        spine.set_visible(False)

    plt.tight_layout()
    plt.savefig('visual_3_threats.png')
    plt.close()

# Fonksiyonları çalıştır
plot_data_sources()
plot_architecture()
plot_threat_matrix()