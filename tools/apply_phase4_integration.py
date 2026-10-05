# -*- coding: utf-8 -*-
"""
Script de Integração Master da Etapa 4: Design Definitivo Bento Grid & Alta Dopamina
Supervisão e Integração por Antigravity
"""
import os
import re
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GEN_PATH = os.path.join(BASE_DIR, "tools", "generate_full_html.py")

with open(GEN_PATH, "r", encoding="utf-8") as f:
    code = f.read()

# 1. Carregar artefatos produzidos pelos subagentes
with open(os.path.join(BASE_DIR, "scratch", "bento_layout_spec.css"), "r", encoding="utf-8") as f:
    bento_css = f.read()

with open(os.path.join(BASE_DIR, "scratch", "dopamine_styles.css"), "r", encoding="utf-8") as f:
    dopamine_css = f.read()

with open(os.path.join(BASE_DIR, "scratch", "mobile_landscape.css"), "r", encoding="utf-8") as f:
    mobile_css = f.read()

with open(os.path.join(BASE_DIR, "scratch", "mobile_landscape_overlay.html"), "r", encoding="utf-8") as f:
    mobile_overlay_html = f.read()

with open(os.path.join(BASE_DIR, "scratch", "dopamine_microinteractions.js"), "r", encoding="utf-8") as f:
    dopamine_js = f.read()

with open(os.path.join(BASE_DIR, "scratch", "mobile_landscape.js"), "r", encoding="utf-8") as f:
    mobile_js = f.read()

print(f"Artefatos carregados ({len(bento_css) + len(dopamine_css) + len(mobile_css)} bytes de CSS). Iniciando integração...")

# ==============================================================================
# PASSO 1: INJEÇÃO DE CSS (BENTO GRID + DOPAMINA + MOBILE LANDSCAPE + BRIDGE)
# ==============================================================================
css_target = "  </style>\n</head>"
if css_target not in code:
    print("ERRO: css_target não encontrado no código!")
    sys.exit(1)

