import json
import yt_dlp
import os

DIR = "C:/Users/luizd/.gemini/antigravity/scratch/anime-music-quiz"
OUT_PATH = os.path.join(DIR, "tools", "found_25_songs.json")

queries = [
    ("Kaguya-sama: Love is War", "Love Dramatic", "Masayuki Suzuki feat. Rikka Ihara", 2019, "2010s", "⭐ Fácil",
     ["Romance", "Comédia Escolar", "Batalha Psicológica", "A-1 Pictures"],
     ["kaguya-sama", "kaguya sama", "love is war", "kaguya-sama wa kokurasetai", "kaguya"],
     "Romance / Comédia Escolar / Duelo Psicológico de Confissões",
     "ytsearch3:Kaguya-sama Love is War opening 1 Love Dramatic Masayuki Suzuki"),

    ("Cyberpunk: Edgerunners", "This Fffire", "Franz Ferdinand", 2022, "2020s", "⭐ Fácil",
     ["Cyberpunk", "Ação / Ficção Científica", "Night City / David", "Studio Trigger"],
     ["cyberpunk edgerunners", "cyberpunk", "edgerunners"],
     "Ficção Científica / Cyberpunk / Night City / Studio Trigger",
     "ytsearch3:Cyberpunk Edgerunners opening This Fffire Franz Ferdinand"),

    ("Bocchi the Rock!", "Seishun Complex", "Kessoku Band", 2022, "2020s", "⭐ Fácil",
     ["Comédia", "Música / Banda", "Ansiedade Social / Guitarra", "CloverWorks"],
     ["bocchi the rock", "bocchi the rock!", "bocchi"],
     "Comédia / Música / Guitarra e Ansiedade Social / Kessoku Band",
     "ytsearch3:Bocchi the Rock opening Seishun Complex Kessoku Band"),

    ("Overlord", "Clattanoia", "OxT", 2015, "2010s", "⭐ Fácil",
     ["Isekai", "Fantasia Sombria", "Ainz Ooal Gown / Nazarick", "Madhouse"],
     ["overlord", "ainz ooal gown"],
     "Isekai / Fantasia Sombria / Grande Tumba de Nazarick / Madhouse",
     "ytsearch3:Overlord opening 1 Clattanoia OxT"),

    ("Blue Lock", "Chaos ga Kiwamaru", "UNISON SQUARE GARDEN", 2022, "2020s", "⭐ Fácil",
     ["Esportes", "Futebol / Egoísmo", "Isagi Yoichi", "Eight Bit"],
     ["blue lock", "bluelock"],
     "Esportes / Futebol Egoísta / Projeto Blue Lock",
     "ytsearch3:Blue Lock opening 1 Chaos ga Kiwamaru UNISON SQUARE GARDEN"),

    ("Akame ga Kill!", "Skyreach", "Sora Amamiya", 2014, "2010s", "⭐⭐ Média",
     ["Ação", "Fantasia Sombria", "Assassinos / Night Raid", "White Fox"],
     ["akame ga kill", "akame ga kill!"],
     "Ação / Fantasia Sombria / Grupo Rebelde Night Raid / Armas Teigu",
     "ytsearch3:Akame ga Kill opening 1 Skyreach Sora Amamiya"),

    ("Delicious in Dungeon", "Sleep Walking Orchestra", "BUMP OF CHICKEN", 2024, "2020s", "⭐ Fácil",
     ["Fantasia", "Culinária de Monstros", "Masmorra / Laios", "Studio Trigger"],
     ["delicious in dungeon", "dungeon meshi", "dungeon meshi: delicious in dungeon"],
     "Fantasia / Cozinha de Monstros em Masmorra / Studio Trigger",
     "ytsearch3:Delicious in Dungeon opening Sleep Walking Orchestra BUMP OF CHICKEN"),

    ("Samurai Champloo", "Battlecry", "Nujabes feat. Shing02", 2004, "2000s", "⭐⭐ Média",
     ["Samurai / Hip-Hop", "Ação Histórica", "Mugen & Jin", "Manglobe"],
     ["samurai champloo", "champloo"],
     "Samurais & Hip-Hop / Era Edo / Mugen e Jin / Estúdio Manglobe",
     "ytsearch3:Samurai Champloo opening Battlecry Nujabes feat Shing02"),

    ("Trigun", "H.T.", "Tsuneo Imahori", 1998, "classicos", "⭐⭐ Média",
     ["Western Espacial", "Ação / Ficção Científica", "Vash the Stampede", "Madhouse"],
     ["trigun", "vash the stampede", "trigun 1998"],
     "Western Espacial / Tufão Humanoide Vash / Madhouse",
     "ytsearch3:Trigun opening HT Tsuneo Imahori"),

    ("Monster", "Grain", "Kuniaki Haishima", 2004, "2000s", "⭐⭐⭐ Difícil",
     ["Suspense Psicológico", "Mistério / Drama", "Dr. Tenma / Johan Liebert", "Madhouse"],
     ["monster", "dr tenma", "naoki urasawa monster"],
     "Suspense Psicológico / Dr. Kenzo Tenma & Johan Liebert / Madhouse",
     "ytsearch3:Monster opening Grain Kuniaki Haishima"),

    ("Hellsing Ultimate", "Logos Naki World", "Yasushi Ishii", 2006, "2000s", "⭐⭐ Média",
     ["Vampiros", "Ação Sobrenatural / Terror", "Alucard / Organização Hellsing", "Madhouse / Satelight"],
     ["hellsing", "hellsing ultimate", "alucard"],
     "Vampiros / Sobrenatural Sombrio / Alucard / Organização Hellsing",
     "ytsearch3:Hellsing opening Logos Naki World Yasushi Ishii"),

    ("Bleach: Thousand-Year Blood War", "Scar", "Tatsuya Kitani", 2022, "2020s", "⭐ Fácil",
     ["Ação / Shinigami", "Guerra de Sangue de Mil Anos", "Quincy / Yhwach", "Studio Pierrot"],
     ["bleach thousand year blood war", "bleach tybw", "bleach sennen kessen-hen", "bleach guerra sangrenta"],
     "Shinigami vs Quincy / Guerra de Mil Anos / Yhwach / Pierrot",
     "ytsearch3:Bleach Thousand-Year Blood War opening Scar Tatsuya Kitani"),

    ("Classroom of the Elite", "Caste Room", "ZAQ", 2017, "2010s", "⭐⭐ Média",
     ["Drama Psicológico", "Escola de Elite / Turma D", "Kiyotaka Ayanokouji", "Lerche"],
     ["classroom of the elite", "youkoso jitsuryoku shijou shugi no kyoushitsu e", "cote"],
     "Psicológico / Manipulação Escolar / Turma D / Kiyotaka Ayanokouji",
     "ytsearch3:Classroom of the Elite opening 1 Caste Room ZAQ"),

    ("Fate/stay night: Unlimited Blade Works", "Brave Shine", "Aimer", 2015, "2010s", "⭐ Fácil",
     ["Fantasia / Magia", "Guerra do Santo Graal", "Shirou Emiya & Archer", "ufotable"],
     ["fate stay night unlimited blade works", "fate stay night ubw", "fate ubw", "unlimited blade works"],
     "Guerra do Santo Graal / Shirou Emiya & Archer / I am the bone of my sword / ufotable",
     "ytsearch3:Fate stay night Unlimited Blade Works opening 2 Brave Shine Aimer"),

    ("Horimiya", "Iro Kousui", "Yoh Kamiyama", 2021, "2020s", "⭐⭐ Média",
     ["Romance Escolar", "Comédia / Slice of Life", "Hori & Miyamura", "CloverWorks"],
     ["horimiya", "hori-san to miyamura-kun"],
     "Romance Escolar / Dupla Identidade Secreta / Hori e Miyamura / CloverWorks",
     "ytsearch3:Horimiya opening Iro Kousui Yoh Kamiyama"),

    ("Clannad", "Megumeru", "eufonius", 2007, "2000s", "⭐⭐⭐ Difícil",
     ["Drama / Emoção", "Romance / Sobrenatural", "Tomoya & Nagisa / Dango", "Kyoto Animation"],
     ["clannad", "clannad after story"],
     "Drama Emocionante / Dango Daikazoku / Tomoya & Nagisa / Kyoto Animation",
     "ytsearch3:Clannad opening Megumeru eufonius"),

    ("Steins;Gate 0", "Fatima", "Kanako Itou", 2018, "2010s", "⭐⭐ Média",
     ["Ficção Científica", "Viagem no Tempo / Linha Beta", "Okabe Rintarou / Amadeus", "White Fox"],
     ["steins gate 0", "steins;gate 0", "steinsgate 0"],
     "Viagem no Tempo / Linha do Tempo Beta / IA Amadeus Kurisu / White Fox",
     "ytsearch3:Steins Gate 0 opening Fatima Kanako Itou"),

    ("Made in Abyss", "Deep in Abyss", "Miyu Tomita & Mariya Ise", 2017, "2010s", "⭐⭐ Média",
     ["Aventura / Fantasia", "Exploração do Abismo", "Riko & Reg", "Kinema Citrus"],
     ["made in abyss", "o abismo"],
     "Aventura Sombria / Fossa Profunda do Abismo / Riko & Reg / Apito Branco",
     "ytsearch3:Made in Abyss opening 1 Deep in Abyss"),

    ("Dororo", "Kaen", "Queen Bee", 2019, "2010s", "⭐⭐ Média",
     ["Ação / Sobrenatural", "Demônios & Samurai", "Hyakkimaru / Próteses", "MAPPA / Tezuka Productions"],
     ["dororo", "hyakkimaru"],
     "Japão Feudal / 48 Demônios / Hyakkimaru recuperando partes do corpo / MAPPA",
     "ytsearch3:Dororo opening 1 Kaen Queen Bee"),

    ("Charlotte", "Bravely You", "Lia", 2015, "2010s", "⭐⭐ Média",
     ["Superpoderes Juvenis", "Drama / Escolar", "Yuu Otosaka & Nao Tomori", "P.A. Works"],
     ["charlotte", "charlote"],
     "Superpoderes Imperfeitos na Adolescência / Yuu Otosaka & Nao Tomori / P.A. Works",
     "ytsearch3:Charlotte opening Bravely You Lia"),

    ("Guilty Crown", "My Dearest", "supercell", 2011, "2010s", "⭐⭐ Média",
     ["Ação / Ficção Científica", "Poder do Genoma Vazio", "Shu Ouma & Inori", "Production I.G"],
     ["guilty crown", "inori yuzuriha"],
     "Ficção Científica / Vírus do Apocalipse / Poder Void de Inori / Production I.G",
     "ytsearch3:Guilty Crown opening 1 My Dearest supercell"),

    ("Noragami Aragoto", "Kyouran Hey Kids!!", "THE ORAL CIGARETTES", 2015, "2010s", "⭐ Fácil",
     ["Ação / Sobrenatural", "Deus Menor por 5 Ienes", "Yato, Yukine & Hiyori", "Bones"],
     ["noragami aragoto", "noragami", "noragami 2"],
     "Deus da Calamidade por 5 Ienes / Yato & Espada Sagrada Yukine / Bones",
     "ytsearch3:Noragami Aragoto opening Kyouran Hey Kids THE ORAL CIGARETTES"),

    ("DanMachi (Is It Wrong to Try to Pick Up Girls in a Dungeon?)", "Hey World", "Yuka Iguchi", 2015, "2010s", "⭐ Fácil",
     ["Fantasia / Aventura", "Família de Deusa & Masmorra", "Bell Cranel & Hestia", "J.C.Staff"],
     ["danmachi", "is it wrong to try to pick up girls in a dungeon", "dungeon ni deai wo motomeru no wa machigatteiru darou ka", "familia myth"],
     "Aventura em Masmorra / Bell Cranel & Deusa Hestia / J.C.Staff",
     "ytsearch3:DanMachi opening 1 Hey World Yuka Iguchi"),

    ("Black Lagoon", "Red fraction", "MELL", 2006, "2000s", "⭐⭐ Média",
     ["Ação / Crime / Armas", "Mercenários em Roanapur", "Revy 'Two-Hands' & Rock", "Madhouse"],
     ["black lagoon", "roanapur", "revy"],
     "Crime & Mercenários / Cidade sem Lei de Roanapur / Revy Duas Mãos / Madhouse",
     "ytsearch3:Black Lagoon opening Red fraction MELL"),

    ("Assassination Classroom", "Seishun Satsubatsuron", "3-nen E-gumi Utatan", 2015, "2010s", "⭐ Fácil",
     ["Comédia / Escolar", "Professor Polvo Alien", "Koro-sensei / Turma 3-E", "Lerche"],
     ["assassination classroom", "ansatsu kyoushitsu", "koro sensei", "koro-sensei"],
     "Escola de Assassinos / Alvo: Professor Polvo Amarelo Koro-sensei / Lerche",
     "ytsearch3:Assassination Classroom opening 1 Seishun Satsubatsuron")
]

