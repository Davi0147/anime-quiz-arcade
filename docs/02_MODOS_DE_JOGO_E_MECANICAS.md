# 🎮 02. Modos de Jogo e Mecânicas Detalhadas

Este documento descreve detalhadamente cada um dos **5 modos** disponíveis no **Anime Music & Scene Quiz (Arcade Edition)**, incluindo lógica interna, regras de entrada, pontuação específica, atalhos de teclado e ciclo de vida de cada rodada.

---

## 🧭 Visão Geral dos Modos

| Modo | Nome | Tipo de Desafio | Entrada do Jogador | Temporizador |
| :---: | :--- | :--- | :--- | :---: |
| **Modo 1** | **Blind Test (Audição)** | Adivinhar anime apenas pelo áudio da abertura | Autocomplete (697 animes) + Atalho TAB | 30s |
| **Modo 2** | **Qual é a Abertura?** | Escolha entre 3 opções de animes (A, B, C) com prévia sonora | Clique em Card + Play individual | 25s |
| **Modo 3** | **Adivinhe a Cena** | Identificar anime por screenshot de cena | Input Autocomplete + 3 Dicas Reveláveis | 30s |
| **Modo 4** | **Salas Multiplayer P2P** | Duelo ao vivo em tempo real entre amigos | WebRTC P2P (PeerJS) sincronizado | 20s/rodada |
| **Modo 5** | **Hall of Fame** | Placar de Líderes Global com Top 50 e Badges | Visualização e Filtro por Modo | - |

---

## 🎵 Modo 1: Blind Test (Audição Pura)

### 1. Descrição e Conceito
O jogador ouve uma abertura de anime oficial enquanto assiste a uma animação de **disco de vinil neon giratório** com visualizador de frequências de áudio em tempo real (Canvas Spectrum Waves).

```
┌────────────────────────────────────────────────────────┐
│                   MODO 1: BLIND TEST                   │
│                                                        │
│       ┌──────────────┐         (( 🎵 ONDAS NEON 🎵 ))  │
│       │  VINIL NEON  │                                 │
│       │   GIRATÓRIO  │         [ ⏱️ 00:24s RESTANTES ] │
│       └──────────────┘                                 │
│                                                        │
│   [ Digite o nome do anime...             ] [ SUBMETER ]│
│   └─> Sugestões rápidas (TAB para preencher)            │
└────────────────────────────────────────────────────────┘
```

### 2. Mecânica de Jogo
1. **Seleção Aleatória de Faixa:** O jogo sorteia uma música de `anime_songs_verified.json` (mais de 100 faixas com metadados verificados).
2. **Reprodução com Fallback Silencioso:**
   - Tenta reproduzir o arquivo local em `audio/<arquivo>.mp3`.
   - Se o arquivo local falhar (erro de rede ou arquivo inexistente), comuta automaticamente para a URL externa do CDN/servidor remoto sem travar a interface.
3. **Temporizador:** 30 segundos contados regressivamente. Ao atingir 5 segundos, ativa o estado visual e sonoro de **Modo Pânico** (pulso vermelho e bipe acelerado).
4. **Sistema de Entrada & Autocomplete:**
   - Campo de texto inteligente com busca instantânea em `anime_autocomplete_db.json` (697+ animes).
   - Suporta nomes em japonês (Romaji), títulos ocidentais e sinônimos populares (ex: `Boku no Hero` -> `My Hero Academia`, `Kimetsu no Yaiba` -> `Demon Slayer`).
   - **Atalho Teclado:**
     - `TAB`: Autocompleta imediatamente com a primeira sugestão da lista suspensa.
     - `ENTER`: Submete o palpite instantaneamente.
5. **Cálculo de Pontuação:**
   - Acerto base: `+100 pontos`.
   - Bônus de Velocidade: `+(tempo_restante * 5) pontos`.
   - Multiplicador de Combo Streak: `x1.0` a `x2.0`.

---

## 🎼 Modo 2: Qual é a Abertura? (Tripla Escolha)