bridge_css = """
/* ==========================================================================
   ETAPA 4: BENTO GRID, DOPAMINE & MULTIPLAYER LIVE SIDEBAR BRIDGE CSS
   ========================================================================== */
#game-container, .container {
  width: 100% !important;
  max-width: 1560px !important;
  height: 100vh !important;
  max-height: 100vh !important;
  margin: 0 auto !important;
  padding: 8px 16px !important;
  box-sizing: border-box !important;
  display: flex !important;
  flex-direction: column !important;
  overflow: hidden !important;
}

html, body {
  width: 100vw !important;
  height: 100vh !important;
  max-height: 100vh !important;
  overflow: hidden !important;
  margin: 0 !important;
  padding: 0 !important;
  background: #080a14 !important;
  background: radial-gradient(130% 120% at 50% 0%, #101735 0%, #080c1a 55%, #04060c 100%) !important;
  color: #f8fafc !important;
  font-family: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif !important;
}

/* Header Bento */
.bento-header {
  display: flex !important;
  align-items: center !important;
  justify-content: space-between !important;
  gap: 12px !important;
  height: clamp(50px, 6.8vh, 60px) !important;
  min-height: clamp(50px, 6.8vh, 60px) !important;
  padding: 5px 14px !important;
  background: rgba(13, 20, 38, 0.85) !important;
  backdrop-filter: blur(16px) !important;
  -webkit-backdrop-filter: blur(16px) !important;
  border: 1px solid rgba(40, 56, 95, 0.6) !important;
  border-radius: 14px !important;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4) !important;
  margin-bottom: 6px !important;
  flex-shrink: 0 !important;
}

.bento-logo-block {
  display: flex !important;
  align-items: center !important;
  gap: 10px !important;
}

.bento-logo-icon-box {
  width: 34px !important;
  height: 34px !important;
  border-radius: 10px !important;
  background: linear-gradient(135deg, rgba(0, 240, 255, 0.25), rgba(139, 92, 246, 0.25)) !important;
  border: 1px solid rgba(0, 240, 255, 0.5) !important;
  box-shadow: 0 0 12px rgba(0, 240, 255, 0.3) !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  font-size: 17px !important;
}

.bento-logo-text-group {
  display: flex !important;
  flex-direction: column !important;
}

.bento-app-title {
  font-size: clamp(14px, 1.3vw, 17px) !important;
  font-weight: 900 !important;
  letter-spacing: -0.02em !important;
  color: #ffffff !important;
  margin: 0 !important;
  line-height: 1.1 !important;
  white-space: nowrap !important;
}

.bento-app-title .quiz-accent {
  background: linear-gradient(135deg, #00f0ff 0%, #8b5cf6 100%) !important;
  -webkit-background-clip: text !important;
  -webkit-text-fill-color: transparent !important;
}

.bento-app-subtitle {
  font-size: 10px !important;
  color: #94a3b8 !important;
  margin: 0 !important;
  white-space: nowrap !important;
}

/* 4 KPIs Bento Bar */
.bento-kpi-bar {
  display: flex !important;
  align-items: center !important;
  gap: 8px !important;
  flex: 1 !important;
  justify-content: center !important;
  max-width: 680px !important;
}

.bento-kpi-card {
  display: flex !important;
  align-items: center !important;
  gap: 8px !important;
  padding: 4px 12px !important;
  background: rgba(18, 27, 52, 0.7) !important;
  border: 1px solid rgba(50, 70, 115, 0.5) !important;
  border-radius: 10px !important;
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.05) !important;
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
  flex: 1 !important;
  min-width: 0 !important;
}

.bento-kpi-card:hover {
  transform: translateY(-2px) scale(1.02) !important;
  box-shadow: 0 4px 16px rgba(0, 240, 255, 0.25) !important;
}

.bento-kpi-card.kpi-score {
  border-color: rgba(0, 240, 255, 0.35) !important;
}
.bento-kpi-card.kpi-score .kpi-val-text {
  color: #00f0ff !important;
}

.bento-kpi-card.kpi-correct {
  border-color: rgba(16, 185, 129, 0.35) !important;
}
.bento-kpi-card.kpi-correct .kpi-val-text {
  color: #10b981 !important;
}

.bento-kpi-card.kpi-streak {
  border-color: rgba(245, 158, 11, 0.35) !important;
}
.bento-kpi-card.kpi-streak .kpi-val-text {
  color: #f59e0b !important;
}

.bento-kpi-card.kpi-progress {
  border-color: rgba(139, 92, 246, 0.35) !important;
}
.bento-kpi-card.kpi-progress .kpi-val-text {
  color: #c084fc !important;
}

.kpi-icon-badge {
  font-size: 15px !important;
  line-height: 1 !important;
  flex-shrink: 0 !important;
}

.kpi-data-col {
  display: flex !important;
  flex-direction: column !important;
  min-width: 0 !important;
  overflow: hidden !important;
}

.kpi-label-text {
  font-size: 9px !important;
  font-weight: 700 !important;
  text-transform: uppercase !important;
  letter-spacing: 0.05em !important;
  color: #94a3b8 !important;
  white-space: nowrap !important;
}

.kpi-val-text {
  font-size: clamp(12px, 1.2vw, 15px) !important;
  font-weight: 900 !important;
  font-variant-numeric: tabular-nums !important;
  white-space: nowrap !important;
}

/* Audio & Settings Pod */
.bento-audio-settings-box {
  display: flex !important;
  align-items: center !important;
  gap: 10px !important;
  position: relative !important;
  flex-shrink: 0 !important;
}

.bento-gear-btn {
  width: 32px !important;
  height: 32px !important;
  border-radius: 9px !important;
  background: rgba(20, 30, 58, 0.8) !important;
  border: 1px solid rgba(60, 80, 130, 0.6) !important;
  color: #cbd5e1 !important;
  font-size: 15px !important;
  cursor: pointer !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  transition: all 0.25s ease !important;
}

.bento-gear-btn:hover {
  transform: rotate(45deg) scale(1.08) !important;
  border-color: #00f0ff !important;
  box-shadow: 0 0 12px rgba(0, 240, 255, 0.4) !important;
  color: #00f0ff !important;
}

.bento-inline-sliders-col {
  display: flex !important;
  flex-direction: column !important;
  gap: 3px !important;
  width: 130px !important;
}

.bento-slider-row {
  display: flex !important;
  align-items: center !important;
  gap: 5px !important;
}

.slider-label {
  font-size: 9px !important;
  font-weight: 700 !important;
  color: #94a3b8 !important;
  width: 42px !important;
  white-space: nowrap !important;
}

.bento-neon-slider {
  flex: 1 !important;
  height: 4px !important;
  accent-color: #00f0ff !important;
  cursor: pointer !important;
  background: rgba(40, 55, 95, 0.8) !important;
  border-radius: 2px !important;
}

.bento-slider-pct {
  font-size: 9px !important;
  font-weight: 800 !important;
  color: #38bdf8 !important;
  width: 26px !important;
  text-align: right !important;
  font-variant-numeric: tabular-nums !important;
}

/* Mode Navigation Bar */
.bento-mode-nav-bar {
  display: flex !important;
  align-items: center !important;
  justify-content: space-between !important;
  height: clamp(34px, 4.2vh, 38px) !important;
  min-height: clamp(34px, 4.2vh, 38px) !important;
  background: rgba(11, 17, 34, 0.7) !important;
  border: 1px solid rgba(35, 50, 88, 0.5) !important;
  border-radius: 12px !important;
  padding: 2px 8px !important;
  margin-bottom: 6px !important;
  flex-shrink: 0 !important;
}

.bento-mode-pills-list {
  display: flex !important;
  align-items: center !important;
  gap: 6px !important;
  flex: 1 !important;
}

.bento-pill-tab {
  display: inline-flex !important;
  align-items: center !important;
  gap: 6px !important;
  padding: 4px 12px !important;
  font-size: clamp(11px, 1.05vw, 12px) !important;
  font-weight: 700 !important;
  color: #94a3b8 !important;
  background: transparent !important;
  border: 1px solid transparent !important;
  border-radius: 8px !important;
  cursor: pointer !important;
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
  white-space: nowrap !important;
}

.bento-pill-tab:hover {
  color: #ffffff !important;
  background: rgba(30, 45, 80, 0.5) !important;
  border-color: rgba(70, 95, 155, 0.4) !important;
  transform: translateY(-1px) scale(1.02) !important;
}

.bento-pill-tab.active {
  color: #ffffff !important;
  background: linear-gradient(135deg, rgba(0, 240, 255, 0.22) 0%, rgba(99, 102, 241, 0.25) 100%) !important;
  border: 1px solid rgba(0, 240, 255, 0.55) !important;
  box-shadow: 0 0 14px rgba(0, 240, 255, 0.3) !important;
}

.bento-arcade-grill {
  display: flex !important;
  align-items: center !important;
  gap: 4px !important;
  padding-right: 8px !important;
}

.bento-arcade-grill-slot {
  width: 14px !important;
  height: 4px !important;
  background: rgba(45, 60, 105, 0.5) !important;
  border-radius: 2px !important;
  transform: skewX(-20deg) !important;
}

/* Master Bento Grid (Stage + Sidebar) */
.bento-main-grid {
  display: grid !important;
  grid-template-columns: 1fr 310px !important;
  gap: 10px !important;
  flex: 1 1 0 !important;
  min-height: 0 !important;
  overflow: hidden !important;
}

.bento-stage-col {
  display: flex !important;
  flex-direction: column !important;
  min-height: 0 !important;
  overflow-y: auto !important;
  overflow-x: hidden !important;
  gap: 6px !important;
  padding-right: 2px !important;
}

/* Estilização dos Cards no Stage Bento */
.bento-stage-col .quiz-card {
  background: rgba(13, 20, 38, 0.82) !important;
  backdrop-filter: blur(14px) !important;
  -webkit-backdrop-filter: blur(14px) !important;
  border: 1px solid rgba(40, 56, 95, 0.6) !important;
  border-radius: 14px !important;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.45) !important;
  padding: 12px 16px !important;
  margin-bottom: 0 !important;
}

/* Live Ranking Sidebar Integrada no Bento */
.mp-live-sidebar {
  display: flex !important;
  flex-direction: column !important;
  background: rgba(13, 20, 38, 0.85) !important;
  backdrop-filter: blur(16px) !important;
  -webkit-backdrop-filter: blur(16px) !important;
  border: 1px solid rgba(40, 56, 95, 0.6) !important;
  border-radius: 14px !important;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.45) !important;
  padding: 10px !important;
  min-height: 0 !important;
  overflow: hidden !important;
  box-sizing: border-box !important;
}

.mp-sidebar-header {
  display: flex !important;
  align-items: center !important;
  justify-content: space-between !important;
  padding-bottom: 6px !important;
  border-bottom: 1px solid rgba(45, 60, 105, 0.4) !important;
  margin-bottom: 6px !important;
  flex-shrink: 0 !important;
}

.mp-sidebar-title {
  font-size: 13px !important;
  font-weight: 800 !important;
  color: #ffffff !important;
  display: flex !important;
  align-items: center !important;
  gap: 6px !important;
}

.bento-ranking-live-badge {
  display: flex !important;
  align-items: center !important;
  gap: 5px !important;
  font-size: 10px !important;
  font-weight: 800 !important;
  color: #34d399 !important;
  background: rgba(16, 185, 129, 0.15) !important;
  border: 1px solid rgba(16, 185, 129, 0.35) !important;
  border-radius: 10px !important;
  padding: 2px 8px !important;
}

.mp-sidebar-live-dot {
  width: 6px !important;
  height: 6px !important;
  border-radius: 50% !important;
  background: #34d399 !important;
  box-shadow: 0 0 8px #34d399 !important;
  animation: bentoLiveDotPulse 1.5s infinite !important;
}

@keyframes bentoLiveDotPulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.4; transform: scale(0.85); }
}

.mp-sidebar-list {
  flex: 1 1 0 !important;
  min-height: 0 !important;
  overflow-y: auto !important;
  overflow-x: hidden !important;
  display: flex !important;
  flex-direction: column !important;
  gap: 5px !important;
  padding-right: 4px !important;
}

.mp-sidebar-list::-webkit-scrollbar,
.bento-stage-col::-webkit-scrollbar {
  width: 4px !important;
}
.mp-sidebar-list::-webkit-scrollbar-thumb,
.bento-stage-col::-webkit-scrollbar-thumb {
  background: rgba(50, 70, 120, 0.6) !important;
  border-radius: 2px !important;
}

.mp-player-rank-item {
  display: flex !important;
  align-items: center !important;
  gap: 8px !important;
  padding: 5px 8px !important;
  background: rgba(18, 27, 52, 0.55) !important;
  border: 1px solid rgba(38, 54, 96, 0.4) !important;
  border-radius: 10px !important;
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
}

.mp-player-rank-item:hover {
  background: rgba(26, 38, 72, 0.8) !important;
  border-color: rgba(0, 240, 255, 0.4) !important;
  transform: translateX(2px) scale(1.01) !important;
}

.mp-player-rank-item.mp-first-place {
  background: linear-gradient(135deg, rgba(245, 158, 11, 0.15) 0%, rgba(20, 30, 58, 0.7) 100%) !important;
  border-color: rgba(245, 158, 11, 0.55) !important;
  box-shadow: 0 0 12px rgba(245, 158, 11, 0.2) !important;
}

.mp-rank-pos-badge {
  font-size: 13px !important;
  font-weight: 800 !important;
  width: 22px !important;
  text-align: center !important;
}

.mp-rank-avatar {
  width: 30px !important;
  height: 30px !important;
  border-radius: 50% !important;
  background: linear-gradient(135deg, #3b82f6, #8b5cf6) !important;
  border: 2px solid rgba(255, 255, 255, 0.2) !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  font-size: 13px !important;
  font-weight: 800 !important;
  color: #fff !important;
  flex-shrink: 0 !important;
}

.mp-player-rank-item.mp-first-place .mp-rank-avatar {
  border-color: #f59e0b !important;
  box-shadow: 0 0 10px rgba(245, 158, 11, 0.5) !important;
}

.mp-rank-info {
  flex: 1 !important;
  min-width: 0 !important;
  overflow: hidden !important;
}

.mp-rank-name {
  font-size: 12px !important;
  font-weight: 800 !important;
  color: #f8fafc !important;
  white-space: nowrap !important;
  overflow: hidden !important;
  text-overflow: ellipsis !important;
  display: flex !important;
  align-items: center !important;
  gap: 4px !important;
}

.mp-rank-stats {
  font-size: 10px !important;
  color: #94a3b8 !important;
  display: flex !important;
  align-items: center !important;
  gap: 6px !important;
}

.mp-player-status-badge {
  font-size: 9px !important;
  padding: 1px 5px !important;
  border-radius: 4px !important;
  font-weight: 700 !important;
}

.mp-player-status-badge.answered {
  background: rgba(16, 185, 129, 0.2) !important;
  color: #34d399 !important;
}

.mp-player-status-badge.thinking {
  background: rgba(245, 158, 11, 0.2) !important;
  color: #fbbf24 !important;
}

.mp-rank-points-col {
  text-align: right !important;
  flex-shrink: 0 !important;
}

.mp-rank-points {
  font-size: 13px !important;
  font-weight: 900 !important;
  color: #38bdf8 !important;
  font-variant-numeric: tabular-nums !important;
}

.mp-sidebar-footer {
  display: flex !important;
  align-items: center !important;
  justify-content: space-between !important;
  padding-top: 6px !important;
  border-top: 1px solid rgba(45, 60, 105, 0.4) !important;
  margin-top: 5px !important;
  font-size: 11px !important;
  color: #94a3b8 !important;
  flex-shrink: 0 !important;
}

.bento-ranking-footer-link {
  color: #38bdf8 !important;
  text-decoration: none !important;
  cursor: pointer !important;
  font-weight: 700 !important;
  font-size: 11px !important;
  transition: color 0.15s ease !important;
}

.bento-ranking-footer-link:hover {
  color: #7dd3fc !important;
  text-decoration: underline !important;
}

/* Emergency Panic Card Bento */
.bento-panic-card {
  background: rgba(22, 13, 28, 0.8) !important;
  border: 1px solid rgba(239, 68, 68, 0.45) !important;
  border-radius: 12px !important;
  padding: 6px 14px !important;
  box-shadow: 0 0 16px rgba(239, 68, 68, 0.2) !important;
  display: flex !important;
  align-items: center !important;
  justify-content: space-between !important;
  margin-top: 4px !important;
  flex-shrink: 0 !important;
}

.bento-panic-header {
  font-size: 11px !important;
  font-weight: 800 !important;
  color: #f87171 !important;
  display: flex !important;
  align-items: center !important;
  gap: 6px !important;
  text-transform: uppercase !important;
}

.bento-panic-center-row {
  display: flex !important;
  align-items: center !important;
  gap: 8px !important;
}

.bento-ecg-wave {
  font-family: var(--font-mono, monospace) !important;
  font-size: 11px !important;
  color: rgba(239, 68, 68, 0.5) !important;
  letter-spacing: 1px !important;
}

.bento-panic-timer-dial {
  font-size: 17px !important;
  font-weight: 900 !important;
  color: #ef4444 !important;
  font-variant-numeric: tabular-nums !important;
  background: rgba(239, 68, 68, 0.15) !important;
  border: 1px solid rgba(239, 68, 68, 0.4) !important;
  border-radius: 8px !important;
  padding: 2px 10px !important;
}

.bento-panic-footer-row {
  display: flex !important;
  align-items: center !important;
  gap: 12px !important;
}

.bento-panic-status-text {
  font-size: 11px !important;
  color: #cbd5e1 !important;
  display: flex !important;
  align-items: center !important;
  gap: 5px !important;
}

.bento-skip-vote-btn {
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.3), rgba(37, 99, 235, 0.4)) !important;
  border: 1px solid rgba(59, 130, 246, 0.6) !important;
  border-radius: 8px !important;
  color: #93c5fd !important;
  font-size: 11px !important;
  font-weight: 800 !important;
  padding: 4px 12px !important;
  cursor: pointer !important;
  display: flex !important;
  align-items: center !important;
  gap: 6px !important;
  transition: all 0.2s ease !important;
}

.bento-skip-vote-btn:hover {
  background: rgba(59, 130, 246, 0.5) !important;
  color: #ffffff !important;
  transform: translateY(-1px) scale(1.02) !important;
}

/* Bottom Row (Pódium da Semana & Próximas Novidades) */
.bento-bottom-row {
  display: grid !important;
  grid-template-columns: 1fr 310px !important;
  gap: 10px !important;
  height: clamp(80px, 12.5vh, 105px) !important;
  min-height: clamp(80px, 12.5vh, 105px) !important;
  margin-top: 6px !important;
  flex-shrink: 0 !important;
}

.bento-podium-card {
  display: flex !important;
  align-items: center !important;
  justify-content: space-between !important;
  padding: 6px 16px !important;
  background: rgba(13, 20, 38, 0.8) !important;
  backdrop-filter: blur(14px) !important;
  border: 1px solid rgba(40, 56, 95, 0.6) !important;
  border-radius: 14px !important;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4) !important;
  overflow: hidden !important;
}

.bento-podium-left-group {
  display: flex !important;
  flex-direction: column !important;
  gap: 4px !important;
}

.bento-podium-title-row {
  display: flex !important;
  align-items: center !important;
  gap: 6px !important;
  font-size: 12px !important;
  font-weight: 800 !important;
  color: #f59e0b !important;
}

.bento-podium-pillars-row {
  display: flex !important;
  align-items: flex-end !important;
  gap: 12px !important;
}

.bento-podium-pillar-col {
  display: flex !important;
  flex-direction: column !important;
  align-items: center !important;
  gap: 2px !important;
}

.bento-podium-avatar-wrap {
  width: 26px !important;
  height: 26px !important;
  border-radius: 50% !important;
  background: #1e293b !important;
  border: 1.5px solid rgba(255, 255, 255, 0.3) !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  font-size: 13px !important;
}

.bento-podium-avatar-wrap.gold {
  border-color: #fbbf24 !important;
  box-shadow: 0 0 10px rgba(251, 191, 36, 0.5) !important;
}
.bento-podium-avatar-wrap.silver {
  border-color: #cbd5e1 !important;
}
.bento-podium-avatar-wrap.bronze {
  border-color: #d97706 !important;
}

.bento-podium-step {
  padding: 1px 8px !important;
  border-radius: 4px !important;
  font-size: 10px !important;
  font-weight: 900 !important;
}

.bento-podium-step.rank-1 {
  background: linear-gradient(135deg, #fbbf24, #d97706) !important;
  color: #000 !important;
}
.bento-podium-step.rank-2 {
  background: #94a3b8 !important;
  color: #000 !important;
}
.bento-podium-step.rank-3 {
  background: #b45309 !important;
  color: #fff !important;
}

.bento-podium-subtext {
  font-size: 9px !important;
  color: #94a3b8 !important;
  font-weight: 700 !important;
  white-space: nowrap !important;
}

.bento-podium-quote-block {
  display: flex !important;
  align-items: center !important;
  gap: 12px !important;
  border-left: 1px solid rgba(45, 60, 105, 0.4) !important;
  padding-left: 16px !important;
  max-width: 320px !important;
}

.bento-podium-quote-text {
  font-size: 11px !important;
  font-style: italic !important;
  color: #cbd5e1 !important;
  margin: 0 !important;
  line-height: 1.3 !important;
}

.bento-podium-quote-author {
  font-size: 9px !important;
  color: #64748b !important;
  margin-top: 2px !important;
}

.bento-podium-silhouette-art {
  font-size: 24px !important;
  color: rgba(99, 102, 241, 0.4) !important;
  text-shadow: 0 0 15px rgba(99, 102, 241, 0.5) !important;
}

.bento-news-card {
  display: flex !important;
  flex-direction: column !important;
  justify-content: space-between !important;
  padding: 6px 12px !important;
  background: rgba(13, 20, 38, 0.8) !important;
  backdrop-filter: blur(14px) !important;
  border: 1px solid rgba(40, 56, 95, 0.6) !important;
  border-radius: 14px !important;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4) !important;
  overflow: hidden !important;
}

.bento-news-header {
  font-size: 11px !important;
  font-weight: 800 !important;
  color: #f59e0b !important;
  display: flex !important;
  align-items: center !important;
  gap: 5px !important;
}

.bento-news-list {
  list-style: none !important;
  padding: 0 !important;
  margin: 3px 0 !important;
  display: flex !important;
  flex-direction: column !important;
  gap: 2px !important;
}

.bento-news-list li {
  font-size: 10px !important;
  color: #cbd5e1 !important;
  display: flex !important;
  align-items: center !important;
  gap: 4px !important;
}

.bento-news-stay-tuned-btn {
  background: rgba(30, 45, 80, 0.6) !important;
  border: 1px solid rgba(70, 95, 155, 0.4) !important;
  border-radius: 6px !important;
  color: #93c5fd !important;
  font-size: 10px !important;
  font-weight: 700 !important;
  padding: 3px 8px !important;
  cursor: pointer !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  gap: 4px !important;
  transition: all 0.2s ease !important;
}

.bento-news-stay-tuned-btn:hover {
  background: rgba(59, 130, 246, 0.3) !important;
  color: #ffffff !important;
  border-color: #00f0ff !important;
}
"""

