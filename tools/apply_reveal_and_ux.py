import os
import sys

GEN_PATH = "C:/Users/luizd/.gemini/antigravity/scratch/anime-music-quiz/tools/generate_full_html.py"

with open(GEN_PATH, "r", encoding="utf-8") as f:
    code = f.read()

# 1. Bump version
code = code.replace("v2.4.0", "v2.5.0")

# 2. Add Visual Reveal Card CSS
old_css_player = """.player-container {
      position: relative;
      width: 100%;
      aspect-ratio: 16 / 9;
      max-height: 280px;
      background: #080b16;
      border-radius: 14px;
      overflow: hidden;
      border: 2px solid var(--card-border);
      margin-bottom: 20px;
      box-shadow: 0 8px 24px rgba(0,0,0,0.5);
    }

    .player-container iframe,
    .player-container video {
      width: 100%;
      height: 100%;
      border: none;
      object-fit: contain;
      background: #000;
    }

    .blind-mask {
      position: absolute;
      top: 0; left: 0; right: 0; bottom: 0;
      background: radial-gradient(circle at center, #1e2444 0%, #080b16 85%);
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      z-index: 5;
      transition: opacity 0.4s ease, visibility 0.4s;
    }

    .blind-mask.unmasked {
      opacity: 0;
      visibility: hidden;
      pointer-events: none;
    }"""

new_css_player = """.player-container {
      position: relative;
      width: 100%;
      aspect-ratio: 16 / 9;
      max-height: 280px;
      background: #080b16;
      border-radius: 14px;
      overflow: hidden;
      border: 2px solid var(--card-border);
      margin-bottom: 20px;
      box-shadow: 0 8px 24px rgba(0,0,0,0.5);
    }

    .player-visual-card {
      position: absolute;
      inset: 0;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      overflow: hidden;
    }

    .player-bg-art {
      position: absolute;
      inset: 0;
      background-size: cover;
      background-position: center;
      opacity: 0;
      transform: scale(1.08);
      transition: opacity 0.6s ease, transform 0.6s ease;
      filter: blur(2px) brightness(0.38);
    }

    .player-visual-card.is-revealed .player-bg-art {
      opacity: 1;
      transform: scale(1);
    }

    .player-scrim {
      position: absolute;
      inset: 0;
      background: radial-gradient(circle at center, rgba(15, 20, 36, 0.4) 0%, rgba(7, 9, 19, 0.88) 100%);
      pointer-events: none;
    }

    .player-blind-content {
      position: relative;
      z-index: 2;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      text-align: center;
      padding: 16px;
    }

    .player-revealed-content {
      position: relative;
      z-index: 2;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      text-align: center;
      padding: 16px 20px;
      animation: fadeIn 0.4s ease;
      width: 100%;
    }

    .revealed-hero-row {
      display: flex;
      align-items: center;
      gap: 16px;
      max-width: 550px;
      text-align: left;
    }

    .revealed-thumb-img {
      width: 68px;
      height: 96px;
      object-fit: cover;
      border-radius: 8px;
      border: 2px solid var(--accent);
      box-shadow: 0 4px 18px rgba(99, 102, 241, 0.45);
      flex-shrink: 0;
    }

    .revealed-info-col {
      display: flex;
      flex-direction: column;
      gap: 3px;
      min-width: 0;
    }

    .revealed-badge {
      font-size: 11px;
      font-weight: 800;
      color: #34d399;
      letter-spacing: 0.5px;
      text-transform: uppercase;
    }

    .revealed-badge.wrong {
      color: #f87171;
    }

    .revealed-anime-title {
      font-size: 20px;
      font-weight: 800;
      color: #ffffff;
      line-height: 1.2;
      text-shadow: 0 2px 10px rgba(0,0,0,0.8);
    }

    .revealed-song-name {
      font-size: 15px;
      font-weight: 700;
      color: #a5b4fc;
    }

    .revealed-artist-meta {
      font-size: 12px;
      color: #cbd5e1;
    }

    .player-container iframe,
    .player-container video {
      display: none !important;
    }

    .blind-mask {
      display: none;
    }"""

if old_css_player not in code:
    print("ERRO: old_css_player nao encontrado!")
    sys.exit(1)

code = code.replace(old_css_player, new_css_player, 1)

