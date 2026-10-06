# 🗺️ 05. Roadmap e Histórico de Versões

Este documento cataloga o histórico cronológico de versões (Changelog) do **Anime Music & Scene Quiz (Arcade Edition)** e estabelece as próximas fases de evolução planejadas para o projeto.

---

## 📜 Histórico de Versões (Changelog)

### `v3.2.6 • Arcade` (Versão Atual)
* **Auditoria Completa Ponta a Ponta & Suíte de Testes Automatizados (`tools/run_e2e_audit.py`):**
  - **100% de Aprovação em Todos os Testes:** Datasets (PASS), Estrutura HTML (PASS), CSS & Layout (PASS), Sintaxe JS V8 (PASS), Referências DOM (PASS), e Simulação de Gameplay (PASS).
  - **Otimização Extrema de Performance (Zero Lag nos Modais):** Redução universal de todos os filtros de desfoque pesados (`blur(10px)` a `blur(16px)`) para o padrão estrito de alta performance `blur(3px)` na barra lateral, caixas de feedback, cards de resposta, popovers de áudio e modais de alerta. Abertura do modal de Finalizar Partida agora roda a 60fps lisos sem sobrecarga de GPU.
  - **Blindagem Anti-Crash de Elementos do DOM:** Adicionados guards de nulidade defensivos em `renderCatalogTable()` e `m1ToggleMask()`, prevenindo falhas de inicialização ou chamadas órfãs.
  - **Sanitização de Script Inline:** Escapamento seguro de tokens HTML dentro do `document.write` de fallback do PeerJS, eliminando ambiguidades de fechamento de tags em analisadores estáticos.
  - **Verificação do Servidor de Streaming:** Testes automatizados confirmando suporte a requisições com cabeçalho `Range: bytes=X-Y` com status HTTP 206 Partial Content no `server.py`.

### `v3.2.5 • Arcade`
* **Sincronização Online 100% Autoritativa no Multiplayer:**
  - **Correção da Rodada Congelada:** Corrigido o bug onde o convidado ficava preso na rodada #1 enquanto o host avançava. O loop de sincronização de rede (`startGuestSync`) agora persiste ininterrupto durante toda a partida (não sendo mais finalizado prematuramente por `clearAllTimers` entre rodadas).
  - **Host como Fonte da Verdade Única:** Estado de jogo versionado (`v`), sincronizado atomicamente por dois canais simultâneos (WebRTC P2P + Nuvem Firebase REST). Se o pacote P2P for bloqueado, o estado via Nuvem assume imediatamente em tempo real.
  - **Sincronia Estrita de Rodadas e Cronômetro:** O convidado sempre acompanha a rodada exata do host (`state.currentRoundIdx`), impedindo descompasso (se o host estiver na rodada 5, o convidado estará na rodada 5).
  - **Heartbeat & Presença Ativa:** Pings periódicos de presença (`presence/${playerId}`) para detectar quedas e desconexões reais, além de limpeza automática de salas encerradas no Firebase.
  - **Deduplicação de Respostas e Pontos:** Respostas recebidas simultaneamente por P2P e Nuvem são computadas exatamente uma vez, com feedback otimista e pontuações consolidadas no HUD e no Live Ranking.
  - **Proteção do Botão Finalizar no Multiplayer:** Clicar em "Finalizar" durante uma partida ativa online agora aciona confirmação para sair da sala com segurança, sem zerar a sessão erradamente.