all_new_css = f"\n\n{bridge_css}\n\n{bento_css}\n\n{dopamine_css}\n\n{mobile_css}\n"
code = code.replace(css_target, f"{all_new_css}\n  </style>\n</head>")
print("Passo 1: CSS injetado com sucesso.")

# ==============================================================================
# PASSO 2: INJEÇÃO DO OVERLAY MOBILE LANDSCAPE APÓS <body>
# ==============================================================================
body_target = "<body>\n\n<!-- Canvas Global de Confetes & Partículas de Vitória -->"
if body_target not in code:
    print("ERRO: body_target não encontrado no código!")
    sys.exit(1)

new_body_start = f"<body>\n\n{mobile_overlay_html}\n\n<!-- Canvas Global de Confetes & Partículas de Vitória -->"
code = code.replace(body_target, new_body_start)
print("Passo 2: Overlay Mobile Landscape injetado com sucesso.")

# ==============================================================================
# PASSO 3: TRANSFORMAÇÃO DO HEADER E SCOREBOARD NO PADRÃO BENTO
# ==============================================================================
p_header_start = code.find('<div class="container">\n\n  <!-- Header -->')
p_header_end = code.find('  <!-- Multiplayer In-Game HUD (Visível apenas durante partidas multiplayer em salas) -->')

