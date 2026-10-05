import os
import sys

GEN_PATH = "C:/Users/luizd/.gemini/antigravity/scratch/anime-music-quiz/tools/generate_full_html.py"

with open(GEN_PATH, "r", encoding="utf-8") as f:
    code = f.read()

# 1. Update title version
code = code.replace("v2.3.0", "v2.4.0")

# 2. Add Shake & Pulse CSS
old_css_target = """.quiz-input:focus {
      border-color: var(--accent);
      box-shadow: 0 0 15px var(--accent-glow);
    }"""

new_css = """.quiz-input:focus {
      border-color: var(--accent);
      box-shadow: 0 0 15px var(--accent-glow);
    }

    @keyframes shakeError {
      0%, 100% { transform: translateX(0); }
      20%, 60% { transform: translateX(-8px); }
      40%, 80% { transform: translateX(8px); }
    }

    .input-error-shake {
      animation: shakeError 0.4s ease-in-out !important;
      border-color: #ef4444 !important;
      box-shadow: 0 0 18px rgba(239, 68, 68, 0.5) !important;
    }

    @keyframes pulseSuccess {
      0% { transform: scale(1); }
      50% { transform: scale(1.02); }
      100% { transform: scale(1); }
    }

    .input-success-pulse {
      animation: pulseSuccess 0.4s ease-in-out !important;
      border-color: #10b981 !important;
      box-shadow: 0 0 18px rgba(16, 185, 129, 0.5) !important;
    }"""

if old_css_target not in code:
    print("ERRO: old_css_target nao encontrado!")
    sys.exit(1)

code = code.replace(old_css_target, new_css, 1)

# 3. Add Web Audio API SFX synthesizer before matching logic
sfx_and_variants_code = """// Web Audio API Synthesizer (SFX Sensitivo Instantâneo)
function playSfx(type) {
  try {
    const AudioContext = window.AudioContext || window.webkitAudioContext;
    if (!AudioContext) return;
    if (!window._sfxCtx) window._sfxCtx = new AudioContext();
    const ctx = window._sfxCtx;
    if (ctx.state === 'suspended') ctx.resume();

    const vol = (typeof masterVolume !== 'undefined' ? masterVolume : 0.8) * 0.25;
    if (typeof isMuted !== 'undefined' && isMuted) return;
    if (vol <= 0.001) return;

    if (type === 'correct') {
      [523.25, 659.25, 783.99].forEach((freq, idx) => {
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(freq, ctx.currentTime + idx * 0.08);
        gain.gain.setValueAtTime(vol, ctx.currentTime + idx * 0.08);
        gain.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + idx * 0.08 + 0.28);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start(ctx.currentTime + idx * 0.08);
        osc.stop(ctx.currentTime + idx * 0.08 + 0.3);
      });
    } else if (type === 'wrong') {
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.type = 'triangle';
      osc.frequency.setValueAtTime(160, ctx.currentTime);
      osc.frequency.exponentialRampToValueAtTime(90, ctx.currentTime + 0.22);
      gain.gain.setValueAtTime(vol * 1.2, ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + 0.25);
      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.start(ctx.currentTime);
      osc.stop(ctx.currentTime + 0.26);
    }
  } catch (e) {
    // AudioContext blocked or not supported
  }
}

function getAcceptedVariants(title, synonyms = []) {
  const set = new Set();
  function add(s) {
    if (!s) return;
    const n = normalizeString(s);
    if (n && n.length >= 2) set.add(n);
  }
  if (!title) return [];
  add(title);

  // 1. Text in parentheses: "Attack on Titan (Shingeki no Kyojin)" -> "Shingeki no Kyojin"
  const parens = title.match(/\\((.*?)\\)/g);
  if (parens) {
    parens.forEach(p => add(p.replace(/[()]/g, '')));
  }

  // 2. Text without parentheses: "Attack on Titan (Shingeki no Kyojin)" -> "Attack on Titan"
  const noParen = title.replace(/\\(.*?\\)/g, '').trim();
  add(noParen);

  // 3. Subtitles before separators: ":", " - ", " – ", ";", " / "
  // "Bleach: Thousand-Year Blood War" -> "Bleach"
  const seps = [':', ' - ', ' – ', ' — ', ';', ' / '];
  seps.forEach(sep => {
    if (noParen.includes(sep)) {
      const pre = noParen.split(sep)[0].trim();
      if (pre.length >= 3) add(pre);
    }
  });

  // 4. Strip season / part / movie / edition suffixes
  const seasonPatterns = [
    /\\bseason\\s*\\d+\\b.*/gi,
    /\\b\\d+(st|nd|rd|th)\\s*season\\b.*/gi,
    /\\bfinal\\s*season(\\s*pt\\s*\\d+)?\\b.*/gi,
    /\\bpart\\s*\\d+\\b.*/gi,
    /\\bpt\\s*\\d+\\b.*/gi,
    /\\bthe\\s*animation\\b.*/gi,
    /\\bthe\\s*movie\\b.*/gi,
    /\\bmovie\\b.*/gi,
    /\\b(ii|iii|iv|v|vi)\\b.*/gi,
    /\\b(born|hero|new)\\b.*/gi,
    /\\b(shou|ten|ketsu)\\b.*/gi,
    /\\baragoto\\b.*/gi,
    /\\b2nd\\b.*/gi,
    /\\b3rd\\b.*/gi,
    /\\b\\d+$/g
  ];
  let baseClean = noParen;
  seasonPatterns.forEach(pat => {
    baseClean = baseClean.replace(pat, '').trim();
  });
  if (baseClean.length >= 3) add(baseClean);

  // 5. Synonyms
  (synonyms || []).forEach(syn => add(syn));

  return Array.from(set);
}

function checkAnimeMatch(guess, canonical, synonyms) {
  const cleanGuess = normalizeString(guess);
  if (!cleanGuess || cleanGuess.length < 2) {
    return { match: false, distance: 99 };
  }

  const variants = getAcceptedVariants(canonical, synonyms);
  let minDistance = 999;

  for (const v of variants) {
    // Exact normalized match
    if (cleanGuess === v) {
      return { match: true, distance: 0 };
    }

    // Prefix match (se guess tem >= 3 letras e eh prefixo do titulo, ex: "bleach" para "bleach thousand year blood war", "attack on titan" para "attack on titan season 2")
    if (cleanGuess.length >= 3 && v.startsWith(cleanGuess + ' ')) {
      return { match: true, distance: 0 };
    }
    if (v.length >= 3 && cleanGuess.startsWith(v + ' ')) {
      return { match: true, distance: 0 };
    }

    const dist = levenshtein(cleanGuess, v);
    if (dist < minDistance) minDistance = dist;
  }

  // Tolerancia para pequenos erros de digitacao (typos):
  // 5 a 8 letras: tolera 1 erro
  // 9+ letras: tolera ate 2 erros
  if (cleanGuess.length >= 5 && minDistance <= 1) {
    return { match: true, distance: minDistance };
  }
  if (cleanGuess.length >= 9 && minDistance <= 2) {
    return { match: true, distance: minDistance };
  }

  return { match: false, distance: minDistance };
}"""

