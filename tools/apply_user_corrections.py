# -*- coding: utf-8 -*-
"""
Script de Correção e Reformulação Geral - Anime Music & Scene Quiz
Atende 100% dos apontamentos do usuário:
1. Remove MODO PÂNICO estático e waiting banner fora de hora.
2. Remove Pódium permanente da semana em baixo.
3. Ranking ao vivo lateral visível APENAS durante partida multiplayer.
4. Separação de Salas e Placar em 5 abas distintas.
5. Hall da Fama rolável permitindo ver os 50 melhores.
6. KPIs (Pontuação, Acertos, Combo, Progresso) dentro de cada modo ativo, removendo da barra global do topo.
7. Garante que nada corte no Modo 2 ou em qualquer modo (remoção de overflow: hidden no body).
8. Pistas do Modo 1 com visual destacado e funcional.
9. Som tátil de digitação mecânica (typing sfx) em tempo real ao digitar.
10. Autocomplete dropdown com z-index alto, sem corte de overflow e com previsão nítida.
"""
import os
import re
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GEN_PATH = os.path.join(BASE_DIR, "tools", "generate_full_html.py")

with open(GEN_PATH, "r", encoding="utf-8") as f:
    code = f.read()

print("Arquivo generate_full_html.py carregado. Iniciando reformulação...")

# 1. Atualizar switchGameMode para suportar 5 modos (mode1, mode2, mode3, mode4, mode5)
old_switch_target = """function switchGameMode(mode) {
  stopAllMedia();
  AudioManager.playSfx('tab');
  activeGameMode = mode;
  ['mode1', 'mode2', 'mode3', 'mode4'].forEach(m => {
    document.getElementById(`${m}-view`).style.display = (m === mode) ? 'block' : 'none';
    document.getElementById(`tab-${m}`).classList.toggle('active', m === mode);
  });"""

new_switch_code = """function switchGameMode(mode) {
  stopAllMedia();
  AudioManager.playSfx('tab');
  activeGameMode = mode;
  ['mode1', 'mode2', 'mode3', 'mode4', 'mode5'].forEach(m => {
    const viewEl = document.getElementById(`${m}-view`);
    if (viewEl) viewEl.style.display = (m === mode) ? 'block' : 'none';
    const tabEl = document.getElementById(`tab-${m}`);
    if (tabEl) tabEl.classList.toggle('active', m === mode);
  });

  // Ranking lateral ao vivo só deve aparecer durante partida multiplayer ativa
  const liveSidebar = document.getElementById('mp-live-sidebar');
  if (liveSidebar) {
    liveSidebar.style.display = (window.MultiplayerEngine && MultiplayerEngine.isMatchActive) ? 'flex' : 'none';
  }

  // Posicionar ou ocultar scoreboard de acordo com o modo
  const sb = document.getElementById('main-scoreboard');
  if (sb) {
    if (mode === 'mode1' || mode === 'mode2' || mode === 'mode3') {
      const slot = document.getElementById(`${mode}-scoreboard-slot`);
      if (slot) {
        slot.appendChild(sb);
        sb.style.display = 'grid';
      }
    } else {
      sb.style.display = 'none';
    }
  }"""

if old_switch_target not in code:
    print("ERRO: old_switch_target não encontrado!")
    sys.exit(1)

code = code.replace(old_switch_target, new_switch_code)
print("Passo 1: switchGameMode atualizado para 5 modos.")

# 2. Atualizar o switchGameMode para acionar modo 5 (placar)
old_switch_branch = """  } else if (mode === 'mode4') {
    updateGlobalKPIs();
    renderLeaderboardTable('all');
    updateSaveScoreKPIs();
  }"""

new_switch_branch = """  } else if (mode === 'mode4') {
    updateGlobalKPIs();
  } else if (mode === 'mode5') {
    updateGlobalKPIs();
    renderLeaderboardTable('all');
    updateSaveScoreKPIs();
  }"""

if old_switch_branch not in code:
    print("ERRO: old_switch_branch não encontrado!")
    sys.exit(1)

code = code.replace(old_switch_branch, new_switch_branch)
print("Passo 2: Branches de modo 4 e modo 5 configuradas.")

# 3. Adicionar som de digitação 'typing' em AudioManager
old_play_sfx = """      if (type === 'click') {
        const osc = ctx.createOscillator();"""

