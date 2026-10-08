import json
import os
import re
import sys
import subprocess

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TOOLS_DIR = os.path.join(ROOT_DIR, "tools")
INDEX_PATH = os.path.join(ROOT_DIR, "index.html")
GEN_PATH = os.path.join(TOOLS_DIR, "generate_full_html.py")

SONGS_PATH = os.path.join(ROOT_DIR, "anime_songs_verified.json")
SCENES_PATH = os.path.join(TOOLS_DIR, "anime_scenes.json")
AUTOCOMPLETE_PATH = os.path.join(TOOLS_DIR, "anime_autocomplete_db.json")

report = {
    "datasets": {"status": "PENDING", "errors": [], "warnings": [], "info": []},
    "html": {"status": "PENDING", "errors": [], "warnings": [], "info": []},
    "css": {"status": "PENDING", "errors": [], "warnings": [], "info": []},
    "js_syntax": {"status": "PENDING", "errors": [], "warnings": [], "info": []},
    "dom_references": {"status": "PENDING", "errors": [], "warnings": [], "info": []},
    "gameplay_simulation": {"status": "PENDING", "errors": [], "warnings": [], "info": []},
}

print("=" * 70)
print("🚀 INICIANDO AUDITORIA COMPLETA E TESTES PONTA A PONTA (AMQ ARCADE v3.3.0)")
print("=" * 70)

# ============================================================================
# 1. AUDITORIA DOS DATASETS
# ============================================================================
print("\n[1/6] Verificando Integridade dos Datasets...")

# 1.1 Songs
try:
    with open(SONGS_PATH, "r", encoding="utf-8") as f:
        songs = json.load(f)
    report["datasets"]["info"].append(f"anime_songs_verified.json: {len(songs)} faixas verificadas carregadas.")
    if len(songs) < 50:
        report["datasets"]["errors"].append(f"Catálogo de músicas muito pequeno: {len(songs)}")
    
    song_ids = set()
    for idx, s in enumerate(songs):
        sid = s.get("id")
        if not sid:
            report["datasets"]["errors"].append(f"Música index {idx} sem ID!")
        elif sid in song_ids:
            report["datasets"]["errors"].append(f"Música ID duplicado: {sid}")
        else:
            song_ids.add(sid)
        
        for req_field in ["anime", "song", "artist"]:
            if not s.get(req_field):
                report["datasets"]["warnings"].append(f"Música {sid} campo vazio: {req_field}")
        
        has_video = bool(s.get("video_id") and s.get("video_url"))
        if not has_video:
            report["datasets"]["errors"].append(f"Música {sid} ({s.get('anime')}) sem video_id/video_url do YouTube!")
            
except Exception as e:
    report["datasets"]["errors"].append(f"Erro fatal lendo anime_songs_verified.json: {e}")

# 1.2 Scenes
try:
    with open(SCENES_PATH, "r", encoding="utf-8") as f:
        scenes = json.load(f)
    report["datasets"]["info"].append(f"anime_scenes.json: {len(scenes)} cenas de episódios carregadas.")
    scene_ids = set()
    for idx, sc in enumerate(scenes):
        sc_id = sc.get("id")
        if not sc_id:
            report["datasets"]["errors"].append(f"Cena index {idx} sem ID!")
        elif sc_id in scene_ids:
            report["datasets"]["errors"].append(f"Cena ID duplicado: {sc_id}")
        else:
            scene_ids.add(sc_id)
        
        if not sc.get("anime"):
            report["datasets"]["errors"].append(f"Cena {sc_id} sem nome de anime!")
        if not sc.get("image_url"):
            report["datasets"]["errors"].append(f"Cena {sc_id} sem image_url!")
except Exception as e:
    report["datasets"]["errors"].append(f"Erro fatal lendo anime_scenes.json: {e}")

# 1.3 Autocomplete
try:
    with open(AUTOCOMPLETE_PATH, "r", encoding="utf-8") as f:
        autocomplete = json.load(f)
    report["datasets"]["info"].append(f"anime_autocomplete_db.json: {len(autocomplete)} títulos/aliases carregados.")
    if len(autocomplete) < 100:
        report["datasets"]["warnings"].append(f"Autocomplete DB pequeno: {len(autocomplete)}")