if p_header_start == -1 or p_header_end == -1:
    print("ERRO: Marcadores de Header não encontrados!")
    sys.exit(1)

old_header_chunk = code[p_header_start:p_header_end]

new_header_bento = """<div class="container bento-app-container" id="game-container">

  <!-- ====================================================================
       1. CABEÇALHO INTEGRADO (HEADER BENTO WIDESCREEN)
       ==================================================================== -->
  <header class="bento-header" id="bento-header">
    <!-- Logo & Título com Nota Musical Neon -->
    <div class="bento-logo-block">
      <div class="bento-logo-icon-box">
        <span class="neon-note-icon">🎵</span>
      </div>
      <div class="bento-logo-text-group">
        <h1 class="bento-app-title">Anime Music & Scene <span class="quiz-accent">Quiz</span></h1>
        <p class="bento-app-subtitle">Teste seus conhecimentos de anime!</p>
      </div>
    </div>

    <!-- Badge de Versão com Compatibilidade Retroativa v3.0.0 -->
    <div class="version-badge" style="display: inline-flex; align-items: center; padding: 3px 8px;">
      <span>🎮 v4.0.0 (upgrade de v3.0.0)</span> • <span>Bento Grid & Alta Dopamina</span>
    </div>

    <!-- 4 Cartões KPI de Vidro (Glassmorphism Neon) -->
    <div class="scoreboard bento-kpi-bar" id="main-scoreboard">
      <!-- KPI 1: Pontuação -->
      <div class="score-card bento-kpi-card kpi-score">
        <div class="kpi-icon-badge">🏆</div>
        <div class="kpi-data-col">
          <span class="score-label kpi-label-text">Pontuação</span>
          <span class="score-val kpi-val-text" id="kpi-score" style="color: var(--neon-cyan);">0</span>
        </div>
      </div>

      <!-- KPI 2: Acertos -->
      <div class="score-card bento-kpi-card kpi-correct">
        <div class="kpi-icon-badge">✅</div>
        <div class="kpi-data-col">
          <span class="score-label kpi-label-text">Acertos</span>
          <span class="score-val kpi-val-text" id="kpi-correct" style="color: var(--neon-green);">0</span>
        </div>
      </div>

      <!-- KPI 3: Combo Streak -->
      <div class="score-card bento-kpi-card kpi-streak">
        <div class="kpi-icon-badge">🔥</div>
        <div class="kpi-data-col">
          <span class="score-label kpi-label-text">Combo Streak</span>
          <span class="score-val kpi-val-text" id="kpi-streak" style="color: var(--neon-gold);">0</span>
        </div>
      </div>

      <!-- KPI 4: Progresso -->
      <div class="score-card bento-kpi-card kpi-progress">
        <div class="kpi-icon-badge">🚩</div>
        <div class="kpi-data-col">
          <span class="score-label kpi-label-text">Progresso</span>
          <span class="score-val kpi-val-text" id="kpi-progress">1 / 100</span>
        </div>
      </div>
    </div>

    <!-- Controles de Som & Configurações Integrados -->
    <div class="bento-audio-settings-box">
      <button class="bento-gear-btn audio-btn-toggle" id="btn-audio-settings" onclick="toggleAudioSettingsPopover()" title="Configurações de Áudio">
        ⚙️
      </button>

      <div class="bento-inline-sliders-col">
        <!-- BGM Slider Inline -->
        <div class="bento-slider-row">
          <span class="slider-label">🔊 BGM</span>
          <input type="range" class="audio-slider bento-neon-slider" id="bgm-vol-slider" min="0" max="1" step="0.05" value="0.8" oninput="AudioManager.setBgmVolume(this.value)" />
          <span class="audio-channel-val bento-slider-pct" id="bgm-vol-text">80%</span>
        </div>
        <!-- SFX Slider Inline -->
        <div class="bento-slider-row">
          <span class="slider-label">🔔 SFX</span>
          <input type="range" class="audio-slider bento-neon-slider" id="sfx-vol-slider" min="0" max="1" step="0.05" value="0.8" oninput="AudioManager.setSfxVolume(this.value)" />
          <span class="audio-channel-val bento-slider-pct" id="sfx-vol-text">80%</span>
        </div>
      </div>

      <!-- Audio Popover (Full controls & mute toggle) -->
      <div class="audio-settings-popover" id="audio-settings-popover">
        <div style="font-size: 13px; font-weight: 800; margin-bottom: 12px; color: #ffffff; display: flex; justify-content: space-between; align-items: center;">
          <span>🎧 Canais de Áudio</span>
          <span style="font-size: 10px; color: var(--accent); background: rgba(99,102,241,0.15); padding: 2px 6px; border-radius: 4px;">WebAudio</span>
        </div>
        <button class="audio-mute-toggle-btn" id="btn-mute-toggle" onclick="AudioManager.toggleMute()">
          <span id="mute-btn-icon">🔊</span> <span id="mute-btn-text">Mutar Todo o Jogo</span>
        </button>
      </div>
    </div>
  </header>

  <!-- Challenge Mode Banner -->
  <div class="challenge-banner" id="challenge-banner" style="display: none;">
    ⚔️ <strong>MODO DUELO ATIVO!</strong> Você está jogando com a semente compartilhada. Seus amigos terão exatamente as mesmas rodadas!
  </div>

  <!-- ====================================================================
       2. BARRA DE MODOS (PILL TABS NEON & ARCADE GRILL)
       ==================================================================== -->
  <nav class="mode-nav bento-mode-nav-bar" id="bento-mode-nav-bar">
    <div class="bento-mode-pills-list">
      <button class="mode-tab-btn bento-pill-tab active" id="tab-mode1" onclick="switchGameMode('mode1')">
        <span class="pill-icon">🎧</span> Modo 1: Blind Test
      </button>
      <button class="mode-tab-btn bento-pill-tab" id="tab-mode2" onclick="switchGameMode('mode2')">
        <span class="pill-icon">🎵</span> Modo 2: Qual é a Abertura?
      </button>
      <button class="mode-tab-btn bento-pill-tab" id="tab-mode3" onclick="switchGameMode('mode3')">
        <span class="pill-icon">🖼️</span> Modo 3: Adivinhe a Cena
      </button>
      <button class="mode-tab-btn bento-pill-tab" id="tab-mode4" onclick="switchGameMode('mode4')">
        <span class="pill-icon">🎮</span> Salas & Placar
      </button>
    </div>

    <!-- Arcade Ventilation Grill (Grelha estética arcade) -->
    <div class="bento-arcade-grill">
      <div class="bento-arcade-grill-slot"></div>
      <div class="bento-arcade-grill-slot"></div>
      <div class="bento-arcade-grill-slot"></div>
      <div class="bento-arcade-grill-slot"></div>
    </div>
  </nav>

"""