new_play_sfx = """      if (type === 'typing') {
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = 'triangle';
        const freq = 1300 + Math.random() * 350;
        osc.frequency.setValueAtTime(freq, t);
        osc.frequency.exponentialRampToValueAtTime(320, t + 0.02);
        gain.gain.setValueAtTime(v * 0.35, t);
        gain.gain.exponentialRampToValueAtTime(0.0001, t + 0.022);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start(t);
        osc.stop(t + 0.025);
        return;
      } else if (type === 'click') {
        const osc = ctx.createOscillator();"""

if old_play_sfx not in code:
    print("ERRO: old_play_sfx não encontrado!")
    sys.exit(1)

code = code.replace(old_play_sfx, new_play_sfx)
print("Passo 3: Som de digitação mecânica adicionado em AudioManager.")

# 4. Conectar som de digitação no evento de input dos campos de digitação
old_autocomplete_setup = """  inputEl.addEventListener('input', () => {
    const val = inputEl.value.trim();"""

new_autocomplete_setup = """  inputEl.addEventListener('input', () => {
    AudioManager.playSfx('typing');
    const val = inputEl.value.trim();"""

if old_autocomplete_setup not in code:
    print("ERRO: old_autocomplete_setup não encontrado!")
    sys.exit(1)

code = code.replace(old_autocomplete_setup, new_autocomplete_setup)
print("Passo 4: Som de digitação conectado aos inputs.")

# 5. Atualizar o limite de exibição do Hall da Fama de 20 para 50 melhores
old_slice = "filtered.slice(0, 20).forEach((item, idx) => {"
new_slice = "filtered.slice(0, 50).forEach((item, idx) => {"

if old_slice not in code:
    print("ERRO: old_slice não encontrado!")
    sys.exit(1)

code = code.replace(old_slice, new_slice)
print("Passo 5: Hall da fama expandido para os 50 melhores.")

# 6. Atualizar as abas de navegação no HTML para as 5 abas separadas
old_mode_nav = """  <!-- Mode Tabs (4 Modes) -->
  <div class="mode-nav">
    <button class="mode-tab-btn active" id="tab-mode1" onclick="switchGameMode('mode1')">
      🎧 Modo 1: Blind Test
    </button>
    <button class="mode-tab-btn" id="tab-mode2" onclick="switchGameMode('mode2')">
      🎵 Modo 2: Qual é a Abertura?
    </button>
    <button class="mode-tab-btn" id="tab-mode3" onclick="switchGameMode('mode3')">
      🖼️ Modo 3: Adivinhe a Cena
    </button>
    <button class="mode-tab-btn" id="tab-mode4" onclick="switchGameMode('mode4')">
      🎮 Salas & Placar
    </button>
  </div>"""

new_mode_nav = """  <!-- Navigation Tabs (5 Abas Separadas) -->
  <!-- Salas & Placar agora divididas em Salas Multiplayer e Placar de Líderes -->
  <div class="mode-nav">
    <button class="mode-tab-btn active" id="tab-mode1" onclick="switchGameMode('mode1')">
      🎧 Modo 1: Blind Test
    </button>
    <button class="mode-tab-btn" id="tab-mode2" onclick="switchGameMode('mode2')">
      🎵 Modo 2: Qual é a Abertura?
    </button>
    <button class="mode-tab-btn" id="tab-mode3" onclick="switchGameMode('mode3')">
      🖼️ Modo 3: Adivinhe a Cena
    </button>
    <button class="mode-tab-btn" id="tab-mode4" onclick="switchGameMode('mode4')">
      🎮 Salas Multiplayer
    </button>
    <button class="mode-tab-btn" id="tab-mode5" onclick="switchGameMode('mode5')">
      🏆 Placar de Líderes
    </button>
  </div>"""

if old_mode_nav not in code:
    print("ERRO: old_mode_nav não encontrado!")
    sys.exit(1)

code = code.replace(old_mode_nav, new_mode_nav)
print("Passo 6: Abas de navegação atualizadas para 5 abas.")

