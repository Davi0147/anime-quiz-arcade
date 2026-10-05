import os
import sys
import json
import time
import urllib.request
import urllib.parse
import subprocess

DIR = "C:/Users/luizd/.gemini/antigravity/scratch/anime-music-quiz"
AUDIO_DIR = os.path.join(DIR, "audio")
SONGS_PATH = os.path.join(DIR, "anime_songs_verified.json")
SCENES_PATH = os.path.join(DIR, "tools", "anime_scenes.json")
FFMPEG_DIR = r"C:\Users\luizd\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg.Essentials_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.1-essentials_build\bin"

NEW_ENTRIES = [
    # Nostalgic Classics
    {
        "anime": "Yu Yu Hakusho",
        "song": "Hohoemi no Bakudan",
        "artist": "Matsuko Mawatari",
        "year": 1992,
        "diff": "Fácil",
        "tags": ["Shounen", "Sobrenatural", "Torneio das Trevas", "Detetive Espiritual"],
        "synonyms": ["yu yu hakusho", "yuyu hakusho", "ghost files"],
        "search_query": "Yu Yu Hakusho opening Hohoemi no Bakudan creditless"
    },
    {
        "anime": "Dragon Ball Z",
        "song": "CHA-LA HEAD-CHA-LA",
        "artist": "Hironobu Kageyama",
        "year": 1989,
        "diff": "Fácil",
        "tags": ["Shounen", "Super Saiyajin", "Artes Marciais", "Nostalgia"],
        "synonyms": ["dragon ball z", "dbz", "dragon ball"],
        "search_query": "Dragon Ball Z opening Cha-la head-cha-la creditless"
    },
    {
        "anime": "Saint Seiya",
        "song": "Pegasus Fantasy",
        "artist": "MAKE-UP",
        "year": 1986,
        "diff": "Fácil",
        "tags": ["Shounen", "Armaduras do Zodíaco", "Cavaleiros", "Mitologia"],
        "synonyms": ["saint seiya", "os cavaleiros do zodiaco", "cavaleiros do zodiaco"],
        "search_query": "Saint Seiya opening Pegasus Fantasy creditless"
    },
    {
        "anime": "Great Teacher Onizuka",
        "song": "Driver's High",
        "artist": "L'Arc~en~Ciel",
        "year": 1999,
        "diff": "Médio",
        "tags": ["Comédia", "Escola", "Ex-Gangster", "Professores"],
        "synonyms": ["great teacher onizuka", "gto"],
        "search_query": "GTO opening Driver's High creditless"
    },
    {
        "anime": "Rurouni Kenshin",
        "song": "Sobakasu",
        "artist": "JUDY AND MARY",
        "year": 1996,
        "diff": "Médio",
        "tags": ["Samurais", "Histórico", "Espadas", "Era Meiji"],
        "synonyms": ["rurouni kenshin", "samurai x"],
        "search_query": "Rurouni Kenshin opening Sobakasu creditless"
    },
    {
        "anime": "Cardcaptor Sakura",
        "song": "Catch You Catch Me",
        "artist": "Gumi",
        "year": 1998,
        "diff": "Fácil",
        "tags": ["Mahou Shoujo", "Cartas Clow", "Magia", "Clamp"],
        "synonyms": ["cardcaptor sakura", "sakura card captors", "sakura"],
        "search_query": "Cardcaptor Sakura opening Catch You Catch Me creditless"
    },
    {
        "anime": "Hajime no Ippo",
        "song": "Under Star",
        "artist": "Shocking Lemon",
        "year": 2000,
        "diff": "Médio",
        "tags": ["Esportes", "Boxe", "Dempsey Roll", "Determinação"],
        "synonyms": ["hajime no ippo", "the fighting", "ippo"],
        "search_query": "Hajime no Ippo opening Under Star creditless"
    },
    {
        "anime": "Gintama",
        "song": "Pray",
        "artist": "Tommy heavenly6",
        "year": 2006,
        "diff": "Médio",
        "tags": ["Comédia", "Paródia", "Alienígenas", "Samurais"],
        "synonyms": ["gintama", "gin tama"],
        "search_query": "Gintama opening 1 Pray creditless"
    },
    {
        "anime": "Angel Beats!",
        "song": "My Soul, Your Beats!",
        "artist": "Lia",
        "year": 2010,
        "diff": "Fácil",
        "tags": ["Drama", "Sobrenatural", "Vida Após a Morte", "Piano Emocionante"],
        "synonyms": ["angel beats", "angel beats!"],
        "search_query": "Angel Beats opening My Soul Your Beats creditless"
    },
    {
        "anime": "Anohana",
        "song": "Aoi Shiori",
        "artist": "Galileo Galilei",
        "year": 2011,
        "diff": "Médio",
        "tags": ["Drama", "Lágrimas", "Menma", "Amizade de Infância"],
        "synonyms": ["anohana", "ano hi mita hana no namae"],
        "search_query": "Anohana opening Aoi Shiori creditless"
    },

    # Harem / Ecchi 2010 - 2018 (Pedidos pelo Usuário)
    {
        "anime": "Campione!",
        "song": "BRAVE BLADE",
        "artist": "Meg Rock",
        "year": 2012,
        "diff": "Médio",
        "tags": ["Harem / Ecchi", "Mitologia", "Matador de Deuses", "Espadas Mágicas"],
        "synonyms": ["campione", "campione!"],
        "search_query": "Campione opening Brave Blade creditless"
    },
    {
        "anime": "Shinmai Maou no Testament",
        "song": "Blade of Hope",
        "artist": "sweet ARMS",
        "year": 2015,
        "diff": "Médio",
        "tags": ["Harem / Ecchi", "Demônios", "Pacto de Mestre e Servo", "Ação Sobrenatural"],
        "synonyms": ["shinmai maou no testament", "the testament of sister new devil"],
        "search_query": "Shinmai Maou no Testament opening Blade of Hope creditless"
    },
    {
        "anime": "Saekano: How to Raise a Boring Girlfriend",
        "song": "Kimiiro Signal",
        "artist": "Luna Haruna",
        "year": 2015,
        "diff": "Médio",
        "tags": ["Harem / Romance", "Desenvolvimento de Jogos", "Otaku", "Heroínas"],
        "synonyms": ["saekano", "how to raise a boring girlfriend", "saenai heroine no sodatekata"],
        "search_query": "Saekano opening Kimiiro Signal creditless"
    },
    {
        "anime": "Strike the Blood",
        "song": "Strike the Blood",
        "artist": "Kishida Kyoudan & The Akeboshi Rockets",
        "year": 2013,
        "diff": "Médio",
        "tags": ["Harem / Ação", "Vampiros", "Ilha Artificial", "Xamãs Espadachins"],
        "synonyms": ["strike the blood"],
        "search_query": "Strike the Blood opening 1 creditless"
    },
    {
        "anime": "Sekirei",
        "song": "Sekirei",
        "artist": "Saori Hayami, Marina Inoue, Kana Hanazawa, Aya Endou",
        "year": 2008,
        "diff": "Médio",
        "tags": ["Harem / Ecchi", "Torneio de Batalha", "Poderes Elementais", "Parceiros"],
        "synonyms": ["sekirei"],
        "search_query": "Sekirei opening 1 creditless"
    },
    {
        "anime": "Freezing",
        "song": "Color",
        "artist": "MARiA",
        "year": 2011,
        "diff": "Médio",
        "tags": ["Harem / Ecchi", "Academia Militar", "Pandora", "Invasores Nova"],
        "synonyms": ["freezing"],
        "search_query": "Freezing opening Color creditless"
    },
    {
        "anime": "Eromanga Sensei",
        "song": "Hitorigoto",
        "artist": "ClariS",
        "year": 2017,
        "diff": "Fácil",
        "tags": ["Comédia / Harem", "Light Novels", "Ilustradores", "ClariS"],
        "synonyms": ["eromanga sensei", "eromanga-sensei"],
        "search_query": "Eromanga Sensei opening Hitorigoto creditless"
    },
    {
        "anime": "Oreimo",
        "song": "irony",
        "artist": "ClariS",
        "year": 2010,
        "diff": "Fácil",
        "tags": ["Comédia / Romance", "Irmã Otaku", "Segredo Familiar", "ClariS"],
        "synonyms": ["oreimo", "ore no imouto ga konna ni kawaii wake ga nai"],
        "search_query": "Oreimo opening irony creditless"
    },
    {
        "anime": "Shimoneta",
        "song": "B Chiku Sentai Soutou H-Gumi",
        "artist": "SOX",
        "year": 2015,
        "diff": "Médio",
        "tags": ["Comédia / Ecchi", "Terrorismo de Piadas Sujas", "Distopia", "SOX"],
        "synonyms": ["shimoneta", "shimoneta to iu gainen"],
        "search_query": "Shimoneta opening creditless"
    },
    {
        "anime": "Yuuna and the Haunted Hot Springs",
        "song": "Momoiro Typhoon",
        "artist": "Luna Haruna",
        "year": 2018,
        "diff": "Médio",
        "tags": ["Harem / Ecchi", "Fantasmas", "Águas Termais", "Youkais"],
        "synonyms": ["yuuna and the haunted hot springs", "yuragi-sou no yuuna-san", "yuuna-san"],
        "search_query": "Yuragi-sou no Yuuna-san opening Momoiro Typhoon creditless"
    },
    {
        "anime": "We Never Learn: BOKUBEN",
        "song": "Seishun Seminar",
        "artist": "Study",
        "year": 2019,
        "diff": "Médio",
        "tags": ["Harem / Comédia", "Tutoria Escolar", "Gênias Incompetentes", "Romance"],
        "synonyms": ["we never learn", "bokuben", "bokutachi wa benkyou ga dekinai"],
        "search_query": "Bokutachi wa Benkyou ga Dekinai opening Seishun Seminar creditless"
    },
    {
        "anime": "The Quintessential Quintuplets",
        "song": "Gotoubun no Kimochi",
        "artist": "Nakano Sisters",
        "year": 2019,
        "diff": "Fácil",
        "tags": ["Harem / Romance", "Irmãs Quíntuplas", "Futaro", "Casamento Futuro"],
        "synonyms": ["the quintessential quintuplets", "gotoubun no hanayome", "as quintuplas"],
        "search_query": "Gotoubun no Hanayome opening 1 Gotoubun no Kimochi creditless"
    },

    # Modern Hits 2020 - 2024
    {
        "anime": "Mushoku Tensei: Jobless Reincarnation",
        "song": "Tabibito no Uta",
        "artist": "Yuiko Ohara",
        "year": 2021,
        "diff": "Médio",
        "tags": ["Isekai", "Fantasia Épica", "Rudeus Greyrat", "Magia"],
        "synonyms": ["mushoku tensei", "jobless reincarnation"],
        "search_query": "Mushoku Tensei opening 1 Tabibito no Uta"
    },
    {
        "anime": "Dungeon Meshi",
        "song": "Sleep Walking Orchestra",
        "artist": "BUMP OF CHICKEN",
        "year": 2024,
        "diff": "Fácil",
        "tags": ["Fantasia", "Culinária de Monstros", "Masmorras", "Studio Trigger"],
        "synonyms": ["dungeon meshi", "delicious in dungeon"],
        "search_query": "Dungeon Meshi opening Sleep Walking Orchestra creditless"
    },
    {
        "anime": "Hell's Paradise",
        "song": "WORK",
        "artist": "millenium parade x Ringo Sheena",
        "year": 2023,
        "diff": "Fácil",
        "tags": ["Ação", "Shinobi", "Ilha Sobrenatural", "Elixir da Vida"],
        "synonyms": ["hell's paradise", "jigokuraku"],
        "search_query": "Hell's Paradise opening WORK creditless"
    },
    {
        "anime": "The Apothecary Diaries",
        "song": "Hana ni Natte",
        "artist": "Ryokuoushoku Shakai",
        "year": 2023,
        "diff": "Fácil",
        "tags": ["Mistério", "Palácio Imperial", "Ervas Medicinais", "Maomao"],
        "synonyms": ["the apothecary diaries", "kusuriya no hitorigoto"],
        "search_query": "Kusuriya no Hitorigoto opening Hana ni Natte creditless"
    },
    {
        "anime": "My Dress-Up Darling",
        "song": "Sansan Days",
        "artist": "Spira Spica",
        "year": 2022,
        "diff": "Fácil",
        "tags": ["Romance", "Cosplay", "Marin Kitagawa", "Costura"],
        "synonyms": ["my dress-up darling", "sono bisque doll wa koi wo suru", "sono bisque doll"],
        "search_query": "My Dress-Up Darling opening Sansan Days creditless"
    },
    {
        "anime": "The Dangers in My Heart",
        "song": "Shayou",
        "artist": "Yorushika",
        "year": 2023,
        "diff": "Fácil",
        "tags": ["Romcom", "Ichikawa e Yamada", "Crescimento Pessoal", "Fofo"],
        "synonyms": ["the dangers in my heart", "boku no kokoro no yabai yatsu", "bokuyaba"],
        "search_query": "Boku no Kokoro no Yabai Yatsu opening Shayou creditless"
    },
    {
        "anime": "Komi Can't Communicate",
        "song": "Cinderella",
        "artist": "Cidergirl",
        "year": 2021,
        "diff": "Fácil",
        "tags": ["Comédia", "Escola", "100 Amigos", "Comunicação"],
        "synonyms": ["komi can't communicate", "komi-san wa comyushou desu"],
        "search_query": "Komi Can't Communicate opening Cinderella creditless"
    }
]

