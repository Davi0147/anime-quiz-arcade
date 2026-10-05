# 🏗️ 01. Arquitetura e Estrutura Técnica

Este documento detalha toda a infraestrutura, pipeline de compilação, bancos de dados estáticos, integrações de nuvem e camada de rede P2P do **Anime Music & Scene Quiz (Arcade Edition)**.

---

## 📐 1. Visão Geral da Arquitetura

O projeto adota uma arquitetura **JAMstack Monolítica de Alta Performance** otimizada para web e hospedagem em **GitHub Pages**.

```
┌─────────────────────────────────────────────────────────────┐
│                       FONTES DE DADOS                       │
│  • anime_songs_verified.json (100+ Aberturas Oficiais)      │
│  • tools/anime_scenes.json (127 Cenas Reais de Episódios)   │
│  • tools/anime_autocomplete_db.json (697+ Títulos Animes)   │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                 GERADOR DO PROJETO (BUILDER)                │
│  • tools/generate_full_html.py                              │
│    -> Injeta JSONs estáticos diretamente no HTML             │
│    -> Compila CSS, HTML e JavaScript Inline                 │
│    -> Gera index.html e desafio_anime_quiz.html             │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                      SAÍDA & VALIDAÇÃO                      │
│  • index.html (Build Final de Produção)                     │
│  • tools/trace_divs.py (Verificador Estrito de Tags HTML)   │
└──────────────────────────────┬──────────────────────────────┘
                               │
               ┌───────────────┴───────────────┐
               ▼                               ▼
┌─────────────────────────────┐ ┌─────────────────────────────┐
│   FIREBASE REALTIME DB      │ │      MULTIPLAYER P2P        │
│   (REST API - Nuvem Global) │ │   (WebRTC via PeerJS v1.5)  │
│   • Leaderboard Top 50      │ │   • Salas Privadas (Código) │
│   • Sincronização Silenciosa│ │   • Sincronia de Partida    │
└─────────────────────────────┘ └─────────────────────────────┘
```

---

## 📁 2. Estrutura de Pastas e Arquivos

```
anime-music-quiz/
├── audio/                      # Músicas locais MP3 para modo offline / desenvolvimento
├── icons/                      # Conjunto de ícones PNG estilizados neon (Search, Vinyl, Padlock, etc.)
├── libs/                       # Dependências locais com fallback CDN (PeerJS 1.5.4)
├── scratch/                    # Rascunhos de layout e especificações técnicas
├── tools/                      # Ferramentas de automação e dados adicionais
│   ├── anime_autocomplete_db.json   # 697 títulos e sinônimos para preenchimento automático
│   ├── anime_scenes.json            # 127 frames oficiais com tags de ano, estúdio e pistas
│   ├── generate_full_html.py        # Compilador principal (ÚNICO local de alteração de código)
│   └── trace_divs.py                # Script de validação sintática de balanceamento de divs
├── docs/                       # Documentação completa categorizada do sistema
│   ├── 01_ARQUITETURA_E_ESTRUTURA.md
│   ├── 02_MODOS_DE_JOGO_E_MECANICAS.md
│   ├── 03_SISTEMA_DE_PONTUACAO_TAGS_E_PRESTIGIO.md
│   ├── 04_REGRAS_DE_OURO_E_DIRETRIZES_DO_USUARIO.md
│   ├── 05_ROADMAP_E_HISTORICO_DE_VERSOES.md
│   └── INDEX.md
├── anime_songs_verified.json   # Catálogo mestre de 100 aberturas verificadas
├── desafio_anime_quiz.html     # Cópia compilada de backup
├── index.html                  # Arquivo servido em produção pelo GitHub Pages
├── README.md                   # Apresentação do repositório
└── server.py                   # Servidor de desenvolvimento local (Python HTTP)
```

---

## ⚙️ 3. Pipeline de Compilação & Modificação

