# 🏅 03. Sistema de Pontuação, Tags de Prestígio e Ciclo de Sessão

Este documento detalha as fórmulas matemáticas de pontuação, o multiplicador de sequências (combo streak), as **9 Badges de Prestígio Oficiais**, as regras estritas de validação de apelido (nickname) e o ciclo de vida completo de finalização e zeramento de sessão.

---

## 🧮 1. Fórmulas de Pontuação

A pontuação do jogo é calculada em tempo real com base em **precisão**, **tempo de resposta** e **sequência de vitórias**.

```
Pontuação Total da Rodada = (Pontos Base + Bônus de Velocidade - Penalidade de Dicas) × Multiplicador de Combo
```

### Detalhamento dos Componentes:

| Componente | Valor / Fórmula | Explicação |
| :--- | :--- | :--- |
| **Pontos Base** | `100 pts` | Concedido por qualquer resposta correta em qualquer modo. |
| **Bônus de Velocidade** | `Math.floor(tempoRestante × 5) pts` | Premia respostas rápidas. Exemplo: responder aos 20s de 30s concede `20 × 5 = +100 pts` de bônus. |
| **Penalidade de Dicas** | `-20 a -25 pts por dica` | Exclusivo do Modo 3 (Adivinhe a Cena). Cada dica revelada diminui a pontuação máxima possível daquela rodada. |
| **Multiplicador de Combo** | `1.0x` até `2.0x` | Aumenta proporcionalmente à quantidade de acertos consecutivos sem errar. |

### Tabela de Multiplicadores de Combo Streak:

```
┌───────────────────┬──────────────┬────────────────────────┐
│ Sequência (Streak)│ Multiplicador│ Efeito Visual / Sonoro │
│ 1 a 2 acertos     │     1.0x     │ Faíscas sutis          │
│ 3 a 4 acertos     │     1.2x     │ Brilho amarelo neon    │
│ 5 a 7 acertos     │     1.5x     │ Chamas laranjas vivas  │
│ 8 ou mais acertos │     2.0x     │ 🔥 MODO ULTRA FOGO 🔥  │
└───────────────────┴──────────────┴────────────────────────┘
```

> [!NOTE]
> Um erro em qualquer rodada reseta instantaneamente o contador de **Combo Streak** para `0` e o multiplicador volta para `1.0x`.

---

## 🎖️ 2. Sistema de Tags de Prestígio (9 Badges Oficiais)

Quando o jogador atinge marcos específicos durante a partida, o sistema desbloqueia automaticamente **Tags de Prestígio**. Essas tags são exibidas no painel de fim de jogo e gravadas no **Hall of Fame Global**.

```
┌────────────────────────────────────────────────────────────────────────┐
│                        CATÁLOGO DE BADGES                              │
│                                                                        │
│  [⚡ Velocista Neon]     [🔥 Em Chamas]         [🏆 Lenda Otaku]       │
│  [🎯 Precisão Absoluta]  [🧠 Enciclopédia]      [🎵 Ouvido Absoluto]   │
│  [⚔️ Guerreiro P2P]      [🛡️ Mestre das Cenas]  [⭐ Colecionador]       │
└────────────────────────────────────────────────────────────────────────┘
```

### Tabela Completa de Badges:

| ID | Nome da Badge | Ícone | Critério de Desbloqueio | Cor Neon |
| :--- | :--- | :---: | :--- | :---: |
| `speed_demon` | **Velocista Neon** | ⚡ | Respondeu corretamente em **menos de 5 segundos** de rodada. | Ciano `#00f3ff` |
| `on_fire` | **Em Chamas** | 🔥 | Atingiu um **Combo Streak de 5 ou mais** acertos consecutivos. | Laranja `#f97316` |
| `otaku_legend` | **Lenda Otaku** | 🏆 | Acumulou uma pontuação de **1.000 pontos ou mais** na sessão. | Dourado `#eab308` |
| `perfectionist` | **Precisão Absoluta**| 🎯 | Manteve **100% de taxa de acerto** tendo respondido ao menos 3 rodadas. | Verde `#10b981` |
| `encyclopedia` | **Enciclopédia** | 🧠 | Acertou uma cena no Modo 3 **sem abrir nenhuma das 4 dicas**. | Roxo `#a855f7` |
| `perfect_pitch`| **Ouvido Absoluto** | 🎵 | Acertou **3 aberturas seguidas** no Modo 1 (Blind Test). | Rosa `#ec4899` |
| `p2p_warrior` | **Guerreiro P2P** | ⚔️ | Pontuou ou venceu uma partida no Modo 4 (Multiplayer). | Vermelho `#ef4444` |
| `scene_master` | **Mestre das Cenas** | 🛡️ | Conquistou um Streak de 3 acertos consecutivos no Modo 3. | Azul `#3b82f6` |
| `arcade_collector`| **Colecionador**| ⭐ | Experimentou e pontuou em **todos os modos de jogo** na mesma sessão.| Âmbar `#f59e0b` |

