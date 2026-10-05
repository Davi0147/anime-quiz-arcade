# -*- coding: utf-8 -*-
"""
Script Definitivo de Construção v3.1.0
- Sidebar Mini-Rail Retrátil (Desktop) & Bottom Navigation Bar (Mobile)
- Modo 1 em Grid de 2 Colunas (Player/Mídia na Esquerda + Dicas/Palpite na Direita)
- Remoção Completa da Parte 3 (Catálogo de 100 Aberturas)
- Correção do Bug do Placar de Líderes (Modo 5)
- Ícones Oficiais PNG em todo o sistema (Filtros de cor para pretos, ícone invertido para Anterior)
- Modal Completo de Configurações de Áudio, SFX e Atalhos
- Microinterações de Hover de Alta Satisfação com Efeitos Sonoros
"""
import os
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GEN_FILE = os.path.join(BASE_DIR, "tools", "generate_full_html.py")
BAK_FILE = os.path.join(BASE_DIR, "backup_v3.0.0", "generate_full_html.py")

with open(BAK_FILE, "r", encoding="utf-8") as f:
    code = f.read()

print(f"Base v3.0.0 carregada: {len(code)} bytes.")

# ==============================================================================
# 1. INJETAR CSS v3.1.0 (ÍCONES, SIDEBAR MINI-RAIL, BOTTOM NAV, 2-COLUNAS)
# ==============================================================================
v3_1_css = """
/* ==============================================================
   ESTILOS v3.1.0: ÍCONES PNG, SIDEBAR RETRÁTIL & LAYOUT WIDESCREEN
   ============================================================== */
:root {
  --sidebar-w: 64px;
  --sidebar-w-expanded: 230px;
}

/* Ícones Oficiais do Aplicativo via PNG */
.app-icon {
  width: 18px;
  height: 18px;
  vertical-align: middle;
  display: inline-block;
  object-fit: contain;
  transition: transform 0.2s cubic-bezier(0.34, 1.56, 0.64, 1), filter 0.2s ease;
  pointer-events: none;
}
.app-icon-sm { width: 14px; height: 14px; }
.app-icon-md { width: 20px; height: 20px; }
.app-icon-lg { width: 24px; height: 24px; }
.app-icon-xl { width: 36px; height: 36px; }

/* Filtros de Cores para Ícones Pretos */
.icon-white {
  filter: brightness(0) invert(1);
}
.icon-neon-cyan {
  filter: brightness(0) invert(1) drop-shadow(0 0 6px #06b6d4);
}
.icon-gold {
  filter: invert(78%) sepia(53%) saturate(1200%) hue-rotate(359deg) brightness(102%) contrast(106%);
}
.icon-raw {
  filter: none !important;
}
.icon-prev {
  transform: scaleX(-1);
  display: inline-block;
}

/* Estrutura Geral com Sidebar */
.app-layout {
  display: flex;
  min-height: 100vh;
  width: 100%;
  position: relative;
}

/* SIDEBAR MINI-RAIL (DESKTOP) */
.app-sidebar {
  width: var(--sidebar-w);
  background: rgba(10, 15, 30, 0.95);
  border-right: 1px solid rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(16px);
  display: flex;
  flex-direction: column;
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  z-index: 1000;
  transition: width 0.28s cubic-bezier(0.4, 0, 0.2, 1);
  overflow-x: hidden;
  box-shadow: 4px 0 24px rgba(0, 0, 0, 0.45);
}

.app-sidebar:hover,
.app-sidebar.expanded {
  width: var(--sidebar-w-expanded);
}

.sidebar-header {
  height: 60px;
  display: flex;
  align-items: center;
  padding: 0 16px;
  gap: 14px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
  flex-shrink: 0;
}
.sidebar-logo-icon {
  width: 32px;
  height: 32px;
  min-width: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.sidebar-title {
  font-size: 13px;
  font-weight: 800;
  letter-spacing: 0.5px;
  color: #fff;
  white-space: nowrap;
  opacity: 0;
  transition: opacity 0.2s ease;
  pointer-events: none;
  background: linear-gradient(135deg, #38bdf8, #818cf8);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.app-sidebar:hover .sidebar-title,
.app-sidebar.expanded .sidebar-title {
  opacity: 1;
  pointer-events: auto;
}

.sidebar-nav {
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding: 12px 8px;
  flex: 1;
}

.sidebar-item {
  position: relative;
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 11px 12px;
  border-radius: 12px;
  background: transparent;
  border: 1px solid transparent;
  color: #94a3b8;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  text-align: left;
  white-space: nowrap;
  user-select: none;
  width: 100%;
}

.sidebar-icon-wrap {
  width: 24px;
  height: 24px;
  min-width: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.sidebar-label {
  font-size: 13px;
  font-weight: 600;
  opacity: 0;
  transition: opacity 0.2s ease;
  pointer-events: none;
}
.app-sidebar:hover .sidebar-label,
.app-sidebar.expanded .sidebar-label {
  opacity: 1;
  pointer-events: auto;
}

/* Microinteração e Feedback Visual no Hover */
.sidebar-item:hover {
  background: rgba(99, 102, 241, 0.16);
  color: #ffffff;
  border-color: rgba(99, 102, 241, 0.4);
  transform: translateX(4px) scale(1.02);
  box-shadow: 0 4px 18px rgba(99, 102, 241, 0.3);
}
.sidebar-item:hover .sidebar-icon-wrap .app-icon {
  filter: brightness(0) invert(1) drop-shadow(0 0 6px #38bdf8);
  transform: scale(1.18);
}

.sidebar-item.active {
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.3), rgba(168, 85, 247, 0.25));
  border-color: #6366f1;
  color: #ffffff;
  font-weight: 700;
  box-shadow: 0 0 16px rgba(99, 102, 241, 0.4);
}
.sidebar-item.active .sidebar-icon-wrap .app-icon {
  filter: brightness(0) invert(1) drop-shadow(0 0 8px #818cf8);
}

.sidebar-divider {
  height: 1px;
  background: rgba(255, 255, 255, 0.08);
  margin: 6px 4px;
}

.sidebar-spacer {
  flex: 1;
}

/* ÁREA CENTRAL PRINCIPAL */
.app-main-content {
  flex: 1;
  margin-left: var(--sidebar-w);
  padding: 14px 20px;
  min-height: 100vh;
  box-sizing: border-box;
  transition: margin-left 0.28s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  flex-direction: column;
  align-items: center;
}

.container-center {
  width: 100%;
  max-width: 1100px;
}

/* Header Compacto Superior */
.app-top-header {
  margin-bottom: 12px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
  padding: 8px 16px;
  background: rgba(15, 23, 42, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 12px;
}
.app-top-header h1 {
  font-size: 16px;
  margin: 0;
  font-weight: 800;
  display: flex;
  align-items: center;
  gap: 8px;
}
.app-top-header .subtitle {
  font-size: 11px;
  color: var(--text-muted);
  margin: 0;
}

/* GRID 2 COLUNAS DO MODO 1 (DESKTOP ZERO-SCROLL) */
.mode-split-grid {
  display: grid;
  grid-template-columns: 1fr 1.15fr;
  gap: 18px;
  align-items: start;
}
.mode-col-media {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.mode-col-interactive {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

/* Modal de Configurações Central */
.settings-modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(5, 8, 16, 0.85);
  backdrop-filter: blur(8px);
  z-index: 99999;
  display: none;
  align-items: center;
  justify-content: center;
  padding: 20px;
}
.settings-modal-card {
  width: 100%;
  max-width: 480px;
  background: #0f172a;
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 18px;
  padding: 24px;
  box-shadow: 0 16px 40px rgba(0, 0, 0, 0.6);
  position: relative;
}
.settings-modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  padding-bottom: 12px;
}
.settings-modal-title {
  font-size: 16px;
  font-weight: 800;
  color: #fff;
  display: flex;
  align-items: center;
  gap: 10px;
}
.settings-close-btn {
  background: transparent;
  border: none;
  color: #94a3b8;
  font-size: 20px;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 6px;
  transition: color 0.2s ease;
}
.settings-close-btn:hover {
  color: #fff;
  background: rgba(255, 255, 255, 0.1);
}

/* Animação do Vinil */
.vinyl-spin-img {
  animation: vinylSpin 6s linear infinite;
  animation-play-state: paused;
}
.playing .vinyl-spin-img {
  animation-play-state: running;
}
@keyframes vinylSpin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* BOTTOM NAVIGATION BAR PARA MOBILE */
@media (max-width: 900px) {
  .app-sidebar {
    top: auto;
    bottom: 0;
    left: 0;
    right: 0;
    width: 100% !important;
    height: 62px;
    flex-direction: row;
    box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.6);
    border-right: none;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    padding: 0 4px;
  }
  .sidebar-header,
  .sidebar-divider,
  .sidebar-spacer,
  .sidebar-label {
    display: none !important;
  }
  .sidebar-nav {
    flex-direction: row;
    justify-content: space-around;
    align-items: center;
    width: 100%;
    padding: 0;
    gap: 2px;
  }
  .sidebar-item {
    padding: 10px;
    border-radius: 10px;
    flex: 1;
    justify-content: center;
  }
  .sidebar-item:hover {
    transform: none;
  }
  .app-main-content {
    margin-left: 0 !important;
    padding: 10px 10px 76px 10px;
  }
  .mode-split-grid {
    grid-template-columns: 1fr;
    gap: 14px;
  }
}
"""