### `v3.2.4 • Arcade`
* **Multiplayer Híbrido WebRTC P2P + Cloud Relay (Firebase):**
  - **Canal WSS Universal:** Conexão segura forçada (`secure: true`, porta 443 WSS) no PeerJS, eliminando o erro de protocolo cruzado entre testes no `localhost` (HTTP) e jogadores no GitHub Pages (HTTPS).
  - **Pool de 8 Servidores STUN:** Inclusão de servidores STUN de alta velocidade (Google 1-4, Cloudflare, Mozilla, Twilio) e expurgo de servidores TURN inativos do PeerJS que causavam timeouts de ICE.
  - **Sanitização de Código de Sala:** Limpeza automática de espaços e caracteres especiais (como `#`), prevenindo IDs inválidos no PeerJS.
  - **Auto-Fallback para Nuvem (Zero-Failure):** Se a conexão direta P2P travar ou for bloqueada por CGNAT / Firewall / 4G (timeout de 3.8s), o jogo comuta automaticamente e silenciosamente para sincronização via REST API do Firebase Realtime Database.
  - **DataChannel Confiável:** Adição de `{ reliable: true }` para garantir entrega sequencial de pacotes sem perda em redes remotas.

### `v3.2.3 • Arcade`
* **UX de Finalização Aprimorada:**
  - Botão **Finalizar Partida** posicionado **lado a lado** com o botão **Confirmar Escolha** no Modo 2, com largura compacta (`max-width: 130px`) para prevenir cliques acidentais.
  - Efeito visual de brilho neon glow no hover (`box-shadow: 0 0 16px rgba(239, 68, 68, 0.65)`).
* **Eliminação Total de Lag no Modal:**
  - Desfoque reduzido para `blur(3px)` e remoção de chuva prematura de confetes durante a abertura do modal. Confetes agora explodem exclusivamente após o sucesso do salvamento.
* **Correção no Ciclo de Sessão:**
  - Clicar em `🗑️ Não Salvar (Zerar)` agora executa `discardSessionAndReset()`, zerando a pontuação acumulada, acertos e combo streak, reiniciando o jogo limpo.

### `v3.2.2 • Arcade`
* **Defesa contra Overflow & Altura Rígida de Tags:**
  - Padronização das tags de dicas no Modo 3 e Modo 4 em grid 2x2 com **altura fixa rigorosa de 38px**, impedindo estiramento vertical e quebras de layout.
  - Implementação de preloading de imagens e fallback automático com tratamento de erro 404 para cenas.
* **Responsividade da Sidebar Multiplayer:**
  - Tratamento para telas com largura <= 1120px, evitando compressão da área de jogo principal.

### `v3.2.1 • Arcade`
* **Conexão Invisível à Nuvem:**
  - Eliminação de botões de sincronização manual e caixas de URL de banco de dados para os jogadores.
  - Conexão 100% silenciosa e automática com a REST API do Firebase Realtime Database.
* **Validação de Nickname:**
  - Implementação da regra estrita de **mínimo de 5 caracteres** para registro de pontuação no ranking mundial.

### `v3.2.0 • Arcade`
* **Integração com Firebase Realtime Database:**
  - Criação da tabela de classificação global em nuvem (Leaderboard Top 50).
  - Persistência de apelido, pontuação, acertos, taxa de acerto e badges conquistadas.

### `v3.1.0 • Arcade`
* **Autocomplete Expandido:**
  - Integração do banco `anime_autocomplete_db.json` com 697+ animes e suporte a sinônimos em japonês e inglês.
  - Adição do atalho `TAB` para preenchimento instantâneo da primeira sugestão.
* **Sistema de 9 Badges de Prestígio:**
  - Criação do catálogo oficial de badges neon com detecção automática de conquistas.

### `v3.0.0 • Arcade`
* **Expansão para 4 Modos de Jogo:**
  - Lançamento do Modo 3 (Adivinhe a Cena com 127 capturas oficiais de episódios).
  - Lançamento do Modo 4 (Multiplayer P2P WebRTC via PeerJS com salas privadas por código).
* **Migração para o Pipeline Builder:**
  - Criação de `tools/generate_full_html.py` e validador de sintaxe `tools/trace_divs.py`.

### `v2.0.0 a v2.5.0`
* Lançamento dos Modos 1 (Blind Test com espectro de áudio) e Modo 2 (Qual é a Abertura com cards visuais A, B e C).
* Inclusão do banco oficial com 100+ aberturas verificadas (`anime_songs_verified.json`).

