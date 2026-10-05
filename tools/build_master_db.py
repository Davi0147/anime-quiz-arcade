import json
import re

# Load existing 42 songs
with open("C:/Users/luizd/.gemini/antigravity/scratch/anime-music-quiz/anime_songs_verified.json", "r", encoding="utf-8") as f:
    existing = json.load(f)

# Load new 19 songs
with open("C:/Users/luizd/.gemini/antigravity/scratch/anime-music-quiz/tools/new_songs_verified.json", "r", encoding="utf-8") as f:
    new_songs = json.load(f)

# Fix #32 Boku no Hero (replace Portuguese cover with official Japanese version)
for s in existing:
    if s["id"] == 32:
        s["video_id"] = "yu0HjPzFYnY"
        s["video_url"] = "https://www.youtube.com/watch?v=yu0HjPzFYnY"
        s["video_title"] = "My Hero Academia Opening 1 | The Day"

# Metadata enrichment dictionary for the existing 42 songs
metadata_42 = {
    1: { # InuYasha
        "era": "classicos",
        "diff": "⭐⭐ Média",
        "tags": ["Shounen", "Fantasia Feudal", "Youkai / Meio-Demônio", "Joia de Quatro Almas", "Estúdio Sunrise"],
        "synonyms": ["inuyasha", "inu yasha", "inu-yasha"]
    },
    2: { # Digimon Tamers
        "era": "classicos",
        "diff": "⭐⭐⭐ Difícil",
        "tags": ["Monstros Digitais", "Cartas & Digivoluções", "Guilmon", "Mundo Real vs Digital", "Toei Animation"],
        "synonyms": ["digimon tamers", "digimon 3", "digimon tamer"]
    },
    3: { # Shaman King
        "era": "classicos",
        "diff": "⭐⭐⭐ Difícil",
        "tags": ["Xamanismo", "Espíritos Guardiões", "Torneio Xamã", "Yoh Asakura", "Estúdio Xebec"],
        "synonyms": ["shaman king", "o rei dos xamas", "rei dos xamas"]
    },
    4: { # Naruto
        "era": "classicos",
        "diff": "⭐ Fácil",
        "tags": ["Ninjas / Shinobi", "Exame Chuunin", "Floresta da Morte", "Konoha", "Studio Pierrot"],
        "synonyms": ["naruto", "naruto classico", "naruto shonen"]
    },
    5: { # Fullmetal Alchemist 2003
        "era": "classicos",
        "diff": "⭐⭐ Média",
        "tags": ["Alquimia", "Irmãos Elric", "Braço de Metal", "Pedra Filosofal", "Estúdio Bones"],
        "synonyms": ["fullmetal alchemist", "fullmetal", "fma", "fma 2003", "hagane no renkinjutsushi"]
    },
    6: { # Bleach
        "era": "classicos",
        "diff": "⭐ Fácil",
        "tags": ["Shinigami / Ceifeiros", "Espadas Zanpakutou", "Hollows", "Ichigo Kurosaki", "Studio Pierrot"],
        "synonyms": ["bleach", "burichi"]
    },
    7: { # Naruto OP 4
        "era": "classicos",
        "diff": "⭐ Fácil",
        "tags": ["Ninjas", "We Are Fighting Dreamers", "Vale do Fim", "Sasuke & Naruto", "Studio Pierrot"],
        "synonyms": ["naruto", "naruto classico"]
    },
    8: { # Death Note
        "era": "ouro",
        "diff": "⭐ Fácil",
        "tags": ["Suspense Psicológico", "Caderno da Morte", "Shinigami Ryuk", "Light vs L", "Estúdio Madhouse"],
        "synonyms": ["death note", "caderno da morte", "deathnote"]
    },
    9: { # Code Geass
        "era": "ouro",
        "diff": "⭐⭐ Média",
        "tags": ["Mecha / Robôs", "Estratégia Militar", "Olho do Geass", "Lelouch / Zero", "Estúdio Sunrise"],
        "synonyms": ["code geass", "code geass lelouch of the rebellion", "lelouch of the rebellion"]
    },
    10: { # Fate/stay night
        "era": "ouro",
        "diff": "⭐⭐⭐ Difícil",
        "tags": ["Guerra do Santo Graal", "Mestres & Servos", "Saber / Excalibur", "Magia Urbana", "Studio Deen"],
        "synonyms": ["fate stay night", "fate/stay night", "fate", "fate 2006"]
    },
    11: { # Gurren Lagann
        "era": "ouro",
        "diff": "⭐⭐ Média",
        "tags": ["Mecha Épico", "Brocas Gigantes", "Kamina & Simon", "Perfurar os Céus", "Estúdio Gainax"],
        "synonyms": ["tengen toppa gurren lagann", "gurren lagann", "ttgl"]
    },
    12: { # Naruto Shippuden
        "era": "ouro",
        "diff": "⭐ Fácil",
        "tags": ["Ninjas", "Habataitara", "Akatsuki", "Konoha", "Studio Pierrot"],
        "synonyms": ["naruto shippuden", "naruto shippuuden", "naruto"]
    },
    13: { # Soul Eater
        "era": "ouro",
        "diff": "⭐⭐ Média",
        "tags": ["Armas & Artífices", "Academia DWMA", "Gadanha Mortal", "Maka & Soul", "Estúdio Bones"],
        "synonyms": ["soul eater", "souleater"]
    },
    14: { # Toradora!
        "era": "ouro",
        "diff": "⭐⭐⭐ Difícil",
        "tags": ["Romance Escolar", "Comédia", "Tigresa de Bolso", "Taiga & Ryuuji", "J.C.Staff"],
        "synonyms": ["toradora", "toradora!"]
    },
    15: { # Fullmetal Alchemist: Brotherhood
        "era": "ouro",
        "diff": "⭐ Fácil",
        "tags": ["Alquimia", "Irmãos Elric", "Homúnculos", "Amestris", "Estúdio Bones"],
        "synonyms": ["fullmetal alchemist brotherhood", "fullmetal alchemist", "fmab", "fma brotherhood", "fma"]
    },
    16: { # Bakemonogatari
        "era": "ouro",
        "diff": "⭐⭐ Média",
        "tags": ["Sobrenatural", "Vampiros & Maldições", "Renai Circulation", "Araragi & Nadeko", "Estúdio Shaft"],
        "synonyms": ["bakemonogatari", "monogatari", "monogatari series"]
    },
    17: { # Fairy Tail
        "era": "ouro",
        "diff": "⭐⭐ Média",
        "tags": ["Guilda de Magos", "Dragon Slayer de Fogo", "Natsu & Happy", "Magia", "A-1 Pictures"],
        "synonyms": ["fairy tail", "fairytail"]
    },
    18: { # Durarara!!
        "era": "ouro",
        "diff": "⭐⭐ Média",
        "tags": ["Mistério Urbano", "Ikebukuro", "Motoqueira Sem Cabeça", "Gangue Dollars", "Brain's Base"],
        "synonyms": ["durarara", "durarara!!", "drrr"]
    },
    19: { # Steins;Gate
        "era": "moderna",
        "diff": "⭐⭐ Média",
        "tags": ["Ficção Científica", "Viagem no Tempo", "Cientista Louco", "Okabe & Kurisu", "White Fox"],
        "synonyms": ["steins gate", "steins;gate", "steinsgate"]
    },
    20: { # Hunter x Hunter
        "era": "moderna",
        "diff": "⭐ Fácil",
        "tags": ["Exame Hunter", "Energia Nen", "Gon & Killua", "You can smile again!", "Estúdio Madhouse"],
        "synonyms": ["hunter x hunter", "hunter hunter", "hxh", "hunter x hunter 2011"]
    },
    21: { # Fate/Zero
        "era": "moderna",
        "diff": "⭐⭐⭐ Difícil",
        "tags": ["Guerra do Santo Graal", "Assassino de Magos", "Kiritsugu", "Tragédia Épica", "ufotable"],
        "synonyms": ["fate zero", "fate/zero"]
    },
    22: { # Sword Art Online
        "era": "moderna",
        "diff": "⭐ Fácil",
        "tags": ["Isekai / Realidade Virtual", "Espadas & MMORPG", "Kirito & Asuna", "Aincrad", "A-1 Pictures"],
        "synonyms": ["sword art online", "sao"]
    },
    23: { # JoJo's Bizarre Adventure
        "era": "moderna",
        "diff": "⭐⭐ Média",
        "tags": ["Família Joestar", "Hamon & Vampiros", "Dio Brando", "Jonathan Joestar", "David Production"],
        "synonyms": ["jojo", "jojos bizarre adventure", "jojo no kimyou na bouken", "phantom blood"]
    },
    24: { # Attack on Titan
        "era": "moderna",
        "diff": "⭐ Fácil",
        "tags": ["Muralhas & Titãs", "Tropa de Exploração", "Eren & Mikasa", "Dispositivo DMT", "Wit Studio"],
        "synonyms": ["attack on titan", "shingeki no kyojin", "ataque dos titas", "aot", "snk", "shingeki"]
    },
    25: { # Kill la Kill
        "era": "moderna",
        "diff": "⭐⭐⭐ Difícil",
        "tags": ["Fibras de Vida", "Espada Tesoura", "Ryuko Matoi", "Academia Honnouji", "Studio Trigger"],
        "synonyms": ["kill la kill", "klk"]
    },
    26: { # Tokyo Ghoul
        "era": "moderna",
        "diff": "⭐ Fácil",
        "tags": ["Ghouls de Tóquio", "Máscara & Kagune", "Kaneki Ken", "Café Anteiku", "Studio Pierrot"],
        "synonyms": ["tokyo ghoul", "tokyoghoul"]
    },
    27: { # No Game No Life
        "era": "moderna",
        "diff": "⭐⭐ Média",
        "tags": ["Isekai de Jogos", "Irmãos Kuuhaku (Espaço em Branco)", "Sora & Shiro", "Deus dos Jogos Tet", "Estúdio Madhouse"],
        "synonyms": ["no game no life", "ngnl"]
    },
    28: { # Your Lie in April
        "era": "moderna",
        "diff": "⭐⭐ Média",
        "tags": ["Drama Musical", "Piano & Violino", "Kousei & Kaori", "Primavera", "A-1 Pictures"],
        "synonyms": ["your lie in april", "shigatsu wa kimi no uso", "sua mentira em abril"]
    },
    29: { # Noragami
        "era": "moderna",
        "diff": "⭐⭐⭐ Difícil",
        "tags": ["Deus por 5 Ienes", "Espíritos & Regalias", "Yato & Hiyori", "Fantasmas Ayakashi", "Estúdio Bones"],
        "synonyms": ["noragami", "noragami aragoto"]
    },
    30: { # Haikyuu!!
        "era": "moderna",
        "diff": "⭐⭐ Média",
        "tags": ["Vôlei Colegial", "Corvos do Karasuno", "Hinata & Kageyama", "Esportes", "Production I.G"],
        "synonyms": ["haikyuu", "haikyuu!!", "haikyu"]
    },
    31: { # One Punch Man
        "era": "moderna",
        "diff": "⭐ Fácil",
        "tags": ["Herói por Hobby", "Derrota com 1 Soco", "Saitama & Genos", "Associação de Heróis", "Estúdio Madhouse"],
        "synonyms": ["one punch man", "one punch", "opm", "homem de um soco so"]
    },
    32: { # Boku no Hero Academia
        "era": "recente",
        "diff": "⭐ Fácil",
        "tags": ["Super-Heróis", "All Might & Deku", "One For All", "Escola U.A.", "Estúdio Bones"],
        "synonyms": ["boku no hero academia", "my hero academia", "boku no hero", "mha", "bnha"]
    },
    33: { # Mob Psycho 100
        "era": "recente",
        "diff": "⭐⭐ Média",
        "tags": ["Poderes Psíquicos", "Reigen Mestre Trapaceiro", "Shigeo Kageyama (Mob)", "Porcentagem 100%", "Estúdio Bones"],
        "synonyms": ["mob psycho 100", "mob psycho", "mob"]
    },
    34: { # Re:Zero
        "era": "recente",
        "diff": "⭐⭐ Média",
        "tags": ["Retorno através da Morte", "Subaru & Emilia", "Rem & Ram", "Isekai Sombrio", "White Fox"],
        "synonyms": ["re zero", "re:zero", "re:zero kara hajimeru isekai seikatsu", "rezero"]
    },
    35: { # KonoSuba
        "era": "recente",
        "diff": "⭐⭐ Média",
        "tags": ["Comédia / Paródia Isekai", "Deusa Aqua Inútil", "Megumin Explosão", "Kazuma", "Studio Deen"],
        "synonyms": ["konosuba", "kono subarashii sekai ni shukufuku wo", "kono suba"]
    },
    36: { # Boku no Hero Academia S2
        "era": "recente",
        "diff": "⭐⭐ Média",
        "tags": ["Festival Esportivo da U.A.", "Midoriya vs Todoroki", "Paz e Vitória", "Estúdio Bones", "Super-Heróis"],
        "synonyms": ["boku no hero academia", "my hero academia", "boku no hero", "mha", "bnha"]
    },
    37: { # Black Clover
        "era": "recente",
        "diff": "⭐⭐ Média",
        "tags": ["Garoto Sem Magia", "Grimório do Trevo de 5 Folhas", "Asta & Yuno", "Touros Negros", "Studio Pierrot"],
        "synonyms": ["black clover", "blackclover"]
    },
    38: { # Kimetsu no Yaiba
        "era": "recente",
        "diff": "⭐ Fácil",
        "tags": ["Caçadores de Demônios / Onis", "Respiração da Água & Sol", "Tanjiro & Nezuko", "Espadas Nichirin", "ufotable"],
        "synonyms": ["kimetsu no yaiba", "demon slayer", "kimetsu", "demon slayer kimetsu no yaiba"]
    },
    39: { # The Promised Neverland
        "era": "recente",
        "diff": "⭐⭐⭐ Difícil",
        "tags": ["Orfanato Sinistro", "Crianças Gênias", "Emma, Norman & Ray", "Fuga dos Demônios", "CloverWorks"],
        "synonyms": ["the promised neverland", "yakusoku no neverland", "promised neverland"]
    },
    40: { # Vinland Saga
        "era": "recente",
        "diff": "⭐⭐⭐ Difícil",
        "tags": ["Vikings Históricos", "Vingança de Thorfinn", "Askeladd & Canute", "Inglaterra Medieval", "Wit Studio"],
        "synonyms": ["vinland saga", "vinland"]
    },
    41: { # Dr. Stone
        "era": "recente",
        "diff": "⭐⭐ Média",
        "tags": ["Mundo de Pedra Petrificado", "Renascimento pela Ciência", "Senku Ishigami", "Reino da Ciência", "TMS Entertainment"],
        "synonyms": ["dr stone", "dr. stone", "doctor stone"]
    },
    42: { # Jujutsu Kaisen
        "era": "recente",
        "diff": "⭐ Fácil",
        "tags": ["Feiticeiros Jujutsu", "Dedos de Sukuna", "Yuji Itadori & Gojo Satoru", "Energia Amaldiçoada", "Estúdio MAPPA"],
        "synonyms": ["jujutsu kaisen", "jujutsu", "jjk", "batalha de feiticeiros"]
    }
}