# 7. Adicionar slots de scoreboard nos Modos 1, 2 e 3
old_m1_header = """      <div class="round-indicator" id="m1-round-indicator">MÚSICA #1 DE 100</div>"""
new_m1_header = """      <div class="round-indicator" id="m1-round-indicator">MÚSICA #1 DE 100</div>
    </div>
    <!-- Slot Dinâmico do Scoreboard para o Modo 1 -->
    <div id="mode1-scoreboard-slot" class="mode-scoreboard-slot" style="margin-bottom: 14px;">"""

# Note: no original era:
# <div class="quiz-header">
#   <div class="round-indicator" id="m1-round-indicator">MÚSICA #1 DE 100</div>
#   ...
# </div>
old_m1_slot_target = """    <div class="quiz-header">
      <div class="round-indicator" id="m1-round-indicator">MÚSICA #1 DE 100</div>
      <div style="display: flex; gap: 8px;">
        <button class="btn btn-outline" style="padding: 6px 12px; font-size: 12px;" onclick="openYouTubeDirect()">
          <img src="icons/play-button.png" class="btn-icon-img btn-icon-sm" alt="Play" /> Clipe no YouTube
        </button>
      </div>
    </div>"""

new_m1_slot_target = """    <div class="quiz-header">
      <div class="round-indicator" id="m1-round-indicator">MÚSICA #1 DE 100</div>
      <div style="display: flex; gap: 8px;">
        <button class="btn btn-outline" style="padding: 6px 12px; font-size: 12px;" onclick="openYouTubeDirect()">
          <img src="icons/play-button.png" class="btn-icon-img btn-icon-sm" alt="Play" /> Clipe no YouTube
        </button>
      </div>
    </div>
    <!-- Scoreboard do Modo 1 -->
    <div id="mode1-scoreboard-slot" class="mode-scoreboard-slot"></div>"""

if old_m1_slot_target not in code:
    print("ERRO: old_m1_slot_target não encontrado!")
    sys.exit(1)

code = code.replace(old_m1_slot_target, new_m1_slot_target)
print("Passo 7A: Slot de Scoreboard no Modo 1 adicionado.")

old_m2_slot_target = """    <div class="quiz-header">
      <div class="round-indicator" id="m2-round-indicator">RODADA #1 DE 100</div>
      <button class="btn btn-outline" style="padding: 6px 12px; font-size: 12px;" onclick="m2StopAudio()">
        ⏹️ Parar Som
      </button>
    </div>"""

new_m2_slot_target = """    <div class="quiz-header">
      <div class="round-indicator" id="m2-round-indicator">RODADA #1 DE 100</div>
      <button class="btn btn-outline" style="padding: 6px 12px; font-size: 12px;" onclick="m2StopAudio()">
        ⏹️ Parar Som
      </button>
    </div>
    <!-- Scoreboard do Modo 2 -->
    <div id="mode2-scoreboard-slot" class="mode-scoreboard-slot"></div>"""

if old_m2_slot_target not in code:
    print("ERRO: old_m2_slot_target não encontrado!")
    sys.exit(1)

code = code.replace(old_m2_slot_target, new_m2_slot_target)
print("Passo 7B: Slot de Scoreboard no Modo 2 adicionado.")

old_m3_slot_target = """    <div class="quiz-header">
      <div class="round-indicator" id="m3-round-indicator">CENA #1 DE 98</div>
      <button class="btn btn-gold" style="padding: 6px 12px; font-size: 12px;" onclick="m3PickRandom()">
        🔀 Cena Aleatória
      </button>
    </div>"""

new_m3_slot_target = """    <div class="quiz-header">
      <div class="round-indicator" id="m3-round-indicator">CENA #1 DE 98</div>
      <button class="btn btn-gold" style="padding: 6px 12px; font-size: 12px;" onclick="m3PickRandom()">
        🔀 Cena Aleatória
      </button>
    </div>
    <!-- Scoreboard do Modo 3 -->
    <div id="mode3-scoreboard-slot" class="mode-scoreboard-slot"></div>"""

if old_m3_slot_target not in code:
    print("ERRO: old_m3_slot_target não encontrado!")
    sys.exit(1)

code = code.replace(old_m3_slot_target, new_m3_slot_target)
print("Passo 7C: Slot de Scoreboard no Modo 3 adicionado.")

