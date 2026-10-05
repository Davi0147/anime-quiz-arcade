import urllib.request
import urllib.parse
import re
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

candidates = [
    {
        "anime": "Rosario + Vampire",
        "song": "DISCOTHEQUE",
        "artist": "Nana Mizuki",
        "year": 2008,
        "era": "ouro",
        "diff": "⭐ Fácil",
        "tags": ["Harém", "Ecchi", "Vampira & Monstros", "Moka Akashiya", "Gonzo"],
        "synonyms": ["rosario vampire", "rosario to vampire", "rosario + vampire capu2", "rosario"],
        "q": "Rosario Vampire Capu2 opening DISCOTHEQUE Nana Mizuki official"
    },
    {
        "anime": "Highschool of the Dead",
        "song": "HIGHSCHOOL OF THE DEAD",
        "artist": "Kishida Kyoudan & THE Akeboshi Rockets",
        "year": 2010,
        "era": "ouro",
        "diff": "⭐ Fácil",
        "tags": ["Ecchi / Sobrevivência", "Zumbis no Colégio", "Armas & Ação", "Estúdio Madhouse", "Apocalipse"],
        "synonyms": ["highschool of the dead", "hotd", "high school of the dead", "escola dos mortos"],
        "q": "Highschool of the Dead opening Kishida Kyoudan"
    },
    {
        "anime": "Sora no Otoshimono",
        "song": "Ring My Bell",
        "artist": "blue drops",
        "year": 2009,
        "era": "ouro",
        "diff": "⭐⭐ Média",
        "tags": ["Harém / Ecchi", "Anjo Artificial (Angeloid)", "Ikaros", "Comédia / Romance", "AIC A.S.T.A."],
        "synonyms": ["sora no otoshimono", "heavens lost property", "heaven's lost property"],
        "q": "Sora no Otoshimono opening Ring My Bell"
    },
    {
        "anime": "IS: Infinite Stratos",
        "song": "STRAIGHT JET",
        "artist": "Minami Kuribayashi",
        "year": 2011,
        "era": "moderna",
        "diff": "⭐⭐ Média",
        "tags": ["Harém / Mecha", "Armaduras Voadoras", "Ichika Orimura", "Academia Feminina", "8bit"],
        "synonyms": ["infinite stratos", "is infinite stratos", "is"],
        "q": "Infinite Stratos opening STRAIGHT JET"
    },
    {
        "anime": "High School DxD",
        "song": "Trip -Innocent of D-",
        "artist": "Larval Stage Planning",
        "year": 2012,
        "era": "moderna",
        "diff": "⭐ Fácil",
        "tags": ["Harém / Ecchi Supremo", "Demônios & Peças de Xadrez", "Issei & Rias Gremory", "Oppai", "TNK"],
        "synonyms": ["high school dxd", "highschool dxd", "dxd"],
        "q": "High School DxD opening 1 Trip Innocent of D"
    },
    {
        "anime": "To LOVE-Ru Darkness",
        "song": "Rakuen PROJECT",
        "artist": "Ray",
        "year": 2012,
        "era": "moderna",
        "diff": "⭐⭐ Média",
        "tags": ["Harém / Ecchi", "Alienígenas", "Momo & Golden Darkness (Yami)", "Rito Yuuki", "Xebec"],
        "synonyms": ["to love ru", "to love-ru", "to love ru darkness", "to loveru"],
        "q": "To LOVE-Ru Darkness opening Rakuen PROJECT Ray"
    },
    {
        "anime": "Date A Live",
        "song": "Date A Live",
        "artist": "sweet ARMS",
        "year": 2013,
        "era": "moderna",
        "diff": "⭐ Fácil",
        "tags": ["Harém / Sci-Fi", "Espíritos", "Conquistar Garotas para Salvar o Mundo", "Tohka & Kurumi", "AIC PLUS+"],
        "synonyms": ["date a live", "dal"],
        "q": "Date A Live opening 1 sweet ARMS"
    },
    {
        "anime": "Nisekoi",
        "song": "CLICK",
        "artist": "ClariS",
        "year": 2014,
        "era": "moderna",
        "diff": "⭐ Fácil",
        "tags": ["Harém / Romcom", "Amor Falso", "Chitoge & Kosaki", "Pingente e Chaves", "Estúdio Shaft"],
        "synonyms": ["nisekoi", "falso amor"],
        "q": "Nisekoi opening 1 CLICK ClariS"
    },
    {
        "anime": "Trinity Seven",
        "song": "Seven Doors",
        "artist": "ZAQ",
        "year": 2014,
        "era": "moderna",
        "diff": "⭐⭐ Média",
        "tags": ["Harém / Magia", "7 Pecados Capitais", "Arata Kasuga", "Mundo dos Magos", "Seven Arcs Pictures"],
        "synonyms": ["trinity seven", "trinity 7"],
        "q": "Trinity Seven opening Seven Doors ZAQ"
    },
    {
        "anime": "Gakusen Toshi Asterisk",
        "song": "Brand-new World",
        "artist": "Shiena Nishizawa",
        "year": 2015,
        "era": "moderna",
        "diff": "⭐⭐ Média",
        "tags": ["Harém de Batalha", "Festa Estelar / Torneio", "Julis & Ayato", "Armas Lux", "A-1 Pictures"],
        "synonyms": ["gakusen toshi asterisk", "the asterisk war", "asterisk war", "gakusen toshi"],
        "q": "The Asterisk War opening 1 Brand-new World Shiena Nishizawa"
    },
    {
        "anime": "Rakudai Kishi no Cavalry",
        "song": "Identity",
        "artist": "Mikio Sakai",
        "year": 2015,
        "era": "moderna",
        "diff": "⭐⭐ Média",
        "tags": ["Cavaleiros Mágicos", "Stella Vermillion", "Ikki Kurogane (O Pior)", "Romance & Espadas", "SILVER LINK."],
        "synonyms": ["rakudai kishi no cavalry", "chivalry of a failed knight", "rakudai kishi"],
        "q": "Rakudai Kishi no Cavalry opening Identity Mikio Sakai"
    },
    {
        "anime": "Monster Musume no Iru Nichijou",
        "song": "Saikousoku Fall in Love",
        "artist": "Miia, Papi, Centorea",
        "year": 2015,
        "era": "moderna",
        "diff": "⭐⭐ Média",
        "tags": ["Harém / Monster Girls", "Mulheres Monstro", "Miia Lamia & Papi Harpia", "Comédia / Ecchi", "Lerche"],
        "synonyms": ["monster musume", "everyday life with monster girls", "monmusu"],
        "q": "Monster Musume opening Saikousoku Fall in Love"
    },
    {
        "anime": "Prison School",
        "song": "Ai no Prison",
        "artist": "Kangoku Danshi",
        "year": 2015,
        "era": "moderna",
        "diff": "⭐⭐ Média",
        "tags": ["Comédia / Ecchi Extremo", "Prisão Escolar", "Conselho Estudantil Secreto", "Kiyoshi", "J.C.Staff"],
        "synonyms": ["prison school", "kangoku gakuen"],
        "q": "Prison School opening Ai no Prison"
    },
    {
        "anime": "Shokugeki no Souma",
        "song": "Kibou no Uta",
        "artist": "Ultra Tower",
        "year": 2015,
        "era": "moderna",
        "diff": "⭐ Fácil",
        "tags": ["Culinária / Ecchi Gastronômico", "Batalhas de Cozinha", "Souma Yukihira & Erina", "Academia Totsuki", "J.C.Staff"],
        "synonyms": ["shokugeki no souma", "food wars", "food wars shokugeki no soma", "shokugeki"],
        "q": "Food Wars opening 1 Kibou no Uta Crunchyroll"
    }
]

results = []

for item in candidates:
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
        print(f"[FOUND] {item['anime']} ({item['year']}) -> {item['video_url']} | {best_title[:45]}")
        results.append(item)
    except Exception as e:
        print(f"[ERR] {item['anime']}: {e}")

out_path = "C:/Users/luizd/.gemini/antigravity/scratch/anime-music-quiz/tools/harem_songs_verified.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"\nFinalizado! {len(results)} animes de Harém/Ecchi verificados e salvos!")