p_style = code.find("</style>")
if p_style == -1:
    print("ERRO: </style> não encontrado!")
    sys.exit(1)
code = code[:p_style] + v3_1_css + code[p_style:]
print("1. CSS v3.1.0 injetado com sucesso!")

# ==============================================================================
# 2. SUBSTITUIR BLOCO SUPERIOR (CONTAINER + HEADER + TABS) PELO APP-LAYOUT
# ==============================================================================
top_target_start = code.find('<div class="container">\n\n  <!-- Header -->')
top_target_end = code.find('      <!-- VIEW 1: MODO 1 - BLIND TEST -->')
if top_target_start == -1 or top_target_end == -1:
    print("ERRO: top_target não encontrado!", top_target_start, top_target_end)
    sys.exit(1)

new_top_layout = """<!-- v3.0.0 e Salas & Placar mantidos para compatibilidade de testes -->
<div class="app-layout" id="app-layout">

  <!-- SIDEBAR MINI-RAIL (PARTE 1 À ESQUERDA) -->
  <aside class="app-sidebar" id="app-sidebar">
    <div class="sidebar-header">
      <div class="sidebar-logo-icon">
        <img src="icons/headphone-symbol.png" class="app-icon app-icon-lg icon-neon-cyan" alt="Logo" />
      </div>
      <div class="sidebar-title">ANIME QUIZ</div>
    </div>

    <!-- Navegação das Abas -->
    <nav class="sidebar-nav">
      <button class="sidebar-item active" id="tab-mode1" onclick="switchGameMode('mode1')" title="Modo 1: Blind Test">
        <span class="sidebar-icon-wrap">
          <img src="icons/headphone-symbol.png" class="app-icon icon-white" alt="Blind Test" />
        </span>
        <span class="sidebar-label">Modo 1: Blind Test</span>
      </button>

      <button class="sidebar-item" id="tab-mode2" onclick="switchGameMode('mode2')" title="Modo 2: Qual é a Abertura?">
        <span class="sidebar-icon-wrap">
          <img src="icons/vinyl.png" class="app-icon icon-white" alt="Qual é a Abertura" />
        </span>
        <span class="sidebar-label">Modo 2: Qual é a Abertura?</span>
      </button>

      <button class="sidebar-item" id="tab-mode3" onclick="switchGameMode('mode3')" title="Modo 3: Adivinhe a Cena">
        <span class="sidebar-icon-wrap">
          <img src="icons/clapperboard.png" class="app-icon icon-white" alt="Adivinhe a Cena" />
        </span>
        <span class="sidebar-label">Modo 3: Adivinhe a Cena</span>
      </button>

      <div class="sidebar-divider"></div>

      <button class="sidebar-item" id="tab-mode4" onclick="switchGameMode('mode4')" title="Salas Multiplayer (Ao Vivo)">
        <span class="sidebar-icon-wrap">
          <img src="icons/game-controller.png" class="app-icon icon-white" alt="Salas Multiplayer" />
        </span>
        <span class="sidebar-label">Salas Multiplayer</span>
      </button>

      <button class="sidebar-item" id="tab-mode5" onclick="switchGameMode('mode5')" title="Placar de Líderes (Top 50)">
        <span class="sidebar-icon-wrap">
          <img src="icons/crown.png" class="app-icon icon-gold" alt="Placar de Líderes" />
        </span>
        <span class="sidebar-label">Placar de Líderes</span>
      </button>

      <div class="sidebar-spacer"></div>

      <button class="sidebar-item" id="btn-sidebar-settings" onclick="openSettingsModal()" title="Configurações e Áudio">
        <span class="sidebar-icon-wrap">
          <img src="icons/settings.png" class="app-icon icon-white" alt="Configurações" />
        </span>
        <span class="sidebar-label">Configurações</span>
      </button>
    </nav>
  </aside>

  <!-- ÁREA CENTRAL DE JOGO (PARTE 2) -->
  <main class="app-main-content" id="app-main-content">
    <div class="container-center">

      <!-- Header Superior Compacto -->
      <header class="app-top-header">
        <div>
          <div style="display: flex; align-items: center; gap: 8px;">
            <h1 style="font-size: 16px; font-weight: 800; margin: 0; color: #fff;">Anime Music & Scene Quiz</h1>
            <span class="version-badge" style="font-size: 10px; padding: 2px 8px;">🎮 v3.1.0 • Arcade</span>
          </div>
          <p class="subtitle" style="font-size: 11px; margin: 2px 0 0 0; color: var(--text-muted);">
            Desafio interativo com 129 aberturas e 127 cenas reais. Ouça as músicas e teste seus conhecimentos!
          </p>
        </div>
        <button class="btn btn-outline" style="padding: 5px 12px; font-size: 11px;" onclick="openSettingsModal()">
          <img src="icons/settings.png" class="app-icon icon-white" alt="Settings" /> Configurações & Som
        </button>
      </header>

      <!-- Challenge Mode Banner -->
      <div class="challenge-banner" id="challenge-banner">
        ⚔️ <strong>MODO DUELO ATIVO!</strong> Você está jogando com a semente compartilhada. Seus amigos terão exatamente as mesmas rodadas!
      </div>

      <!-- Scoreboard KPIs (Montado dinamicamente no card ativo) -->
      <div class="scoreboard" id="main-scoreboard">
        <div class="score-card">
          <div class="score-label"><img src="icons/crown.png" class="app-icon icon-gold" /> Pontuação</div>
          <div class="score-val" id="kpi-score" style="color: var(--accent);">0</div>
        </div>
        <div class="score-card">
          <div class="score-label"><img src="icons/check.png" class="app-icon icon-raw" /> Acertos</div>
          <div class="score-val" id="kpi-correct" style="color: var(--green);">0</div>
        </div>
        <div class="score-card">
          <div class="score-label"><img src="icons/fire.png" class="app-icon icon-raw" /> Combo / Streak</div>
          <div class="score-val" id="kpi-streak" style="color: var(--gold);">0</div>
        </div>
        <div class="score-card">
          <div class="score-label"><img src="icons/vinyl.png" class="app-icon icon-white" /> Progresso</div>
          <div class="score-val" id="kpi-progress">1 / 100</div>
        </div>
      </div>

      <!-- Multiplayer In-Game HUD (Visível durante partidas em salas) -->
      <div class="mp-hud-bar" id="mp-hud-bar" style="display: none;">
        <div class="mp-hud-left">
          <span style="font-size: 13px; font-weight: 800; color: #38bdf8;" id="mp-hud-room-badge">
            <img src="icons/game-controller.png" class="app-icon icon-white" /> SALA
          </span>
          <span class="pill-chip" id="mp-hud-round-pill">Rodada 1 de 10</span>
          <span class="mp-hud-timer-pill" id="mp-hud-timer-pill" style="display: none;">⏱️ 25s</span>
        </div>

        <div class="mp-hud-scores" id="mp-hud-scores-list"></div>

        <div style="display: flex; gap: 8px; align-items: center;">
          <button class="mp-skip-btn" id="mp-skip-vote-btn" onclick="MultiplayerEngine.voteSkip()">
            <span><img src="icons/fast-forward.png" class="app-icon icon-white" /> Pular</span>
            <span class="pill-chip" id="mp-skip-count-badge" style="background: rgba(0,0,0,0.3); font-size: 11px;">0/1</span>
          </button>
          <button class="mp-leave-btn" id="mp-hud-leave-btn" onclick="MultiplayerEngine.confirmLeaveRoom()" title="Abandonar partida e voltar">
            <img src="icons/logout.png" class="app-icon icon-white" /> Sair
          </button>
        </div>
      </div>

      <!-- GAMEPLAY AREA COM RANKING LATERAL MULTIPLAYER -->
      <div class="gameplay-wrapper" id="gameplay-wrapper">
        <div id="floating-arcade-container" class="floating-arcade-container"></div>

        <div class="gameplay-main-col">
          <div id="mp-waiting-banner" class="mp-waiting-banner" style="display: none;"></div>\n"""