---

## 🚀 Fases do Roadmap

```
┌────────────────────────────────────────────────────────┐
│             ESTADO DO CRONOGRAMA DE FASES              │
├────────────────────────────────────────────────────────┤
│ [CONCLUÍDA] ✅ FASE 1: Core Engine, 4 Modos & Nuvem    │
│ [PLANEJADA] ⏳ FASE 2: Compressão de Áudio & Cache SW  │
│ [PLANEJADA] ⏳ FASE 3: Progressive Web App (PWA)       │
│ [PLANEJADA] ⏳ FASE 4: Modo Sobrevivência & Time Attack│
│ [PLANEJADA] ⏳ FASE 5: Torneio Eliminatório P2P        │
└────────────────────────────────────────────────────────┘
```

---

### ✅ FASE 1: Fundação, Modos Core & Nuvem Global (CONCLUÍDA)
- [x] Motor de áudio nativo com Web Audio API e Canvas Spectrum Analyzer.
- [x] Modo 1: Blind Test com autocomplete de 697 animes e atalho TAB.
- [x] Modo 2: Qual é a Abertura com cards A, B e C e finalização compacta side-by-side.
- [x] Modo 3: Adivinhe a Cena com 127 frames 16:9 e grid de dicas 2x2 de 38px.
- [x] Modo 4: Multiplayer P2P WebRTC com salas privadas e live sidebar.
- [x] Integração silenciosa com Firebase Realtime Database.
- [x] Sistema de 9 Badges de Prestígio e validação de nickname >= 5 caracteres.
- [x] Zero scroll vertical no desktop e overlay educacional para mobile landscape.

---

### ⏳ FASE 2: Otimização de Performance e Compressão de Áudio Web
- [ ] **Conversão para WebM/Opus:** Codificar amostras de áudio para formato Opus de alta fidelidade com taxas de bits reduzidas (64-96 kbps), diminuindo o tempo de carregamento em redes móveis 3G/4G.
- [ ] **Service Worker com Cache Storage:** Armazenar em cache local os primeiros 5 segundos das músicas mais frequentes para início instantâneo de reprodução.
- [ ] **IndexedDB Local:** Cache do banco de cenas e autocomplete no dispositivo do usuário para inicialização a frio em menos de 300ms.

---

### ⏳ FASE 3: Progressive Web App (PWA)
- [ ] **Manifesto Web (`manifest.json`):** Configuração completa com cores temáticas neon (`#0a0b10`), orientação paisagem forçada (`landscape`) e tela cheia (`display: standalone`).
- [ ] **Ícones PWA Adaptativos:** Geração de ícones em resoluções 192x192 e 512x512 com tema de arcade neon.
- [ ] **Instalação em 1 Clique:** Prompt nativo elegante para adicionar à tela inicial no Android e iOS.

---

### ⏳ FASE 4: Modos Arcade Adicionais (Sobrevivência & Time Attack)
- [ ] **Modo Sobrevivência (Sudden Death):**
  - O jogador começa com **3 vidas (Corações Neon ❤️❤️❤️)**.
  - A partida só termina ao perder todas as vidas.
  - A velocidade da música ou a dificuldade das opções aumentam gradualmente.
- [ ] **Modo Time Attack (60 Segundos Frenéticos):**
  - Temporizador global contínuo de 60 segundos.
  - Cada acerto adiciona `+3 segundos` ao relógio; cada erro subtrai `-5 segundos`.

---

### ⏳ FASE 5: Torneio Eliminatório P2P com Chaves (Brackets)
- [ ] **Chaves de Mata-Mata (Brackets):** Suporte a partidas eliminatórias de 4 ou 8 jogadores em rede P2P.
- [ ] **Sincronia de Telas de Transição:** Gráfico dinâmico estilo anime exibindo confrontos diretos (ex: *Jogador A vs Jogador B*).
- [ ] **Pódio do Campeão:** Animação comemorativa de troféu dourado para o campeão do torneio.