# 3. Update Mode 1 Player Markup
old_html_player = """      <div style="display: flex; gap: 8px;">
        <button class="btn btn-outline" style="padding: 6px 12px; font-size: 12px;" onclick="m1ToggleMask()">
          <span id="mask-toggle-icon">🙈</span> <span id="mask-toggle-text">Ocultar Vídeo</span>
        </button>
        <button class="btn btn-outline" style="padding: 6px 12px; font-size: 12px;" onclick="openYouTubeDirect()">
          ▶️ Abrir YouTube
        </button>
      </div>
    </div>

    <!-- Mode 1 Player -->
    <div class="player-container">
      <video id="local-video-player" playsinline preload="metadata" style="display: none;"></video>
      <iframe id="video-frame" allow="autoplay; encrypted-media"></iframe>
      <div class="blind-mask" id="blind-mask">
        <div class="vinyl" id="vinyl-icon">🎵</div>
        <div class="sound-bars" id="sound-bars">
          <div class="bar"></div><div class="bar"></div><div class="bar"></div><div class="bar"></div><div class="bar"></div>
        </div>
        <div style="margin-top: 12px; font-size: 13px; color: #94a3b8;" id="mask-status-text">
          🎧 Modo Blind Test Ativo (Vídeo Ocultado)
        </div>
      </div>
    </div>"""

new_html_player = """      <div style="display: flex; gap: 8px;">
        <button class="btn btn-outline" style="padding: 6px 12px; font-size: 12px;" onclick="openYouTubeDirect()">
          ▶️ Clipe no YouTube
        </button>
      </div>
    </div>

    <!-- Mode 1 Player (Capa e Nome Revelados sem tela preta!) -->
    <div class="player-container" id="m1-player-container">
      <audio id="local-video-player" preload="auto" style="display: none;"></audio>
      <iframe id="video-frame" allow="autoplay; encrypted-media" style="display: none;"></iframe>
      <div class="player-visual-card" id="player-visual-card">
        <div class="player-bg-art" id="player-bg-art"></div>
        <div class="player-scrim"></div>

        <!-- Blind Guessing View -->
        <div class="player-blind-content" id="player-blind-content">
          <div class="vinyl" id="vinyl-icon">🎵</div>
          <div class="sound-bars" id="sound-bars">
            <div class="bar"></div><div class="bar"></div><div class="bar"></div><div class="bar"></div><div class="bar"></div>
          </div>
          <div style="margin-top: 12px; font-size: 13px; color: #94a3b8;" id="mask-status-text">
            🎧 Modo Blind Test Ativo • Ouça a música e adivinhe o anime!
          </div>
        </div>

        <!-- Revealed Answer View -->
        <div class="player-revealed-content" id="player-revealed-content" style="display: none;">
          <div class="revealed-hero-row">
            <img id="reveal-thumb-img" class="revealed-thumb-img" src="" alt="Capa" />
            <div class="revealed-info-col">
              <div class="revealed-badge" id="reveal-badge-status">🎉 RESPOSTA REVELADA</div>
              <div class="revealed-anime-title" id="reveal-anime-title">Nome do Anime</div>
              <div class="revealed-song-name" id="reveal-song-name">🎵 "Nome da Música"</div>
              <div class="revealed-artist-meta" id="reveal-artist-meta">por Artista (Ano) • ⭐ Dificuldade</div>
            </div>
          </div>
          <div class="sound-bars active" style="margin-top: 10px;">
            <div class="bar"></div><div class="bar"></div><div class="bar"></div><div class="bar"></div><div class="bar"></div>
          </div>
        </div>
      </div>
    </div>"""

if old_html_player not in code:
    print("ERRO: old_html_player nao encontrado!")
    sys.exit(1)

code = code.replace(old_html_player, new_html_player, 1)

# 4. Add TAB button badge hints
old_input_group = """    <!-- Input Box with Autocomplete -->
    <div class="input-group">
      <div class="autocomplete-wrapper">
        <input type="text" class="quiz-input" id="guess-input" placeholder="Comece a digitar o nome do anime..." autocomplete="off" />
        <div class="autocomplete-dropdown" id="guess-autocomplete"></div>
      </div>
      <button class="btn btn-green" onclick="submitGuess()">Enviar Palpite</button>
    </div>"""