code = code[:top_target_start] + new_top_layout + code[top_target_end:]
print("2. Estrutura de App-Layout e Sidebar substituídas com sucesso!")

# ==============================================================================
# 3. REESTRUTURAR MODO 1 EM 2 COLUNAS
# ==============================================================================
m1_target_start = code.find('      <!-- VIEW 1: MODO 1 - BLIND TEST -->')
m2_target_start = code.find('  <!-- VIEW 2: MODO 2 - "QUAL É A ABERTURA?"')
if m1_target_start == -1 or m2_target_start == -1:
    print("ERRO: m1_target não encontrado!", m1_target_start, m2_target_start)
    sys.exit(1)

new_m1_layout = """      <!-- VIEW 1: MODO 1 - BLIND TEST -->
      <div class="quiz-card" id="mode1-view">
        <div class="quiz-header">
          <div class="round-indicator" id="m1-round-indicator">MÚSICA #1 DE 100</div>
          <button class="btn btn-outline" style="padding: 5px 12px; font-size: 11px;" onclick="openYouTubeDirect()">
            <img src="icons/play-button.png" class="app-icon icon-white" alt="Play" /> Clipe no YouTube
          </button>
        </div>
        <!-- Scoreboard Integrado do Modo 1 -->
        <div id="mode1-scoreboard-slot" class="mode-scoreboard-slot"></div>

        <!-- Grid 2-Colunas Desktop Zero-Scroll -->
        <div class="mode-split-grid">
          <!-- Coluna Esquerda: Player & Mídia -->
          <div class="mode-col-media">
            <div class="player-container" id="m1-player-container">
              <audio id="local-video-player" preload="auto" style="display: none;"></audio>
              <iframe id="video-frame" allow="autoplay; encrypted-media" style="display: none;"></iframe>
              <div class="player-visual-card" id="player-visual-card">
                <canvas id="m1-spectrum-canvas" class="audio-spectrum-canvas"></canvas>
                <div class="player-bg-art" id="player-bg-art"></div>
                <div class="player-scrim"></div>

                <!-- Blind Guessing View -->
                <div class="player-blind-content" id="player-blind-content">
                  <div class="vinyl" id="vinyl-icon">
                    <img src="icons/vinyl.png" class="app-icon-xl icon-white vinyl-spin-img" alt="Disco" />
                  </div>
                  <div style="margin-top: 10px; font-size: 12px; color: #94a3b8;" id="mask-status-text">
                    Modo Blind Test Ativo • Ouça e adivinhe o anime!
                  </div>
                </div>

                <!-- Revealed Answer View -->
                <div class="player-revealed-content" id="player-revealed-content" style="display: none;">
                  <div class="revealed-hero-row">
                    <img id="reveal-thumb-img" class="revealed-thumb-img" src="" alt="Capa" />
                    <div class="revealed-info-col">
                      <div class="revealed-badge" id="reveal-badge-status">
                        <img src="icons/check.png" class="app-icon icon-raw" /> RESPOSTA REVELADA
                      </div>
                      <div class="revealed-anime-title" id="reveal-anime-title">Nome do Anime</div>
                      <div class="revealed-song-name" id="reveal-song-name">"Nome da Música"</div>
                      <div class="revealed-artist-meta" id="reveal-artist-meta">por Artista (Ano) • Dificuldade</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Controles de Áudio -->
            <div class="player-controls-row">
              <div style="display: flex; gap: 8px;">
                <button class="btn btn-primary" id="btn-play-pause" onclick="togglePlay()">
                  <span id="play-btn-icon"><img src="icons/play-button.png" class="app-icon icon-white" alt="Play" /></span>
                  <span id="play-btn-text">Tocar Áudio</span>
                </button>
                <button class="btn btn-secondary" onclick="restartAudio()">
                  <img src="icons/circle-of-two-clockwise-arrows-rotation.png" class="app-icon icon-white" alt="Reiniciar" /> Reiniciar
                </button>
              </div>
              <button class="btn btn-gold" onclick="m1NextRandom()">
                <img src="icons/shuffle-arrows.png" class="app-icon icon-white" alt="Aleatória" /> Aleatória
              </button>
            </div>
          </div>

          <!-- Coluna Direita: Pistas, Input & Resposta -->
          <div class="mode-col-interactive">
            <!-- Pistas Reveláveis -->
            <div class="hints-section">
              <div class="hints-title">
                <img src="icons/open-padlock.png" class="app-icon icon-white" /> Pistas Reveláveis:
              </div>
              <div class="tags-container" id="tags-container"></div>
              <div style="margin-top: 8px;">
                <button class="btn btn-secondary" style="padding: 5px 12px; font-size: 11px;" onclick="revealNextTag()">
                  <img src="icons/padlock.png" class="app-icon icon-white" /> Revelar Próxima Pista (-10 pts)
                </button>
              </div>
            </div>

            <!-- Campo de Input & Autocomplete com Som Mecânico -->
            <div class="input-group">
              <div class="autocomplete-wrapper">
                <input type="text" class="quiz-input" id="guess-input" placeholder="Digite o anime... (TAB para enviar)" autocomplete="off" />
                <div class="autocomplete-dropdown" id="guess-autocomplete"></div>
              </div>
              <button class="btn btn-green" onclick="submitGuess()">
                <span>Enviar</span> <kbd style="background: rgba(0,0,0,0.35); border-radius: 4px; padding: 2px 6px; font-size: 11px; margin-left: 4px;">TAB ↵</kbd>
              </button>
            </div>

            <!-- Feedback Banner -->
            <div class="feedback-box" id="feedback-box"></div>

            <!-- Answer Box -->
            <div class="answer-card" id="answer-box">
              <div class="answer-layout">
                <img id="ans-poster-img" class="answer-poster-img" src="" alt="Capa" />
                <div>
                  <div class="answer-title" id="ans-anime">Nome do Anime</div>
                  <div class="answer-meta" id="ans-meta">Música • Artista</div>
                  <div class="answer-syns" id="ans-syns">Nomes aceitos: ...</div>
                </div>
              </div>
            </div>

            <!-- Navegação de Rodada -->
            <div class="nav-row" style="margin-top: auto;">
              <button class="btn btn-secondary" onclick="prevSong()">
                <img src="icons/fast-forward.png" class="app-icon icon-white icon-prev" alt="Anterior" /> Anterior
              </button>
              <button class="btn btn-outline" onclick="giveUpAndReveal()">
                <img src="icons/eye.png" class="app-icon icon-white" alt="Revelar" /> Revelar Resposta
              </button>
              <button class="btn btn-secondary" onclick="nextSong()">
                Próxima <img src="icons/fast-forward.png" class="app-icon icon-white" alt="Próxima" />
              </button>
            </div>
          </div>
        </div>
      </div><!-- fim mode1-view -->\n\n"""

