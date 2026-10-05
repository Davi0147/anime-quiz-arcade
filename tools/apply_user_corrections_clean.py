# -*- coding: utf-8 -*-
"""
Script Limpo de Aplicação das Correções do Usuário
Anime Music & Scene Quiz
"""
import os
import re
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GEN_PATH = os.path.join(BASE_DIR, "tools", "generate_full_html.py")
BAK_PATH = os.path.join(BASE_DIR, "tools", "generate_full_html.py.pre_etapa4_bak")

# Começamos sempre da base estável pré-etapa 4
with open(BAK_PATH, "r", encoding="utf-8") as f:
    code = f.read()

print("Base limpa carregada com sucesso:", len(code), "bytes.")

# ==============================================================================
# 1. ATUALIZAR switchGameMode PARA 5 MODOS COM SCOREBOARD NO CARD ATIVO
# ==============================================================================
old_switch_target = """function switchGameMode(mode) {
  stopAllMedia();
  AudioManager.playSfx('tab');
  activeGameMode = mode;
  ['mode1', 'mode2', 'mode3', 'mode4'].forEach(m => {
    document.getElementById(`${m}-view`).style.display = (m === mode) ? 'block' : 'none';
    document.getElementById(`tab-${m}`).classList.toggle('active', m === mode);
  });

  if (window.MultiplayerEngine && MultiplayerEngine.isMatchActive) {
    updateGlobalKPIs();
    return;
  }

  if (mode === 'mode1') {
    updateGlobalKPIs();
  } else if (mode === 'mode2') {
    updateGlobalKPIs();
    if (m2Options.length === 0) {
      m2StartGame();
    }
  } else if (mode === 'mode3') {
    updateGlobalKPIs();
    if (m3UnplayedQueue.length === 0) {
      m3StartGame();
    }
  } else if (mode === 'mode4') {
    updateGlobalKPIs();
    renderLeaderboardTable('all');
    updateSaveScoreKPIs();
  }
}"""

new_switch_target = """function switchGameMode(mode) {
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

  // O Scoreboard de KPIs pertence exclusivamente dentro de cada modo solo ativo
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
  }

  if (window.MultiplayerEngine && MultiplayerEngine.isMatchActive) {
    updateGlobalKPIs();
    return;
  }

  if (mode === 'mode1') {
    updateGlobalKPIs();
  } else if (mode === 'mode2') {
    updateGlobalKPIs();
    if (m2Options.length === 0) {
      m2StartGame();
    }
  } else if (mode === 'mode3') {
    updateGlobalKPIs();
    if (m3UnplayedQueue.length === 0) {
      m3StartGame();
    }
  } else if (mode === 'mode4') {
    updateGlobalKPIs();
  } else if (mode === 'mode5') {
    updateGlobalKPIs();
    renderLeaderboardTable('all');
    updateSaveScoreKPIs();
  }
}"""

assert old_switch_target in code, "old_switch_target não encontrado!"
code = code.replace(old_switch_target, new_switch_target)
print("1. switchGameMode atualizado para 5 modos com slot de scoreboard.")

# ==============================================================================
# 2. ADICIONAR SOM DE DIGITAÇÃO MECÂNICA EM AudioManager
# ==============================================================================
old_play_sfx = """      if (type === 'click') {
        const osc = ctx.createOscillator();"""

new_play_sfx = """      if (type === 'typing') {
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = 'triangle';
        const freq = 1250 + Math.random() * 350;
        osc.frequency.setValueAtTime(freq, t);
        osc.frequency.exponentialRampToValueAtTime(300, t + 0.02);
        gain.gain.setValueAtTime(v * 0.35, t);
        gain.gain.exponentialRampToValueAtTime(0.0001, t + 0.022);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start(t);
        osc.stop(t + 0.025);
        return;
      } else if (type === 'click') {
        const osc = ctx.createOscillator();"""

assert old_play_sfx in code, "old_play_sfx não encontrado!"
code = code.replace(old_play_sfx, new_play_sfx)
print("2. Som de digitação mecânica adicionado a AudioManager.")

# ==============================================================================
# 3. CONECTAR SOM DE DIGITAÇÃO NO AUTOCOMPLETE & INPUTS
# ==============================================================================
old_autocomplete_setup = """  inputEl.addEventListener('input', () => {
    const val = inputEl.value.trim();"""

new_autocomplete_setup = """  inputEl.addEventListener('input', () => {
    AudioManager.playSfx('typing');
    const val = inputEl.value.trim();"""

assert old_autocomplete_setup in code, "old_autocomplete_setup não encontrado!"
code = code.replace(old_autocomplete_setup, new_autocomplete_setup)
print("3. Som de digitação conectado aos inputs.")

# ==============================================================================
# 4. EXPANDIR LIMITE DO HALL DA FAMA PARA OS 50 MELHORES
# ==============================================================================
old_slice = "filtered.slice(0, 20).forEach((item, idx) => {"
new_slice = "filtered.slice(0, 50).forEach((item, idx) => {"

