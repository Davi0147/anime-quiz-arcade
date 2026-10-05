import json
import subprocess
import urllib.request
import re
import os

SONGS_FILE = 'anime_songs_verified.json'

with open(SONGS_FILE, 'r', encoding='utf-8') as f:
    songs = json.load(f)

QUERIES = {
    101: "Yu Yu Hakusho opening Hohoemi no Bakudan creditless",
    102: "Dragon Ball Z opening Cha-La Head-Cha-La creditless",
    103: "Saint Seiya opening Pegasus Fantasy creditless",
    104: "GTO opening 1 Driver's High creditless",
    105: "Rurouni Kenshin opening Sobakasu creditless",
    106: "Cardcaptor Sakura opening Catch You Catch Me creditless",
    107: "Hajime no Ippo opening Under Star creditless",
    108: "Gintama opening 1 Pray creditless",
    109: "Angel Beats opening My Soul Your Beats creditless",
    110: "Anohana opening Aoi Shiori creditless",
    111: "Campione opening BRAVE BLADE creditless",
    112: "Shinmai Maou no Testament opening Blade of Hope creditless",
    113: "Saekano opening Kimiiro Signal creditless",
    114: "Strike the Blood opening 1 creditless",
    115: "Sekirei opening 1 creditless",
    116: "Freezing opening Color creditless",
    117: "Eromanga Sensei opening Hitorigoto creditless",
    118: "Oreimo opening irony creditless",
    119: "Shimoneta opening creditless",
    120: "Yuragi-sou no Yuuna-san opening Momoiro Typhoon creditless",
    121: "Bokutachi wa Benkyou ga Dekinai opening Seishun Seminar creditless",
    122: "Gotoubun no Hanayome opening 1 Gotoubun no Kimochi creditless",
    123: "Mushoku Tensei opening 1 Tabibito no Uta",
    124: "Dungeon Meshi opening Sleep Walking Orchestra creditless",
    125: "Hell's Paradise opening WORK creditless",
    126: "Kusuriya no Hitorigoto opening Hana ni Natte creditless",
    127: "My Dress-Up Darling opening Sansan Days creditless",
    128: "Boku no Kokoro no Yabai Yatsu opening Shayou creditless",
    129: "Komi Can't Communicate opening Cinderella creditless"
}

yt_pattern = re.compile(r'^[a-zA-Z0-9_-]{11}$')

updated_count = 0
for s in songs:
    sid = s.get('id')
    vid = s.get('video_id', '')
    if sid in QUERIES and (not yt_pattern.match(vid) or vid in ['auto_download', 'unavailable']):
        query = QUERIES[sid]
        print(f"[{sid}] Buscando YouTube ID para {s['anime']} ('{query}')...")
        try:
            cmd = ['python', '-m', 'yt_dlp', '--default-search', 'ytsearch1', '--print', '%(id)s', f'ytsearch1:{query}']
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=25)
            new_id = res.stdout.strip()
            if yt_pattern.match(new_id):
                # Validar se thumbnail é real e existe
                thumb_url = f"https://i.ytimg.com/vi/{new_id}/hqdefault.jpg"
                req = urllib.request.Request(thumb_url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=5) as resp:
                    data = resp.read()
                    if len(data) > 3500:
                        s['video_id'] = new_id
                        s['video_url'] = f"https://www.youtube.com/watch?v={new_id}"
                        print(f"  -> OK! ID: {new_id} ({len(data)} bytes thumb)")
                        updated_count += 1
                    else:
                        print(f"  -> AVISO: Thumbnail muito pequeno ({len(data)} bytes)")
            else:
                print(f"  -> AVISO: ID inválido retornado: {new_id}")
        except Exception as e:
            print(f"  -> ERRO para {sid}: {e}")

print(f"\nTotal atualizados: {updated_count}/{len(QUERIES)}")

with open(SONGS_FILE, 'w', encoding='utf-8') as f:
    json.dump(songs, f, indent=2, ensure_ascii=False)
print(f"Salvo em {SONGS_FILE} com sucesso!")