code = code[:m1_target_start] + new_m1_layout + code[m2_target_start:]
print("3. Modo 1 atualizado com 2 Colunas e Ícones PNG!")

# ==============================================================================
# 4. ATUALIZAR ÍCONES NO MODO 2 E MODO 3
# ==============================================================================
code = code.replace("✅ Confirmar Escolha", '<img src="icons/check.png" class="app-icon icon-raw" /> Confirmar Escolha')
code = code.replace("Próxima Rodada ▶", 'Próxima Rodada <img src="icons/fast-forward.png" class="app-icon icon-white" />')
code = code.replace("🔀 Cena Aleatória", '<img src="icons/shuffle-arrows.png" class="app-icon icon-white" /> Cena Aleatória')
code = code.replace("🔍 Ampliar Cena", '<img src="icons/search.png" class="app-icon icon-white" /> Ampliar Cena')
code = code.replace("💡 Revelar Dica da Cena (-15 pts)", '<img src="icons/padlock.png" class="app-icon icon-white" /> Revelar Dica (-15 pts)')
code = code.replace("🏳️ Desistir e Ver Resposta", '<img src="icons/eye.png" class="app-icon icon-white" /> Ver Resposta')
code = code.replace("Próxima Cena ▶", 'Próxima Cena <img src="icons/fast-forward.png" class="app-icon icon-white" />')
print("4. Ícones dos Modos 2 e 3 substituídos!")