> [!IMPORTANT]
> **REGRA FUNDAMENTAL DE DESENVOLVIMENTO:**
> Nunca edite o arquivo `index.html` ou `desafio_anime_quiz.html` diretamente!
> Qualquer alteração de CSS, HTML ou JavaScript **DEVE** ser feita dentro do script gerador `tools/generate_full_html.py`.

### Ciclo Obrigatório de Atualização:
1. **Edição do Código**: Aplicar as melhorias no arquivo `tools/generate_full_html.py`.
2. **Compilação**: Executar o compilador Python:
   ```powershell
   python tools/generate_full_html.py
   ```
3. **Verificação Estrutural de Tags**:
   ```powershell
   python tools/trace_divs.py
   ```
   *(A saída DEVE ser obrigatoriamente: `All divs matched!`)*.
4. **Verificação de Sintaxe JavaScript**:
   Testar a integridade dos blocos de script com Node.js para garantir ausência de quebras de sintaxe.
5. **Controle de Versão**:
   * Adicionar os arquivos gerados ao Git:
     ```powershell
     git add desafio_anime_quiz.html index.html tools/generate_full_html.py
     git commit -m "feat/fix: descrição clara da alteração"
     git push origin main
     ```
6. **Abertura Local no Navegador**:
   ```powershell
   Start-Process "index.html"
   ```

---

## ☁️ 4. Banco de Dados em Nuvem (`CloudLeaderboard`)

O jogo conecta-se ao **Firebase Realtime Database** via **REST API nativa** (sem SDKs pesados), operando de forma 100% invisível ao jogador:

* **Endpoint Oficial**: `https://anime-quiz-arcade-default-rtdb.firebaseio.com/leaderboard.json`
* **Leitura (GET)**: Ao iniciar a aplicação ou navegar até o Hall da Fama (Modo 5), as pontuações mundiais são carregadas em segundo plano.
* **Escrita (POST)**: Ao salvar um recorde no modal de Fim de Partida (`#game-over-modal`), um objeto padronizado é gravado via `POST` com os atributos:
  ```json
  {
    "id": 1740000000000,
    "name": "Levi_Ackerman",
    "mode": "mode2",
    "score": 1450,
    "correct": 12,
    "streak": 6,
    "badgeTitle": "Mestre Otaku",
    "badgeIcon": "👑",
    "date": "05/10/2026",
    "timestamp": 1740000000000
  }
  ```
* **Fallback e Cache Local**: Caso o dispositivo esteja temporariamente offline ou a rede oscile, as pontuações são preservadas e combinadas usando `localStorage` (`AMQ_LEADERBOARD_V2`), garantindo que o Hall da Fama nunca fique em branco.
* **Sem Intervenção Manual**: Não existem botões para o usuário conectar URL, autorizar acesso ou sincronizar manualmente.

---

## 🌐 5. Multiplayer em Tempo Real P2P (WebRTC)

O módulo `MultiplayerEngine` viabiliza partidas cooperativas e competitivas sem necessidade de hospedar servidores caros:

* **Biblioteca Base**: **PeerJS** (`libs/peerjs.min.js` com fallback automático para CDN).
* **Topologia**: *Mesh / Star Híbrido* onde o Host coordena a sincronia do cronômetro, geração de sementes aleatórias de rodada e computação dos votos de skip.
* **Protocolo de Mensagens**:
  * `ROOM_STATE`: Atualiza lista de jogadores conectados e status de preparação.
  * `MATCH_START`: Transmite configurações da partida, itens de rodadas (`roundItems`) e semente de sincronização.
  * `ROUND_START`: Inicia rodada em sincronia milimétrica entre todos os navegadores.
  * `PLAYER_ANSWER`: Informa que um participante respondeu, ativando bônus de rapidez.
  * `SKIP_VOTE`: Registra voto para avançar para a próxima rodada por maioria simples.
  * `MATCH_END`: Envia as pontuações finais para a cerimônia do Pódio.
