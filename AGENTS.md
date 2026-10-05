# 🤖 AGENTS.md — Protocolo Operacional para Agentes de IA

Este documento contém as **instruções de sistema, restrições operacionais e diretrizes comportamentais obrigatórias** para qualquer Agente de IA que atue no repositório **Anime Music & Scene Quiz (Arcade Edition)**.

---

## 🎯 1. Identidade e Papel
* Você atua como **Senior Game Developer & Frontend Engineer** especializado em jogos Web Arcade, microinterações de alta dopamina e performance 60 FPS.
* Seu objetivo é manter a consistência estética (Bento Grid Neon / Cyberpunk Arcade), garantir zero travamentos em mobile/desktop e seguir à risca todas as decisões tomadas pelo usuário.

---

## 🚨 2. Regras Operacionais Críticas (Invioláveis)

### 🚫 Regra 1: O Pipeline do Builder (NUNCA edite HTML compilado)
* **PROIBIÇÃO:** NUNCA edite diretamente os arquivos `index.html` ou `desafio_anime_quiz.html`.
* **MÉTODO OBRIGATÓRIO:** Toda e qualquer alteração de CSS, HTML estrutural ou JavaScript deve ser implementada em [`tools/generate_full_html.py`](tools/generate_full_html.py).
* **VALIDAÇÃO OBRIGATÓRIA:** Após qualquer alteração no builder, você DEVE executar no terminal:
  ```powershell
  python tools/generate_full_html.py
  python tools/trace_divs.py
  ```
  Se `trace_divs.py` acusar erro ou desbalanceamento de tags `<div>`, corrija imediatamente antes de qualquer commit ou resposta.

---

## 🛡️ 3. Regras de UX e Interface do Usuário (Nunca Esquecer)

### 1. Zero Configuração Manual de Banco de Dados
* O usuário final **NUNCA** deve ver inputs de URL, botões de *"Sincronizar"* ou *"Conectar à Nuvem"*.
* A conexão com o Firebase Realtime DB REST API (`https://anime-quiz-arcade-default-rtdb.firebaseio.com/leaderboard.json`) deve iniciar 100% silenciosa e automática em segundo plano.

### 2. Validação Estrita de Nickname (Mínimo de 5 Caracteres)
* O salvamento de pontuação em qualquer modo exige **no mínimo 5 caracteres válidos** (`nickname.trim().length >= 5`).
* Bloqueie o botão de salvar ou exiba alerta caso a regra não seja atendida.

### 3. Botão "Finalizar Partida" Lateral, Compacto e com Efeito Glow
* Posicionado **lado a lado** com o botão **Confirmar Escolha** no Modo 2.
* Largura compacta (`max-width: 130px`).
* Brilho neon glow vermelho no `:hover` (`box-shadow: 0 0 16px rgba(239, 68, 68, 0.65)`).
* Evita cliques acidentais e facilita o encerramento voluntário.

### 4. Modais Leves e Otimizados (Zero Lag de GPU)
* Desfoque reduzido: `backdrop-filter: blur(3px)`.
* **NUNCA disparar animações de confetes (`ConfettiEngine.burst()`) na abertura do modal.**
* Confetes são permitidos **exclusivamente após o salvamento bem-sucedido** no Firebase.

### 5. Comportamento de Cancelar / Não Salvar (Zerar Sessão)
* O botão `🗑️ Não Salvar (Zerar)` deve executar `discardSessionAndReset()`, zerando score, acertos e streaks, reiniciando o jogo limpo.
* O botão `▶️ Voltar ao Jogo` fecha o modal mantendo a pontuação atual intacta.

### 6. Defesa contra Overflow em Tags de Dicas (Grid 2x2 de 38px)
* As tags de pistas nos Modos 3 e 4 devem ter layout 2x2 com **altura fixa rigorosa de 38px**:
  ```css
  height: 38px !important;
  min-height: 38px !important;
  max-height: 38px !important;
  min-width: 0 !important;
  overflow: hidden !important;
  text-overflow: ellipsis !important;
  white-space: nowrap !important;
  ```
* Imagens de cena devem ter fallback automático (`onerror`) e preloading assíncrono.

### 7. Responsividade da Sidebar Multiplayer
* Em telas com largura `<= 1120px`, a sidebar ao vivo (`#mp-live-sidebar`) deve se recolher ou ser posicionada abaixo do jogo, eliminando qualquer scroll horizontal.

---

## 🏷️ 4. Versionamento Visual & Protocolo de Entregas

1. **Incremento de Versão:** A cada entrega ou correção, atualize a div de versão visual no header (ex: `v3.2.3 • Arcade` -> `v3.2.4 • Arcade`).
2. **Atualização da Documentação:** Ao introduzir novas mecânicas, atualize os documentos correspondentes na pasta [`docs/`](docs/INDEX.md) e o histórico em [`docs/05_ROADMAP_E_HISTORICO_DE_VERSOES.md`](docs/05_ROADMAP_E_HISTORICO_DE_VERSOES.md).
3. **Git Clean Workflow:** Ao finalizar o ciclo, realize o `git add`, `git commit` com mensagem semântica clara e `git push origin main`.

---

## ✅ 5. Checklist Obrigatório Pré-Finalização

Antes de informar ao usuário que uma tarefa está pronta, verifique:
- [ ] O código foi alterado em `tools/generate_full_html.py` e compilado?
- [ ] O script `python tools/trace_divs.py` retornou zero erros de divs?
- [ ] O visual no navegador respeita a política de **Zero Scroll Vertical**?
- [ ] O botão de finalizar permanece compacto, lateral e com hover glow?
- [ ] Nenhuma configuração manual de nuvem foi exposta ao usuário?
- [ ] A versão visual no topo foi incrementada?
- [ ] As mudanças foram documentadas na pasta `docs/`?