new_input_group = """    <!-- Input Box with Autocomplete & TAB auto-submit -->
    <div class="input-group">
      <div class="autocomplete-wrapper">
        <input type="text" class="quiz-input" id="guess-input" placeholder="Digite o anime... (TAB para selecionar e enviar)" autocomplete="off" />
        <div class="autocomplete-dropdown" id="guess-autocomplete"></div>
      </div>
      <button class="btn btn-green" onclick="submitGuess()">
        <span>Enviar</span> <kbd style="background: rgba(0,0,0,0.35); border-radius: 4px; padding: 2px 6px; font-size: 11px; margin-left: 4px;">TAB ↵</kbd>
      </button>
    </div>"""

code = code.replace(old_input_group, new_input_group, 1)

old_m3_input_group = """    <!-- Input for Scene Guess with Autocomplete -->
    <div class="input-group">
      <div class="autocomplete-wrapper">
        <input type="text" class="quiz-input" id="m3-input" placeholder="Comece a digitar o nome do anime..." autocomplete="off" />
        <div class="autocomplete-dropdown" id="m3-autocomplete"></div>
      </div>
      <button class="btn btn-green" onclick="m3SubmitGuess()">Adivinhar</button>
    </div>"""

new_m3_input_group = """    <!-- Input for Scene Guess with Autocomplete & TAB auto-submit -->
    <div class="input-group">
      <div class="autocomplete-wrapper">
        <input type="text" class="quiz-input" id="m3-input" placeholder="Digite o anime... (TAB para selecionar e enviar)" autocomplete="off" />
        <div class="autocomplete-dropdown" id="m3-autocomplete"></div>
      </div>
      <button class="btn btn-green" onclick="m3SubmitGuess()">
        <span>Adivinhar</span> <kbd style="background: rgba(0,0,0,0.35); border-radius: 4px; padding: 2px 6px; font-size: 11px; margin-left: 4px;">TAB ↵</kbd>
      </button>
    </div>"""

code = code.replace(old_m3_input_group, new_m3_input_group, 1)

# 5. Add playKeyClick and Progressive Queue helpers
typing_sfx_code = """let lastKeyClickTime = 0;
function playKeyClick() {
  const now = performance.now();
  if (now - lastKeyClickTime < 35) return;
  lastKeyClickTime = now;
  try {
    const AudioContext = window.AudioContext || window.webkitAudioContext;
    if (!AudioContext) return;
    if (!window._sfxCtx) window._sfxCtx = new AudioContext();
    const ctx = window._sfxCtx;
    if (ctx.state === 'suspended') ctx.resume();

    const vol = (typeof masterVolume !== 'undefined' ? masterVolume : 0.8) * 0.12;
    if (typeof isMuted !== 'undefined' && isMuted) return;
    if (vol <= 0.001) return;

    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    const pitch = 1500 + (Math.random() * 400 - 200);
    osc.type = 'triangle';
    osc.frequency.setValueAtTime(pitch, ctx.currentTime);
    osc.frequency.exponentialRampToValueAtTime(300, ctx.currentTime + 0.022);

    gain.gain.setValueAtTime(vol, ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + 0.022);

    osc.connect(gain);
    gain.connect(ctx.destination);
    osc.start(ctx.currentTime);
    osc.stop(ctx.currentTime + 0.025);
  } catch (e) {}
}

function getDifficultyRank(item) {
  const norm = normalizeString(item.diff || item.hint || '');
  if (norm.includes('facil')) return 1;
  if (norm.includes('medio') || norm.includes('media')) return 2;
  return 3;
}

function buildProgressiveQueue(items) {
  const easy = items.filter(it => getDifficultyRank(it) === 1);
  const med = items.filter(it => getDifficultyRank(it) === 2);
  const hard = items.filter(it => getDifficultyRank(it) === 3);

  // Embaralhar aleatoriamente cada grupo individual
  easy.sort(() => Math.random() - 0.5);
  med.sort(() => Math.random() - 0.5);
  hard.sort(() => Math.random() - 0.5);

  return [...easy, ...med, ...hard];
}
"""

if "function playSfx(type) {" not in code:
    print("ERRO: playSfx nao encontrado!")
    sys.exit(1)