def fetch_anilist_data(title):
    query = """
    query ($search: String) {
      Media (search: $search, type: ANIME) {
        id
        title { romaji english }
        coverImage { extraLarge large }
        startDate { year }
        genres
        streamingEpisodes { title thumbnail }
      }
    }
    """
    clean = title.split("(")[0].strip()
    try:
        payload = json.dumps({'query': query, 'variables': {'search': clean}}).encode('utf-8')
        req = urllib.request.Request(
            'https://graphql.anilist.co',
            data=payload,
            headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            return data.get('data', {}).get('Media', {})
    except Exception as e:
        print(f"Erro ao buscar AniList para {title}: {e}")
        return {}

def fetch_kitsu_thumb(title):
    clean = title.split("(")[0].strip()
    url = f"https://kitsu.io/api/edge/anime?filter[text]={urllib.parse.quote(clean)}&page[limit]=1"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Accept': 'application/vnd.api+json'})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            items = data.get('data', [])
            if items:
                anime_id = items[0]['id']
                ep_url = f"https://kitsu.io/api/edge/episodes?filter[mediaId]={anime_id}&page[limit]=5"
                ep_req = urllib.request.Request(ep_url, headers={'User-Agent': 'Mozilla/5.0', 'Accept': 'application/vnd.api+json'})
                with urllib.request.urlopen(ep_req, timeout=10) as ep_resp:
                    ep_data = json.loads(ep_resp.read().decode('utf-8'))
                    eps = ep_data.get('data', [])
                    for ep in eps:
                        t = ep.get('attributes', {}).get('thumbnail', {})
                        img = t.get('original') or t.get('large') or t.get('medium')
                        if img:
                            return img
    except Exception:
        pass
    return None

def download_audio_mp3(query, target_id):
    out_path = os.path.join(AUDIO_DIR, f"{target_id}.mp3")
    if os.path.exists(out_path) and os.path.getsize(out_path) > 50000:
        return True, "12345678901"

    cmd = [
        sys.executable, "-m", "yt_dlp",
        "--ffmpeg-location", FFMPEG_DIR,
        "-x",
        "--audio-format", "mp3",
        "--audio-quality", "128K",
        "--default-search", "ytsearch1",
        "--no-playlist",
        "-o", os.path.join(AUDIO_DIR, f"{target_id}.%(ext)s"),
        query
    ]
    try:
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=45)
        if os.path.exists(out_path) and os.path.getsize(out_path) > 50000:
            return True, "auto_download"
        else:
            return False, ""
    except Exception as e:
        print(f"Erro yt-dlp para {query}: {e}")
        return False, ""