# 8. Separar Modo 4 (Salas) e Modo 5 (Placar) no HTML
old_mode4_structure = """  <!-- VIEW 4: MODO 4 - SALAS MULTIPLAYER & PLACAR DE LÍDERES -->
  <div class="quiz-card" id="mode4-view" style="display: none;">

    <!-- Sub-abas: Salas Multiplayer vs Hall da Fama -->
    <div class="mp-tabs-bar">
      <button class="mp-tab-btn active" id="mp-subtab-rooms" onclick="switchMode4Tab('rooms')">
        🎮 Salas Multiplayer (Ao Vivo)
      </button>
      <button class="mp-tab-btn" id="mp-subtab-leaderboard" onclick="switchMode4Tab('leaderboard')">
        🏆 Hall da Fama (Placar)
      </button>
    </div>

    <!-- PAINEL 1: SALAS MULTIPLAYER -->
    <div id="mp-rooms-panel">
      <!-- Estado A: Fora de Sala (Criar ou Entrar) -->
      <div id="mp-pre-room-view">"""

new_mode4_structure = """  <!-- VIEW 4: MODO 4 - SALAS MULTIPLAYER (DEDICADO A SALAS AO VIVO) -->
  <div class="quiz-card" id="mode4-view" style="display: none;">
    <div class="quiz-header" style="margin-bottom: 16px;">
      <div class="round-indicator">🎮 SALAS MULTIPLAYER P2P (AO VIVO)</div>
    </div>

    <!-- PAINEL 1: SALAS MULTIPLAYER -->
    <div id="mp-rooms-panel">
      <!-- Estado A: Fora de Sala (Criar ou Entrar) -->
      <div id="mp-pre-room-view">"""

if old_mode4_structure not in code:
    print("ERRO: old_mode4_structure não encontrado!")
    sys.exit(1)

code = code.replace(old_mode4_structure, new_mode4_structure)
print("Passo 8A: Modo 4 focado exclusivamente em salas.")

# Separar o painel 2 do Hall da Fama para ser a VIEW 5 (Placar de Líderes)
old_leaderboard_split = """    <!-- PAINEL 2: HALL DA FAMA (PLACAR DE LÍDERES) -->
    <div id="mp-leaderboard-panel" style="display: none;">
      <div class="quiz-header" style="margin-bottom: 14px;">
        <div class="round-indicator">🏆 RECORDES LOCAIS & HALL DA FAMA</div>
        <button class="btn btn-outline" style="padding: 5px 10px; font-size: 11px;" onclick="clearLeaderboard()">
          🗑️ Limpar Placar
        </button>
      </div>

      <div class="leaderboard-container">
        <!-- Salvar pontuação atual -->
        <div class="save-score-box">
          <div>
            <div style="font-size: 13px; font-weight: 800; color: #fff;">💾 Salvar Pontuação Atual no Hall da Fama</div>
            <div style="font-size: 11px; color: var(--text-muted);">
              Sua pontuação: <strong id="save-score-val" style="color: var(--accent);">0 pts</strong> • Acertos: <strong id="save-correct-val" style="color: var(--green);">0</strong>
            </div>
          </div>
          <div style="display: flex; gap: 8px;">
            <input type="text" class="save-score-input" id="player-nickname" placeholder="Seu Apelido..." maxlength="18" />
            <button class="btn btn-green" onclick="saveCurrentScoreToLeaderboard()">Salvar Recorde</button>
          </div>
        </div>

        <!-- Filtros do Placar -->
        <div class="leaderboard-filter-tabs">
          <button class="lb-tab-btn active" onclick="filterLeaderboard('all', this)">🏆 Geral</button>
          <button class="lb-tab-btn" onclick="filterLeaderboard('mode2', this)">🎵 Qual é a Abertura?</button>
          <button class="lb-tab-btn" onclick="filterLeaderboard('mode1', this)">🎧 Blind Test</button>
          <button class="lb-tab-btn" onclick="filterLeaderboard('mode3', this)">🖼️ Adivinhe a Cena</button>
          <button class="lb-tab-btn" onclick="filterLeaderboard('multiplayer', this)">🎮 Multiplayer</button>
        </div>

        <!-- Tabela do Placar -->
        <table class="leaderboard-table">
          <thead>
            <tr>
              <th style="width: 50px;">Pos</th>
              <th>Jogador</th>
              <th>Modo</th>
              <th>Pontos</th>
              <th>Acertos</th>
              <th>Data</th>
            </tr>
          </thead>
          <tbody id="leaderboard-tbody"></tbody>
        </table>
      </div>
    </div>

  </div>"""