code = code.replace("function playSfx(type) {", typing_sfx_code + "\nfunction playSfx(type) {", 1)

# 6. Update setupAutocomplete with Typing sound & Tab auto-submit
old_autocomplete_keydown = """  inputEl.addEventListener('keydown', (e) => {
    const items = dropdownEl.querySelectorAll('.autocomplete-item');
    if (dropdownEl.style.display === 'block' && items.length > 0) {
      if (e.key === 'ArrowDown') {
        e.preventDefault();
        activeIndex = (activeIndex + 1) % items.length;
        items.forEach((it, i) => it.classList.toggle('active', i === activeIndex));
        items[activeIndex].scrollIntoView({ block: 'nearest' });
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        activeIndex = (activeIndex - 1 + items.length) % items.length;
        items.forEach((it, i) => it.classList.toggle('active', i === activeIndex));
        items[activeIndex].scrollIntoView({ block: 'nearest' });
      } else if (e.key === 'Enter') {
        if (activeIndex >= 0 && items[activeIndex]) {
          e.preventDefault();
          inputEl.value = items[activeIndex].textContent.trim();
          closeDropdown();
          if (onSelectSubmit) onSelectSubmit();
          return;
        }
      } else if (e.key === 'Escape') {
        closeDropdown();
      }
    }
    
    if (e.key === 'Enter' && (!dropdownEl.style.display || dropdownEl.style.display === 'none')) {
      if (onSelectSubmit) onSelectSubmit();
    }
  });"""

new_autocomplete_keydown = """  inputEl.addEventListener('keydown', (e) => {
    // Barulhinho sutil de digitar (teclado mecânico)
    if (e.key.length === 1 || e.key === 'Backspace' || e.key === 'Delete') {
      playKeyClick();
    }

    const items = dropdownEl.querySelectorAll('.autocomplete-item');
    const isDropdownOpen = dropdownEl.style.display === 'block' && items.length > 0;

    // TAB: Preenche automaticamente a 1ª opção mais próxima e já envia o palpite instantaneamente!
    if (e.key === 'Tab') {
      e.preventDefault();
      if (isDropdownOpen) {
        const chosen = (activeIndex >= 0 && items[activeIndex]) ? items[activeIndex] : items[0];
        inputEl.value = chosen.textContent.trim();
        closeDropdown();
        if (onSelectSubmit) onSelectSubmit();
        return;
      } else if (inputEl.value.trim().length > 0) {
        if (onSelectSubmit) onSelectSubmit();
        return;
      }
    }

    if (isDropdownOpen) {
      if (e.key === 'ArrowDown') {
        e.preventDefault();
        activeIndex = (activeIndex + 1) % items.length;
        items.forEach((it, i) => it.classList.toggle('active', i === activeIndex));
        items[activeIndex].scrollIntoView({ block: 'nearest' });
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        activeIndex = (activeIndex - 1 + items.length) % items.length;
        items.forEach((it, i) => it.classList.toggle('active', i === activeIndex));
        items[activeIndex].scrollIntoView({ block: 'nearest' });
      } else if (e.key === 'Enter') {
        e.preventDefault();
        const chosen = (activeIndex >= 0 && items[activeIndex]) ? items[activeIndex] : items[0];
        inputEl.value = chosen.textContent.trim();
        closeDropdown();
        if (onSelectSubmit) onSelectSubmit();
        return;
      } else if (e.key === 'Escape') {
        closeDropdown();
      }
    }
    
    if (e.key === 'Enter' && (!dropdownEl.style.display || dropdownEl.style.display === 'none')) {
      if (onSelectSubmit) onSelectSubmit();
    }
  });"""

if old_autocomplete_keydown not in code:
    print("ERRO: old_autocomplete_keydown nao encontrado!")
    sys.exit(1)

code = code.replace(old_autocomplete_keydown, new_autocomplete_keydown, 1)

# 7. Update Mode 1 State & Progressive Queue
code = code.replace("let m1CurrentIndex = 0;", "let m1CurrentIndex = 0;\nlet m1Playlist = [];\nlet m1PlaylistIndex = 0;")