code = code[:p_header_start] + new_header_bento + code[p_header_end:]
print("Passo 3: Header e Scoreboard Bento transformados com sucesso.")

# ==============================================================================
# PASSO 4: ACOPLAMENTO DO PANIC CARD E LINHA INFERIOR
# ==============================================================================
gameplay_end_target = "</div><!-- fim .gameplay-wrapper -->"
if gameplay_end_target not in code:
    print("ERRO: gameplay_end_target não encontrado no código!")
    sys.exit(1)

# Inserir o Panic Card no final de .gameplay-main-col (antes de fechar gameplay-main-col)
stage_end_target = "</div><!-- fim .gameplay-main-col -->"
if stage_end_target not in code:
    print("ERRO: stage_end_target não encontrado!")
    sys.exit(1)

panic_card_html = """
      <!-- Card de Pânico e Timer Integrado no Centro-Inferior do Palco Bento -->
      <aside class="bento-panic-card" id="bento-panic-card" style="display: none;">
        <div class="bento-panic-header">
          <span class="bento-pulse-dot"></span> <span>⚠️ MODO PÂNICO</span>
        </div>
        <div class="bento-panic-center-row">
          <span class="bento-ecg-wave">&gt;&gt;&gt; —/\\/\\—</span>
          <div class="bento-panic-timer-dial" id="bento-panic-timer-dial">05s</div>
          <span class="bento-ecg-wave">—/\\/\\— &lt;&lt;&lt;</span>
        </div>
        <div class="bento-panic-footer-row">
          <div class="bento-panic-status-text" id="bento-panic-status-text">
            <span>⏳</span> <span>Aguardando jogadores...</span>
          </div>
          <button class="bento-skip-vote-btn mp-skip-btn" onclick="MultiplayerEngine.voteSkip()">
            <span>⏩ Pular</span>
          </button>
        </div>
      </aside>
"""