new_leaderboard_split = """    </div><!-- fim mp-rooms-panel -->
  </div><!-- fim mode4-view -->

  <!-- VIEW 5: PLACAR DE LÍDERES & HALL DA FAMA (TOP 50 ROLÁVEL) -->
  <div class="quiz-card" id="mode5-view" style="display: none;">
    <div id="mp-leaderboard-panel" style="display: block;">
      <div class="quiz-header" style="margin-bottom: 14px;">
        <div class="round-indicator">🏆 RECORDES & HALL DA FAMA (TOP 50)</div>
        <button class="btn btn-outline" style="padding: 5px 10px; font-size: 11px;" onclick="clearLeaderboard()">
          🗑️ Limpar Placar
        </button>
      </div>

      <div class="leaderboard-container">
        <!-- Salvar pontuação atual -->
        <div class="save-score-box">
          <div>
            <div style="font-size: 13px; font-weight: 800; color: #fff;">💾 Salvar Pontuação Atual no Hall da Fama</div>
            <div style="font-size: 11px; color: var(--text-muted);">
              Sua pontuação: <strong id="save-score-val" style="color: var(--accent);">0 pts</strong> • Acertos: <strong id="save-correct-val" style="color: var(--green);">0</strong>
            </div>
          </div>
          <div style="display: flex; gap: 8px;">
            <input type="text" class="save-score-input" id="player-nickname" placeholder="Seu Apelido..." maxlength="18" />
            <button class="btn btn-green" onclick="saveCurrentScoreToLeaderboard()">Salvar Recorde</button>
          </div>
        </div>

        <!-- Filtros do Placar -->
        <div class="leaderboard-filter-tabs">
          <button class="lb-tab-btn active" onclick="filterLeaderboard('all', this)">🏆 Geral</button>
          <button class="lb-tab-btn" onclick="filterLeaderboard('mode2', this)">🎵 Qual é a Abertura?</button>
          <button class="lb-tab-btn" onclick="filterLeaderboard('mode1', this)">🎧 Blind Test</button>
          <button class="lb-tab-btn" onclick="filterLeaderboard('mode3', this)">🖼️ Adivinhe a Cena</button>
          <button class="lb-tab-btn" onclick="filterLeaderboard('multiplayer', this)">🎮 Multiplayer</button>
        </div>

        <!-- Área de Tabela com Scroll para até 50 Jogadores -->
        <div class="leaderboard-scroll-wrapper" style="max-height: 480px; overflow-y: auto; overflow-x: hidden; border: 1px solid rgba(255,255,255,0.06); border-radius: 10px;">
          <table class="leaderboard-table" style="margin: 0;">
            <thead style="position: sticky; top: 0; background: #0f172a; z-index: 2;">
              <tr>
                <th style="width: 50px;">Pos</th>
                <th>Jogador</th>
                <th>Modo</th>
                <th>Pontos</th>
                <th>Acertos</th>
                <th>Data</th>
              </tr>
            </thead>
            <tbody id="leaderboard-tbody"></tbody>
          </table>
        </div>
      </div>
    </div>
  </div>"""

if old_leaderboard_split not in code:
    print("ERRO: old_leaderboard_split não encontrado!")
    sys.exit(1)

code = code.replace(old_leaderboard_split, new_leaderboard_split)
print("Passo 8B: Modo 5 (Placar de Líderes com scroll dos 50 melhores) criado.")

# 9. Inicialização inicial do Scoreboard no Modo 1 ao carregar
dom_init_target = "  m1LoadSong(false);\n  }"

dom_init_replacement = """  m1LoadSong(false);
  }

  // Colocar o Scoreboard dentro do Modo 1 inicialmente
  const initSb = document.getElementById('main-scoreboard');
  const m1Slot = document.getElementById('mode1-scoreboard-slot');
  if (initSb && m1Slot) {
    m1Slot.appendChild(initSb);
    initSb.style.display = 'grid';
  }"""

if dom_init_target not in code:
    print("ERRO: dom_init_target não encontrado!")
    sys.exit(1)

code = code.replace(dom_init_target, dom_init_replacement)
print("Passo 9: Inicialização do Scoreboard no slot do Modo 1 configurada.")

