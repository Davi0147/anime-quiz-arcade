import urllib.request
import urllib.parse
import re
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

new_candidates = [
    # 90s Classics
    {"anime": "Neon Genesis Evangelion", "song": "A Cruel Angel's Thesis", "artist": "Yoko Takahashi", "year": 1995, 
     "era": "classicos", "diff": "⭐ Fácil", 
     "tags": ["Mecha", "Psicológico", "Anjos & Evas", "Estúdio Gainax", "Anos 90"],
     "synonyms": ["evangelion", "neon genesis evangelion", "eva", "shin seiki evangelion"],
     "q": "Neon Genesis Evangelion opening A Cruel Angel's Thesis"},
    
    {"anime": "Cowboy Bebop", "song": "Tank!", "artist": "The Seatbelts", "year": 1998,
     "era": "classicos", "diff": "⭐ Fácil",
     "tags": ["Ficção Científica", "Jazz / Noir", "Caçadores de Recompensa", "Estúdio Sunrise", "Espaço"],
     "synonyms": ["cowboy bebop", "bebop"],
     "q": "Cowboy Bebop opening Tank The Seatbelts"},
    
    {"anime": "One Piece", "song": "We Are!", "artist": "Hiroshi Kitadani", "year": 1999,
     "era": "classicos", "diff": "⭐ Fácil",
     "tags": ["Piratas", "Shounen", "Akuma no Mi", "Luffy", "Toei Animation"],
     "synonyms": ["one piece", "op", "wan pisu"],
     "q": "One Piece opening 1 We Are Hiroshi Kitadani"},
    
    {"anime": "Digimon Adventure", "song": "Butter-Fly", "artist": "Koji Wada", "year": 1999,
     "era": "classicos", "diff": "⭐ Fácil",
     "tags": ["Monstros Digitais", "Digiescolhidos", "Agumon", "Nostalgia", "Toei Animation"],
     "synonyms": ["digimon", "digimon adventure", "digimon 1"],
     "q": "Digimon Adventure opening Butter-Fly Koji Wada"},

    # 2010s Extra Hits
    {"anime": "Bleach", "song": "Ranbu no Melody", "artist": "SID", "year": 2010,
     "era": "ouro", "diff": "⭐⭐ Média",
     "tags": ["Shounen", "Shinigami", "Batalha de Karakura", "Ichigo vs Aizen", "Studio Pierrot"],
     "synonyms": ["bleach", "burichi"],
     "q": "Bleach opening 13 Ranbu no Melody SID VIZ"},

    {"anime": "Parasyte: The Maxim", "song": "Let Me Hear", "artist": "Fear, and Loathing in Las Vegas", "year": 2014,
     "era": "moderna", "diff": "⭐⭐ Média",
     "tags": ["Ficção Científica", "Horror / Suspense", "Parasitas Alienígenas", "Migi", "Estúdio Madhouse"],
     "synonyms": ["parasyte", "parasyte the maxim", "kiseijuu", "kiseiju", "parasita"],
     "q": "Parasyte opening Let Me Hear Fear and Loathing in Las Vegas"},

    {"anime": "Erased", "song": "Re:Re:", "artist": "Asian Kung-Fu Generation", "year": 2016,
     "era": "recente", "diff": "⭐⭐ Média",
     "tags": ["Mistério", "Viagem no Tempo", "Revival", "Suspense", "A-1 Pictures"],
     "synonyms": ["erased", "boku dake ga inai machi", "bokumachi", "a cidade onde apenas eu nao existo"],
     "q": "Erased opening Re Re Asian Kung-Fu Generation"},

    {"anime": "Fire Force", "song": "Inferno", "artist": "Mrs. GREEN APPLE", "year": 2019,
     "era": "recente", "diff": "⭐ Fácil",
     "tags": ["Shounen", "Bombeiros Especiais", "Chamas & Demônios", "David Production", "Ação"],
     "synonyms": ["fire force", "enen no shouboutai", "enen"],
     "q": "Fire Force opening 1 Inferno Mrs GREEN APPLE"},

    # Post-2020 Hits (Nova Geração)
    {"anime": "Tokyo Revengers", "song": "Cry Baby", "artist": "Official HIGE DANdism", "year": 2021,
     "era": "nova_geracao", "diff": "⭐ Fácil",
     "tags": ["Gangues de Rua", "Viagem no Tempo", "Delinquentes", "Takemichi e Mikey", "LIDENFILMS"],
     "synonyms": ["tokyo revengers", "tokyo revenger", "tokrev"],
     "q": "Tokyo Revengers opening 1 Cry Baby Official HIGE DANdism"},

    {"anime": "Chainsaw Man", "song": "KICK BACK", "artist": "Kenshi Yonezu", "year": 2022,
     "era": "nova_geracao", "diff": "⭐ Fácil",
     "tags": ["Demônio da Motosserra", "Denji & Pochita", "Caçadores de Demônios", "Estúdio MAPPA", "Gore / Ação"],
     "synonyms": ["chainsaw man", "chainsawman", "homem motosserra", "csm"],
     "q": "Chainsaw Man opening KICK BACK Kenshi Yonezu MAPPA"},

    {"anime": "Spy x Family", "song": "Mixed Nuts", "artist": "Official HIGE DANdism", "year": 2022,
     "era": "nova_geracao", "diff": "⭐ Fácil",
     "tags": ["Espiões", "Família Falsa", "Anya & Waku Waku", "Comédia / Slice of Life", "Wit Studio / CloverWorks"],
     "synonyms": ["spy x family", "spy family", "spyxfamily"],
     "q": "Spy x Family opening 1 Mixed Nuts Official HIGE DANdism"},

    {"anime": "Attack on Titan Final Season Pt 2", "song": "The Rumbling", "artist": "SiM", "year": 2022,
     "era": "nova_geracao", "diff": "⭐ Fácil",
     "tags": ["O Estrondo", "Metal / Rock", "Eren Jaeger", "Titãs Colossais", "Estúdio MAPPA"],
     "synonyms": ["attack on titan", "shingeki no kyojin", "shingeki", "aot", "ataque dos titas"],
     "q": "Attack on Titan The Rumbling SiM opening Crunchyroll"},

    {"anime": "Oshi no Ko", "song": "Idol", "artist": "YOASOBI", "year": 2023,
     "era": "nova_geracao", "diff": "⭐ Fácil",
     "tags": ["Idols Japonesas", "Showbiz / Reencarnação", "Ai Hoshino", "Mistério & Drama", "Doga Kobo"],
     "synonyms": ["oshi no ko", "my star", "oshinoko"],
     "q": "Oshi no Ko opening Idol YOASOBI"},

    {"anime": "Jujutsu Kaisen S2 (Shibuya)", "song": "SPECIALZ", "artist": "King Gnu", "year": 2023,
     "era": "nova_geracao", "diff": "⭐ Fácil",
     "tags": ["Incidente de Shibuya", "You are my special", "Feiticeiros Jujutsu", "Sukuna", "Estúdio MAPPA"],
     "synonyms": ["jujutsu kaisen", "jujutsu kaisen s2", "jujutsu kaisen 2", "jujutsu", "jjk", "batalha de feiticeiros"],
     "q": "Jujutsu Kaisen Season 2 opening SPECIALZ King Gnu"},

    {"anime": "Frieren: Beyond Journey's End", "song": "Yuusha", "artist": "YOASOBI", "year": 2023,
     "era": "nova_geracao", "diff": "⭐⭐ Média",
     "tags": ["Fantasia Épica", "Maga Elfa", "Pós-Derrota do Rei Demônio", "Estúdio Madhouse", "Aventura"],
     "synonyms": ["frieren", "frieren beyond journeys end", "sousou no frieren", "frieren e a jornada para o alem"],
     "q": "Frieren opening Yuusha YOASOBI"},

    {"anime": "Solo Leveling", "song": "LEveL", "artist": "SawanoHiroyuki[nZk]:TXT", "year": 2024,
     "era": "nova_geracao", "diff": "⭐ Fácil",
     "tags": ["Caçadores & Dungeons", "Sung Jinwoo", "Erga-se / Arise", "A-1 Pictures", "Manhwa Coreano"],
     "synonyms": ["solo leveling", "ore dake level up na ken"],
     "q": "Solo Leveling opening LEveL Sawano Hiroyuki TXT"},

    {"anime": "Mashle: Magic and Muscles S2", "song": "Bling-Bang-Bang-Born", "artist": "Creepy Nuts", "year": 2024,
     "era": "nova_geracao", "diff": "⭐ Fácil",
     "tags": ["Magia & Músculos", "Creepy Nuts", "Dança Viral", "Escola de Magia", "A-1 Pictures"],
     "synonyms": ["mashle", "mashle magic and muscles", "mashle s2"],
     "q": "Mashle Season 2 opening Bling-Bang-Bang-Born Creepy Nuts"},

    {"anime": "Dandadan", "song": "Otonoke", "artist": "Creepy Nuts", "year": 2024,
     "era": "nova_geracao", "diff": "⭐ Fácil",
     "tags": ["Aliens & Fantasmas / Youkai", "Creepy Nuts", "Momo & Okarun", "Science SARU", "Comédia Sobrenatural"],
     "synonyms": ["dandadan"],
     "q": "Dandadan opening Otonoke Creepy Nuts"},

    {"anime": "Kaiju No. 8", "song": "Abyss", "artist": "YUNGBLUD", "year": 2024,
     "era": "nova_geracao", "diff": "⭐⭐ Média",
     "tags": ["Monstros Gigantes / Kaijus", "Força de Defesa", "Kafka Hibino", "Production I.G", "Ação Sci-Fi"],
     "synonyms": ["kaiju no 8", "kaiju 8", "kaiju numero 8", "kaijuu 8-gou"],
     "q": "Kaiju No 8 opening Abyss YUNGBLUD"}
]