old_m1_load = """function m1LoadSong(autoPlay = false) {
  stopAllMedia();
  m1AnsweredCurrent = false;
  m1Attempts = 0;
  m1RevealedTagsCount = 0;
  feedbackBox.style.display = 'none';
  feedbackBox.className = 'feedback-box';
  answerBox.style.display = 'none';
  guessInput.value = '';
  guessInput.disabled = false;
  guessInput.classList.remove('input-error-shake', 'input-success-pulse');

  const song = ALL_SONGS[m1CurrentIndex];
  m1RoundIndicator.textContent = `MÚSICA #${song.id} DE ${ALL_SONGS.length} • ${song.diff} (${song.year})`;
  kpiProgress.textContent = `${m1CurrentIndex + 1} / ${ALL_SONGS.length}`;

  blindMask.classList.remove('unmasked');
  soundBars.classList.remove('active');
  vinylIcon.classList.remove('spinning');"""

new_m1_load = """function m1LoadSong(autoPlay = false) {
  stopAllMedia();
  m1AnsweredCurrent = false;
  m1Attempts = 0;
  m1RevealedTagsCount = 0;
  feedbackBox.style.display = 'none';
  feedbackBox.className = 'feedback-box';
  answerBox.style.display = 'none';
  guessInput.value = '';
  guessInput.disabled = false;
  guessInput.classList.remove('input-error-shake', 'input-success-pulse');

  if (m1Playlist.length === 0) {
    m1Playlist = buildProgressiveQueue(ALL_SONGS);
  }
  const song = m1Playlist[m1PlaylistIndex] || ALL_SONGS[0];
  m1CurrentIndex = ALL_SONGS.findIndex(s => s.id === song.id);

  m1RoundIndicator.textContent = `MÚSICA #${m1PlaylistIndex + 1} DE ${m1Playlist.length} • ${song.diff} (${song.year})`;
  kpiProgress.textContent = `${m1PlaylistIndex + 1} / ${m1Playlist.length}`;

  // Reset visual reveal card to blind mode
  const visualCard = document.getElementById('player-visual-card');
  const bgArt = document.getElementById('player-bg-art');
  const blindContent = document.getElementById('player-blind-content');
  const revealedContent = document.getElementById('player-revealed-content');

  if (visualCard) visualCard.classList.remove('is-revealed');
  if (bgArt) bgArt.style.backgroundImage = 'none';
  if (blindContent) blindContent.style.display = 'flex';
  if (revealedContent) revealedContent.style.display = 'none';

  soundBars.classList.remove('active');
  vinylIcon.classList.remove('spinning');"""

if old_m1_load not in code:
    print("ERRO: old_m1_load nao encontrado!")
    sys.exit(1)

code = code.replace(old_m1_load, new_m1_load, 1)

# 8. Update revealM1Answer with image backdrop & text in front
old_reveal_m1 = """function revealM1Answer(isCorrect) {
  m1AnsweredCurrent = true;
  guessInput.disabled = true;
  blindMask.classList.add('unmasked');

  Array.from(tagsContainer.children).forEach(t => revealTagElement(t));

  const song = ALL_SONGS[m1CurrentIndex];
  answerBox.style.display = 'block';
  ansAnime.innerHTML = isCorrect ? `🎉 ${song.anime}` : `❌ Resposta: ${song.anime}`;
  ansMeta.textContent = `Abertura: "${song.song}" por ${song.artist} (${song.year}) • ${song.diff}`;
  ansSyns.textContent = `Nomes reconhecidos: ${(song.synonyms || []).slice(0, 5).join(' • ')}`;
  if (song.image_url) {
    ansPosterImg.src = song.image_url;
  }
}"""

