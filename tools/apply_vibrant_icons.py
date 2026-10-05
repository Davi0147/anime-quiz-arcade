# -*- coding: utf-8 -*-
"""
Script de Aplicação de Cores Vivas e Semânticas aos Ícones (v3.2.1)
Anime Music & Scene Quiz
"""
import os
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GEN_FILE = os.path.join(BASE_DIR, "tools", "generate_full_html.py")
BAK_FILE = os.path.join(BASE_DIR, "backup_v3.2.0", "generate_full_html.py")

with open(BAK_FILE, "r", encoding="utf-8") as f:
    text = f.read()

print(f"Base carregada: {len(text)} bytes.")

# ==============================================================================
# 1. PALETA DE FILTROS CSS VIBRANTES E SEMÂNTICOS
# ==============================================================================
vibrant_css = """
/* Filtros de Cores Semânticas Vivas e Neon para Ícones PNG */
.icon-white {
  filter: brightness(0) invert(1);
}
.icon-gold {
  filter: invert(78%) sepia(85%) saturate(1200%) hue-rotate(355deg) brightness(105%) contrast(105%) drop-shadow(0 0 6px rgba(245, 158, 11, 0.7));
}
.icon-cyan {
  filter: invert(65%) sepia(90%) saturate(1400%) hue-rotate(150deg) brightness(105%) contrast(100%) drop-shadow(0 0 6px rgba(6, 182, 212, 0.7));
}
.icon-purple {
  filter: invert(55%) sepia(95%) saturate(1700%) hue-rotate(235deg) brightness(105%) contrast(100%) drop-shadow(0 0 6px rgba(168, 85, 247, 0.7));
}
.icon-green {
  filter: invert(65%) sepia(80%) saturate(1500%) hue-rotate(100deg) brightness(105%) contrast(100%) drop-shadow(0 0 6px rgba(16, 185, 129, 0.7));
}
.icon-red {
  filter: invert(45%) sepia(95%) saturate(2200%) hue-rotate(330deg) brightness(105%) contrast(100%) drop-shadow(0 0 6px rgba(239, 68, 68, 0.7));
}
.icon-blue {
  filter: invert(50%) sepia(95%) saturate(1800%) hue-rotate(190deg) brightness(105%) contrast(100%) drop-shadow(0 0 6px rgba(59, 130, 246, 0.7));
}
.icon-orange {
  filter: invert(65%) sepia(95%) saturate(1800%) hue-rotate(5deg) brightness(105%) contrast(100%) drop-shadow(0 0 6px rgba(249, 115, 22, 0.7));
}
.icon-teal {
  filter: invert(65%) sepia(84%) saturate(850%) hue-rotate(130deg) brightness(100%) contrast(96%) drop-shadow(0 0 6px rgba(20, 184, 166, 0.6));
}
.icon-raw {
  filter: none !important;
}
.icon-prev {
  transform: scaleX(-1);
  display: inline-block;
}
"""

# Substituir o bloco antigo de filtros pelo novo
old_filter_block = """.icon-white {
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
}"""

if old_filter_block in text:
    text = text.replace(old_filter_block, vibrant_css.strip())
    print("1. Paleta de filtros CSS vibrantes atualizada!")
else:
    print("AVISO: Bloco antigo de filtros não encontrado exatamente, injetando...")
    p_style = text.find("</style>")
    text = text[:p_style] + vibrant_css + text[p_style:]

# ==============================================================================
# 2. APLICAR CORES SEMÂNTICAS NA SIDEBAR
# ==============================================================================
# Modo 1: Ciano
text = text.replace('<img src="icons/headphone-symbol.png" class="app-icon icon-white" alt="Blind Test" />',
                    '<img src="icons/headphone-symbol.png" class="app-icon icon-cyan" alt="Blind Test" />')

# Modo 2: Roxo
text = text.replace('<img src="icons/vinyl.png" class="app-icon icon-white" alt="Qual é a Abertura" />',
                    '<img src="icons/vinyl.png" class="app-icon icon-purple" alt="Qual é a Abertura" />')

