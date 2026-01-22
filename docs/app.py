import requests
from flask import Flask, render_template, jsonify, request
import time
import random

app = Flask(__name__)

# --- 1. OTOMATİK VERİ ÇEKME MODÜLÜ (CANLI) ---
def get_ctftime_events(limit=20):
    """
    CTFtime API'den canlı veri çeker ve frontend formatına hazırlar.
    """
    start_time = int(time.time())
    finish_time = start_time + 60*60*24*90 # 3 aylık veri
    url = f"https://ctftime.org/api/v1/events/?limit={limit}&start={start_time}&finish={finish_time}"
    headers = {'User-Agent': 'Mozilla/5.0 (CyberVault/2.0)'}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            events = []
            for item in data:
                events.append({
                    'id': item.get('id'),
                    'title': item.get('title'),
                    'start': item.get('start', '').replace('T', ' ')[:16],
                    'type': 'CTF',
                    'format': item.get('format'),
                    'url': item.get('url'),
                    # Arama filtresi için etiketler oluşturuyoruz
                    'tags': ' '.join([x.lower() for x in item.get('format', '').split()]) + ' ctf jeopardy',
                    'description': item.get('description', 'Açıklama yok.')
                })
            return events
        return []
    except Exception as e:
        print(f"Hata (CTFtime): {e}")
        return []

def get_conferences():
    """
    Resmi Konferanslar (Mock Data - Scraping Simülasyonu)
    """
    fake_conferences = [
        {
            'id': 901,
            'title': 'Black Hat USA 2026',
            'start': '2026-08-08 09:00',
            'type': 'Conference',
            'format': 'Talks',
            'url': 'https://www.blackhat.com',
            'tags': 'web pwn network enterprise',
            'description': 'Dünyanın en prestijli siber güvenlik konferansı.'
        },
        {
            'id': 902,
            'title': 'DEF CON 34',
            'start': '2026-08-11 10:00',
            'type': 'Conference',
            'format': 'Convention',
            'url': 'https://defcon.org',
            'tags': 'hardware pwn social-engineering community',
            'description': 'Hacker kültürünün kalbi.'
        }
    ]
    return fake_conferences

# --- 2. ARŞİV SİSTEMİ (GEÇMİŞ ETKİNLİKLER & WRITE-UP) ---
def get_archived_events():
    return [
        {
            'title': 'Google CTF 2025',
            'date': '2025-06-23',
            'category': 'Web Security',
            'writeup_link': '#',
            'file_type': 'PDF'
        },
        {
            'title': 'DEF CON 33 - Biohacking Village',
            'date': '2025-08-10',
            'category': 'Medical/IoT',
            'writeup_link': '#',
            'file_type': 'SLIDES'
        },
        {
            'title': 'Pwn2Own Vancouver',
            'date': '2025-03-15',
            'category': 'Exploit Dev',
            'writeup_link': '#',
            'file_type': 'VIDEO'
        }
    ]

# --- ROUTE'LAR ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/events')
def api_events():
    # Canlı Takvim ve Liste için veriler birleştirilir
    ctf = get_ctftime_events()
    conf = get_conferences()
    return jsonify(ctf + conf)

@app.route('/api/archive')
def api_archive():
    return jsonify(get_archived_events())

if __name__ == '__main__':
    app.run(debug=True, port=5000)