old_check_target = """function checkAnimeMatch(guess, canonical, synonyms) {
  const cleanGuess = normalizeString(guess);
  if (!cleanGuess || cleanGuess.length < 2) {
    return { match: false, distance: 99 };
  }

  const targets = [canonical, ...(synonyms || [])];
  let minDistance = 999;

  for (const t of targets) {
    const cleanTarget = normalizeString(t);
    if (!cleanTarget) continue;

    // Exact match
    if (cleanGuess === cleanTarget) {
      return { match: true, distance: 0 };
    }

    const dist = levenshtein(cleanGuess, cleanTarget);
    if (dist < minDistance) minDistance = dist;
  }

  // Tolerância Levenshtein estrita para evitar que "k" ou "fate" acerte tudo:
  // - Palavras com 6 a 9 letras: tolera no máximo 1 letra errada.
  // - Palavras com 10 ou mais letras: tolera no máximo 2 letras erradas.
  if (cleanGuess.length >= 6 && minDistance <= 1) {
    return { match: true, distance: minDistance };
  }
  if (cleanGuess.length >= 10 && minDistance <= 2) {
    return { match: true, distance: minDistance };
  }

  return { match: false, distance: minDistance };
}"""

if old_check_target not in code:
    print("ERRO: old_check_target nao encontrado!")
    sys.exit(1)

code = code.replace(old_check_target, sfx_and_variants_code, 1)