assert old_slice in code, "old_slice não encontrado!"
code = code.replace(old_slice, new_slice)
print("4. Hall da fama expandido para os 50 melhores.")

# ==============================================================================
# 5. ATUALIZAR AS ABAS DE NAVEGAÇÃO PARA 5 ABAS INDEPENDENTES
# ==============================================================================
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
  <!-- Salas & Placar agora separadas em Salas Multiplayer e Placar de Líderes -->
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

assert old_mode_nav in code, "old_mode_nav não encontrado!"
code = code.replace(old_mode_nav, new_mode_nav)
print("5. Abas de navegação atualizadas para 5 abas.")

# ==============================================================================
# 6. INSERIR SLOTS DE SCOREBOARD NOS MODOS 1, 2 E 3
# ==============================================================================
old_m1_header = """    <div class="quiz-header">
      <div class="round-indicator" id="m1-round-indicator">MÚSICA #1 DE 100</div>
      <div style="display: flex; gap: 8px;">
        <button class="btn btn-outline" style="padding: 6px 12px; font-size: 12px;" onclick="openYouTubeDirect()">
          <img src="icons/play-button.png" class="btn-icon-img btn-icon-sm" alt="Play" /> Clipe no YouTube
        </button>
      </div>
    </div>"""

new_m1_header = """    <div class="quiz-header">
      <div class="round-indicator" id="m1-round-indicator">MÚSICA #1 DE 100</div>
      <div style="display: flex; gap: 8px;">
        <button class="btn btn-outline" style="padding: 6px 12px; font-size: 12px;" onclick="openYouTubeDirect()">
          <img src="icons/play-button.png" class="btn-icon-img btn-icon-sm" alt="Play" /> Clipe no YouTube
        </button>
      </div>
    </div>
    <!-- Scoreboard Integrado do Modo 1 -->
    <div id="mode1-scoreboard-slot" class="mode-scoreboard-slot"></div>"""

assert old_m1_header in code, "old_m1_header não encontrado!"
code = code.replace(old_m1_header, new_m1_header)
print("6A. Slot de Scoreboard no Modo 1 adicionado.")

old_m2_header = """    <div class="quiz-header">
      <div class="round-indicator" id="m2-round-indicator">RODADA #1 DE 100</div>
      <button class="btn btn-outline" style="padding: 6px 12px; font-size: 12px;" onclick="m2StopAudio()">
        ⏹️ Parar Som
      </button>
    </div>"""

new_m2_header = """    <div class="quiz-header">
      <div class="round-indicator" id="m2-round-indicator">RODADA #1 DE 100</div>
      <button class="btn btn-outline" style="padding: 6px 12px; font-size: 12px;" onclick="m2StopAudio()">
        ⏹️ Parar Som
      </button>
    </div>
    <!-- Scoreboard Integrado do Modo 2 -->
    <div id="mode2-scoreboard-slot" class="mode-scoreboard-slot"></div>"""

assert old_m2_header in code, "old_m2_header não encontrado!"
code = code.replace(old_m2_header, new_m2_header)
print("6B. Slot de Scoreboard no Modo 2 adicionado.")

old_m3_header = """    <div class="quiz-header">
      <div class="round-indicator" id="m3-round-indicator">CENA #1 DE 98</div>
      <button class="btn btn-gold" style="padding: 6px 12px; font-size: 12px;" onclick="m3PickRandom()">
        🔀 Cena Aleatória
      </button>
    </div>"""

new_m3_header = """    <div class="quiz-header">
      <div class="round-indicator" id="m3-round-indicator">CENA #1 DE 98</div>
      <button class="btn btn-gold" style="padding: 6px 12px; font-size: 12px;" onclick="m3PickRandom()">
        🔀 Cena Aleatória
      </button>
    </div>
    <!-- Scoreboard Integrado do Modo 3 -->
    <div id="mode3-scoreboard-slot" class="mode-scoreboard-slot"></div>"""

assert old_m3_header in code, "old_m3_header não encontrado!"
code = code.replace(old_m3_header, new_m3_header)
print("6C. Slot de Scoreboard no Modo 3 adicionado.")

# ==============================================================================
# 7. SEPARAR MODO 4 (SALAS MULTIPLAYER) E MODO 5 (PLACAR DE LÍDERES)
# ==============================================================================
p_m4_start = code.find('  <!-- VIEW 4: MODO 4 - SALAS MULTIPLAYER & PLACAR DE LÍDERES -->')
p_p1 = code.find('    <!-- PAINEL 1: SALAS MULTIPLAYER -->')
p_p2 = code.find('    <!-- PAINEL 2: HALL DA FAMA (PLACAR DE LÍDERES) -->')
p_m4_end = code.find('  <!-- Full Table Overview -->')

assert p_m4_start != -1 and p_p1 != -1 and p_p2 != -1 and p_m4_end != -1, "Marcadores de divisão do Modo 4 não encontrados!"

rooms_panel_inner = code[p_p1:p_p2].rstrip()