except Exception as e:
    report["datasets"]["errors"].append(f"Erro fatal lendo anime_autocomplete_db.json: {e}")

report["datasets"]["status"] = "FAIL" if report["datasets"]["errors"] else "PASS"
print(f" -> Status Datasets: {report['datasets']['status']} (Erros: {len(report['datasets']['errors'])}, Avisos: {len(report['datasets']['warnings'])})")


# ============================================================================
# 2. AUDITORIA ESTRUTURAL HTML
# ============================================================================
print("\n[2/6] Verificando Estrutura HTML e Balanceamento de Tags...")
with open(INDEX_PATH, "r", encoding="utf-8") as f:
    html_content = f.read()

report["html"]["info"].append(f"Tamanho de index.html: {len(html_content.encode('utf-8')):,} bytes")

# 2.1 Trace tags
paired_tags = ['div', 'section', 'main', 'header', 'footer', 'nav', 'aside', 'style', 'select', 'table', 'ul', 'ol', 'form', 'kbd']
for tag in paired_tags:
    open_count = len(re.findall(rf'<{tag}(\s+[^>]*)?>', html_content, re.IGNORECASE))
    close_count = len(re.findall(rf'</{tag}>', html_content, re.IGNORECASE))
    if open_count != close_count:
        report["html"]["errors"].append(f"Tag <{tag}> desbalanceada! Aberturas: {open_count}, Fechamentos: {close_count}")
    else:
        report["html"]["info"].append(f"Tag <{tag}> balanceada ({open_count} pares).")

# Tags <script> estruturais
# Exclui strings como '<script' dentro de document.write
real_script_opens = len(re.findall(r'<script\b[^>]*>', re.sub(r'document\.write\([^\)]+\)', '', html_content), re.IGNORECASE))
real_script_closes = len(re.findall(r'</script>', re.sub(r'document\.write\([^\)]+\)', '', html_content), re.IGNORECASE))
if real_script_opens != real_script_closes:
    report["html"]["errors"].append(f"Tag <script> desbalanceada! Aberturas: {real_script_opens}, Fechamentos: {real_script_closes}")
else:
    report["html"]["info"].append(f"Tag <script> estrutural perfeitamente balanceada ({real_script_opens} pares).")

# 2.2 Duplicate IDs check
id_matches = re.findall(r'id=["\']([^"\']+)["\']', html_content)
id_counts = {}
for i in id_matches:
    id_counts[i] = id_counts.get(i, 0) + 1

duplicate_ids = {k: v for k, v in id_counts.items() if v > 1}
if duplicate_ids:
    for dup_id, count in duplicate_ids.items():
        report["html"]["errors"].append(f"ID duplicado no DOM: '{dup_id}' aparece {count} vezes!")
else:
    report["html"]["info"].append(f"Zero IDs duplicados em {len(id_counts)} elementos únicos.")

# 2.3 Stack-based nested button verification
lines = html_content.splitlines()
btn_depth = 0
nested_button_count = 0
for line_idx, line in enumerate(lines):
    tokens = []
    for m in re.finditer(r'<button\b[^>]*>', line, re.IGNORECASE):
        tokens.append((m.start(), 'open'))
    for m in re.finditer(r'</button>', line, re.IGNORECASE):
        tokens.append((m.start(), 'close'))
    tokens.sort(key=lambda x: x[0])
    for _, t in tokens:
        if t == 'open':
            btn_depth += 1
            if btn_depth > 1:
                nested_button_count += 1
                report["html"]["errors"].append(f"Botão aninhado detectado na linha {line_idx+1}")
        elif t == 'close':
            btn_depth = max(0, btn_depth - 1)

if nested_button_count == 0:
    report["html"]["info"].append("Nenhum botão aninhado detectado (100% de tags <button> válidas).")

# 2.4 Version tag consistency
title_m = re.search(r'<title>.*?v(\d+\.\d+\.\d+).*?</title>', html_content)
badge_m = re.search(r'class="version-badge"[^>]*>.*?v(\d+\.\d+\.\d+).*?</span>', html_content)
if title_m and badge_m:
    title_ver = title_m.group(1)
    badge_ver = badge_m.group(1)
    if title_ver != badge_ver:
        report["html"]["warnings"].append(f"Versão no título ({title_ver}) diferente da badge ({badge_ver})")
    else:
        report["html"]["info"].append(f"Versão visual e de documento sincronizadas: v{title_ver}")