# 4. Update submitGuess (Mode 1)
old_submit_guess = """function submitGuess() {
  if (m1AnsweredCurrent) return;
  const val = guessInput.value.trim();
  if (!val) return;

  m1Attempts++;
  const song = ALL_SONGS[m1CurrentIndex];
  const result = checkAnimeMatch(val, song.anime, song.synonyms);

  if (result.match) {
    const points = Math.max(20, 100 - (m1RevealedTagsCount * 10) - ((m1Attempts - 1) * 15));
    m1Score += points;
    m1CorrectCount++;
    m1Streak++;

    feedbackBox.className = 'feedback-box correct';
    feedbackBox.innerHTML = `🎉 <strong>VOCÊ ACERTOU! (+${points} pts)</strong> É <strong>${song.anime}</strong>!`;
    kpiScore.textContent = m1Score;
    kpiCorrect.textContent = m1CorrectCount;
    kpiStreak.textContent = `🔥 x${m1Streak}`;

    revealM1Answer(true);
  } else {
    m1Streak = 0;
    kpiStreak.textContent = '0';
    if (result.distance <= 4) {
      feedbackBox.className = 'feedback-box partial';
      feedbackBox.innerHTML = `⚠️ <strong>MUITO PERTO!</strong> Faltou pouco (diferença de apenas ${result.distance} letras). Escolha a opção exata na lista abaixo!`;
    } else {
      feedbackBox.className = 'feedback-box wrong';
      feedbackBox.innerHTML = `❌ <strong>Incorreto!</strong> (Tentativa ${m1Attempts}). Escolha ou digite o anime específico na lista de sugestões.`;
    }
  }
}"""

new_submit_guess = """function submitGuess() {
  if (m1AnsweredCurrent) return;
  const val = guessInput.value.trim();
  if (!val) return;

  m1Attempts++;
  const song = ALL_SONGS[m1CurrentIndex];
  const result = checkAnimeMatch(val, song.anime, song.synonyms);

  feedbackBox.style.display = 'block';

  if (result.match) {
    const points = Math.max(20, 100 - (m1RevealedTagsCount * 10) - ((m1Attempts - 1) * 15));
    m1Score += points;
    m1CorrectCount++;
    m1Streak++;

    guessInput.classList.remove('input-error-shake');
    guessInput.classList.add('input-success-pulse');
    playSfx('correct');

    feedbackBox.className = 'feedback-box correct';
    feedbackBox.innerHTML = `🎉 <strong>VOCÊ ACERTOU! (+${points} pts)</strong> É <strong>${song.anime}</strong>!`;
    kpiScore.textContent = m1Score;
    kpiCorrect.textContent = m1CorrectCount;
    kpiStreak.textContent = `🔥 x${m1Streak}`;

    revealM1Answer(true);
  } else {
    m1Streak = 0;
    kpiStreak.textContent = '0';

    guessInput.classList.remove('input-error-shake');
    void guessInput.offsetWidth;
    guessInput.classList.add('input-error-shake');
    guessInput.select();
    playSfx('wrong');

    if (result.distance <= 4) {
      feedbackBox.className = 'feedback-box partial';
      feedbackBox.innerHTML = `⚠️ <strong>MUITO PERTO!</strong> Faltou pouco (diferença de apenas ${result.distance} letras). Escolha a opção exata na lista abaixo!`;
    } else {
      feedbackBox.className = 'feedback-box wrong';
      feedbackBox.innerHTML = `❌ <strong>Incorreto!</strong> (Tentativa ${m1Attempts}). Não é esse anime. Use as dicas ou selecione na lista abaixo.`;
    }
  }
}"""

if old_submit_guess not in code:
    print("ERRO: old_submit_guess nao encontrado!")
    sys.exit(1)

code = code.replace(old_submit_guess, new_submit_guess, 1)

# 5. Update m3SubmitGuess (Mode 3)
old_m3_submit_guess = """function m3SubmitGuess() {
  if (m3Answered) return;
  const val = m3Input.value.trim();
  if (!val) return;

  const scene = ALL_SCENES[m3CurrentIndex];
  const res = checkAnimeMatch(val, scene.anime, scene.synonyms);

  if (res.match) {
    m3Streak++;
    m3CorrectCount++;
    const pts = Math.max(25, 100 - (m3HintsRevealed * 15) + (m3Streak > 1 ? (m3Streak - 1) * 20 : 0));
    m3Score += pts;

    m3FeedbackBox.className = 'feedback-box correct';
    m3FeedbackBox.innerHTML = `🎉 <strong>ACERTOU A CENA! (+${pts} pts)</strong> É do anime <strong>${scene.anime}</strong>!`;
    kpiScore.textContent = m3Score;
    kpiCorrect.textContent = m3CorrectCount;
    kpiStreak.textContent = `🔥 x${m3Streak}`;

    m3RevealSceneAnswer(true);
  } else {
    m3Streak = 0;
    kpiStreak.textContent = '0';
    if (res.distance <= 4) {
      m3FeedbackBox.className = 'feedback-box partial';
      m3FeedbackBox.innerHTML = `⚠️ <strong>QUASE LÁ!</strong> Faltou muito pouco (erro de ${res.distance} letras). Escolha a opção correta na lista de sugestões!`;
    } else {
      m3FeedbackBox.className = 'feedback-box wrong';
      m3FeedbackBox.innerHTML = `❌ <strong>Incorreto!</strong> Não é esse anime. Use os botões de dicas ou selecione na lista de sugestões abaixo.`;
    }
  }
}"""