results = []

for item in new_candidates:
    q = item["q"]
    url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(q)}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        html = urllib.request.urlopen(req, timeout=8).read().decode('utf-8')
        vids = list(dict.fromkeys(re.findall(r'watch\?v=([a-zA-Z0-9_-]{11})', html)))[:5]
        
        best_id = ""
        best_title = ""
        for v in vids:
            try:
                res = json.loads(urllib.request.urlopen(f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={v}&format=json", timeout=4).read().decode('utf-8'))
                title = res.get("title", "")
                # Ignore covers
                if not any(w in title.lower() for w in ["cover", "fandub", "português", "pt-br", "parodia"]):
                    best_id = v
                    best_title = title
                    break
            except:
                pass
        
        if not best_id and vids:
            best_id = vids[0]
            best_title = "(Fallback Video)"
            
        item["video_id"] = best_id
        item["video_url"] = f"https://www.youtube.com/watch?v={best_id}"
        item["video_title"] = best_title
        print(f"[FOUND] {item['anime']} ({item['year']}) -> {item['video_url']} | {best_title[:40]}")
        results.append(item)
    except Exception as e:
        print(f"[ERR] {item['anime']}: {e}")

with open("C:/Users/luizd/.gemini/antigravity/scratch/anime-music-quiz/tools/new_songs_verified.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"\nConcluído: {len(results)} novas músicas verificadas!")