---

## ✍️ 3. Regra Estrita de Apelido (Nickname Rule)

Para garantir qualidade, legibilidade e autenticidade no ranking mundial:

> [!IMPORTANT]
> **Tamanho Mínimo de 5 Caracteres:**
> O campo de nome no modal de fim de jogo exige **no mínimo 5 caracteres válidos** (`nickname.trim().length >= 5`).
> - Se o campo tiver menos de 5 caracteres:
>   - O botão `💾 Salvar no Ranking` permanece desabilitado ou exibe alerta explicativo: *"O apelido deve ter no mínimo 5 caracteres!"*.
>   - A borda do input adota cor de aviso âmbar/vermelha.
> - Ao atingir 5 ou mais caracteres:
>   - O botão de salvar acende com brilho neon verde e é liberado imediatamente.

---

## 🔄 4. Ciclo de Finalização, Modal Leve e Zeramento de Sessão

Ao clicar em **Finalizar Partida** (ou ao término das rodadas de um modo), o sistema abre o modal consolidado `#game-over-modal`.

```
┌────────────────────────────────────────────────────────┐
│                   🎉 FIM DE PARTIDA                    │
│                                                        │
│   Pontuação Final: 1.450 pts   •   Acertos: 9/10       │
│   Sequência Máxima: 5x 🔥      •   Precisão: 90%       │
│                                                        │
│   Tags Conquistadas:                                   │
│   [⚡ Velocista Neon] [🔥 Em Chamas] [🏆 Lenda Otaku]  │
│                                                        │
│   Digite seu Nickname para o Hall of Fame:             │
│   [ AnimeMaster_99                        ] (>= 5 car.)│
│                                                        │
│  ┌───────────────────┬───────────────────┬───────────┐ │
│  │ ▶️ Voltar ao Jogo │ 🗑️ Não Salvar    │ 💾 Salvar │ │
│  │  (Mantém pontos)  │    (Zerar Sessão) │ no Ranking│ │
│  └───────────────────┴───────────────────┴───────────┘ │
└────────────────────────────────────────────────────────┘
```

### Comportamento dos 3 Botões de Ação:

#### 1. `▶️ Voltar ao Jogo`
- **Ação:** Fecha o modal imediatamente.
- **Estado dos Dados:** **Preserva 100% da sessão atual intacta**. A pontuação, acertos e combo streak continuam ativos para o jogador prosseguir jogando e acumulando pontos.

#### 2. `🗑️ Não Salvar (Zerar)`
- **Ação:** Executa a função `discardSessionAndReset()`.
- **Estado dos Dados:**
  - Zera completamente `score = 0`, `correctAnswers = 0`, `streak = 0`.
  - Atualiza os 4 cartões de KPI no topo da tela.
  - Fecha o modal e reinicia uma nova rodada limpa.
  - Garante que partidas descartadas não deixem resíduos de pontuação para o próximo ciclo.

#### 3. `💾 Salvar no Ranking`
- **Ação:**
  1. Valida se o apelido possui `>= 5` caracteres.
  2. Monta o payload JSON com score, badges conquistadas, timestamp e modo.
  3. Envia silenciosamente via requisição `POST` para o endpoint `/leaderboard.json` do Firebase.
  4. **Feedback de Dopamina:** Dispara a animação comemorativa de confetes (`ConfettiEngine.burst()`) e efeito sonoro de vitória.
  5. Fecha o modal e reseta a sessão atual via `resetModeSession()` para iniciar uma nova jornada limpa.

### ⚡ Otimização Anti-Lag do Modal
- **Sem Chuva Prematura de Partículas:** O motor de confetes é disparado **apenas** após o clique de salvar bem-sucedido, nunca no momento da abertura do modal.
- **Filtro Leve de Fundo:** Utiliza `backdrop-filter: blur(3px)` e fundo preto semitransparente, garantindo taxa de quadros estável em 60 FPS em qualquer smartphone ou PC modesto.