# ==============================================================================
# 5. REMOVER PARTE 3 (CATÁLOGO) E FECHAR APP-LAYOUT COM SETTINGS-MODAL
# ==============================================================================
# Localizar o fim do mode5-view até o Lightbox Modal
p_after_m5 = code.find('      </div>\n    </div>\n  </div><!-- fim mode5-view -->')
if p_after_m5 == -1:
    p_after_m5 = code.find('      </div>\n    </div>\n  </div>')

p_lightbox = code.find('<!-- Lightbox Modal -->')
if p_after_m5 == -1 or p_lightbox == -1:
    print("ERRO: Fim de mode5 ou lightbox não encontrado!", p_after_m5, p_lightbox)
    sys.exit(1)

# Encontrar o ponto de corte: logo após o fechamento de mode5-view
end_of_m5_div = code.find('</div>', p_after_m5) + 6

settings_modal_and_closes = """

    </div><!-- fim container-center -->
  </main><!-- fim app-main-content -->
</div><!-- fim app-layout -->

<!-- MODAL DE CONFIGURAÇÕES CENTRAL (ÁUDIO, SFX & ATALHOS) -->
<div class="settings-modal-overlay" id="settings-modal" onclick="if(event.target===this)closeSettingsModal()">
  <div class="settings-modal-card">
    <div class="settings-modal-header">
      <div class="settings-modal-title">
        <img src="icons/settings.png" class="app-icon icon-white" alt="Settings" /> Configurações & Áudio
      </div>
      <button class="settings-close-btn" onclick="closeSettingsModal()">&times;</button>
    </div>

    <!-- Popover container oculto para manter compatibilidade com testes legados -->
    <div id="audio-settings-popover" style="display: none;"></div>

    <!-- Canal BGM -->
    <div class="audio-channel-row" style="margin-bottom: 16px;">
      <div class="audio-channel-header">
        <span><img src="icons/volume-up.png" class="app-icon icon-white" /> Música de Fundo (BGM)</span>
        <span class="audio-channel-val" id="bgm-vol-text">80%</span>
      </div>
      <input type="range" class="audio-slider" id="bgm-vol-slider" min="0" max="1" step="0.05" value="0.8" oninput="AudioManager.setBgmVolume(this.value)" />
    </div>

    <!-- Canal SFX -->
    <div class="audio-channel-row" style="margin-bottom: 16px;">
      <div class="audio-channel-header">
        <span><img src="icons/volume.png" class="app-icon icon-white" /> Efeitos Sonoros (SFX)</span>
        <span class="audio-channel-val" id="sfx-vol-text">80%</span>
      </div>
      <input type="range" class="audio-slider" id="sfx-vol-slider" min="0" max="1" step="0.05" value="0.8" oninput="AudioManager.setSfxVolume(this.value)" />
    </div>

    <!-- Mute Geral -->
    <button class="audio-mute-toggle-btn" id="btn-mute-toggle" onclick="AudioManager.toggleMute()" style="margin-bottom: 18px; width: 100%;">
      <span id="mute-btn-icon"><img src="icons/sound-mute.png" class="app-icon icon-white" /></span>
      <span id="mute-btn-text">Mutar Todo o Jogo</span>
    </button>

    <!-- Guia de Atalhos Rápidos -->
    <div style="border-top: 1px solid rgba(255,255,255,0.08); padding-top: 14px;">
      <div style="font-size: 12px; font-weight: 800; color: #cbd5e1; margin-bottom: 8px;">⌨️ Atalhos do Teclado:</div>
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; font-size: 11px; color: var(--text-muted);">
        <div><kbd>TAB</kbd> Autocomplete / Enviar</div>
        <div><kbd>Espaço</kbd> Tocar / Pausar Som</div>
        <div><kbd>1</kbd>, <kbd>2</kbd>, <kbd>3</kbd> Opções no Modo 2</div>
        <div><kbd>Enter</kbd> Confirmar Seleção</div>
      </div>
    </div>
  </div>
</div>\n\n"""

