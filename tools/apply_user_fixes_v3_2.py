# -*- coding: utf-8 -*-
"""
Script de Aplicação das Correções do Usuário (v3.2.0)
- Alargamento da Sidebar (sem corte no Modo 2)
- Remoção completa de tooltips nativos (title=...)
- Anti-Jitter / Altura Fixa Estável no Modo 1 (sem pulos ao acertar/errar)
- Modo 2: Apenas ícone de Play/Pause nos cards (sem texto Ouvir/Continuar/Pausar)
- Remoção do botão de Configurações do cabeçalho superior
- Ranking ao vivo Multiplayer expandido para 290px (sem espremer Respondido/Pensando)
- Bloqueio de troca de abas durante partida ou sala multijogador ativa
- Substituição massiva de emojis por ícones PNG e sistema de detecção automática
"""
import os
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GEN_FILE = os.path.join(BASE_DIR, "tools", "generate_full_html.py")
BAK_FILE = os.path.join(BASE_DIR, "backup_v3.1.0", "generate_full_html.py")

with open(BAK_FILE, "r", encoding="utf-8") as f:
    text = f.read()

print(f"Base carregada: {len(text)} bytes.")

# ==============================================================================
# 1. SIDEBAR: ALARGAR PARA 260px E REMOVER TOOLTIPS (TITLE=...)
# ==============================================================================
text = text.replace("--sidebar-w-expanded: 230px;", "--sidebar-w-expanded: 260px;")

# Remover atributos title dos itens da sidebar
text = text.replace(' title="Modo 1: Blind Test"', '')
text = text.replace(' title="Modo 2: Qual é a Abertura?"', '')
text = text.replace(' title="Modo 3: Adivinhe a Cena"', '')
text = text.replace(' title="Salas Multiplayer (Ao Vivo)"', '')
text = text.replace(' title="Placar de Líderes (Top 50)"', '')
text = text.replace(' title="Configurações e Áudio"', '')
text = text.replace(' title="Expandir/Recolher Menu"', '')

# Adicionar padding extra e prevenir quebra no label da sidebar
text = text.replace('.sidebar-label {\n  font-size: 13px;\n  font-weight: 600;\n  opacity: 0;',
                    '.sidebar-label {\n  font-size: 13px;\n  font-weight: 600;\n  opacity: 0;\n  padding-right: 14px;\n  white-space: nowrap;')

print("1. Sidebar alargada para 260px e tooltips removidos com sucesso!")

# ==============================================================================
# 2. CABEÇALHO SUPERIOR: REMOVER BOTÃO DE CONFIGURAÇÕES (DEIXAR SÓ NA SIDEBAR)
# ==============================================================================
old_top_btn = """        <button class="btn btn-outline" style="padding: 5px 12px; font-size: 11px;" onclick="openSettingsModal()">
          <img src="icons/settings.png" class="app-icon icon-white" alt="Settings" /> Configurações & Som
        </button>"""

if old_top_btn in text:
    text = text.replace(old_top_btn, "")
    print("2. Botão de configurações do topo removido!")
else:
    # Fallback caso haja pequenas variações de whitespace
    text = re.sub(r'<button class="btn btn-outline"[^>]*onclick="openSettingsModal\(\)"[^>]*>.*?Configurações & Som.*?</button>', '', text, flags=re.DOTALL)
    print("2. Botão de configurações do topo removido via regex!")

# ==============================================================================
# 3. MODO 1: ANTI-JITTER & ESTABILIDADE ABSOLUTA DE ALTURA
# ==============================================================================
# Estilizar mode-split-grid, mode-col-interactive e criar slot fixo para o resultado
old_split_css = """.mode-split-grid {
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
}"""

new_split_css = """.mode-split-grid {
  display: grid;
  grid-template-columns: 1fr 1.15fr;
  gap: 18px;
  align-items: stretch;
  min-height: 510px;
}
.mode-col-media {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 12px;
  height: 100%;
}
.mode-col-interactive {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 10px;
  height: 100%;
  min-height: 510px;
}
.m1-result-slot {
  min-height: 135px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 8px;
  transition: all 0.3s ease;
}
.hints-section {
  min-height: 105px;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
}
.tags-container {
  min-height: 38px;
}
.answer-card {
  max-height: 110px;
  overflow: hidden;
  margin-top: 4px;
}"""

text = text.replace(old_split_css, new_split_css)

# Envolver feedback-box e answer-box no slot fixo m1-result-slot no HTML
old_m1_boxes = """        <!-- Feedback Banner -->
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
        </div>"""

new_m1_boxes = """        <!-- Slot Fixo de Resultado Anti-Jitter (Impede o redimensionamento do card) -->
        <div class="m1-result-slot" id="m1-result-slot">
          <div class="feedback-box" id="feedback-box" style="margin: 0;"></div>
          <div class="answer-card" id="answer-box" style="margin: 0;">
            <div class="answer-layout">
              <img id="ans-poster-img" class="answer-poster-img" src="" alt="Capa" />
              <div>
                <div class="answer-title" id="ans-anime">Nome do Anime</div>
                <div class="answer-meta" id="ans-meta">Música • Artista</div>
                <div class="answer-syns" id="ans-syns">Nomes aceitos: ...</div>
              </div>
            </div>
          </div>
        </div>"""

