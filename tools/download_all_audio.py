import os
import json
import yt_dlp
import sys

DIR = "C:/Users/luizd/.gemini/antigravity/scratch/anime-music-quiz"
AUDIO_DIR = os.path.join(DIR, "audio")
JSON_PATH = os.path.join(DIR, "anime_songs_verified.json")

os.makedirs(AUDIO_DIR, exist_ok=True)

with open(JSON_PATH, "r", encoding="utf-8") as f:
    songs = json.load(f)

print(f"Total de musicas para verificar/baixar: {len(songs)}")

updated_json = False

ydl_base_opts = {
    'format': 'ba/18/b',
    'extractor_args': {'youtube': {'player_client': ['android']}},
    'quiet': True,
    'no_warnings': True,
    'noplaylist': True,
}

for i, s in enumerate(songs):
    song_id = s['id']
    target_file = os.path.join(AUDIO_DIR, f"{song_id}.mp4")

    # Check if already downloaded and valid size
    if os.path.exists(target_file) and os.path.getsize(target_file) > 200 * 1024:
        print(f"[{i+1}/{len(songs)}] #{song_id} {s['anime']} - Ja baixado ({round(os.path.getsize(target_file)/1024/1024, 2)} MB). Pulando...")
        continue

    print(f"[{i+1}/{len(songs)}] Baixando #{song_id} {s['anime']} ('{s['song']}' - {s['artist']})...")
    
    opts = dict(ydl_base_opts)
    opts['outtmpl'] = os.path.join(AUDIO_DIR, f"{song_id}.%(ext)s")

    success = False
    # Try 1: Direct video_id
    if s.get('video_id'):
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                ydl.download([f"https://www.youtube.com/watch?v={s['video_id']}"])
                if os.path.exists(target_file) and os.path.getsize(target_file) > 100 * 1024:
                    success = True
                    print(f"  -> Sucesso direto! ({round(os.path.getsize(target_file)/1024/1024, 2)} MB)")
        except Exception as e:
            print(f"  -> Link original com erro ({e}). Tentando busca alternativa...")

    # Try 2: Search fallback
    if not success:
        search_query = f"ytsearch1:{s['anime']} {s['song']} {s['artist']} opening"
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(search_query, download=True)
                if 'entries' in info and info['entries']:
                    entry = info['entries'][0]
                    new_vid = entry.get('id')
                    if new_vid and new_vid != s.get('video_id'):
                        s['video_id'] = new_vid
                        s['video_url'] = f"https://www.youtube.com/watch?v={new_vid}"
                        updated_json = True
                        print(f"  -> Atualizado novo video_id: {new_vid}")
                
                if os.path.exists(target_file) and os.path.getsize(target_file) > 100 * 1024:
                    success = True
                    print(f"  -> Sucesso via busca! ({round(os.path.getsize(target_file)/1024/1024, 2)} MB)")
        except Exception as e:
            print(f"  -> Falha na busca para #{song_id} {s['anime']}: {e}")

if updated_json:
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(songs, f, ensure_ascii=False, indent=2)
    print("anime_songs_verified.json atualizado com os novos video_ids!")

# Check total downloaded
downloaded_files = [f for f in os.listdir(AUDIO_DIR) if f.endswith('.mp4')]
print(f"\n==========================================")
print(f"TOTAL BAIXADO: {len(downloaded_files)} / {len(songs)} faixas disponiveis localmente!")
print(f"Pasta: {AUDIO_DIR}")
print(f"==========================================")
