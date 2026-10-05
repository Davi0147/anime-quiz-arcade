# 🎮 Anime Music & Scene Quiz (Arcade Edition)

Desafio interativo de adivinhação de aberturas e cenas de animes clássicos e modernos com visualizador espectral de ondas sonoras, multiplayer ao vivo P2P (WebRTC), design Bento Grid responsivo, conexão automática com Firebase e zero rolagem vertical.

---

## 📚 Documentação Completa do Projeto

Toda a documentação técnica, regras de negócio e diretrizes de desenvolvimento estão organizadas e categorizadas na pasta [`docs/`](docs/INDEX.md):

* 🏗️ [**01. Arquitetura e Estrutura Técnica**](docs/01_ARQUITETURA_E_ESTRUTURA.md) — Infraestrutura, pipeline do gerador (`tools/generate_full_html.py`), bancos JSON, Firebase REST API e WebRTC PeerJS.
* 🎮 [**02. Modos de Jogo e Mecânicas**](docs/02_MODOS_DE_JOGO_E_MECANICAS.md) — Blind Test, Qual é a Abertura?, Adivinhe a Cena, Multiplayer P2P e Hall of Fame.
* 🏅 [**03. Sistema de Pontuação, Tags e Prestígio**](docs/03_SISTEMA_DE_PONTUACAO_TAGS_E_PRESTIGIO.md) — Fórmulas de pontuação, as 9 badges de prestígio, validação de nickname (>= 5 caracteres) e ciclo de sessões.
* 📜 [**04. Regras de Ouro e Diretrizes do Usuário**](docs/04_REGRAS_DE_OURO_E_DIRETRIZES_DO_USUARIO.md) — Regras mandatórias e invioláveis de UX, performance e layout solicitadas pelo usuário.
* 🗺️ [**05. Roadmap e Histórico de Versões**](docs/05_ROADMAP_E_HISTORICO_DE_VERSOES.md) — Changelog detalhado (v1.0.0 a v3.2.3) e cronograma das Fases 1 a 5.

---

## 🌟 Modos de Jogo

1. **Blind Test (Modo 1):** Ouça a música sem saber o anime e digite seu palpite com autocomplete inteligente (697 animes, atalho TAB para preencher).
2. **Qual é a Abertura? (Modo 2):** Descubra qual das 3 faixas de áudio é a abertura oficial com pré-escuta independente e botão de finalizar lado a lado.
3. **Adivinhe a Cena (Modo 3):** Identifique o anime a partir de capturas de tela HD 16:9 oficiais com pistas de Ano, Gênero, Estúdio e Sinopse.
4. **Salas Multiplayer P2P (Modo 4):** Crie salas com código privado para duelar ao vivo com amigos usando WebRTC via PeerJS em tempo real.
5. **Hall of Fame (Modo 5):** Placar global Top 50 integrado de forma silenciosa ao Firebase Realtime Database.

---

## 🚀 Como Executar Localmente

Basta abrir o arquivo `index.html` em qualquer navegador moderno ou rodar um servidor HTTP local:
```bash
python -m http.server 8000
```
Acesse: `http://localhost:8000/index.html`

---

## 🛠️ Como Compilar Alterações (Pipeline do Builder)

> [!IMPORTANT]
> **NUNCA altere `index.html` diretamente!** Todas as alterações de CSS, HTML ou JavaScript devem ser feitas em `tools/generate_full_html.py`.

Para compilar e validar:
```bash
python tools/generate_full_html.py
python tools/trace_divs.py
```
