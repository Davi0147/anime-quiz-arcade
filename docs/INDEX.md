# 📚 Índice Mestre da Documentação Técnica

Bem-vindo à documentação oficial e central do projeto **Anime Music & Scene Quiz (Arcade Edition)**.

Esta documentação foi categorizada e dividida em tópicos específicos para garantir consulta rápida, evitar esquecimento de regras solicitadas pelo usuário e orientar futuras manutenções e novas funcionalidades.

---

## 🗂️ Módulos de Documentação

| Arquivo | Título & Tema Principal | Conteúdo Principal |
| :--- | :--- | :--- |
| [**01. Arquitetura e Estrutura**](01_ARQUITETURA_E_ESTRUTURA.md) | Infraestrutura, Pipeline e Dados | • Arquitetura JAMstack Monolítica<br>• Pipeline do Builder (`generate_full_html.py`)<br>• Bancos de Dados JSON Estáticos<br>• Conexão Firebase REST API<br>• Multiplayer P2P WebRTC (PeerJS) |
| [**02. Modos de Jogo e Mecânicas**](02_MODOS_DE_JOGO_E_MECANICAS.md) | Regras e Lógica de Cada Modo | • Modo 1: Blind Test (Vinyl & Spectrum)<br>• Modo 2: Qual é a Abertura? (Tripla Escolha)<br>• Modo 3: Adivinhe a Cena (Frames & 4 Dicas)<br>• Modo 4: Multiplayer P2P (Salas & Placar)<br>• Modo 5: Hall of Fame (Top 50 Global) |
| [**03. Sistema de Pontuação e Badges**](03_SISTEMA_DE_PONTUACAO_TAGS_E_PRESTIGIO.md) | Cálculos, Tags e Sessão | • Fórmulas de Pontos, Bônus e Combos<br>• Catálogo das 9 Badges de Prestígio<br>• Regra de Nickname (Mínimo 5 caracteres)<br>• Ciclo de Finalização e Zeramento de Sessão |
| [**04. Regras de Ouro e Diretrizes**](04_REGRAS_DE_OURO_E_DIRETRIZES_DO_USUARIO.md) | **Diretrizes Invioláveis do Usuário** | • Zero Configuração Manual pelo Usuário<br>• Botão Finalizar Lateral e com Neon Glow<br>• Modal Leve sem Lag de GPU<br>• Comportamento de Cancelar/Zerar Sessão<br>• Defesa de Overflow (Tags de 38px)<br>• Disciplina do Compilador Builder |
| [**05. Roadmap e Histórico de Versões**](05_ROADMAP_E_HISTORICO_DE_VERSOES.md) | Changelog e Futuras Fases | • Changelog detalhado (v1.0.0 a v3.2.3)<br>• Fase 1 Concluída<br>• Fases 2 a 5 Planejadas (PWA, Opus, Sobrevivência, Torneio) |

---

## 🧭 Como Usar Esta Documentação
1. **Antes de editar qualquer código:** Sempre consulte o documento [04_REGRAS_DE_OURO_E_DIRETRIZES_DO_USUARIO.md](04_REGRAS_DE_OURO_E_DIRETRIZES_DO_USUARIO.md) para garantir conformidade com as exigências do usuário.
2. **Ao modificar telas ou mecânicas:** Consulte o documento [02_MODOS_DE_JOGO_E_MECANICAS.md](02_MODOS_DE_JOGO_E_MECANICAS.md) e [03_SISTEMA_DE_PONTUACAO_TAGS_E_PRESTIGIO.md](03_SISTEMA_DE_PONTUACAO_TAGS_E_PRESTIGIO.md).
3. **Ao compilar e gerar a build de produção:** Siga rigorosamente o fluxo em [01_ARQUITETURA_E_ESTRUTURA.md](01_ARQUITETURA_E_ESTRUTURA.md).
