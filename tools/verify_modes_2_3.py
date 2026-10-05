# -*- coding: utf-8 -*-
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Mode 2 Assertions
assert 'id="mode2-view"' in html, 'mode2-view missing'
assert 'class="target-anime-banner"' in html, 'target-anime-banner missing'
assert 'id="m2-target-poster"' in html, 'm2-target-poster missing'
assert 'id="m2-target-name"' in html, 'm2-target-name missing'
assert 'id="m2-target-meta"' in html, 'm2-target-meta missing'
assert 'id="m2-player-container"' in html, 'm2-player-container missing'
assert 'id="m2-spectrum-canvas"' in html, 'm2-spectrum-canvas missing'
assert 'id="m2-vinyl-icon"' in html, 'm2-vinyl-icon missing'
assert 'icons/vinyl.png' in html, 'vinyl icon image missing'
assert 'id="m2-revealed-content"' in html, 'm2-revealed-content missing'
assert 'id="m2-reveal-thumb-img"' in html, 'm2-reveal-thumb-img missing'
assert 'id="m2-reveal-badge"' in html, 'm2-reveal-badge missing'
assert 'id="m2-card-0"' in html, 'm2-card-0 missing'
assert 'id="m2-card-1"' in html, 'm2-card-1 missing'
assert 'id="m2-card-2"' in html, 'm2-card-2 missing'
assert 'id="m2-btn-confirm"' in html, 'm2-btn-confirm missing'
assert 'id="m2-btn-next"' in html, 'm2-btn-next missing'
assert 'id="m2-feedback-banner"' in html, 'm2-feedback-banner missing'

# 2. Mode 3 Assertions
assert 'id="mode3-view"' in html, 'mode3-view missing'
assert 'id="m3-scene-viewport"' in html, 'm3-scene-viewport missing'
assert 'id="m3-scene-img"' in html, 'm3-scene-img missing'
assert 'openLightbox()' in html, 'openLightbox missing'
assert 'id="m3-tags-row"' in html, 'm3-tags-row missing'
assert 'm3RevealNextHint()' in html, 'm3RevealNextHint missing'
assert 'id="m3-input"' in html, 'm3-input missing'
assert 'id="m3-autocomplete"' in html, 'm3-autocomplete missing'
assert 'id="m3-result-slot"' in html, 'm3-result-slot missing'
assert 'id="m3-feedback-box"' in html, 'm3-feedback-box missing'
assert 'id="m3-answer-box"' in html, 'm3-answer-box missing'
assert 'id="m3-ans-poster"' in html, 'm3-ans-poster missing'
assert 'id="m3-ans-title"' in html, 'm3-ans-title missing'
assert 'm3GiveUp()' in html, 'm3GiveUp missing'
assert 'm3NextScene()' in html, 'm3NextScene missing'

# 3. CSS Layout Assertions
assert '.target-anime-banner' in html, 'CSS .target-anime-banner missing'
assert '.m2-player-container' in html, 'CSS .m2-player-container missing'
assert '.scene-viewport' in html, 'CSS .scene-viewport missing'
assert '.m3-result-slot' in html, 'CSS .m3-result-slot missing'

print("PARABÉNS! Todas as verificações de Layout Bento Grid Modo 2 e Modo 3 passaram 100%!")
