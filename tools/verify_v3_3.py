import json

songs = json.load(open('anime_songs_verified.json', encoding='utf-8'))
s4 = [s for s in songs if s['id'] == 4][0]
s98 = [s for s in songs if s['id'] == 98][0]
auto = json.load(open('tools/anime_autocomplete_db.json', encoding='utf-8'))

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

assert s4['video_id'] == 'y9B_cgqM-kA', 'Song 4 video_id error'
assert 'dungeon ni deai' in s98['synonyms'], 'Danmachi synonym missing'
assert 'Dungeon ni Deai' in auto, 'Autocomplete missing'
assert 'm1-bottom-controls-bar' in html, 'Controls bar missing'
assert 'm1-media-ctrl-card' in html, 'Media ctrl card missing'
assert 'm1-nav-ctrl-card' in html, 'Nav ctrl card missing'
assert 'id="btn-play-pause"' in html, 'Play pause btn missing'
assert 'id="btn-restart"' in html, 'Restart btn missing'
assert 'id="btn-random"' in html, 'Random btn missing'
assert 'id="m1-btn-prev"' in html, 'Prev btn missing'
assert 'id="m1-btn-reveal"' in html, 'Reveal btn missing'
assert 'id="m1-btn-next"' in html, 'Next btn missing'
assert 'id="m1-result-slot"' in html, 'Result slot missing'
assert '.icon-neon-cyan' in html, 'Icon neon cyan missing'
assert 'getSongAudioSrc' in html, 'getSongAudioSrc missing'

print('ALL 15 TARGETED VERIFICATIONS PASSED 100%!')