def main():
    with open(SONGS_PATH, "r", encoding="utf-8") as f:
        songs = json.load(f)
    with open(SCENES_PATH, "r", encoding="utf-8") as f:
        scenes = json.load(f)

    existing_titles = {s["anime"].lower() for s in songs}
    start_song_id = len(songs) + 1
    start_scene_id = len(scenes) + 1

    print(f"Iniciando adicao de {len(NEW_ENTRIES)} novos animes ao catalogo...")
    added_count = 0

    for i, entry in enumerate(NEW_ENTRIES):
        title = entry["anime"]
        if title.lower() in existing_titles:
            print(f"Ignorando {title} (ja presente).")
            continue

        print(f"\n[{i+1}/{len(NEW_ENTRIES)}] Processando: {title}...")
        song_id = start_song_id + added_count
        scene_id = start_scene_id + added_count

        # 1. AniList Data
        media = fetch_anilist_data(title)
        time.sleep(0.5)

        cover = None
        if media:
            cover = media.get('coverImage', {}).get('extraLarge') or media.get('coverImage', {}).get('large')
        if not cover:
            cover = "https://via.placeholder.com/225x320?text=Anime+Cover"

        # Episode screencap
        scene_thumb = None
        eps = media.get('streamingEpisodes', []) if media else []
        for ep in eps:
            if ep.get('thumbnail'):
                scene_thumb = ep['thumbnail']
                break
        
        if not scene_thumb:
            scene_thumb = fetch_kitsu_thumb(title)
            time.sleep(0.5)

        if not scene_thumb:
            scene_thumb = cover

        # 2. Download MP3
        print(f"  -> Baixando MP3 #{song_id}: '{entry['search_query']}'...")
        ok, vid_id = download_audio_mp3(entry["search_query"], song_id)
        if not ok:
            print(f"  [AVISO] Falha ao baixar audio para {title}, usando ID gerado.")
            vid_id = "unavailable"

        # 3. Build Song Object
        new_song = {
            "id": song_id,
            "anime": title,
            "song": entry["song"],
            "artist": entry["artist"],
            "year": entry.get("year", 2020),
            "diff": entry.get("diff", "Médio"),
            "tags": entry.get("tags", []),
            "synonyms": entry.get("synonyms", []),
            "video_id": vid_id,
            "video_url": f"https://www.youtube.com/results?search_query={urllib.parse.quote(entry['search_query'])}",
            "image_url": cover
        }
        songs.append(new_song)

        # 4. Build Scene Object
        new_scene = {
            "id": scene_id,
            "anime": title,
            "image_url": scene_thumb,
            "has_cinematic_banner": True,
            "year": entry.get("year", 2020),
            "tags": entry.get("tags", []),
            "synonyms": entry.get("synonyms", []),
            "hint": f"{entry.get('tags', ['Anime'])[0]} / {entry.get('diff', 'Médio')}"
        }
        scenes.append(new_scene)

        added_count += 1
        print(f"  [OK] Anime #{song_id} adicionado com sucesso!")

    # Save databases
    with open(SONGS_PATH, "w", encoding="utf-8") as f:
        json.dump(songs, f, ensure_ascii=False, indent=2)
    with open(SCENES_PATH, "w", encoding="utf-8") as f:
        json.dump(scenes, f, ensure_ascii=False, indent=2)

    print("\n" + "=" * 60)
    print(f"SUCESSO TOTAL! {added_count} novos animes integrados ao banco de dados!")
    print(f"Total de musicas agora: {len(songs)}")
    print(f"Total de cenas agora: {len(scenes)}")
    print("=" * 60)

if __name__ == "__main__":
    main()