### 1. Descrição e Conceito
Apresenta **3 alternativas (Cards A, B e C)** com banners visuais, títulos e botões individuais de play para escutar trechos de cada anime antes de confirmar a resposta.

```
┌──────────────────────────────────────────────────────────────────┐
│                   MODO 2: QUAL É A ABERTURA?                    │
│                                                                  │
│   ┌───────────────┐     ┌───────────────┐     ┌───────────────┐  │
│   │    CARD A     │     │    CARD B     │     │    CARD C     │  │
│   │ [Banner Anime]│     │ [Banner Anime]│     │ [Banner Anime]│  │
│   │  Shingeki     │     │  Naruto Ship. │     │  Jujutsu Kai. │  │
│   │ [ ▶️ Ouvir ]  │     │ [ ▶️ Ouvir ]  │     │ [ ▶️ Ouvir ]  │  │
│   └───────────────┘     └───────────────┘     └───────────────┘  │
│                                                                  │
│       [ 🟢 Confirmar Escolha ]   [ ⏹️ Finalizar ]                 │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 2. Mecânica de Jogo
1. **Geração das Opções:** Sorteia 1 música correta e 2 distratores aleatórios do banco de dados, embaralhando as posições (A, B, C).
2. **Pré-escuta Independente:** O jogador pode clicar no botão `▶️ Ouvir` de cada card para comparar os temas musicais. Apenas um áudio toca por vez.
3. **Seleção Visual:** Clicar em um card aplica a borda neon ativa (`border: 2px solid var(--accent-neon); box-shadow: 0 0 15px var(--accent-glow)`).
4. **Botões de Ação Inferiores (Regra de UX):**
   - **Botão Confirmar Escolha:** Largo, verde neon, valida o palpite selecionado.
   - **Botão Finalizar Partida:** Localizado **lado a lado** com o confirmar, com largura compacta (`max-width: 130px`) e efeito neon pulsante vermelho (`box-shadow: 0 0 16px rgba(239, 68, 68, 0.65)`) que acende intensamente ao passar o mouse.
5. **Finalização Segura:** Clicar em Finalizar Partida abre o modal consolidado `#game-over-modal` sem travamento de GPU, permitindo salvar no Ranking ou zerar a pontuação.

---

## 🎬 Modo 3: Adivinhe a Cena (Frames & Dicas)

### 1. Descrição e Conceito
O jogador deve identificar o anime através de uma captura de tela oficial de um episódio (127 cenas catalogadas em `tools/anime_scenes.json`).

```
┌────────────────────────────────────────────────────────┐
│                 MODO 3: ADIVINHE A CENA                │
│                                                        │
│   ┌────────────────────────────────────────────────┐   │
│   │                                                │   │
│   │            VIEWPORT DA CENA 16:9               │   │
│   │            (Screenshot HD do Anime)            │   │
│   │                                                │   │
│   └────────────────────────────────────────────────┘   │
│                                                        │
│   ┌────────────────────────┬───────────────────────┐   │
│   │ 🔒 Dica 1: Ano (2019)  │ 🔒 Dica 2: Gênero     │   │
│   ├────────────────────────┼───────────────────────┤   │
│   │ 🔒 Dica 3: Estúdio     │ 💡 Dica 4: Sinopse    │   │
│   └────────────────────────┴───────────────────────┘   │
│                                                        │
│   [ Digite o anime da cena...             ] [ ENVIAR ] │
└────────────────────────────────────────────────────────┘
```

### 2. Mecânica de Jogo
1. **Viewport 16:9 Estável:** A imagem é renderizada com `aspect-ratio: 16 / 9`, `object-fit: cover` e bordas arredondadas neon.
2. **Preloading de Imagens & Fallback Anti-Quebra:**
   - Imagens são pré-carregadas em background.
   - Evento `onerror` no elemento `<img>` substitui automaticamente imagens corrompidas por uma imagem de fallback temática de alta resolução, evitando molduras quebradas.