code = code.replace(stage_end_target, f"{panic_card_html}\n    {stage_end_target}")
print("Passo 4A: Panic Card acoplado com sucesso.")

# Inserir a Linha Inferior (Pódium da Semana & Novidades) antes de <!-- Full Table Overview -->
bottom_row_target = "  <!-- Full Table Overview -->\n  <div class="
if bottom_row_target not in code:
    print("ERRO: bottom_row_target não encontrado!")
    sys.exit(1)

new_bottom_section = """  <!-- ====================================================================
       4. LINHA INFERIOR (PÓDIUM DA SEMANA & PRÓXIMAS NOVIDADES)
       ==================================================================== -->
  <footer class="bento-bottom-row" id="arcade-spotlight-bar">
    <!-- PÓDIUM DA SEMANA -->
    <section class="bento-card bento-podium-card">
      <div class="bento-podium-left-group">
        <div class="bento-podium-title-row">
          <span>🏆</span> <span>PÓDIUM DA SEMANA</span>
          <span style="font-size: 11px; color: var(--text-muted); font-weight: 600;">• Melhores jogadores da semana</span>
        </div>

        <div class="bento-podium-pillars-row">
          <!-- 2º Lugar -->
          <div class="bento-podium-pillar-col">
            <div class="bento-podium-avatar-wrap silver">🐱</div>
            <div class="bento-podium-step rank-2">2</div>
            <span class="bento-podium-subtext">LunaCat • 1.385 pts</span>
          </div>

          <!-- 1º Lugar (Elevado & Dourado) -->
          <div class="bento-podium-pillar-col">
            <div class="bento-podium-avatar-wrap gold">👑</div>
            <div class="bento-podium-step rank-1">1 👑</div>
            <span class="bento-podium-subtext" style="color: #fde68a;">AkiraSensei • 1.480 pts</span>
          </div>

          <!-- 3º Lugar -->
          <div class="bento-podium-pillar-col">
            <div class="bento-podium-avatar-wrap bronze">⚔️</div>
            <div class="bento-podium-step rank-3">3</div>
            <span class="bento-podium-subtext">ZoroX • 1.275 pts</span>
          </div>
        </div>
      </div>

      <!-- Citação Inspiradora & Arte de Silhueta -->
      <div class="bento-podium-quote-block">
        <div>
          <p class="bento-podium-quote-text">
            "Todo grande otaku já foi um iniciante!"
          </p>
          <div class="bento-podium-quote-author">~ Anime Music & Scene Quiz</div>
        </div>
        <div class="bento-podium-silhouette-art">⚡</div>
      </div>
    </section>

    <!-- PRÓXIMAS NOVIDADES -->
    <aside class="bento-card bento-news-card">
      <div class="bento-news-header">
        <span>⭐</span> <span>PRÓXIMAS NOVIDADES</span>
      </div>
      <ul class="bento-news-list">
        <li><span>▶</span> Modo 4: Salas P2P ativas!</li>
        <li><span>▶</span> 129 Músicas + 127 Cenas HD</li>
        <li><span>▶</span> Sistema de conquistas e badges</li>
      </ul>
      <button class="bento-news-stay-tuned-btn" onclick="showToast('⭐ Novas atualizações toda semana!')">
        <span>🔔</span> <span>Fique ligado!</span>
      </button>
    </aside>
  </footer>

  <!-- Full Table Overview -->
  <div class="table-section" style="display: none;" """