text = text.replace(old_m1_boxes, new_m1_boxes)
print("3. Modo 1 configurado com slot estável anti-jitter!")

# ==============================================================================
# 4. MODO 2: BOTÕES COM APENAS ÍCONE (SEM TEXTO OUVI/CONTINUAR/PAUSAR)
# ==============================================================================
# No HTML do Modo 2:
text = text.replace('<span id="m2-icon-0"><img src="icons/play-button.png" class="btn-icon-img" alt="Play" /></span> <span id="m2-txt-0">Ouvir</span>',
                    '<span id="m2-icon-0"><img src="icons/play-button.png" class="app-icon icon-white" alt="Play" /></span>')
text = text.replace('<span id="m2-icon-1"><img src="icons/play-button.png" class="btn-icon-img" alt="Play" /></span> <span id="m2-txt-1">Ouvir</span>',
                    '<span id="m2-icon-1"><img src="icons/play-button.png" class="app-icon icon-white" alt="Play" /></span>')
text = text.replace('<span id="m2-icon-2"><img src="icons/play-button.png" class="btn-icon-img" alt="Play" /></span> <span id="m2-txt-2">Ouvir</span>',
                    '<span id="m2-icon-2"><img src="icons/play-button.png" class="app-icon icon-white" alt="Play" /></span>')

# No CSS do card-play-btn: transformá-lo num botão circular moderno
text = text.replace('.card-play-btn {\n      display: flex;\n      align-items: center;\n      gap: 6px;',
                    '.card-play-btn {\n      display: flex;\n      align-items: center;\n      justify-content: center;\n      width: 38px;\n      height: 38px;\n      min-width: 38px;\n      border-radius: 50%;\n      padding: 0;')

# No JavaScript do Modo 2: remover inserção de texto
text = text.replace("document.getElementById(`m2-txt-${idx}`).textContent = 'Continuar';", "// texto removido conforme solicitado")
text = text.replace("document.getElementById(`m2-txt-${idx}`).textContent = 'Pausar';", "// texto removido conforme solicitado")
text = text.replace("document.getElementById(`m2-txt-${i}`).textContent = 'Ouvir';", "// texto removido conforme solicitado")
print("4. Modo 2 configurado apenas com ícones de áudio!")

# ==============================================================================
# 5. MULTIPLAYER: RANKING AO VIVO EXPANDIDO (SEM ESPREMER PENSANDO/RESPONDIDO)
# ==============================================================================
text = text.replace('.mp-live-sidebar {\n      width: 260px;', '.mp-live-sidebar {\n      width: 290px;')

# Atualizar .mp-rank-stats para quebrar e alinhar com folga
old_stats_css = """.mp-player-status-badge {
      display: inline-flex;
      align-items: center;
      gap: 4px;
      font-size: 10px;
      font-weight: 700;
      padding: 2px 7px;
      border-radius: 999px;
    }"""

new_stats_css = """.mp-rank-stats {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 6px;
      font-size: 11px;
      margin-top: 4px;
      width: 100%;
    }
    .mp-player-status-badge {
      display: inline-flex;
      align-items: center;
      gap: 4px;
      font-size: 10px;
      font-weight: 700;
      padding: 2px 8px;
      border-radius: 999px;
      white-space: nowrap;
      flex-shrink: 0;
    }"""

text = text.replace(old_stats_css, new_stats_css)

# No JS de renderLiveSidebar: usar ícones oficiais em vez de emojis
old_badges_js = """      const statusBadge = hasAnswered 
        ? '<span class="mp-player-status-badge answered">✅ Respondeu</span>' 
        : '<span class="mp-player-status-badge thinking">🤔 Pensando...</span>';"""

new_badges_js = """      const statusBadge = hasAnswered 
        ? '<span class="mp-player-status-badge answered"><img src="icons/check.png" class="app-icon app-icon-sm icon-raw" /> Respondido</span>' 
        : '<span class="mp-player-status-badge thinking"><img src="icons/shuffle-arrows.png" class="app-icon app-icon-sm icon-white" /> Pensando...</span>';"""

text = text.replace(old_badges_js, new_badges_js)
text = text.replace("<span>🎯 ${p.correct || 0} acertos</span>",
                    "<span><img src=\"icons/check.png\" class=\"app-icon app-icon-sm icon-raw\" /> ${p.correct || 0} acertos</span>")
print("5. Ranking ao vivo Multiplayer expandido e desespremido!")

# ==============================================================================
# 6. BLOQUEIO DE TROCA DE ABAS DURANTE PARTIDA MULTIPLAYER ATIVA
# ==============================================================================
old_switch_start = """function switchGameMode(mode) {
  stopAllMedia();
  AudioManager.playSfx('tab');
  activeGameMode = mode;"""