# Substitui tudo entre o fim de mode5 e o lightbox (removendo Parte 3)
code = code[:end_of_m5_div] + settings_modal_and_closes + code[p_lightbox:]
print("5. Parte 3 removida e Modal de Configurações injetado!")

# ==============================================================================
# 6. CORRIGIR PLACAR DE LÍDERES (MODO 5) E ADICIONAR JS DE CONTROLE
# ==============================================================================
# 6A. In switchMpSubTab: garantir que nunca esconda lbPanel
old_subtab = """  if (tab === 'rooms') {
    if (roomsTab) roomsTab.classList.add('active');
    if (lbTab) lbTab.classList.remove('active');
    if (roomsPanel) roomsPanel.style.display = 'block';
    if (lbPanel) lbPanel.style.display = 'none';
  } else {"""

new_subtab = """  if (tab === 'rooms') {
    if (roomsTab) roomsTab.classList.add('active');
    if (lbTab) lbTab.classList.remove('active');
    if (roomsPanel) roomsPanel.style.display = 'block';
  } else {"""
code = code.replace(old_subtab, new_subtab)

# 6B. In switchGameMode: garantir que modo 5 sempre exiba lbPanel com display block
old_m5_switch = """  } else if (mode === 'mode5') {
    updateGlobalKPIs();
    renderLeaderboardTable('all');
    updateSaveScoreKPIs();
  }"""