code = code.replace(bottom_row_target, new_bottom_section)
print("Passo 4B: Linha Inferior (Pódium da Semana & Novidades) injetada com sucesso.")

# ==============================================================================
# PASSO 5: INJEÇÃO DOS SCRIPTS JS (DOPAMINE INTERACTIONS & MOBILE LANDSCAPE)
# ==============================================================================
js_target = "  renderCatalogTable();\n});\n</script>"
if js_target not in code:
    print("ERRO: js_target não encontrado no código!")
    sys.exit(1)

solo_leaderboard_js = """
// ==========================================================================
// ETAPA 4: POVOAMENTO DO RANKING LATERAL NO MODO SOLO / LOBBY (LOOK & FEEL MOCKUP)
// ==========================================================================
function renderSoloLeaderboardSidebar() {
  const sidebar = document.getElementById('mp-live-sidebar');
  const list = document.getElementById('mp-sidebar-list');
  if (!sidebar || !list) return;

  // Se partida multiplayer estiver ativa, MultiplayerEngine assume o controle
  if (window.MultiplayerEngine && MultiplayerEngine.isMatchActive) {
    return;
  }

  // Jogadores da semana exibidos de forma vibrante idêntico à imagem conceitual
  const weeklyTopOtakus = [
    { name: 'AkiraSensei 👑', score: 1480, hits: 10, rank: 1, delta: '+185 pts', answered: true, avatar: '👑' },
    { name: 'LunaCat', score: 1385, hits: 9, rank: 2, delta: null, answered: true, avatar: '🐱' },
    { name: 'ZoroX', score: 1275, hits: 8, rank: 3, delta: null, answered: false, avatar: '⚔️' },
    { name: 'Nico', score: 1240, hits: 8, rank: 4, delta: null, answered: true, avatar: '🌸' },
    { name: 'Rin', score: 1120, hits: 7, rank: 5, delta: null, answered: true, avatar: '🏹' },
    { name: 'Sora', score: 980, hits: 6, rank: 6, delta: null, answered: false, avatar: '🌌' },
    { name: 'Kaito', score: 945, hits: 6, rank: 7, delta: null, answered: true, avatar: '🎩' },
    { name: 'Yuki', score: 890, hits: 5, rank: 8, delta: null, answered: true, avatar: '❄️' }
  ];

  list.innerHTML = '';
  weeklyTopOtakus.forEach(p => {
    const medal = p.rank === 1 ? '🥇' : (p.rank === 2 ? '🥈' : (p.rank === 3 ? '🥉' : `${p.rank}`));
    const isFirst = (p.rank === 1);
    const statusBadge = p.answered 
      ? '<span class="mp-player-status-badge answered">✓ Answered</span>' 
      : '<span class="mp-player-status-badge thinking">⏳ Thinking...</span>';
    const deltaBadge = p.delta ? `<span class="mp-rank-delta" style="background: rgba(16,185,129,0.2); color: #34d399; font-size: 10px; padding: 1px 4px; border-radius: 4px; margin-left: 4px;">${p.delta}</span>` : '';

    const item = document.createElement('div');
    item.className = `mp-player-rank-item ${isFirst ? 'mp-first-place' : ''}`;
    item.innerHTML = `
      <div class="mp-rank-pos-badge">${medal}</div>
      <div class="mp-rank-avatar">${p.avatar}</div>
      <div class="mp-rank-info">
        <div class="mp-rank-name">
          <span class="mp-rank-name-text">${p.name}</span>
        </div>
        <div class="mp-rank-stats">
          <span>🎯 ${p.hits} acertos</span>
          ${statusBadge}
        </div>
      </div>
      <div class="mp-rank-points-col">
        <div class="mp-rank-points">${p.score} <span style="font-size: 9px; color: #94a3b8;">pts</span></div>
        ${deltaBadge}
      </div>
    `;
    list.appendChild(item);
  });
}
"""

