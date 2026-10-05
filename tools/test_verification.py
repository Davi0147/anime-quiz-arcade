import re
import sys

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

checks = []

# 1. HTML structure and tags
checks.append(('Closing tags present', '</html>' in html and '</body>' in html))
checks.append(('Version badge v3.0.0', 'v3.0.0' in html))

# 2. Canvases
checks.append(('Mode 1 spectrum canvas', 'id="m1-spectrum-canvas"' in html))
checks.append(('Mode 2 spectrum canvas', 'id="m2-spectrum-canvas"' in html))
checks.append(('Gamer confetti canvas', 'id="gamer-confetti-canvas"' in html))

# 3. SoundGroups and Audio Settings Popover
checks.append(('Audio settings popover', 'id="audio-settings-popover"' in html))
checks.append(('BGM slider', 'id="bgm-vol-slider"' in html))
checks.append(('SFX slider', 'id="sfx-vol-slider"' in html))
checks.append(('AudioManager object with BGM and SFX', 'AudioManager' in html and 'setBgmVolume' in html and 'setSfxVolume' in html))

# 4. Visualizer and Celebration Engines
checks.append(('VisualizerEngine implementation', 'VisualizerEngine' in html and 'drawOnCanvas' in html and 'setupAudioContext' in html))
checks.append(('ConfettiEngine implementation', 'ConfettiEngine' in html and 'burst(' in html))
checks.append(('Combo Fire Badge implementation', 'combo-super-fire' in html and 'updateStreakBadge' in html))

# 5. Mode 1, Mode 2 and Mode 3 integration
checks.append(('Mode 1 header does not leak year', re.search(r'm1RoundIndicator\.textContent\s*=\s*`[^`]*\$\{song\.year\}[^`]*`', html) is None))
checks.append(('Mode 1 tags do not include difficulty', re.search(r'const tagsList\s*=\s*\[[^\]]*\$\{song\.diff\}[^\]]*\]', html) is None))
checks.append(('Mode 2 visual card exists', 'id="m2-visual-card"' in html))
checks.append(('Mode 3 uses official poster', 'm3AnsPoster.src = officialPoster' in html))
checks.append(('Keyboard shortcuts for Mode 2', "e.key === '1'" in html and "e.key === 'Enter'" in html))

# 6. User Feedback Specific Verifications
checks.append(('No sound-bars equalizer elements in HTML', 'class="sound-bars' not in html))
checks.append(('No "0ms local" in code', '(0ms local)' not in html))
checks.append(('Custom play icon present in HTML', 'icons/play-button.png' in html))
checks.append(('Custom pause icon present in code', 'icons/pause.png' in html))
checks.append(('formatDifficulty function defined', 'function formatDifficulty' in html))
checks.append(('Single star for Fácil in formatDifficulty', "'⭐ Fácil'" in html))

# 7. Phase 3: Multiplayer Rooms & Leaderboard Verifications
checks.append(('PeerJS local script tag', 'libs/peerjs.min.js' in html))
checks.append(('PeerJS CDN fallback tag', 'unpkg.com/peerjs' in html))
checks.append(('Mode 4 renamed to Salas & Placar', 'Salas & Placar' in html))
checks.append(('Multiplayer HUD bar in DOM', 'id="mp-hud-bar"' in html))
checks.append(('Multiplayer Sub-tabs in Mode 4', 'id="mp-pre-room-view"' in html and 'id="mp-leaderboard-panel"' in html))
checks.append(('Lobby view and Player Slots', 'id="mp-lobby-view"' in html and 'id="mp-lobby-players-grid"' in html))
checks.append(('Podium and Pillars row in DOM', 'id="mp-podium-view"' in html and 'id="mp-podium-pillars"' in html))
checks.append(('30 Rodadas option available', 'value="30"' in html and '30 Rodadas' in html))
checks.append(('MultiplayerEngine object exists', 'const MultiplayerEngine =' in html))
checks.append(('MultiplayerEngine initialized on DOMContentLoaded', 'MultiplayerEngine.init()' in html))
checks.append(('Automatic Name Disambiguation logic', 'disambiguateName(' in html))
checks.append(('Fast Skip Voting (> 50% threshold)', 'Math.floor(total / 2) + 1' in html))
checks.append(('Test Bot generator button and logic', 'addTestBot()' in html))
checks.append(('Mode 1 hooks into MultiplayerEngine', 'MultiplayerEngine.onPlayerAnswer(true, points)' in html))
checks.append(('Mode 2 hooks into MultiplayerEngine', 'MultiplayerEngine.onPlayerAnswer(true, pts)' in html))
checks.append(('Mode 3 hooks into MultiplayerEngine', 'MultiplayerEngine.onPlayerAnswer(true, pts)' in html))
checks.append(('Multiplayer next round voting hooks in next buttons', 'MultiplayerEngine.voteSkip()' in html))
# 8. Live Ranking Sidebar & Dynamic Speed Bonus Verifications
checks.append(('Live Ranking Sidebar element in DOM', 'id="mp-live-sidebar"' in html))
checks.append(('Live Ranking Sidebar list container', 'id="mp-sidebar-list"' in html))
checks.append(('renderLiveSidebar method in MultiplayerEngine', 'renderLiveSidebar()' in html))
checks.append(('Animated rank trend badges in CSS', 'mp-rank-trend.up' in html and 'mp-rank-trend.down' in html))
checks.append(('Speed bonus calculation in MultiplayerEngine', 'calculateSpeedBonus()' in html))
checks.append(('Speed bonus feedback breakdown in modes', 'Bônus Rapidez:' in html))
checks.append(('updateGlobalKPIs function for unified score', 'function updateGlobalKPIs()' in html))
checks.append(('Unified streak in MultiplayerEngine', 'this.myStreak' in html))
checks.append(('Jujutsu Kaisen S2 official video ID in code', '5yb2N3pnztU' in html))