new_m3_submit_guess = """function m3SubmitGuess() {
  if (m3Answered) return;
  const val = m3Input.value.trim();
  if (!val) return;

  const scene = ALL_SCENES[m3CurrentIndex];
  const res = checkAnimeMatch(val, scene.anime, scene.synonyms);

  m3FeedbackBox.style.display = 'block';

  if (res.match) {
    m3Streak++;
    m3CorrectCount++;
    const pts = Math.max(25, 100 - (m3HintsRevealed * 15) + (m3Streak > 1 ? (m3Streak - 1) * 20 : 0));
    m3Score += pts;

    m3Input.classList.remove('input-error-shake');
    m3Input.classList.add('input-success-pulse');
    playSfx('correct');

    m3FeedbackBox.className = 'feedback-box correct';
    m3FeedbackBox.innerHTML = `🎉 <strong>ACERTOU A CENA! (+${pts} pts)</strong> É do anime <strong>${scene.anime}</strong>!`;
    kpiScore.textContent = m3Score;
    kpiCorrect.textContent = m3CorrectCount;
    kpiStreak.textContent = `🔥 x${m3Streak}`;

    m3RevealSceneAnswer(true);
  } else {
    m3Streak = 0;
    kpiStreak.textContent = '0';

    m3Input.classList.remove('input-error-shake');
    void m3Input.offsetWidth;
    m3Input.classList.add('input-error-shake');
    m3Input.select();
    playSfx('wrong');

    if (res.distance <= 4) {
      m3FeedbackBox.className = 'feedback-box partial';
      m3FeedbackBox.innerHTML = `⚠️ <strong>QUASE LÁ!</strong> Faltou muito pouco (erro de ${res.distance} letras). Escolha a opção correta na lista de sugestões!`;
    } else {
      m3FeedbackBox.className = 'feedback-box wrong';
      m3FeedbackBox.innerHTML = `❌ <strong>Incorreto!</strong> Não é esse anime. Use os botões de dicas ou selecione na lista de sugestões abaixo.`;
    }
  }
}"""

if old_m3_submit_guess not in code:
    print("ERRO: old_m3_submit_guess nao encontrado!")
    sys.exit(1)

code = code.replace(old_m3_submit_guess, new_m3_submit_guess, 1)

# 6. Reset classes in m1LoadSong and m3InitScene
old_m1_reset = """  guessInput.value = '';
  guessInput.disabled = false;"""

new_m1_reset = """  guessInput.value = '';
  guessInput.disabled = false;
  guessInput.classList.remove('input-error-shake', 'input-success-pulse');"""

code = code.replace(old_m1_reset, new_m1_reset, 1)

old_m3_reset = """  m3Input.value = '';
  m3Input.disabled = false;"""

new_m3_reset = """  m3Input.value = '';
  m3Input.disabled = false;
  m3Input.classList.remove('input-error-shake', 'input-success-pulse');"""

code = code.replace(old_m3_reset, new_m3_reset, 1)

# 7. Add SFX to Mode 2 confirm
old_m2_sfx = """    m2FeedbackBanner.className = 'feedback-banner correct';"""
new_m2_sfx = """    playSfx('correct');
    m2FeedbackBanner.className = 'feedback-banner correct';"""
code = code.replace(old_m2_sfx, new_m2_sfx, 1)

old_m2_wrong_sfx = """    m2FeedbackBanner.className = 'feedback-banner wrong';"""
new_m2_wrong_sfx = """    playSfx('wrong');
    m2FeedbackBanner.className = 'feedback-banner wrong';"""
code = code.replace(old_m2_wrong_sfx, new_m2_wrong_sfx, 1)

# 8. Switch video to MP3 playback
code = code.replace("localVideoPlayer.src = `audio/${song.id}.mp4`;", "localVideoPlayer.src = `audio/${song.id}.mp3`;")
code = code.replace("m2LocalVideo.src = `audio/${song.id}.mp4`;", "m2LocalVideo.src = `audio/${song.id}.mp3`;")
code = code.replace("m2LocalVideo.src = `audio/${correctSong.id}.mp4`;", "m2LocalVideo.src = `audio/${correctSong.id}.mp3`;")

with open(GEN_PATH, "w", encoding="utf-8") as f:
    f.write(code)

print("SUCESSO: generate_full_html.py atualizado com sucesso!")