master_list = []
curr_id = 1

# Merge existing 42 with metadata
for s in existing:
    meta = metadata_42.get(s["id"], {})
    item = {
        "id": curr_id,
        "anime": s["anime"],
        "song": s["song"],
        "artist": s["artist"],
        "year": s["year"],
        "era": meta.get("era", "classicos"),
        "diff": meta.get("diff", "⭐⭐ Média"),
        "tags": meta.get("tags", ["Anime", "Abertura"]),
        "synonyms": meta.get("synonyms", [s["anime"].lower()]),
        "video_id": s["video_id"],
        "video_url": s["video_url"],
        "hint": s.get("hint", "")
    }
    master_list.append(item)
    curr_id += 1

# Add new 19 songs
for n in new_songs:
    item = {
        "id": curr_id,
        "anime": n["anime"],
        "song": n["song"],
        "artist": n["artist"],
        "year": n["year"],
        "era": n["era"],
        "diff": n["diff"],
        "tags": n["tags"],
        "synonyms": n["synonyms"],
        "video_id": n["video_id"],
        "video_url": n["video_url"],
        "hint": " / ".join(n["tags"][:3])
    }
    master_list.append(item)
    curr_id += 1

# Sort chronologically by year (and then by id)
master_list.sort(key=lambda x: (x["year"], x["id"]))

# Re-index ids 1 to N
for idx, item in enumerate(master_list, start=1):
    item["id"] = idx

print(f"Total master songs compiled: {len(master_list)}")
print(f"Years range: {master_list[0]['year']} to {master_list[-1]['year']}")

# Save master json
output_path = "C:/Users/luizd/.gemini/antigravity/scratch/anime-music-quiz/anime_songs_verified.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(master_list, f, ensure_ascii=False, indent=2)

print(f"Saved master songs to {output_path}")