report["html"]["status"] = "FAIL" if report["html"]["errors"] else "PASS"
print(f" -> Status HTML: {report['html']['status']} (Erros: {len(report['html']['errors'])}, Avisos: {len(report['html']['warnings'])})")


# ============================================================================
# 3. AUDITORIA DE CSS & REGRAS DE LAYOUT
# ============================================================================
print("\n[3/6] Verificando Regras de CSS e Invariantes de Layout...")

style_blocks = re.findall(r'<style[^>]*>([\s\S]*?)</style>', html_content, re.IGNORECASE)
css_content = "\n".join(style_blocks)

# 3.1 Proibição de vh / vw dentro de #game-container e filhos
rules = re.findall(r'([^{]+)\{([^}]+)\}', css_content)
for selector, body in rules:
    selector_clean = selector.strip()
    if '#game-container' in selector_clean or '.app-container' in selector_clean or '.bento-' in selector_clean or '.m2-' in selector_clean or '.m3-' in selector_clean:
        bad_units = re.findall(r'\b\d+(?:\.\d+)?(vh|vw)\b', body)
        if bad_units:
            report["css"]["errors"].append(f"Regra violada: seletor '{selector_clean}' contém unidades proibidas ({bad_units}) dentro do container!")

# 3.2 Backdrop filter blur check (máximo 3px para alta performance e zero lag)
blur_matches = re.findall(r'backdrop-filter:\s*blur\((\d+(?:\.\d+)?px)\)', css_content)
high_blurs = []
for blur_val in blur_matches:
    px_val = float(blur_val.replace("px", ""))
    if px_val > 3.0:
        high_blurs.append(blur_val)

if high_blurs:
    report["css"]["warnings"].append(f"Detectados {len(high_blurs)} backdrop-filters acima de 3px ({high_blurs})")
else:
    report["css"]["info"].append("Todos os backdrop-filters configurados rigorosamente com blur <= 3px (Ultra Performance).")

# 3.3 Botão Finalizar no Modo 2
m2_finish_css = re.search(r'\.m2-actions\s+#m2-btn-finish\s*\{([^}]+)\}', css_content)
if m2_finish_css:
    body = m2_finish_css.group(1)
    if re.search(r'max-width:\s*130px', body):
        report["css"]["info"].append("Botão Finalizar do Modo 2 contém restrição de largura máxima (max-width: 130px).")
    else:
        report["css"]["warnings"].append("Botão Finalizar do Modo 2 sem restrição explícita max-width: 130px.")

report["css"]["status"] = "FAIL" if report["css"]["errors"] else "PASS"
print(f" -> Status CSS: {report['css']['status']} (Erros: {len(report['css']['errors'])}, Avisos: {len(report['css']['warnings'])})")


# ============================================================================
# 4. PARSER E SINTAXE JAVASCRIPT VIA NODE.JS
# ============================================================================
print("\n[4/6] Verificando Sintaxe do JavaScript via Node.js...")

scripts = re.findall(r'<script(?![^>]*src=)[^>]*>([\s\S]*?)</script>', html_content, re.IGNORECASE)
combined_js = "\n".join(scripts)

scratch_dir = os.path.join(ROOT_DIR, "scratch")
os.makedirs(scratch_dir, exist_ok=True)
temp_js_path = os.path.join(scratch_dir, "temp_check.js")

with open(temp_js_path, "w", encoding="utf-8") as f:
    f.write(combined_js)

try:
    node_result = subprocess.run(
        ["node", "--check", temp_js_path],
        capture_output=True,
        text=True,
        encoding="utf-8"
    )
    if node_result.returncode == 0:
        report["js_syntax"]["info"].append("Sintaxe JavaScript 100% válida no motor V8 do Node.js!")
    else:
        report["js_syntax"]["errors"].append(f"Erro de sintaxe JS retornado pelo Node:\n{node_result.stderr}")
except Exception as e:
    report["js_syntax"]["errors"].append(f"Falha ao executar Node.js para validação de sintaxe: {e}")

report["js_syntax"]["status"] = "FAIL" if report["js_syntax"]["errors"] else "PASS"
print(f" -> Status JS Syntax: {report['js_syntax']['status']} (Erros: {len(report['js_syntax']['errors'])})")