ydl_opts = {
    'quiet': True,
    'extract_flat': True,
    'skip_download': True
}

import sys
sys.stdout.reconfigure(encoding='utf-8')

verified_entries = []
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    for idx, (anime, song, artist, year, era, diff, tags, syns, hint, q) in enumerate(queries):
        info = ydl.extract_info(q, download=False)
        entries = info.get('entries', [])
        chosen_id = entries[0].get('id') if entries else ""
        chosen_title = entries[0].get('title', '') if entries else ""
        safe_title = chosen_title.encode('ascii', 'replace').decode('ascii')
        print(f"[{idx+1}/25] {anime} -> {chosen_id} ({safe_title[:30]}...)")
        
        verified_entries.append({
            "id": 75 + idx + 1,
            "anime": anime,
            "song": song,
            "artist": artist,
            "year": year,
            "era": era,
            "diff": diff,
            "tags": tags,
            "synonyms": syns,
            "video_id": chosen_id,
            "video_url": f"https://www.youtube.com/watch?v={chosen_id}",
            "hint": hint,
            "image_url": ""
        })

with open(OUT_PATH, "w", encoding="utf-8") as f:
    json.dump(verified_entries, f, ensure_ascii=False, indent=2)

print("\nConcluído com sucesso! Salvo em:", OUT_PATH)