# 9. Arcade Floating Juice, Leave Room & Layout Stabilization
checks.append(('Floating Arcade container in DOM', 'id="floating-arcade-container"' in html))
checks.append(('FloatingArcade engine object defined', 'const FloatingArcade =' in html))
checks.append(('FloatingArcade spawned on Mode 1, 2, 3', 'FloatingArcade.spawn(' in html))
checks.append(('Leave room button in MP HUD bar', 'id="mp-hud-leave-btn"' in html))
checks.append(('confirmLeaveRoom method in MultiplayerEngine', 'confirmLeaveRoom()' in html))
checks.append(('beforeunload listener for active match', "beforeunload" in html and "isMatchActive" in html))
checks.append(('Defensive min-height on quiz-card', 'min-height: 520px' in html))
checks.append(('Defensive min-height on target anime name', 'min-height: 44px' in html))
checks.append(('Defensive min-height on music-card', 'min-height: 62px' in html))
checks.append(('Sidebar flex-direction column containment', 'display: flex' in html and 'flex-direction: column' in html and 'box-sizing: border-box' in html))

# 10. Regressões: engine exposta no window, deltas de pontuação, classe de 1º lugar
checks.append(('MultiplayerEngine exposed on window (root cause fix)', 'window.MultiplayerEngine = MultiplayerEngine;' in html))
checks.append(('Host player id guaranteed via ensurePlayerId', 'id: this.ensurePlayerId(),' in html))
checks.append(('Live score delta badge (+X)', 'mp-rank-delta' in html and 'scoreDeltas' in html))
checks.append(('Sidebar no longer uses colliding .rank-1 class', "'rank-1' : ''" not in html and 'mp-first-place' in html))

# 11. Timer Panic Mode, Áudio Beep e Defesas Anti-Skip Fantasma
checks.append(('Timer Panic mode CSS with shake animation', 'timerPanicShake' in html and '.mp-hud-timer-pill.panic' in html))
checks.append(('Audio synthesizer countdown beep method', 'playCountdownBeep(secondsLeft)' in html))
checks.append(('Multiplayer waiting banner in DOM', 'id="mp-waiting-banner"' in html))
checks.append(('Centralized clearAllTimers method', 'clearAllTimers()' in html))
checks.append(('Player answer tracking Set (answeredPlayers)', 'answeredPlayers: new Set()' in html))
checks.append(('checkAllAnswered method for seamless group advancement', 'checkAllAnswered()' in html))
checks.append(('Adaptive podium pillars for 1, 2 or 3 players', 'sorted.length === 1' in html and 'sorted.length === 2' in html))


all_passed = True
for name, res in checks:
    status = "PASS" if res else "FAIL"
    print(f'[{status}] {name}')
    if not res:
        all_passed = False

if not all_passed:
    print("\nERRO: Algumas verificacoes falharam!")
    sys.exit(1)
else:
    print("\nTODOS OS TESTES (FASES 1, 2 E 3) PASSARAM COM 100% DE SUCESSO!")