# Leaderboard panel vai de p_p2 até antes de </div>\n\n  <!-- Full Table Overview -->
# No original, o fechamento da div de mode4 é duas tags </div> antes de <!-- Full Table Overview -->
p_lb_end = code.rfind('  </div>\n\n  <!-- Full Table Overview -->')
assert p_lb_end != -1, "p_lb_end não encontrado!"
leaderboard_inner = code[p_p2:p_lb_end].rstrip()

# Criar a separação das views 4 e 5
new_separated_views = f"""  <!-- VIEW 4: MODO 4 - SALAS MULTIPLAYER (DEDICADO A SALAS AO VIVO) -->
  <div class="quiz-card" id="mode4-view" style="display: none;">
    <div class="quiz-header" style="margin-bottom: 16px;">
      <div class="round-indicator">🎮 SALAS MULTIPLAYER P2P (AO VIVO)</div>
    </div>
{rooms_panel_inner}
  </div><!-- fim mode4-view -->

  <!-- VIEW 5: PLACAR DE LÍDERES & HALL DA FAMA (TOP 50 ROLÁVEL) -->
  <div class="quiz-card" id="mode5-view" style="display: none;">
    <div id="mp-leaderboard-panel" style="display: block;">
      <div class="quiz-header" style="margin-bottom: 14px;">
        <div class="round-indicator">🏆 RECORDES LOCAIS & HALL DA FAMA (TOP 50)</div>
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
              Sua pontuação: <strong id="save-score-val" style="color: var(--accent);">0 pts</strong> • Acertos: <strong id="save-correct-val">0</strong>
            </div>
          </div>
          <div style="display: flex; gap: 8px;">
            <input type="text" class="save-score-input" id="player-nickname" placeholder="Seu Apelido..." maxlength="15" />
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
  </div>

"""

code = code[:p_m4_start] + new_separated_views + code[p_m4_end:]
print("7. Modo 4 e Modo 5 completamente separados e formatados.")

# ==============================================================================
# 8. INICIALIZAÇÃO INICIAL DO SCOREBOARD NO MODO 1
# ==============================================================================
dom_init_target = "  m1LoadSong(false);\n  }"

dom_init_replacement = """  m1LoadSong(false);
  }

  // Posicionar o Scoreboard dentro do Modo 1 inicialmente
  const initSb = document.getElementById('main-scoreboard');
  const m1Slot = document.getElementById('mode1-scoreboard-slot');
  if (initSb && m1Slot) {
    m1Slot.appendChild(initSb);
    initSb.style.display = 'grid';
  }"""

assert dom_init_target in code, "dom_init_target não encontrado!"
code = code.replace(dom_init_target, dom_init_replacement)
print("8. Inicialização do Scoreboard no slot do Modo 1 configurada.")

# ==============================================================================
# 9. CSS REFINADO: FLUIDO, ANTI-CORTE, PISTAS NÍTIDAS E AUTOCOMPLETE DESTACADO
# ==============================================================================
css_patch = """
    /* ==========================================================
       AJUSTES DE DESIGN FLUIDO, ANTI-CORTE & ALTA VISIBILIDADE
       ========================================================== */
    .container {
      width: 100%;
      max-width: 1040px;
      margin: 0 auto;
      padding: 14px 16px 50px;
      box-sizing: border-box;
    }

    body {
      overflow-x: hidden;
      overflow-y: auto !important; /* Sem cortes: permite rolagem suave e acesso a todos os botões */
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
      border: 1.5px solid #38bdf8 !important;
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
      background: rgba(15, 23, 42, 0.65);
      border: 1px solid rgba(99, 102, 241, 0.3);
      border-radius: 12px;
      padding: 14px 16px;
      margin-bottom: 16px;
    }

    .hints-title {
      font-size: 13px;
      font-weight: 800;
      color: #e2e8f0;
      margin-bottom: 10px;
    }

    .tags-container {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      min-height: 36px;
      align-items: center;
    }

    .hint-tag {
      background: rgba(30, 41, 59, 0.9);
      border: 1.5px solid rgba(56, 189, 248, 0.5);
      color: #38bdf8;
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
      background: rgba(56, 189, 248, 0.15);
      transform: translateY(-2px);
      box-shadow: 0 0 12px rgba(56, 189, 248, 0.4);
    }

    .hint-tag.revealed {
      background: rgba(16, 185, 129, 0.2);
      border-color: #10b981;
      color: #34d399;
    }

    /* Modo 2: Espaçamento Confortável e Acessível */
    #mode2-view .player-container {
      max-height: 170px !important;
    }
    #mode2-view .music-card {
      padding: 10px 14px !important;
      margin-bottom: 8px !important;
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
assert style_end_marker in code, "style_end_marker não encontrado!"
code = code.replace(style_end_marker, f"{css_patch}\n  </style>")
print("9. CSS anti-corte, pistas destacadas e autocomplete nítido adicionados.")

# Salvar arquivo
with open(GEN_PATH, "w", encoding="utf-8") as f:
    f.write(code)

print("SUCESSO ABSOLUTO: generate_full_html.py atualizado!")