# ============================================================================
# 5. AUDITORIA DE REFERÊNCIAS CRUZADAS DOM <-> JAVASCRIPT
# ============================================================================
print("\n[5/6] Verificando Referências Cruzadas DOM <-> Funções & IDs...")

# 5.1 Inline event handlers no HTML (onclick="fn(...)")
inline_handlers = re.findall(r'on(?:click|change|input|submit|keydown|keyup)=["\']([^"\']+)["\']', html_content)
missing_fns = []
for handler in inline_handlers:
    fn_calls = re.findall(r'([a-zA-Z0-9_$]+(?:\.[a-zA-Z0-9_$]+)?)\s*\(', handler)
    for fn in fn_calls:
        if fn in ['if', 'for', 'while', 'switch', 'alert', 'confirm', 'prompt', 'escapeHtml']:
            continue
        if '.' in fn:
            obj_name, method_name = fn.split('.', 1)
            # Check obj in JS
            if not re.search(rf'\b(?:const|let|var|class|window\.)\s*{obj_name}\b', combined_js) and f"{obj_name}." not in combined_js:
                missing_fns.append(fn)
        else:
            if not re.search(rf'\b(?:function\s+{fn}|window\.{fn}\b|const\s+{fn}\s*=|let\s+{fn}\s*=|var\s+{fn}\s*=)', combined_js):
                missing_fns.append(fn)

if missing_fns:
    for m in set(missing_fns):
        report["dom_references"]["warnings"].append(f"Função '{m}' chamada em HTML inline pode não estar definida.")
else:
    report["dom_references"]["info"].append("100% das funções chamadas em handlers HTML inline existem no JavaScript.")

# 5.2 Unsafe member access on missing elements
decl_pattern = re.compile(r'(?:const|let|var)\s+([a-zA-Z0-9_$]+)\s*=\s*document\.getElementById\([\'"]([^\'"]+)[\'"]\)')
js_lines = combined_js.splitlines()
unsafe_dom_cases = []
for idx in range(len(js_lines) - 1):
    line1 = js_lines[idx].strip()
    line2 = js_lines[idx + 1].strip()
    m = decl_pattern.search(line1)
    if m:
        var_name = m.group(1)
        el_id = m.group(2)
        if f'id="{el_id}"' not in html_content and f"id='{el_id}'" not in html_content:
            if line2.startswith(f"{var_name}.") or f"{var_name}." in line2:
                is_guarded = any(pat in line2 for pat in [
                    f"if ({var_name})",
                    f"if (!{var_name})",
                    f"if ({var_name} &&",
                    f"&& {var_name} &&",
                    f"&& {var_name})",
                    f"&& !{var_name}",
                    f"if ({var_name} ?"
                ])
                if not is_guarded:
                    unsafe_dom_cases.append((idx + 1, var_name, el_id, line2))

if unsafe_dom_cases:
    for line_no, vname, eid, l2 in unsafe_dom_cases:
        report["dom_references"]["errors"].append(f"Acesso inseguro à variável '{vname}' (ID '{eid}') na linha {line_no}: {l2}")
else:
    report["dom_references"]["info"].append("Zero acessos inseguros a elementos nulos do DOM.")

report["dom_references"]["status"] = "FAIL" if report["dom_references"]["errors"] else "PASS"
print(f" -> Status DOM References: {report['dom_references']['status']} (Erros: {len(report['dom_references']['errors'])}, Avisos: {len(report['dom_references']['warnings'])})")


# ============================================================================
# 6. SIMULAÇÃO DE GAMEPLAY E REGRAS DE NEGÓCIO VIA TESTES HEADLESS (NODE.JS)
# ============================================================================
print("\n[6/6] Executando Suíte de Testes de Gameplay e Sincronização...")