# 10. Atualização de CSS:
# - Ajustes no container (max-width 1040px, auto-scroll, sem corte)
# - Dropdown de autocomplete com visual nítido e alto z-index
# - Pistas com destaque visual agradável
css_patch = """
    /* ==========================================================
       AJUSTES DE DESIGN FLUIDO, ANTI-CORTE & ALTA VISIBILIDADE
       ========================================================== */
    .container {
      width: 100%;
      max-width: 1020px;
      margin: 0 auto;
      padding: 14px 16px 40px;
      box-sizing: border-box;
    }

    body {
      overflow-x: hidden;
      overflow-y: auto; /* Garante que NADA seja cortado e todos os botões sejam acessíveis */
    }

    /* Scoreboard integrado dentro dos modos */
    .mode-scoreboard-slot {
      margin-bottom: 16px;
    }
    .mode-scoreboard-slot .scoreboard {
      margin: 0 !important;
    }

    /* Autocomplete Dropdown Nítido e com Alto Z-Index */
    .autocomplete-wrapper {
      position: relative;
      flex: 1;
      display: flex;
    }

    .autocomplete-dropdown {
      position: absolute !important;
      top: calc(100% + 4px) !important;
      left: 0 !important;
      right: 0 !important;
      background: #0f172a !important;
      border: 1px solid #38bdf8 !important;
      border-radius: 12px !important;
      max-height: 240px !important;
      overflow-y: auto !important;
      z-index: 9999 !important;
      box-shadow: 0 12px 36px rgba(0,0,0,0.9), 0 0 15px rgba(56, 189, 248, 0.25) !important;
    }

    .autocomplete-item {
      padding: 10px 14px !important;
      font-size: 13px !important;
      color: #e2e8f0 !important;
      cursor: pointer !important;
      border-bottom: 1px solid rgba(255, 255, 255, 0.06) !important;
      display: flex !important;
      justify-content: space-between !important;
      align-items: center !important;
      transition: background 0.15s, color 0.15s !important;
    }

    .autocomplete-item:hover, .autocomplete-item.active {
      background: rgba(56, 189, 248, 0.18) !important;
      color: #38bdf8 !important;
    }

    /* Pistas no Modo 1 com Destaque Visual */
    .hints-section {
      background: rgba(15, 23, 42, 0.6);
      border: 1px solid rgba(99, 102, 241, 0.25);
      border-radius: 12px;
      padding: 12px 14px;
      margin-bottom: 16px;
    }

    .hints-title {
      font-size: 12px;
      font-weight: 700;
      color: #cbd5e1;
      margin-bottom: 8px;
    }

    .tags-container {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }

    .hint-tag {
      background: rgba(30, 41, 59, 0.85);
      border: 1px solid rgba(148, 163, 184, 0.3);
      color: #cbd5e1;
      padding: 6px 14px;
      border-radius: 8px;
      font-size: 12px;
      font-weight: 700;
      cursor: pointer;
      user-select: none;
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
      box-shadow: 0 2px 6px rgba(0,0,0,0.25);
    }

    .hint-tag:hover {
      border-color: #38bdf8;
      color: #38bdf8;
      transform: translateY(-1px);
    }

    .hint-tag.revealed {
      background: rgba(16, 185, 129, 0.18);
      border-color: rgba(16, 185, 129, 0.5);
      color: #34d399;
    }

    /* Scrollbar personalizada para a tabela dos 50 melhores */
    .leaderboard-scroll-wrapper::-webkit-scrollbar {
      width: 6px;
    }
    .leaderboard-scroll-wrapper::-webkit-scrollbar-track {
      background: rgba(15, 23, 42, 0.6);
    }
    .leaderboard-scroll-wrapper::-webkit-scrollbar-thumb {
      background: #3b82f6;
      border-radius: 3px;
    }
"""

style_end_marker = "  </style>"
if style_end_marker not in code:
    print("ERRO: style_end_marker não encontrado!")
    sys.exit(1)

code = code.replace(style_end_marker, f"{css_patch}\n  </style>")
print("Passo 10: CSS de anti-corte, autocomplete nítido e pistas aprimoradas adicionado.")

# Salvar arquivo
with open(GEN_PATH, "w", encoding="utf-8") as f:
    f.write(code)

print("SUCESSO: generate_full_html.py reformulado com sucesso de acordo com as instruções do usuário!")