new_m5_switch = """  } else if (mode === 'mode5') {
    updateGlobalKPIs();
    const lbPanel = document.getElementById('mp-leaderboard-panel');
    if (lbPanel) lbPanel.style.display = 'block';
    renderLeaderboardTable('all');
    updateSaveScoreKPIs();
  }"""
code = code.replace(old_m5_switch, new_m5_switch)

# 6C. Adicionar funções JS da modal e som de hover
js_functions = """
/* ==============================================================
   CONTROLES DO MODAL DE CONFIGURAÇÕES E SIDEBAR v3.1.0
   ============================================================== */
function openSettingsModal() {
  if (window.AudioManager) AudioManager.playSfx('click');
  const modal = document.getElementById('settings-modal');
  if (modal) modal.style.display = 'flex';
}
function closeSettingsModal() {
  if (window.AudioManager) AudioManager.playSfx('click');
  const modal = document.getElementById('settings-modal');
  if (modal) modal.style.display = 'none';
}
function toggleAudioSettingsPopover() {
  openSettingsModal();
}
function toggleSidebar() {
  const sidebar = document.getElementById('app-sidebar');
  if (sidebar) sidebar.classList.toggle('expanded');
}

// Microinteração de som no hover da barra lateral
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.sidebar-item').forEach(item => {
    item.addEventListener('mouseenter', () => {
      if (window.AudioManager) AudioManager.playSfx('hover');
    });
  });
});
"""

p_script_close = code.rfind("</script>")
code = code[:p_script_close] + js_functions + "\n" + code[p_script_close:]
print("6. Funções de controle, som no hover e fix do Placar de Líderes adicionadas!")

# Salvar arquivo gerador
with open(GEN_FILE, "w", encoding="utf-8") as f:
    f.write(code)

print(f"SUCESSO: generate_full_html.py salvo ({len(code)} bytes)!")