audio_sfx_upgrade_js = """
// Suporte aprimorado para hover e streak em AudioManager
if (window.AudioManager) {
  const origPlaySfx = AudioManager.playSfx.bind(AudioManager);
  AudioManager.playSfx = function(type, param) {
    if (type === 'hover') {
      if (this.isMuted || this.sfxVolume <= 0.001) return;
      try {
        const AudioCtx = window.AudioContext || window.webkitAudioContext;
        if (!AudioCtx) return;
        if (!window._sfxCtx) window._sfxCtx = new AudioCtx();
        const ctx = window._sfxCtx;
        if (ctx.state === 'suspended') ctx.resume();
        const v = this.sfxVolume * 0.08;
        const t = ctx.currentTime;
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(1400, t);
        osc.frequency.exponentialRampToValueAtTime(1900, t + 0.035);
        gain.gain.setValueAtTime(v, t);
        gain.gain.exponentialRampToValueAtTime(0.0001, t + 0.035);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start(t);
        osc.stop(t + 0.04);
      } catch (e) {}
      return;
    }
    origPlaySfx(type);
  };
}
"""

dom_ready_enhancement = (
    '\n  renderCatalogTable();\n\n'
    '  // Inicialização dos Módulos da Etapa 4\n'
    + mobile_js + '\n\n'
    + dopamine_js + '\n\n'
    + audio_sfx_upgrade_js + '\n\n'
    + solo_leaderboard_js + '\n\n'
    '  if (typeof MobileLandscapeManager !== \'undefined\') {\n'
    '    MobileLandscapeManager.init();\n'
    '  }\n\n'
    '  if (typeof DopamineInteractions !== \'undefined\') {\n'
    '    DopamineInteractions.init();\n'
    '  }\n\n'
    '  renderSoloLeaderboardSidebar();\n'
    '});\n'
    '</script>'
)

code = code.replace(js_target, dom_ready_enhancement)
print('Passo 5: Módulos JavaScript da Etapa 4 injetados com sucesso.')
# ==============================================================================
# SALVAR O ARQUIVO tools/generate_full_html.py ATUALIZADO
# ==============================================================================
with open(GEN_PATH, "w", encoding="utf-8") as f:
    f.write(code)

print("SUCESSO: generate_full_html.py atualizado com a Etapa 4!")
