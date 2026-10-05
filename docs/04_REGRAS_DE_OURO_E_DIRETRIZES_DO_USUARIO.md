# 📜 04. Regras de Ouro e Diretrizes do Usuário (Invioláveis)

Este documento registra formalmente **todas as regras de ouro, restrições e diretrizes de experiência de usuário (UX)** definidas pelo usuário ao longo de todo o desenvolvimento. 

> [!CAUTION]
> **ATENÇÃO AO AGENTE:** 
> NENHUMA das regras abaixo pode ser desfeita, esquecida, alterada ou ignorada em futuras atualizações, refatorações ou manutenções. Consulte este arquivo antes de qualquer modificação.

---

## 🚫 Regra 1: Zero Configuração Manual pelo Usuário Final

* **Demanda do Usuário:** *"no celular ta assim, tem que se conectar manualmente? Pq o usuario iria ficar com essa atividade? Nada no site deve ser feito pelo usuario, ja tem que iniciar tudo certo, tudo configurado, ja na base de dados conectada, e sem esses botão de conectar na nuvem etc..."*
* **Diretriz Técnica:**
  - O usuário comum **JAMAIS** deve ter que inserir URL de banco de dados, chaves de API, ou clicar em botões como *"Conectar à Nuvem"*, *"Sincronizar Manualmente"* ou *"Configurar Firebase"*.
  - A conexão com o Firebase Realtime DB REST API deve ser **100% automática e invisível** na inicialização da aplicação.
  - O endpoint de produção (`https://anime-quiz-arcade-default-rtdb.firebaseio.com/leaderboard.json`) fica embutido no código-fonte compilado.
  - **Proibição Absoluta:** É estritamente proibido exibir modais, abas ou botões visíveis de configuração de banco de dados para os jogadores.

---

## 📝 Regra 2: Fluxo Obrigatório de Salvamento e Nickname (>= 5 Caracteres)

* **Demanda do Usuário:** *"...ja tem que quando terminar de jogar o modo, o multiplayer etc, aparecer se a pessoa quer salvar a pontuação e ter um campo pra digitar o nome, no minimo 5 carateres, ou apertar pra cancelar caso não queira, isso deve aparecer em todos os modos (lembra que vc colocou sistema de tags dependendo do que o jogador conseguiu fazer, ai tem que ter isso tbm)"*
* **Diretriz Técnica:**
  - Ao concluir ou finalizar qualquer modo de jogo (Modos 1, 2, 3 e 4), o modal `#game-over-modal` deve ser acionado.
  - O campo de nickname exige **validação estrita de no mínimo 5 caracteres** (`nickname.trim().length >= 5`).
  - O botão de salvar no ranking só pode ser habilitado quando o nickname atingir 5 ou mais caracteres válidos.
  - As tags de prestígio conquistadas durante a partida devem ser renderizadas e salvas juntamente com a pontuação.

---

## ⏹️ Regra 3: Botão "Finalizar Partida" Lateral, Compacto e com Efeito Glow

* **Demanda do Usuário:** 
  1. *"esse finalizar partida ta muito facil de clicar, a pessoa pode errar e finalizar quando tentar clicar no confirmar escolha, deixe do lado do confirmar escolhe, mas com uma largura menor e com msg de confirmação, mostrando a pontuação atual na mensagem"*
  2. *"Coloca pro botao finalizar acender ao passar o mouse"*
* **Diretriz Técnica:**
  - O botão **Finalizar Partida** (`.btn-finalize` ou `#btn-finalize-m2`) deve ficar posicionado **lado a lado** (no mesmo container flex) com o botão **Confirmar Escolha**.
  - Possui **largura compacta** (`max-width: 130px; flex: 0 0 auto;`).
  - **Efeito Visual Neon Glow:** Ao passar o mouse (`:hover`), o botão acende intensamente com `box-shadow: 0 0 16px rgba(239, 68, 68, 0.65); transform: translateY(-1px);`.
  - Impede cliques acidentais de quem está tentando apenas submeter a resposta da rodada.

---

## 🪶 Regra 4: Modal Leve e Otimizado (Zero Lag de GPU)

* **Demanda do Usuário:** *"na tela de finalizar fica muito pesado"*
* **Diretriz Técnica:**
  - **Eliminação de Lag:** Modais não devem conter desfoques excessivos (`backdrop-filter` limitado a `blur(3px)`).
  - **Confetes Sob Demanda:** NUNCA disparar partículas de confetes (`ConfettiEngine.burst()`) no momento em que o modal de fim de jogo abre. Confetes rodam em loop de `requestAnimationFrame` no canvas e travam aparelhos celulares quando sobrepostos a modais.
  - Confetes são disparados **exclusivamente após o jogador clicar em Salvar no Ranking**.
  - Fluxo consolidado: apenas um modal limpo, sem modais intermediários redundantes.

