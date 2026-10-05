import json
import os
import re

DIR = "C:/Users/luizd/.gemini/antigravity/scratch/anime-music-quiz"
SONGS_PATH = os.path.join(DIR, "anime_songs_verified.json")
SCENES_PATH = os.path.join(DIR, "tools", "anime_scenes.json")
OUT_PATH = os.path.join(DIR, "tools", "anime_autocomplete_db.json")

def normalize_key(s):
    if not s: return ""
    s = s.lower().strip()
    s = re.sub(r'[àáâãä]', 'a', s)
    s = re.sub(r'[èéêë]', 'e', s)
    s = re.sub(r'[ìíîï]', 'i', s)
    s = re.sub(r'[òóôõö]', 'o', s)
    s = re.sub(r'[ùúûü]', 'u', s)
    s = re.sub(r'[ç]', 'c', s)
    s = re.sub(r'[^a-z0-9]', '', s)
    return s

def extract_canonical_names(raw_title):
    if not raw_title: return []
    candidates = []
    
    # Check parentheses: "Attack on Titan (Shingeki no Kyojin)" -> ["Attack on Titan", "Shingeki no Kyojin"]
    parens = re.findall(r'\((.*?)\)', raw_title)
    no_paren = re.sub(r'\(.*?\)', '', raw_title).strip()
    
    # Strip season indicators
    season_patterns = [
        r'\s+Season\s*\d+.*',
        r'\s+\d+(st|nd|rd|th)\s*Season.*',
        r'\s+Final\s*Season.*',
        r'\s+Part\s*\d+.*',
        r'\s+Pt\s*\d+.*',
        r'\s+The\s*Animation.*',
        r'\s+The\s*Movie.*',
        r'\s+Movie.*',
        r'\s+II\b.*',
        r'\s+III\b.*',
        r'\s+IV\b.*',
        r'\s+New\b.*',
        r'\s+BorN\b.*',
        r'\s+Hero\b.*',
        r'\s+Darkness\b.*',
        r'\s+2nd\b.*',
        r'\s+3rd\b.*',
    ]
    base_clean = no_paren
    for p in season_patterns:
        base_clean = re.sub(p, '', base_clean, flags=re.IGNORECASE).strip()
    
    # Check colon / dash prefix (e.g., "Bleach: Thousand-Year Blood War" -> "Bleach")
    for sep in [':', ' - ', ' – ']:
        if sep in base_clean:
            prefix = base_clean.split(sep)[0].strip()
            if len(prefix) >= 3 and prefix.lower() not in ['fate']:
                candidates.append(prefix)

    candidates.append(base_clean if base_clean else no_paren)
    
    for p in parens:
        p_clean = p.strip()
        if len(p_clean) >= 4 and not re.match(r'^(tv|movie|ova|ona|\d{4})$', p_clean, re.I):
            for sp in season_patterns:
                p_clean = re.sub(sp, '', p_clean, flags=re.IGNORECASE).strip()
            if len(p_clean) >= 4:
                candidates.append(p_clean)
                
    return candidates

# Load database
with open(SONGS_PATH, "r", encoding="utf-8") as f:
    songs = json.load(f)

scenes = []
if os.path.exists(SCENES_PATH):
    with open(SCENES_PATH, "r", encoding="utf-8") as f:
        scenes = json.load(f)

