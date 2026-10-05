# -*- coding: utf-8 -*-
"""
Script de Construção da Versão v3.1.0 (Arcade Widescreen & Ícones PNG)
Anime Music & Scene Quiz
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

print("Base v3.0.0 carregada com sucesso:", len(code), "bytes.")

# ==============================================================================
# 1. REMOVER PARTE 3: CATÁLOGO COMPLETO (100 ABERTURAS)
# ==============================================================================
cat_start = code.find("  <!-- Full Table Overview -->")
if cat_start == -1:
    cat_start = code.find('<div class="table-section">')

if cat_start != -1:
    cat_end = code.find("  <!-- Lightbox Modal -->")
    if cat_end != -1:
        # Remover a seção da tabela mantendo o fechamento do container se necessário
        code = code[:cat_start] + code[cat_end:]
        print("1. Parte 3 (Catálogo Completo) removida com sucesso!")
    else:
        print("AVISO: cat_end não encontrado!")
else:
    print("AVISO: cat_start não encontrado!")

# ==============================================================================
# 2. CSS PARA ÍCONES, SIDEBAR MINI-RAIL, BOTTOM NAV E GRID 2-COLUNAS
# ==============================================================================
new_styles = """
/* ==============================================================
   ESTILOS v3.1.0: ÍCONES PNG, SIDEBAR RETRÁTIL & LAYOUT WIDESCREEN
   ============================================================== */
:root {
  --sidebar-w: 68px;
  --sidebar-w-expanded: 230px;
}

/* Ícones do Aplicativo via PNG */
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
.app-icon-xl { width: 34px; height: 34px; }

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
  transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  overflow-x: hidden;
  box-shadow: 4px 0 24px rgba(0, 0, 0, 0.5);
}

.app-sidebar:hover,
.app-sidebar.expanded {
  width: var(--sidebar-w-expanded);
}

.sidebar-header {
  height: 64px;
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
  font-size: 14px;
  font-weight: 800;
  letter-spacing: 0.5px;
  color: #fff;
  white-space: nowrap;
  opacity: 0;
  transition: opacity 0.25s ease;
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
  padding: 14px 10px;
  flex: 1;
}

.sidebar-item {
  position: relative;
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 12px 14px;
  border-radius: 12px;
  background: transparent;
  border: 1px solid transparent;
  color: #94a3b8;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  text-align: left;
  white-space: nowrap;
  user-select: none;
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
  background: rgba(99, 102, 241, 0.14);
  color: #ffffff;
  border-color: rgba(99, 102, 241, 0.35);
  transform: translateX(3px) scale(1.02);
  box-shadow: 0 4px 16px rgba(99, 102, 241, 0.25);
}
.sidebar-item:hover .sidebar-icon-wrap .app-icon {
  filter: brightness(0) invert(1) drop-shadow(0 0 6px #38bdf8);
  transform: scale(1.2);
}

.sidebar-item.active {
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.28), rgba(168, 85, 247, 0.22));
  border-color: #6366f1;
  color: #ffffff;
  font-weight: 700;
  box-shadow: 0 0 16px rgba(99, 102, 241, 0.35);
}
.sidebar-item.active .sidebar-icon-wrap .app-icon {
  filter: brightness(0) invert(1) drop-shadow(0 0 8px #818cf8);
}

.sidebar-divider {
  height: 1px;
  background: rgba(255, 255, 255, 0.08);
  margin: 8px 4px;
}

.sidebar-spacer {
  flex: 1;
}

/* ÁREA CENTRAL PRINCIPAL */
.app-main-content {
  flex: 1;
  margin-left: var(--sidebar-w);
  padding: 16px 24px;
  min-height: 100vh;
  box-sizing: border-box;
  transition: margin-left 0.3s cubic-bezier(0.4, 0, 0.2, 1);
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
  margin-bottom: 14px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
  padding: 10px 16px;
  background: rgba(15, 23, 42, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 14px;
}
.app-top-header h1 {
  font-size: 18px;
  margin: 0;
  font-weight: 800;
  display: flex;
  align-items: center;
  gap: 10px;
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
  gap: 12px;
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

/* BOTTOM NAVIGATION BAR PARA MOBILE */
@media (max-width: 900px) {
  .app-sidebar {
    top: auto;
    bottom: 0;
    left: 0;
    right: 0;
    width: 100% !important;
    height: 64px;
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
    padding: 12px 10px 80px 10px; /* espaço inferior para o bottom bar */
  }
  .mode-split-grid {
    grid-template-columns: 1fr;
    gap: 14px;
  }
}
"""

# Inserir new_styles logo antes de </style>
style_close_idx = code.find("</style>")
if style_close_idx != -1:
    code = code[:style_close_idx] + new_styles + code[style_close_idx:]
    print("2. Novos estilos de layout e ícones injetados com sucesso!")
else:
    print("ERRO: </style> não encontrado!")

# ==============================================================================
# Salvar e validar
# ==============================================================================
with open(GEN_FILE, "w", encoding="utf-8") as f:
    f.write(code)

print("Etapa 1 e 2 aplicadas com sucesso em generate_full_html.py!")