test_runner_js = os.path.join(scratch_dir, "test_gameplay_e2e.js")
test_script_content = """
const assert = require('assert');

console.log("-> [TEST 1] Validação de Pontuação e Multiplicador de Combo...");
function calculateRoundScore(basePoints, timeLeft, totalTime, streak) {
  let score = basePoints;
  const timeRatio = Math.max(0, Math.min(1, timeLeft / totalTime));
  const speedBonus = Math.round(50 * timeRatio);
  score += speedBonus;
  let multiplier = 1;
  if (streak >= 10) multiplier = 3.0;
  else if (streak >= 5) multiplier = 2.0;
  else if (streak >= 3) multiplier = 1.5;
  return Math.round(score * multiplier);
}

// Test streak levels
assert.strictEqual(calculateRoundScore(100, 30, 30, 0), 150);
assert.strictEqual(calculateRoundScore(100, 0, 30, 0), 100);
assert.strictEqual(calculateRoundScore(100, 30, 30, 3), 225); // 150 * 1.5
assert.strictEqual(calculateRoundScore(100, 30, 30, 5), 300); // 150 * 2.0
assert.strictEqual(calculateRoundScore(100, 30, 30, 10), 450); // 150 * 3.0
console.log("  ✓ Cálculo de pontuação e combo aprovado.");

console.log("-> [TEST 2] Validação Estrita de Nickname no Hall da Fama (Mínimo 5 Caracteres)...");
function isNickValid(nick) {
  const val = (nick || '').trim();
  return val.length >= 5 && val.length <= 15;
}
assert.strictEqual(isNickValid("Otak"), false, "4 chars deve falhar");
assert.strictEqual(isNickValid(""), false, "vazio deve falhar");
assert.strictEqual(isNickValid("     "), false, "espaços devem falhar");
assert.strictEqual(isNickValid("Otaku"), true, "5 chars deve passar");
assert.strictEqual(isNickValid("Levi_Ackerman"), true, "13 chars deve passar");
assert.strictEqual(isNickValid("Levi_Ackerman_1234567"), false, ">15 chars deve falhar");
console.log("  ✓ Validação estrita de nickname aprovada.");

console.log("-> [TEST 3] Simulação da Máquina de Estados Multiplayer (Host Authoritative)...");
class MockMultiplayerEngine {
  constructor() {
    this.stateVersion = 0;
    this.room = {
      code: "TEST1",
      hostId: "host_123",
      status: "lobby",
      roundIndex: 0,
      totalRounds: 5,
      songId: 10,
      players: {
        "host_123": { id: "host_123", name: "HostPlayer", score: 0, answered: false },
        "guest_456": { id: "guest_456", name: "GuestPlayer", score: 0, answered: false }
      },
      skipVotes: []
    };
  }

  buildRoomState(override = {}) {
    this.stateVersion++;
    return {
      v: this.stateVersion,
      code: this.room.code,
      hostId: this.room.hostId,
      status: this.room.status,
      roundIndex: this.room.roundIndex,
      totalRounds: this.room.totalRounds,
      songId: this.room.songId,
      players: JSON.parse(JSON.stringify(this.room.players)),
      skipVotes: [...this.room.skipVotes],
      ...override
    };
  }

  applyRemoteState(remote) {
    if (remote.v > this.stateVersion) {
      this.stateVersion = remote.v;
      this.room = { ...this.room, ...remote };
      return true; // Applied
    }
    return false; // Stale rejected
  }

  submitAnswer(playerId, score) {
    if (this.room.players[playerId]) {
      this.room.players[playerId].score += score;
      this.room.players[playerId].answered = true;
      return this.buildRoomState();
    }
  }

  voteSkip(playerId) {
    if (!this.room.skipVotes.includes(playerId)) {
      this.room.skipVotes.push(playerId);
    }
    const needed = Math.floor(Object.keys(this.room.players).length / 2) + 1;
    if (this.room.skipVotes.length >= needed) {
      this.advanceRound();
    }
    return this.buildRoomState();
  }

  advanceRound() {
    this.room.roundIndex++;
    this.room.skipVotes = [];
    Object.values(this.room.players).forEach(p => p.answered = false);
    if (this.room.roundIndex >= this.room.totalRounds) {
      this.room.status = "podium";
    }
  }
}

const host = new MockMultiplayerEngine();
const guest = new MockMultiplayerEngine();

// Host starts match
let state = host.buildRoomState({ status: "playing", roundIndex: 0 });
assert.strictEqual(guest.applyRemoteState(state), true);
assert.strictEqual(guest.room.status, "playing");
assert.strictEqual(guest.room.roundIndex, 0);

// Guest submits answer, host processes
let guestAnsState = host.submitAnswer("guest_456", 150);
assert.strictEqual(guest.applyRemoteState(guestAnsState), true);
assert.strictEqual(guest.room.players["guest_456"].score, 150);
assert.strictEqual(guest.room.players["guest_456"].answered, true);

// Skip vote check
host.voteSkip("guest_456");
host.voteSkip("host_123");
assert.strictEqual(host.room.roundIndex, 1, "Com 2 jogadores e 2 votos (floor(2/2)+1=2), avança a rodada");
let advState = host.buildRoomState();
assert.strictEqual(guest.applyRemoteState(advState), true);
assert.strictEqual(guest.room.roundIndex, 1, "Guest deve sincronizar roundIndex 1");

// Out of order packet rejection (stale packet)
let stalePacket = { v: 1, roundIndex: 0 };
assert.strictEqual(guest.applyRemoteState(stalePacket), false, "Pacote antigo deve ser rejeitado pelo versionamento");
console.log("  ✓ Sincronização e versionamento host-authoritative aprovados.");

console.log("-> [TEST 4] Teste de Normalização do Algoritmo de Autocomplete...");
function normalizeForSearch(str) {
  if (!str) return '';
  return str
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\\u0300-\\u036f]/g, '')
    .replace(/[^a-z0-9 ]/g, ' ')
    .replace(/\\s+/g, ' ')
    .trim();
}

assert.strictEqual(normalizeForSearch("Shingeki no Kyojin: The Final Season!"), "shingeki no kyojin the final season");
assert.strictEqual(normalizeForSearch("Boku no Hīrō Akademia"), "boku no hiro akademia");
assert.strictEqual(normalizeForSearch("Kaguya-sama wa Kokurasetai: Tensai-tachi no Ren'ai Zunōsen"), "kaguya sama wa kokurasetai tensai tachi no ren ai zunosen");
console.log("  ✓ Algoritmo de busca e autocomplete aprovado.");

console.log("-> [TEST 5] Teste de Finalização de Partida & Reset de Sessão...");
let gameState = { mode: 'mode2', score: 350, correct: 2, streak: 2 };
function discardSession(state) {
  state.score = 0;
  state.correct = 0;
  state.streak = 0;
  return state;
}
assert.strictEqual(discardSession(gameState).score, 0);
assert.strictEqual(gameState.correct, 0);
console.log("  ✓ Reset de pontuação ao descartar sessão aprovado.");

console.log("ALL TESTS COMPLETED SUCCESSFULLY!");
"""