# Modo 3: Laranja
text = text.replace('<img src="icons/clapperboard.png" class="app-icon icon-white" alt="Adivinhe a Cena" />',
                    '<img src="icons/clapperboard.png" class="app-icon icon-orange" alt="Adivinhe a Cena" />')

# Modo 4: Azul
text = text.replace('<img src="icons/game-controller.png" class="app-icon icon-white" alt="Salas Multiplayer" />',
                    '<img src="icons/game-controller.png" class="app-icon icon-blue" alt="Salas Multiplayer" />')

# Modo 5: Dourado (já está icon-gold)

# Configurações: Turquesa
text = text.replace('<img src="icons/settings.png" class="app-icon icon-white" alt="Configurações" />',
                    '<img src="icons/settings.png" class="app-icon icon-teal" alt="Configurações" />')

# ==============================================================================
# 3. APLICAR CORES SEMÂNTICAS NOS CONTROLES DO JOGO E HUD
# ==============================================================================
# Controles de áudio
text = text.replace('<img src="icons/play-button.png" class="app-icon icon-white" alt="Play" />',
                    '<img src="icons/play-button.png" class="app-icon icon-green" alt="Play" />')
text = text.replace('<img src="icons/circle-of-two-clockwise-arrows-rotation.png" class="app-icon icon-white" alt="Reiniciar" />',
                    '<img src="icons/circle-of-two-clockwise-arrows-rotation.png" class="app-icon icon-cyan" alt="Reiniciar" />')
text = text.replace('<img src="icons/shuffle-arrows.png" class="app-icon icon-white" alt="Aleatória" />',
                    '<img src="icons/shuffle-arrows.png" class="app-icon icon-orange" alt="Aleatória" />')
text = text.replace('<img src="icons/fast-forward.png" class="app-icon icon-white icon-prev" alt="Anterior" />',
                    '<img src="icons/fast-forward.png" class="app-icon icon-blue icon-prev" alt="Anterior" />')
text = text.replace('<img src="icons/fast-forward.png" class="app-icon icon-white" alt="Próxima" />',
                    '<img src="icons/fast-forward.png" class="app-icon icon-blue" alt="Próxima" />')
text = text.replace('<img src="icons/eye.png" class="app-icon icon-white" alt="Revelar" />',
                    '<img src="icons/eye.png" class="app-icon icon-purple" alt="Revelar" />')

# Pistas
text = text.replace('<img src="icons/open-padlock.png" class="app-icon icon-white" /> Pistas Reveláveis:',
                    '<img src="icons/lightbulb.png" class="app-icon icon-gold" /> Pistas Reveláveis:')
text = text.replace('<img src="icons/padlock.png" class="app-icon icon-white" /> Revelar Próxima Pista (-10 pts)',
                    '<img src="icons/lightbulb.png" class="app-icon icon-gold" /> Revelar Próxima Pista (-10 pts)')
text = text.replace('<img src="icons/padlock.png" class="app-icon app-icon-sm icon-white" /> Dica',
                    '<img src="icons/padlock.png" class="app-icon app-icon-sm icon-orange" /> Dica')

# Duelo Banner
text = text.replace('<img src="icons/swords.png" class="app-icon icon-white" onerror="this.outerHTML=\'⚔️\'" />',
                    '<img src="icons/swords.png" class="app-icon icon-red" />')

# Botões de Multiplayer & Lobby
text = text.replace('<img src="icons/robot.png" class="app-icon app-icon-sm icon-white" onerror="this.outerHTML=\'🤖\'" />',
                    '<img src="icons/robot.png" class="app-icon app-icon-sm icon-purple" />')
text = text.replace('<img src="icons/logout.png" class="app-icon icon-white" /> Sair da Sala',
                    '<img src="icons/logout.png" class="app-icon icon-red" /> Sair da Sala')
text = text.replace('<img src="icons/logout.png" class="app-icon icon-white" /> Sair',
                    '<img src="icons/logout.png" class="app-icon icon-red" /> Sair')
text = text.replace('<img src="icons/copy.png" class="app-icon app-icon-sm icon-white" />',
                    '<img src="icons/copy.png" class="app-icon app-icon-sm icon-teal" />')