new_switch_start = """function switchGameMode(mode) {
  if (window.MultiplayerEngine) {
    if (MultiplayerEngine.isMatchActive) {
      showToast('⚠️ Você está em uma partida ativa! Saia da sala antes de mudar de modo.');
      if (window.AudioManager) AudioManager.playSfx('wrong');
      return;
    }
    if (MultiplayerEngine.roomCode) {
      if (mode !== 'mode4') {
        showToast('⚠️ Você já está em uma sala ativa! Saia da sala antes de trocar de modo.');
        if (window.AudioManager) AudioManager.playSfx('wrong');
        return;
      } else if (activeGameMode === 'mode4') {
        // Já está no modo de salas dentro de um lobby, não reinicializa
        return;
      }
    }
  }

  stopAllMedia();
  AudioManager.playSfx('tab');
  activeGameMode = mode;"""

text = text.replace(old_switch_start, new_switch_start)
print("6. Bloqueio de troca de modo em partidas/salas ativas implementado!")

# ==============================================================================
# 7. SISTEMA DE ÍCONES DINÂMICOS & SUBSTITUIÇÃO DE EMOJIS
# ==============================================================================
# Substituição nas dicas do Modo 1: usar padlock.png e open-padlock.png
text = text.replace("t.textContent = `🔒 Dica ${idx + 1}`;",
                    't.innerHTML = `<img src="icons/padlock.png" class="app-icon app-icon-sm icon-white" /> Dica ${idx + 1}`;')

old_reveal_tag = """function revealTagElement(el) {
  if (!el.classList.contains('revealed')) {
    el.classList.add('revealed');
    el.textContent = el.dataset.fullText;
    m1RevealedTagsCount++;
    AudioManager.playSfx('hint');
  }
}"""

new_reveal_tag = """function revealTagElement(el) {
  if (!el.classList.contains('revealed')) {
    el.classList.add('revealed');
    let full = el.dataset.fullText || '';
    if (full.startsWith('📅')) {
      const yearText = full.replace('📅', '').trim();
      el.innerHTML = `<img src="icons/calendar.png" class="app-icon app-icon-sm icon-white" onerror="this.outerHTML='📅'" /> ${escapeHtml(yearText)}`;
    } else {
      el.innerHTML = `<img src="icons/open-padlock.png" class="app-icon app-icon-sm icon-white" /> ${escapeHtml(full)}`;
    }
    m1RevealedTagsCount++;
    AudioManager.playSfx('hint');
  }
}"""

text = text.replace(old_reveal_tag, new_reveal_tag)

# Ícones nos Banners de Feedback
text = text.replace("🎉 <strong>VOCÊ ACERTOU!", '<img src="icons/check.png" class="app-icon icon-raw" /> <strong>VOCÊ ACERTOU!')
text = text.replace("❌ <strong>RESPOSTA REVELADA!</strong>", '<img src="icons/remove.png" class="app-icon icon-raw" /> <strong>RESPOSTA REVELADA!</strong>')
text = text.replace("ansAnime.innerHTML = isCorrect ? `🎉 ${song.anime}` : `❌ Resposta: ${song.anime}`;",
                    'ansAnime.innerHTML = isCorrect ? `<img src="icons/check.png" class="app-icon icon-raw" /> ${song.anime}` : `<img src="icons/remove.png" class="app-icon icon-raw" /> Resposta: ${song.anime}`;')

# Ícones de ação no lobby multiplayer
text = text.replace('🤖 Adicionar Bot de Teste', '<img src="icons/robot.png" class="app-icon app-icon-sm icon-white" onerror="this.outerHTML=\'🤖\'" /> Adicionar Bot de Teste')
text = text.replace('🚪 Sair da Sala', '<img src="icons/logout.png" class="app-icon icon-white" /> Sair da Sala')
text = text.replace('🔥 INICIAR PARTIDA AGORA!', '<img src="icons/fire.png" class="app-icon icon-raw" /> INICIAR PARTIDA AGORA!')
text = text.replace('🗑️ Limpar Placar', '<img src="icons/trash-can.png" class="app-icon icon-white" /> Limpar Placar')
text = text.replace('📋</span>', '<img src="icons/copy.png" class="app-icon app-icon-sm icon-white" /></span>')

# Duelo Banner
text = text.replace('⚔️ <strong>MODO DUELO ATIVO!</strong>', '<img src="icons/swords.png" class="app-icon icon-white" onerror="this.outerHTML=\'⚔️\'" /> <strong>MODO DUELO ATIVO!</strong>')

print("7. Emojis substituídos por ícones e sistema de fallback dinâmico configurado!")

# ==============================================================================
# SALVAR ARQUIVO MESTRE
# ==============================================================================
with open(GEN_FILE, "w", encoding="utf-8") as f:
    f.write(text)

print(f"SUCESSO TOTAL: generate_full_html.py atualizado ({len(text)} bytes)!")