---

## 🗑️ Regra 5: Comportamento de Cancelamento / Não Salvar (Zerar Sessão)

* **Demanda do Usuário:** *"quando clico em nao salvar (CANCELAR) ele n zera minha sessão atual, isso era pra acontecer?"*
* **Diretriz Técnica:**
  - O modal de fim de jogo possui 3 opções claras com propósitos bem definidos:
    1. **`▶️ Voltar ao Jogo`:** Fecha o modal e mantém a pontuação acumulada para continuar jogando.
    2. **`🗑️ Não Salvar (Zerar)`:** Executa `discardSessionAndReset()`. Zera totalmente o score (`score = 0`), os acertos e os streaks para que o jogador inicie uma nova tentativa do zero.
    3. **`💾 Salvar no Ranking`:** Persiste no Firebase, comemora com confetes e reseta a sessão.
  - Nunca deixe uma sessão "cancelada" com pontuação residual sem que o usuário tenha escolhido explicitamente voltar ao jogo.

---

## 🛡️ Regra 6: Defesa contra Overflow e Altura Rígida em Tags de Dicas (Grid 2x2 de 38px)

* **Demanda do Usuário:** *"no modo multiplayer quando seleciona ele buga as coisas, deixando coisa pra fora, as tags de dicas ficam esticadas, tem como resolver isso? teve momento que n apareceu imagem"*
* **Diretriz Técnica:**
  - As tags de pistas (Modo 3 e Modo 4) são organizadas em um grid de **2 colunas × 2 linhas**.
  - Cada botão de dica possui **altura fixa rigorosa de 38px**:
    ```css
    height: 38px !important;
    min-height: 38px !important;
    max-height: 38px !important;
    min-width: 0 !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    white-space: nowrap !important;
    ```
  - Isso impede que títulos longos estiquem verticalmente os botões e empurrem o restante da tela para fora.
  - **Fallback de Imagens:** Toda tag `<img>` de cenas deve possuir `onerror="this.onerror=null; this.src='...fallback.png';"` e preloading assíncrono para garantir que falhas de rede nunca mostrem imagens vazias ou quebradas.

---

## 📱 Regra 7: Responsividade Estrita da Sidebar Multiplayer

* **Diretriz Técnica:**
  - Em telas com largura menor ou igual a **1120px** (`@media (max-width: 1120px)`), o placar ao vivo (`#mp-live-sidebar`) não deve espremer a área de jogo principal nem causar scroll horizontal.
  - Deve ser movida para baixo do card principal ou recolhida em modo drawer compacto.

---

## 🏗️ Regra 8: Pipeline Builder Obrigatório (NUNCA editar HTML compilado)

* **Diretriz Técnica:**
  - **NUNCA** edite diretamente `index.html` ou `desafio_anime_quiz.html`.
  - Todas as modificações em CSS, HTML estrutural e JavaScript DEVEM ser feitas dentro de `tools/generate_full_html.py`.
  - Imediatamente após editar o gerador, execute:
    ```powershell
    python tools/generate_full_html.py
    python tools/trace_divs.py
    ```
  - Se `trace_divs.py` acusar desbalanceamento de tags `<div>`, corrija antes de qualquer commit.

---

## 🏷️ Regra 9: Versionamento Visual Front-End Obrigatório

* **Diretriz Técnica:**
  - O header da aplicação possui uma badge visível indicando a versão atual (ex: `v3.2.3 • Arcade`).
  - O Agente DEVE incrementar essa versão a cada entrega relevante ou correção solicitada pelo usuário.

---

## ✨ Regra 10: Microinterações de Alta Dopamina & Orientação Paisagem

* **Demanda do Usuário:** 
  1. *"quanto mais feedbacks que reforcem a dopamina tiver melhor, assim fica algo legal pro usuario, tipo vc passa mouse em uma area e ela acende ou cresce, vc clica algo e tem um barulhinho etc."*
  2. *"se no celular fica com, como estavmos fazendo um aplicativo horizontal, poderia aparecer na tela do mobile pra deixar na horizontal, e ficar melhor visualizado"*
* **Diretriz Técnica:**
  - **Web Audio API Nativa:** Sons de clique, hover sutil, acerto com acorde maior, erro, combo arpeggio e alarme de pânico integrados sem bibliotecas externas pesadas.
  - **Hover & Feedback Tátil:** Efeitos sutis de elevação 3D (`translateY(-2px) scale(1.02)`) e brilhos periféricos.
  - **Orientação Paisagem Mobile:** Overlay educacional animado convidando a virar o aparelho para a horizontal (`@media (orientation: portrait) and (max-width: 900px)`), garantindo **Zero Scroll Vertical**.