3. **Sistema de 4 Pistas (Grid 2x2 com Altura Rígida de 38px):**
   - **Dica 1: Ano de Lançamento** (Custo: -20 pontos)
   - **Dica 2: Gênero Principal** (Custo: -20 pontos)
   - **Dica 3: Estúdio de Animação** (Custo: -25 pontos)
   - **Dica 4: Pista Textual Especial** (Custo: -25 pontos)
   - **Defesa de Layout:** Cada botão de dica possui `height: 38px; min-height: 38px; max-height: 38px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; min-width: 0;`. Não estica nem deforma a interface independentemente do tamanho do texto da pista.
4. **Bonificação de Mente Brilhante:** Acertar a cena sem revelar nenhuma dica desbloqueia a badge de prestígio **🧠 Enciclopédia Otaku** e confere pontuação integral.

---

## 👥 Modo 4: Multiplayer P2P (Salas WebRTC)

### 1. Descrição e Conceito
Permite que amigos joguem juntos na mesma rodada via conexão direta ponto-a-ponto (**WebRTC DataChannels** através do PeerJS), sem necessidade de servidor backend complexo.

```
┌──────────────────────────────────────────────────────────────────┐
│                   MODO 4: SALAS & DUELO P2P                      │
│                                                                  │
│   ┌────────────────────────────┐  ┌──────────────────────────┐   │
│   │      ÁREA DE JOGO P2P      │  │    RANKING AO VIVO       │   │
│   │                            │  │    (Live Sidebar)        │   │
│   │  • Código Sala: #AK8921    │  │                          │   │
│   │  • Rodada 3 de 10          │  │  🥇 Luiz (Host) - 450pts │   │
│   │  • Áudio sincronizado      │  │  🥈 Pedro       - 320pts │   │
│   │  • Input de resposta       │  │  🥉 Carlos      - 210pts │   │
│   │                            │  │                          │   │
│   └────────────────────────────┘  └──────────────────────────┘   │
└──────────────────────────────────────────────────────────────────┘
```

### 2. Mecânica de Jogo
1. **Criação / Entrada de Sala:**
   - Host clica em "Criar Sala" e recebe um código alfanumérico curto (ex: `AMQ-7X9P`).
   - Convidados colam o código e se conectam diretamente via PeerJS.
2. **Sincronização de Rodadas:**
   - O Host escolhe o índice da música/cena e envia mensagem via DataChannel:
     ```json
     { "type": "START_ROUND", "round": 1, "trackIndex": 42, "timestamp": 1728150000 }
     ```
   - Todos os clientes disparam o timer e o áudio simultaneamente.
3. **Placar em Tempo Real (Live Sidebar):**
   - Conforme os participantes respondem, o status é transmitido:
     - `Thinking...` (Amarelo pulsante)
     - `Answered` (Verde neon com tempo gasto)
   - Deltas flutuantes de pontuação (`+185 pts`) sobem suavemente ao lado do nome de quem pontuou.
4. **Responsividade Estrita da Sidebar:**
   - Em telas largas (> 1120px): Exibida na coluna lateral direita.
   - Em telas compactas (<= 1120px): A sidebar é automaticamente movida para o fluxo vertical inferior ou recolhida com botão sanfona, eliminando qualquer risco de transbordamento horizontal.

---

## 🏆 Modo 5: Hall of Fame (Placar Global Top 50)

### 1. Descrição e Conceito
Tabela de classificação mundial atualizada em tempo real que consome dados da REST API do **Firebase Realtime Database**.

### 2. Recursos do Placar
- **Top 50 Classificados:** Mostra Posição (🥇, 🥈, 🥉, 4º...), Nickname, Pontuação Total, Acertos, Taxa de Precisão e Tags de Prestígio.
- **Filtros Dinâmicos:**
  - `Todos os Modos`
  - `Modo 1: Blind Test`
  - `Modo 2: Qual é a Abertura`
  - `Modo 3: Cenas`
  - `Modo 4: Multiplayer`
- **Renderização Rápida:** Cache local de 60 segundos com atualização sob demanda ao trocar de aba, minimizando requisições HTTP e garantindo carregamento instantâneo.