famous_franchises = [
    # Shonen / Action Classics & Modern
    "Dragon Ball", "Dragon Ball Z", "Dragon Ball GT", "Dragon Ball Super",
    "Naruto", "Naruto Shippuden", "Boruto",
    "Bleach",
    "One Piece",
    "Attack on Titan", "Shingeki no Kyojin",
    "Hunter x Hunter",
    "Fullmetal Alchemist", "Fullmetal Alchemist: Brotherhood",
    "Yu Yu Hakusho", "Rurouni Kenshin", "InuYasha", "Shaman King",
    "Soul Eater", "Fire Force", "Black Clover", "Fairy Tail", "Edens Zero",
    "Jujutsu Kaisen", "Chainsaw Man", "Demon Slayer", "Kimetsu no Yaiba",
    "My Hero Academia", "Boku no Hero Academia",
    "Solo Leveling", "Dandadan", "Kaiju No. 8", "Wind Breaker",
    "Mashle: Magic and Muscles", "Undead Unluck", "Shangri-La Frontier",
    "Hell's Paradise", "Jigokuraku", "Dr. Stone", "Tokyo Revengers",
    "Gintama", "Bungo Stray Dogs", "Blood Blockade Battlefront", "Kekkai Sensen",
    "Noragami", "Blue Exorcist", "Ao no Exorcist", "Katekyo Hitman Reborn!",
    "D.Gray-man", "Beelzebub", "Toriko", "Magi", "World Trigger",
    
    # Fate Series & Type-Moon
    "Fate/stay night", "Fate/Zero", "Fate/stay night: Unlimited Blade Works",
    "Fate/Apocrypha", "Fate/Grand Order", "Fate/kaleid liner Prisma Illya",
    "Tsukihime", "Kara no Kyoukai",
    
    # Isekai & Fantasy
    "Sword Art Online", "SAO", "Accel World", "Log Horizon",
    "No Game No Life", "Re:Zero", "KonoSuba", "Overlord",
    "The Rising of the Shield Hero", "Tate no Yuusha",
    "That Time I Got Reincarnated as a Slime", "Tensura",
    "Mushoku Tensei: Jobless Reincarnation", "The Eminence in Shadow",
    "Cautious Hero", "Youjo Senki", "DanMachi", "Goblin Slayer",
    "Grimgar of Fantasy and Ash", "Dungeon Meshi", "Frieren: Beyond Journey's End",
    
    # Harem / Ecchi (2010 - 2018 & Classics)
    "High School DxD",
    "To LOVE-Ru",
    "Rosario + Vampire",
    "Sora no Otoshimono", "Heaven's Lost Property",
    "Monster Musume",
    "Prison School",
    "Gakusen Toshi Asterisk", "The Asterisk War",
    "Rakudai Kishi no Cavalry", "Chivalry of a Failed Knight",
    "Trinity Seven",
    "IS: Infinite Stratos",
    "Highschool of the Dead",
    "Date A Live",
    "Sekirei",
    "Freezing",
    "Campione!",
    "Shinmai Maou no Testament", "The Testament of Sister New Devil",
    "Strike the Blood",
    "Nisekoi",
    "Saekano",
    "Oreimo",
    "Eromanga Sensei",
    "Kanojo ga Flag wo Oraretara",
    "Shimoneta",
    "Why the Hell Are You Here, Teacher!?",
    "Yuuna and the Haunted Hot Springs",
    "We Never Learn: BOKUBEN",
    "The Quintessential Quintuplets", "Gotoubun no Hanayome",
    "Rent-a-Girlfriend", "Kanojo, Okarishimasu",
    "Domestic Girlfriend", "Domestic na Kanojo",
    "Kuzu no Honkai", "Scum's Wish",
    "The 100 Girlfriends",
    
    # Psychological / Thriller / Mystery / Seinen
    "Death Note", "Code Geass", "Steins;Gate", "Monster",
    "Psycho-Pass", "Erased", "Boku dake ga Inai Machi",
    "Tokyo Ghoul", "Parasyte", "Kiseijuu", "Another", "Mirai Nikki",
    "Deadman Wonderland", "Elfen Lied", "Higurashi: When They Cry",
    "Serial Experiments Lain", "Ergo Proxy", "Texhnolyze",
    "Ghost in the Shell", "Akira", "Perfect Blue", "Paprika",
    "Terror in Resonance", "Zankyou no Terror",
    "The Promised Neverland", "Classroom of the Elite",
    "Kakegurui", "Kaiji", "Death Parade",
    "Baccano!", "Durarara!!", "91 Days", "Banana Fish", "Black Lagoon",
    "Hellsing", "Hellsing Ultimate", "Drifters",
    "Berserk", "Claymore", "Vinland Saga", "Kingdom", "Dororo",
    "Golden Kamuy", "Dorohedoro", "Made in Abyss",
    "The Apothecary Diaries", "Heavenly Delusion", "Summer Time Rendering",
    
    # Mecha & Sci-Fi
    "Neon Genesis Evangelion", "Evangelion",
    "Tengen Toppa Gurren Lagann", "Gurren Lagann",
    "Cowboy Bebop", "Trigun", "Space Dandy", "Cyberpunk: Edgerunners",
    "Mobile Suit Gundam", "Gundam Wing", "Gundam SEED", "Gundam 00",
    "Gundam: Iron-Blooded Orphans", "Gundam: The Witch from Mercury",
    "Eureka Seven", "Darling in the FranXX", "Aldnoah.Zero", "86 Eighty-Six",
    "Vivy: Fluorite Eye's Song", "Promare",
    
    # Sports
    "Haikyuu!!", "Kuroko no Basket", "Slam Dunk", "Blue Lock", "Aoashi",
    "Hajime no Ippo", "Megalo Box", "Free!", "Yuri!!! on Ice",
    "Run with the Wind", "Ace of Diamond", "Ping Pong the Animation",
    "Prince of Tennis", "Eyeshield 21", "Yowamushi Pedal",
    
    # Romance / Drama / Slice of Life / Music
    "Toradora!", "Clannad", "Angel Beats!", "Charlotte", "Plastic Memories",
    "Anohana", "Your Lie in April", "Shigatsu wa Kimi no Uso",
    "Violet Evergarden", "A Silent Voice", "Koe no Katachi",
    "Your Name", "Kimi no Na wa", "Weathering with You", "Suzume",
    "5 Centimeters per Second", "I Want to Eat Your Pancreas",
    "Horimiya", "Kaguya-sama: Love is War", "Kaguya-sama",
    "My Dress-Up Darling", "Sono Bisque Doll", "The Dangers in My Heart",
    "Komi Can't Communicate", "Teasing Master Takagi-san",
    "Kimi ni Todoke", "Fruits Basket", "Nana", "Ouran High School Host Club",
    "Kaichou wa Maid-sama!", "Kamisama Kiss", "Ao Haru Ride", "Golden Time",
    "Rascal Does Not Dream of Bunny Girl Senpai", "Seishun Buta Yarou",
    "Oregairu", "Hyouka", "Chuunibyou", "K-On!", "Bocchi the Rock!",
    "Sound! Euphonium", "Hibike! Euphonium", "Beck", "Given", "Carole & Tuesday",
    "Oshi no Ko", "Spy x Family", "Barakamon", "Non Non Biyori", "Yuru Camp",
    "A Place Further Than the Universe", "Nichijou",
    "Daily Lives of High School Boys", "Grand Blue", "GTO: Great Teacher Onizuka",
    "The Melancholy of Haruhi Suzumiya", "Lucky Star",
    "Bakemonogatari", "Monogatari Series",
    "Mob Psycho 100", "One Punch Man", "Kill la Kill", "Little Witch Academia",
    
    # Nostalgia / Childhood
    "Pokemon", "Digimon", "Digimon Adventure", "Digimon Tamers",
    "Yu-Gi-Oh!", "Beyblade", "Sailor Moon", "Cardcaptor Sakura",
    "Medabots", "Saint Seiya", "Cavaleiros do Zodíaco"
]

canonical_map = {}

def add_entry(title):
    t = title.strip()
    if not t or len(t) < 3: return
    t = re.sub(r'[\:\-\s]+$', '', t)
    key = normalize_key(t)
    if not key or len(key) < 3: return
    
    if key not in canonical_map:
        canonical_map[key] = t
    else:
        existing = canonical_map[key]
        if len(t) < len(existing) and not t.isupper():
            canonical_map[key] = t

# Process quiz songs
for s in songs:
    extracted = extract_canonical_names(s["anime"])
    for name in extracted:
        add_entry(name)

# Process scenes
for sc in scenes:
    extracted = extract_canonical_names(sc["anime"])
    for name in extracted:
        add_entry(name)

# Process famous franchises
for f in famous_franchises:
    add_entry(f)

# Sort alphabetically by display title
clean_list = sorted(list(canonical_map.values()), key=lambda x: x.lower())

with open(OUT_PATH, "w", encoding="utf-8") as f:
    json.dump(clean_list, f, ensure_ascii=False, indent=2)

print(f"SUCESSO: Gerada base limpa e sem duplicatas com {len(clean_list)} animes unicos!")