new_reveal_m1 = """function revealM1Answer(isCorrect) {
  m1AnsweredCurrent = true;
  guessInput.disabled = true;

  const song = m1Playlist[m1PlaylistIndex] || ALL_SONGS[m1CurrentIndex];

  // Visual Card: Capa escura no fundo e nomes reluzentes na frente
  const visualCard = document.getElementById('player-visual-card');
  const bgArt = document.getElementById('player-bg-art');
  const blindContent = document.getElementById('player-blind-content');
  const revealedContent = document.getElementById('player-revealed-content');
  const revealThumb = document.getElementById('reveal-thumb-img');
  const revealBadge = document.getElementById('reveal-badge-status');
  const revealTitle = document.getElementById('reveal-anime-title');
  const revealSong = document.getElementById('reveal-song-name');
  const revealMeta = document.getElementById('reveal-artist-meta');

  if (song.image_url) {
    if (bgArt) bgArt.style.backgroundImage = `url('${song.image_url}')`;
    if (revealThumb) revealThumb.src = song.image_url;
  }
  if (revealBadge) {
    revealBadge.className = isCorrect ? 'revealed-badge' : 'revealed-badge wrong';
    revealBadge.textContent = isCorrect ? '🎉 VOCÊ ACERTOU!' : '❌ RESPOSTA REVELADA';
  }
  if (revealTitle) revealTitle.textContent = song.anime;
  if (revealSong) revealSong.textContent = `🎵 "${song.song}"`;
  if (revealMeta) revealMeta.textContent = `por ${song.artist} (${song.year}) • ${song.diff}`;

  if (blindContent) blindContent.style.display = 'none';
  if (revealedContent) revealedContent.style.display = 'flex';
  if (visualCard) visualCard.classList.add('is-revealed');

  Array.from(tagsContainer.children).forEach(t => revealTagElement(t));

  answerBox.style.display = 'block';
  ansAnime.innerHTML = isCorrect ? `🎉 ${song.anime}` : `❌ Resposta: ${song.anime}`;
  ansMeta.textContent = `Abertura: "${song.song}" por ${song.artist} (${song.year}) • ${song.diff}`;
  ansSyns.textContent = `Nomes reconhecidos: ${(song.synonyms || []).slice(0, 5).join(' • ')}`;
  if (song.image_url) {
    ansPosterImg.src = song.image_url;
  }
}"""

if old_reveal_m1 not in code:
    print("ERRO: old_reveal_m1 nao encontrado!")
    sys.exit(1)

code = code.replace(old_reveal_m1, new_reveal_m1, 1)

# 9. Update prev/next navigation to use m1PlaylistIndex
old_nav_m1 = """function prevSong() {
  stopAllMedia();
  if (m1CurrentIndex > 0) {
    m1CurrentIndex--;
    m1LoadSong(true);
  }
}

function nextSong() {
  stopAllMedia();
  if (m1CurrentIndex < ALL_SONGS.length - 1) {
    m1CurrentIndex++;
    m1LoadSong(true);
  }
}

function m1NextRandom() {
  stopAllMedia();
  m1CurrentIndex = Math.floor(Math.random() * ALL_SONGS.length);
  m1LoadSong(true);
}"""

new_nav_m1 = """function prevSong() {
  stopAllMedia();
  if (m1PlaylistIndex > 0) {
    m1PlaylistIndex--;
    m1LoadSong(true);
  }
}

function nextSong() {
  stopAllMedia();
  if (m1PlaylistIndex < m1Playlist.length - 1) {
    m1PlaylistIndex++;
    m1LoadSong(true);
  }
}

function m1NextRandom() {
  stopAllMedia();
  m1PlaylistIndex = Math.floor(Math.random() * m1Playlist.length);
  m1LoadSong(true);
}"""

if old_nav_m1 not in code:
    print("ERRO: old_nav_m1 nao encontrado!")
    sys.exit(1)

code = code.replace(old_nav_m1, new_nav_m1, 1)

# 10. Progressive Queue for Mode 3 (Scenes) and Mode 2
old_m3_start = """function m3StartGame() {
  stopAllMedia();
  m3UnplayedQueue = ALL_SCENES.map((_, i) => i);
  m3UnplayedQueue.sort(() => getGameRandom() - 0.5);
  m3RoundsPlayed = 0;
  m3NextScene();
}"""

new_m3_start = """function m3StartGame() {
  stopAllMedia();
  m3UnplayedQueue = buildProgressiveQueue(ALL_SCENES.map((_, i) => ALL_SCENES[i])).map(s => ALL_SCENES.findIndex(orig => orig.id === s.id));
  m3RoundsPlayed = 0;
  m3NextScene();
}"""

code = code.replace(old_m3_start, new_m3_start, 1)

with open(GEN_PATH, "w", encoding="utf-8") as f:
    f.write(code)

print("SUCESSO: apply_reveal_and_ux.py aplicou todas as alteracoes com sucesso!")