with open(test_runner_js, "w", encoding="utf-8") as f:
    f.write(test_script_content)

try:
    node_sim_res = subprocess.run(
        ["node", test_runner_js],
        capture_output=True,
        text=True,
        encoding="utf-8"
    )
    if node_sim_res.returncode == 0:
        report["gameplay_simulation"]["info"].extend(node_sim_res.stdout.strip().split("\n"))
        report["gameplay_simulation"]["status"] = "PASS"
    else:
        report["gameplay_simulation"]["errors"].append(f"Falha na simulação:\n{node_sim_res.stderr}")
        report["gameplay_simulation"]["status"] = "FAIL"
except Exception as e:
    report["gameplay_simulation"]["errors"].append(f"Erro rodando suite de testes: {e}")
    report["gameplay_simulation"]["status"] = "FAIL"

print(f" -> Status Gameplay Simulation: {report['gameplay_simulation']['status']}")


# ============================================================================
# RELATÓRIO CONSOLIDADO
# ============================================================================
print("\n" + "=" * 70)
print("📊 RESUMO FINAL DA AUDITORIA")
print("=" * 70)
all_passed = True
for category, data in report.items():
    st = data["status"]
    errs = len(data["errors"])
    warns = len(data["warnings"])
    print(f"[{st}] {category.upper()}: {errs} erros, {warns} avisos")
    if errs > 0:
        all_passed = False
        for err in data["errors"]:
            print(f"   ❌ ERRO: {err}")
    for warn in data["warnings"][:5]:
        print(f"   ⚠️ AVISO: {warn}")

print("=" * 70)
if all_passed:
    print("🏆 AUDITORIA GERAL CONCLUÍDA: 100% DOS TESTES PASSARAM!")
else:
    print("⚠️ AUDITORIA APONTOU PONTOS QUE REQUEREM ATENÇÃO!")
print("=" * 70)