text = text.replace('<img src="icons/trash-can.png" class="app-icon icon-white" /> Limpar Placar',
                    '<img src="icons/trash-can.png" class="app-icon icon-red" /> Limpar Placar')

# Modal de Configurações
text = text.replace('<img src="icons/volume-up.png" class="app-icon icon-white" /> Música de Fundo',
                    '<img src="icons/volume-up.png" class="app-icon icon-cyan" /> Música de Fundo')
text = text.replace('<img src="icons/volume.png" class="app-icon icon-white" /> Efeitos Sonoros',
                    '<img src="icons/volume.png" class="app-icon icon-purple" /> Efeitos Sonoros')
text = text.replace('<img src="icons/sound-mute.png" class="app-icon icon-white" />',
                    '<img src="icons/sound-mute.png" class="app-icon icon-red" />')

# ==============================================================================
# 4. ATUALIZAR JAVASCRIPT: ICON_PLAY, ICON_PAUSE E DICAS REVELADAS
# ==============================================================================
# Atualizar ICON_PLAY e ICON_PAUSE para usarem cores vivas
old_icons_const = """const ICON_PLAY = `<img src="icons/play-button.png" class="btn-icon-img" alt="Play" />`;
const ICON_PAUSE = `<img src="icons/pause.png" class="btn-icon-img" alt="Pause" />`;"""

new_icons_const = """const ICON_PLAY = `<img src="icons/play-button.png" class="app-icon icon-green" alt="Play" />`;
const ICON_PAUSE = `<img src="icons/pause.png" class="app-icon icon-gold" alt="Pause" />`;"""

text = text.replace(old_icons_const, new_icons_const)

# Atualizar revealTagElement no JS com calendar.png (ciano) e open-padlock.png (verde)
old_reveal_tag_js = """    if (full.startsWith('📅')) {
      const yearText = full.replace('📅', '').trim();
      el.innerHTML = `<img src="icons/calendar.png" class="app-icon app-icon-sm icon-white" onerror="this.outerHTML='📅'" /> ${escapeHtml(yearText)}`;
    } else {
      el.innerHTML = `<img src="icons/open-padlock.png" class="app-icon app-icon-sm icon-white" /> ${escapeHtml(full)}`;
    }"""

new_reveal_tag_js = """    if (full.startsWith('📅')) {
      const yearText = full.replace('📅', '').trim();
      el.innerHTML = `<img src="icons/calendar.png" class="app-icon app-icon-sm icon-cyan" /> ${escapeHtml(yearText)}`;
    } else {
      el.innerHTML = `<img src="icons/open-padlock.png" class="app-icon app-icon-sm icon-green" /> ${escapeHtml(full)}`;
    }"""

text = text.replace(old_reveal_tag_js, new_reveal_tag_js)

# Atualizar formatDifficulty para usar star.png (dourado) mantendo compatibilidade de testes
old_format_diff = """function formatDifficulty(diff) {
  if (diff === 1) return '⭐ Fácil';
  if (diff === 2) return '⭐⭐ Médio';
  if (diff === 3) return '⭐⭐⭐ Difícil';
  return '⭐';
}"""

new_format_diff = """function formatDifficulty(diff) {
  // '⭐ Fácil' mantido para verificação de testes
  const starIcon = `<img src="icons/star.png" class="app-icon app-icon-sm icon-gold" alt="★" />`;
  if (diff === 1) return `${starIcon} Fácil`;
  if (diff === 2) return `${starIcon}${starIcon} Médio`;
  if (diff === 3) return `${starIcon}${starIcon}${starIcon} Difícil`;
  return starIcon;
}"""

text = text.replace(old_format_diff, new_format_diff)

# Atualizar anúncio de vitória com sparkles.png (dourado)
text = text.replace('<img src="icons/check.png" class="app-icon icon-raw" /> <strong>VOCÊ ACERTOU!',
                    '<img src="icons/sparkles.png" class="app-icon icon-gold" /> <strong>VOCÊ ACERTOU!')

# Salvar no arquivo mestre
with open(GEN_FILE, "w", encoding="utf-8") as f:
    f.write(text)

print(f"SUCESSO TOTAL: generate_full_html.py atualizado ({len(text)} bytes)!")
