import json
import os

DIR = "C:/Users/luizd/.gemini/antigravity/scratch/anime-music-quiz"
with open(os.path.join(DIR, "anime_songs_verified.json"), "r", encoding="utf-8") as f:
    songs = json.load(f)

with open(os.path.join(DIR, "tools", "anime_scenes.json"), "r", encoding="utf-8") as f:
    scenes = json.load(f)

with open(os.path.join(DIR, "tools", "anime_autocomplete_db.json"), "r", encoding="utf-8") as f:
    autocomplete = json.load(f)

songs_json_str = json.dumps(songs, ensure_ascii=False)
scenes_json_str = json.dumps(scenes, ensure_ascii=False)
autocomplete_json_str = json.dumps(autocomplete, ensure_ascii=False)

html_template = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />
  <meta http-equiv="Pragma" content="no-cache" />
  <meta http-equiv="Expires" content="0" />
  <title>🎧 Anime Music & Scene Quiz • v3.3.0 Arcade</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&family=JetBrains+Mono:wght@500;700;800&display=swap" rel="stylesheet">
  <script src="libs/peerjs.min.js"></script>
  <script>if (typeof Peer === 'undefined') { document.write('<' + 'script src="https://unpkg.com/peerjs@1.5.4/dist/peerjs.min.js"><\\/' + 'script>'); }</script>
  <style>
    :root {
      --bg: #070913;
      --card: #0f1424;
      --card-border: #1e2640;
      --card-hover: #161e36;
      --accent: #6366f1;
      --accent-glow: rgba(99, 102, 241, 0.45);
      --accent-hover: #4f46e5;
      --gold: #f59e0b;
      --gold-glow: rgba(245, 158, 11, 0.4);
      --green: #10b981;
      --green-glow: rgba(16, 185, 129, 0.4);
      --red: #ef4444;
      --red-glow: rgba(239, 68, 68, 0.4);
      --cyan: #06b6d4;
      --cyan-glow: rgba(6, 182, 212, 0.4);
      --rose: #f43f5e;
      --text: #f8fafc;
      --text-muted: #94a3b8;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      background: radial-gradient(circle at 50% 0%, #161b36 0%, var(--bg) 80%);
      color: var(--text);
      font-family: 'Plus Jakarta Sans', sans-serif;
      min-height: 100vh;
      padding: 20px 14px 40px;
      display: flex;
      flex-direction: column;
      align-items: center;
    }

    .container {
      width: 100%;
      max-width: 900px;
    }

    /* Global Header & Version Tag */
    header {
      text-align: center;
      margin-bottom: 16px;
      position: relative;
    }

    .header-top-bar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 10px;
      flex-wrap: wrap;
      gap: 10px;
    }

    .version-badge {
      background: rgba(99, 102, 241, 0.15);
      border: 1px solid rgba(99, 102, 241, 0.4);
      color: #a5b4fc;
      font-size: 11px;
      font-weight: 800;
      padding: 4px 12px;
      border-radius: 999px;
      text-transform: uppercase;
      letter-spacing: 1px;
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }

    /* Master Volume Controls */
    .master-vol-control {
      display: flex;
      align-items: center;
      gap: 8px;
      background: var(--card);
      border: 1px solid var(--card-border);
      padding: 5px 12px;
      border-radius: 999px;
      font-size: 12px;
    }

    .master-vol-control input[type="range"] {
      width: 80px;
      accent-color: var(--accent);
      cursor: pointer;
    }

    .vol-btn-mute {
      background: none;
      border: none;
      color: var(--text);
      cursor: pointer;
      font-size: 14px;
      display: flex;
      align-items: center;
    }

    h1 {
      font-size: clamp(22px, 5vw, 36px);
      font-weight: 800;
      background: linear-gradient(135deg, #ffffff 30%, #a5b4fc 70%, #ec4899 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      margin-bottom: 4px;
      letter-spacing: -0.5px;
    }

    p.subtitle {
      color: var(--text-muted);
      font-size: 13px;
      max-width: 650px;
      margin: 0 auto;
    }

    /* Challenge Mode Alert Bar (Multiplayer Seed) */
    .challenge-banner {
      display: none;
      background: linear-gradient(90deg, rgba(236, 72, 153, 0.2), rgba(99, 102, 241, 0.2));
      border: 1px solid #ec4899;
      border-radius: 12px;
      padding: 10px 16px;
      margin-bottom: 16px;
      text-align: center;
      font-size: 13px;
      font-weight: 700;
      color: #fbcfe8;
      animation: pulse-border 2s infinite;
    }

    @keyframes pulse-border {
      0%, 100% { box-shadow: 0 0 10px rgba(236, 72, 153, 0.2); }
      50% { box-shadow: 0 0 20px rgba(236, 72, 153, 0.6); }
    }

    /* Main Mode Navigation Tabs (4 Tabs) */
    .mode-nav {
      display: flex;
      justify-content: center;
      gap: 8px;
      margin: 16px 0 20px;
      background: #0d1222;
      padding: 6px;
      border-radius: 16px;
      border: 1px solid var(--card-border);
      flex-wrap: wrap;
    }

    .mode-tab-btn {
      background: transparent;
      border: 1px solid transparent;
      color: var(--text-muted);
      padding: 9px 16px;
      border-radius: 12px;
      font-size: 13px;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.2s ease;
      display: flex;
      align-items: center;
      gap: 7px;
      font-family: inherit;
    }

    .mode-tab-btn:hover {
      color: #ffffff;
      background: rgba(255, 255, 255, 0.05);
    }

    .mode-tab-btn.active {
      background: var(--accent);
      color: #ffffff;
      border-color: var(--accent);
      box-shadow: 0 0 16px var(--accent-glow);
    }

    /* Scoreboard KPIs */
    .scoreboard {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
      gap: 10px;
      margin-bottom: 18px;
    }

    .score-card {
      background: var(--card);
      border: 1px solid var(--card-border);
      border-radius: 14px;
      padding: 12px;
      text-align: center;
      box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    }

    .score-label {
      font-size: 10px;
      text-transform: uppercase;
      color: var(--text-muted);
      font-weight: 700;
      letter-spacing: 0.6px;
      margin-bottom: 3px;
    }

    .score-val {
      font-size: 22px;
      font-weight: 800;
      font-family: 'JetBrains Mono', monospace;
      color: #ffffff;
    }

    /* Global Quiz Card Container */
    .quiz-card {
      background: var(--card);
      border: 1px solid var(--card-border);
      border-radius: 20px;
      padding: 22px;
      box-shadow: 0 20px 40px rgba(0,0,0,0.4);
      position: relative;
      margin-bottom: 24px;
      min-height: 520px;
      box-sizing: border-box;
    }

    .quiz-card::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 4px;
      background: linear-gradient(90deg, #6366f1, #ec4899, #f59e0b, #10b981);
      border-radius: 20px 20px 0 0;
    }

    .quiz-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 16px;
      flex-wrap: wrap;
      gap: 8px;
    }

    .round-indicator {
      font-size: 12px;
      font-weight: 800;
      color: var(--accent);
      text-transform: uppercase;
      letter-spacing: 1px;
    }

    /* Buttons */
    .btn {
      padding: 9px 18px;
      border-radius: 12px;
      font-weight: 700;
      font-size: 13px;
      cursor: pointer;
      transition: all 0.2s ease;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 7px;
      border: none;
      font-family: inherit;
    }

    .btn:disabled {
      opacity: 0.4;
      cursor: not-allowed;
      transform: none !important;
      box-shadow: none !important;
    }

    .btn-primary {
      background: var(--accent);
      color: #fff;
    }
    .btn-primary:hover:not(:disabled) {
      background: var(--accent-hover);
      box-shadow: 0 0 15px var(--accent-glow);
      transform: translateY(-1px);
    }

    .btn-secondary {
      background: #171f38;
      color: #cbd5e1;
      border: 1px solid #2b385e;
    }
    .btn-secondary:hover:not(:disabled) {
      background: #202b4d;
      color: #fff;
      border-color: #3f5187;
    }

    .btn-green {
      background: var(--green);
      color: #042f1a;
      font-weight: 800;
    }
    .btn-green:hover:not(:disabled) {
      background: #059669;
      color: #fff;
      box-shadow: 0 0 16px var(--green-glow);
    }

    .btn-gold {
      background: var(--gold);
      color: #451a03;
      font-weight: 800;
    }
    .btn-gold:hover:not(:disabled) {
      background: #d97706;
      color: #fff;
      box-shadow: 0 0 16px var(--gold-glow);
    }

    .btn-outline {
      background: transparent;
      border: 1px solid #2c385c;
      color: var(--text-muted);
    }
    .btn-outline:hover:not(:disabled) {
      border-color: var(--accent);
      color: #fff;
    }

    /* Tactile Active Press & Arcade Elevation */
    .btn:active:not(:disabled),
    .mode-tab-btn:active:not(:disabled),
    .music-card:active,
    .card-play-btn:active,
    .mp-room-card:active,
    .option-btn:active {
      transform: translateY(1.5px) scale(0.975) !important;
      filter: brightness(1.18) !important;
    }

    /* Sheen / Shimmer Light Sweep on Hover */
    .btn, .mode-tab-btn, .music-card, .card-play-btn, .mp-room-card {
      position: relative;
      overflow: hidden;
    }

    .btn::after,
    .mode-tab-btn::after,
    .music-card::after,
    .mp-room-card::after {
      content: '';
      position: absolute;
      top: 0;
      left: -160%;
      width: 120%;
      height: 100%;
      background: linear-gradient(
        105deg,
        transparent 20%,
        rgba(255, 255, 255, 0.16) 50%,
        transparent 80%
      );
      transform: skewX(-22deg);
      pointer-events: none;
      z-index: 5;
    }

    .btn:hover:not(:disabled)::after,
    .mode-tab-btn:hover:not(:disabled)::after,
    .music-card:hover::after,
    .mp-room-card:hover::after {
      animation: dopamineSheen 0.65s cubic-bezier(0.2, 0.8, 0.2, 1);
    }

    @keyframes dopamineSheen {
      0% { left: -160%; }
      100% { left: 180%; }
    }

    /* Micro-onda de clique (Ripple) */
    .dopamine-ripple {
      position: absolute;
      border-radius: 50%;
      background: radial-gradient(circle, rgba(255, 255, 255, 0.35) 0%, rgba(255, 255, 255, 0) 70%);
      transform: scale(0);
      pointer-events: none;
      animation: dopamineRipplePop 0.5s ease-out forwards;
      z-index: 10;
    }

    @keyframes dopamineRipplePop {
      0% { transform: scale(0); opacity: 0.8; }
      100% { transform: scale(2.2); opacity: 0; }
    }

    /* ==============================================================
       MODO 1: BLIND TEST STYLES
       ============================================================== */
    .player-container {
      position: relative;
      width: 100%;
      aspect-ratio: 16 / 9;
      max-height: 280px;
      background: #080b16;
      border-radius: 14px;
      overflow: hidden;
      border: 2px solid var(--card-border);
      margin-bottom: 20px;
      box-shadow: 0 8px 24px rgba(0,0,0,0.5);
    }

    .player-visual-card {
      position: absolute;
      inset: 0;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      overflow: hidden;
    }

    .player-bg-art {
      position: absolute;
      inset: 0;
      background-size: cover;
      background-position: center;
      opacity: 0;
      transform: scale(1.08);
      transition: opacity 0.6s ease, transform 0.6s ease;
      filter: blur(2px) brightness(0.38);
    }

    .player-visual-card.is-revealed .player-bg-art {
      opacity: 1;
      transform: scale(1);
    }

    .player-scrim {
      position: absolute;
      inset: 0;
      background: radial-gradient(circle at center, rgba(15, 20, 36, 0.4) 0%, rgba(7, 9, 19, 0.88) 100%);
      pointer-events: none;
    }

    .player-blind-content {
      position: relative;
      z-index: 2;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      text-align: center;
      padding: 16px;
    }

    .player-revealed-content {
      position: relative;
      z-index: 2;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      text-align: center;
      padding: 16px 20px;
      animation: fadeIn 0.4s ease;
      width: 100%;
    }

    .revealed-hero-row {
      display: flex;
      align-items: center;
      gap: 16px;
      max-width: 550px;
      text-align: left;
    }

    .revealed-thumb-img {
      width: 68px;
      height: 96px;
      object-fit: cover;
      border-radius: 8px;
      border: 2px solid var(--accent);
      box-shadow: 0 4px 18px rgba(99, 102, 241, 0.45);
      flex-shrink: 0;
    }

    .revealed-thumb-yt {
      width: 120px;
      height: 75px;
      object-fit: cover;
      border-radius: 8px;
      border: 2px solid var(--accent);
      box-shadow: 0 4px 18px rgba(99, 102, 241, 0.45);
      flex-shrink: 0;
    }

    .revealed-info-col {
      display: flex;
      flex-direction: column;
      gap: 3px;
      min-width: 0;
    }

    .revealed-badge {
      font-size: 11px;
      font-weight: 800;
      color: #34d399;
      letter-spacing: 0.5px;
      text-transform: uppercase;
    }

    .revealed-badge.wrong {
      color: #f87171;
    }

    .revealed-anime-title {
      font-size: 20px;
      font-weight: 800;
      color: #ffffff;
      line-height: 1.2;
      text-shadow: 0 2px 10px rgba(0,0,0,0.8);
    }

    .revealed-song-name {
      font-size: 15px;
      font-weight: 700;
      color: #a5b4fc;
    }

    .revealed-artist-meta {
      font-size: 12px;
      color: #cbd5e1;
    }

    .player-container iframe,
    .player-container video {
      display: none !important;
    }

    .blind-mask {
      display: none;
    }

    .vinyl {
      font-size: 56px;
      animation: spin 3.5s linear infinite paused;
      filter: drop-shadow(0 0 15px rgba(99, 102, 241, 0.4));
      margin-bottom: 10px;
    }

    .vinyl.spinning {
      animation-play-state: running;
    }

    @keyframes spin {
      100% { transform: rotate(360deg); }
    }

    .sound-bars {
      display: flex;
      gap: 4px;
      align-items: flex-end;
      height: 24px;
      margin-top: 8px;
    }

    .sound-bars .bar {
      width: 4px;
      background: var(--accent);
      border-radius: 2px;
      height: 4px;
    }

    .sound-bars {
      display: none !important;
    }

    .btn-icon-img {
      width: 16px;
      height: 16px;
      object-fit: contain;
      vertical-align: -2px;
      display: inline-block;
      filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.4));
    }

    .btn-icon-img.btn-icon-sm {
      width: 13px;
      height: 13px;
      vertical-align: -1px;
    }

    .btn-icon-img.btn-icon-lg {
      width: 20px;
      height: 20px;
      vertical-align: -3px;
    }

    /* ==============================================================
       ETAPA 2: GAMER UI & AUDIO SPECTRUM VISUALIZER
       ============================================================== */
    .audio-spectrum-canvas {
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      pointer-events: none;
      z-index: 1;
      opacity: 0.92;
    }

    .gamer-confetti-canvas {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      pointer-events: none;
      z-index: 9999;
    }

    /* Gamer Audio Settings Modal / Popover */
    .audio-btn-toggle {
      background: rgba(99, 102, 241, 0.15);
      border: 1px solid rgba(99, 102, 241, 0.35);
      color: #cbd5e1;
      border-radius: 999px;
      padding: 6px 14px;
      font-size: 12px;
      font-weight: 700;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      cursor: pointer;
      transition: all 0.2s ease;
    }

    .audio-btn-toggle:hover {
      background: rgba(99, 102, 241, 0.3);
      border-color: var(--accent);
      color: #ffffff;
      box-shadow: 0 0 12px rgba(99, 102, 241, 0.35);
    }

    .audio-settings-popover {
      display: none;
      position: absolute;
      top: 44px;
      right: 0;
      background: rgba(13, 18, 34, 0.96);
      backdrop-filter: blur(3px);
      -webkit-backdrop-filter: blur(3px);
      border: 1px solid rgba(99, 102, 241, 0.4);
      border-radius: 14px;
      padding: 16px;
      width: 280px;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.75), 0 0 20px rgba(99, 102, 241, 0.25);
      z-index: 100;
      animation: popoverFade 0.2s ease;
    }

    .audio-settings-popover.active {
      display: block;
    }

    @keyframes popoverFade {
      from { opacity: 0; transform: translateY(-8px); }
      to { opacity: 1; transform: translateY(0); }
    }

    .audio-channel-row {
      display: flex;
      flex-direction: column;
      gap: 6px;
      margin-bottom: 12px;
    }

    .audio-channel-header {
      display: flex;
      justify-content: space-between;
      font-size: 12px;
      font-weight: 700;
      color: #e2e8f0;
    }

    .audio-channel-val {
      color: var(--accent);
      font-weight: 800;
    }

    .audio-slider {
      width: 100%;
      height: 6px;
      border-radius: 3px;
      background: #1e293b;
      accent-color: var(--accent);
      cursor: pointer;
    }

    .audio-mute-toggle-btn {
      width: 100%;
      background: #1e293b;
      border: 1px solid var(--card-border);
      border-radius: 8px;
      color: #cbd5e1;
      padding: 8px;
      font-size: 12px;
      font-weight: 700;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      transition: all 0.2s;
    }

    .audio-mute-toggle-btn:hover {
      background: #334155;
      color: #ffffff;
    }

    .audio-mute-toggle-btn.muted {
      background: rgba(239, 68, 68, 0.2);
      border-color: #ef4444;
      color: #fca5a5;
    }

    /* Gamer Combo Fire Indicator */
    .score-val.combo-fire {
      color: #f59e0b !important;
      text-shadow: 0 0 12px rgba(245, 158, 11, 0.7);
      animation: comboFlame 0.6s ease-in-out infinite alternate;
    }

    .score-val.combo-super-fire {
      color: #ec4899 !important;
      text-shadow: 0 0 16px rgba(236, 72, 153, 0.8), 0 0 24px rgba(99, 102, 241, 0.6);
      animation: comboSuperFlame 0.5s ease-in-out infinite alternate;
    }

    .score-val.combo-hyper-fire {
      color: #38bdf8 !important;
      text-shadow: 0 0 20px rgba(56, 189, 248, 1), 0 0 35px rgba(168, 85, 247, 0.9), 0 0 50px rgba(236, 72, 153, 0.8);
      animation: comboHyperFlame 0.38s ease-in-out infinite alternate;
    }

    @keyframes comboFlame {
      0% { transform: scale(1); filter: drop-shadow(0 0 4px #f59e0b); }
      100% { transform: scale(1.08); filter: drop-shadow(0 0 12px #ef4444); }
    }

    @keyframes comboSuperFlame {
      0% { transform: scale(1.02); filter: drop-shadow(0 0 8px #ec4899); }
      100% { transform: scale(1.14); filter: drop-shadow(0 0 18px #8b5cf6); }
    }

    @keyframes comboHyperFlame {
      0% { transform: scale(1.05) rotate(-1deg); filter: drop-shadow(0 0 10px #38bdf8) drop-shadow(0 0 20px #a855f7); }
      100% { transform: scale(1.22) rotate(1deg); filter: drop-shadow(0 0 25px #38bdf8) drop-shadow(0 0 40px #ec4899); }
    }

    .player-controls-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 10px;
      margin-bottom: 20px;
      flex-wrap: wrap;
    }

    .hints-section {
      background: #0b0f1d;
      border: 1px solid #1a223a;
      border-radius: 14px;
      padding: 16px;
      margin-bottom: 20px;
    }

    .hints-title {
      font-size: 11px;
      font-weight: 800;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.8px;
      margin-bottom: 10px;
    }

    .tags-container {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }

    .hint-tag {
      background: #141a2e;
      border: 1px solid #232d4d;
      color: #94a3b8;
      padding: 6px 12px;
      border-radius: 8px;
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
      user-select: none;
      transition: all 0.2s ease;
    }

    .hint-tag.revealed {
      background: rgba(99, 102, 241, 0.2);
      border-color: rgba(99, 102, 241, 0.5);
      color: #c7d2fe;
    }

    /* AUTOCOMPLETE WRAPPER & DROPDOWN */
    .input-group {
      display: flex;
      gap: 8px;
      margin-bottom: 14px;
      position: relative;
      width: 100%;
      box-sizing: border-box;
    }

    .autocomplete-wrapper {
      position: relative;
      flex: 1;
      min-width: 0;
      display: flex;
    }

    .quiz-input {
      width: 100%;
      min-width: 0;
      box-sizing: border-box;
      background: #090d1a;
      border: 2px solid #1e2640;
      border-radius: 12px;
      padding: 12px 16px;
      color: #fff;
      font-size: 14px;
      font-family: inherit;
      outline: none;
      transition: border-color 0.2s;
    }

    .quiz-input:focus {
      border-color: var(--accent);
      box-shadow: 0 0 15px var(--accent-glow);
    }

    @keyframes shakeError {
      0%, 100% { transform: translateX(0); }
      20%, 60% { transform: translateX(-8px); }
      40%, 80% { transform: translateX(8px); }
    }

    .input-error-shake {
      animation: shakeError 0.4s ease-in-out !important;
      border-color: #ef4444 !important;
      box-shadow: 0 0 18px rgba(239, 68, 68, 0.5) !important;
    }

    @keyframes pulseSuccess {
      0% { transform: scale(1); }
      50% { transform: scale(1.02); }
      100% { transform: scale(1); }
    }

    .input-success-pulse {
      animation: pulseSuccess 0.4s ease-in-out !important;
      border-color: #10b981 !important;
      box-shadow: 0 0 18px rgba(16, 185, 129, 0.5) !important;
    }

    .autocomplete-dropdown {
      position: absolute;
      top: calc(100% + 4px);
      left: 0;
      right: 0;
      background: #0d1326;
      border: 1px solid #233055;
      border-radius: 12px;
      max-height: 220px;
      overflow-y: auto;
      z-index: 1000;
      box-shadow: 0 12px 30px rgba(0,0,0,0.85);
      display: none;
    }

    .autocomplete-item {
      padding: 10px 14px;
      font-size: 13px;
      color: #cbd5e1;
      cursor: pointer;
      border-bottom: 1px solid #161e38;
      display: flex;
      justify-content: space-between;
      align-items: center;
      transition: background 0.15s;
    }

    .autocomplete-item:last-child {
      border-bottom: none;
    }

    .autocomplete-item:hover,
    .autocomplete-item.active {
      background: #1e294b;
      color: #ffffff;
    }

    .autocomplete-item strong {
      color: #818cf8;
    }

    .feedback-box {
      display: none;
      padding: 12px 16px;
      border-radius: 10px;
      font-size: 13px;
      margin-bottom: 16px;
      animation: fadeIn 0.3s ease;
    }

    .feedback-box.correct {
      background: rgba(16, 185, 129, 0.15);
      border: 1px solid rgba(16, 185, 129, 0.4);
      color: #34d399;
      display: block;
    }

    .feedback-box.partial {
      background: rgba(245, 158, 11, 0.15);
      border: 1px solid rgba(245, 158, 11, 0.4);
      color: #fbbf24;
      display: block;
    }

    .feedback-box.wrong {
      background: rgba(239, 68, 68, 0.15);
      border: 1px solid rgba(239, 68, 68, 0.4);
      color: #f87171;
      display: block;
    }

    .answer-card {
      display: none;
      background: linear-gradient(135deg, rgba(99, 102, 241, 0.12), rgba(15, 20, 36, 0.95));
      border: 1px solid rgba(99, 102, 241, 0.35);
      border-radius: 16px;
      padding: 18px;
      margin-bottom: 20px;
    }

    .answer-layout {
      display: flex;
      gap: 16px;
      align-items: center;
    }

    .answer-poster-img {
      width: 72px;
      height: 100px;
      object-fit: cover;
      border-radius: 8px;
      border: 1px solid #2b385e;
      flex-shrink: 0;
    }

    .answer-title {
      font-size: 18px;
      font-weight: 800;
      color: #fff;
      margin-bottom: 4px;
    }

    .answer-meta {
      font-size: 13px;
      color: #a5b4fc;
      margin-bottom: 6px;
    }

    .answer-syns {
      font-size: 11px;
      color: var(--text-muted);
    }

    .nav-row {
      display: flex;
      justify-content: space-between;
      gap: 10px;
    }

    /* ==============================================================
       MODO 2: "QUAL É A ABERTURA?" (3 MÚSICAS COM BORDA ACESA)
       ============================================================== */
    .target-anime-banner {
      display: flex;
      gap: 14px;
      align-items: center;
      background: linear-gradient(135deg, rgba(19, 26, 48, 0.95) 0%, rgba(13, 18, 34, 0.98) 100%);
      border: 1px solid #243054;
      border-radius: 14px;
      padding: 10px 16px;
      margin-bottom: 14px;
    }

    .target-poster-wrapper {
      width: 52px;
      height: 72px;
      border-radius: 8px;
      overflow: hidden;
      flex-shrink: 0;
      border: 1px solid #33426e;
      box-shadow: 0 4px 12px rgba(0,0,0,0.5);
    }

    .target-poster-img {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }

    .target-info-col {
      flex: 1;
      min-width: 0;
    }

    .target-pre-title {
      font-size: 10px;
      font-weight: 800;
      text-transform: uppercase;
      color: #818cf8;
      letter-spacing: 0.8px;
      margin-bottom: 2px;
    }

    .target-anime-name {
      font-size: 16px;
      font-weight: 800;
      color: #ffffff;
      margin-bottom: 4px;
      letter-spacing: -0.2px;
      line-height: 1.2;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      min-height: 20px;
      display: flex;
      align-items: center;
    }

    .target-meta-pills {
      display: flex;
      gap: 6px;
      flex-wrap: wrap;
      min-height: 22px;
      align-items: center;
    }

    .pill-chip {
      background: #19223c;
      border: 1px solid #293860;
      color: #cbd5e1;
      padding: 3px 8px;
      border-radius: 6px;
      font-size: 11px;
      font-weight: 600;
      display: inline-flex;
      align-items: center;
      gap: 4px;
    }

    .m2-player-container {
      height: 214px;
      min-height: 214px;
      max-height: 214px;
      margin-bottom: 0;
    }

    .music-cards-grid {
      display: flex;
      flex-direction: column;
      gap: 8px;
      margin-bottom: 10px;
    }

    .music-card {
      background: #11172a;
      border: 2px solid #1e2848;
      border-radius: 12px;
      padding: 8px 12px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      min-height: 48px;
      box-sizing: border-box;
      cursor: pointer;
      transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
      user-select: none;
      position: relative;
    }

    .music-card:hover {
      background: #161e36;
      border-color: #3b4c7d;
      transform: translateY(-1px);
    }

    .music-card.selected {
      border-color: var(--cyan);
      box-shadow: 0 0 20px var(--cyan-glow), inset 0 0 10px rgba(6, 182, 212, 0.15);
      background: #13203c;
    }

    .music-card.playing {
      border-color: var(--accent);
      box-shadow: 0 0 22px var(--accent-glow), inset 0 0 12px rgba(99, 102, 241, 0.2);
    }

    .music-card.revealed-correct {
      border-color: var(--green) !important;
      background: rgba(16, 185, 129, 0.15) !important;
      box-shadow: 0 0 25px var(--green-glow) !important;
    }

    .music-card.revealed-wrong {
      border-color: var(--red) !important;
      background: rgba(239, 68, 68, 0.15) !important;
      box-shadow: 0 0 25px var(--red-glow) !important;
    }

    .music-card.revealed-decoy {
      opacity: 0.6;
      border-color: #1e2848;
    }

    .card-left {
      display: flex;
      align-items: center;
      gap: 12px;
      flex: 1;
    }

    .card-radio-ring {
      width: 20px;
      height: 20px;
      border-radius: 50%;
      border: 2px solid #33426e;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
      transition: all 0.2s;
    }

    .music-card.selected .card-radio-ring {
      border-color: var(--cyan);
    }

    .card-radio-dot {
      width: 10px;
      height: 10px;
      border-radius: 50%;
      background: transparent;
      transition: all 0.2s;
    }

    .music-card.selected .card-radio-dot {
      background: var(--cyan);
      box-shadow: 0 0 8px var(--cyan);
    }

    .card-meta {
      display: flex;
      flex-direction: column;
      gap: 2px;
    }

    .card-badge-num {
      font-size: 10px;
      font-weight: 800;
      color: #818cf8;
      text-transform: uppercase;
      letter-spacing: 0.6px;
    }

    .card-title-text {
      font-size: 14px;
      font-weight: 700;
      color: #f1f5f9;
    }

    .card-reveal-sub {
      font-size: 12px;
      color: #94a3b8;
      display: none;
    }

    .card-play-trigger {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .card-equalizer {
      display: none;
      gap: 3px;
    }

    .card-equalizer.active {
      display: flex;
    }

    .card-equalizer span {
      width: 3px;
      height: 4px;
      background: var(--accent);
      border-radius: 1px;
      animation: sound-bounce 0.8s ease-in-out infinite alternate;
    }

    .card-equalizer span:nth-child(2) { animation-delay: 0.15s; }
    .card-equalizer span:nth-child(3) { animation-delay: 0.3s; }
    .card-equalizer span:nth-child(4) { animation-delay: 0.45s; }

    .card-play-btn {
      background: #171e35;
      border: 1px solid #2b385e;
      color: #c7d2fe;
      padding: 7px 12px;
      border-radius: 10px;
      font-size: 12px;
      font-weight: 700;
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .music-card.selected .card-play-btn {
      background: var(--accent);
      border-color: var(--accent);
      color: #fff;
    }

    .m2-actions {
      display: flex;
      gap: 8px;
      align-items: center;
      margin-top: 6px;
      width: 100%;
      box-sizing: border-box;
    }

    .m2-actions #m2-btn-confirm,
    .m2-actions #m2-btn-next {
      flex: 1;
      min-width: 0;
      justify-content: center;
      padding: 12px 16px;
      font-size: 13px;
      font-weight: 700;
    }

    .m2-actions #m2-btn-finish {
      flex: 0 0 auto;
      width: auto;
      min-width: 100px;
      max-width: 130px;
      justify-content: center;
      padding: 12px 14px;
      font-size: 12px;
      border-color: rgba(239, 68, 68, 0.45);
      color: #fca5a5;
      background: rgba(239, 68, 68, 0.08);
      white-space: nowrap;
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
      cursor: pointer;
    }

    .m2-actions #m2-btn-finish:hover,
    #m3-btn-finish:hover,
    .m1-nav-btn[onclick*="finishCurrentGame"]:hover {
      background: rgba(239, 68, 68, 0.28) !important;
      border-color: #ef4444 !important;
      color: #ffffff !important;
      box-shadow: 0 0 16px rgba(239, 68, 68, 0.65), 0 0 28px rgba(239, 68, 68, 0.25) !important;
      transform: translateY(-2px);
      filter: brightness(1.2);
    }

    .m2-actions #m2-btn-finish:active,
    #m3-btn-finish:active,
    .m1-nav-btn[onclick*="finishCurrentGame"]:active {
      transform: translateY(1px);
      box-shadow: 0 0 8px rgba(239, 68, 68, 0.4) !important;
    }

    .m2-feedback-banner {
      display: none;
      padding: 8px 12px;
      border-radius: 10px;
      text-align: center;
      margin-bottom: 10px;
      font-size: 12px;
      animation: fadeIn 0.3s ease;
    }

    .m2-feedback-banner.correct {
      background: rgba(16, 185, 129, 0.15);
      border: 1px solid rgba(16, 185, 129, 0.5);
      color: #34d399;
    }

    .m2-feedback-banner.wrong {
      background: rgba(239, 68, 68, 0.15);
      border: 1px solid rgba(239, 68, 68, 0.5);
      color: #f87171;
    }

    /* ==============================================================
       MODO 3: "ADIVINHE A CENA" (BENTO GRID 2-COLUNAS ZERO-SCROLL)
       ============================================================== */
    .scene-viewport {
      position: relative;
      width: 100%;
      aspect-ratio: 16 / 9;
      min-height: 175px;
      max-height: 240px;
      background: #050811 url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 40 40"><path d="M0 40 L40 0 M0 0 L40 40" stroke="rgba(255,255,255,0.02)" stroke-width="1"/></svg>');
      border-radius: 14px;
      overflow: hidden;
      border: 2px solid var(--card-border);
      margin-bottom: 8px;
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.6);
      display: flex;
      align-items: center;
      justify-content: center;
      box-sizing: border-box;
    }

    .scene-frame-img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      transition: transform 0.3s ease;
      background: #020617;
    }

    .scene-cinema-bar {
      position: absolute;
      left: 0; right: 0;
      height: 12px;
      background: rgba(0,0,0,0.7);
      pointer-events: none;
      z-index: 2;
    }
    .scene-cinema-bar.top { top: 0; }
    .scene-cinema-bar.bottom { bottom: 0; }

    .scene-zoom-trigger {
      position: absolute;
      bottom: 10px;
      right: 10px;
      background: rgba(15, 20, 36, 0.85);
      border: 1px solid #33426e;
      color: #fff;
      padding: 5px 10px;
      border-radius: 6px;
      font-size: 11px;
      font-weight: 700;
      cursor: pointer;
      z-index: 3;
      backdrop-filter: blur(3px);
      display: inline-flex;
      align-items: center;
      gap: 5px;
    }
    .scene-zoom-trigger:hover {
      background: var(--accent);
      border-color: var(--accent);
    }

    .m3-clues-wrapper {
      display: flex;
      flex-direction: column;
      gap: 8px;
      width: 100%;
      box-sizing: border-box;
    }

    .scene-tags-row {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 6px;
      width: 100%;
      box-sizing: border-box;
    }

    .scene-tag-badge {
      background: #11172a;
      border: 1px solid #222d4f;
      color: var(--text-muted);
      padding: 6px 10px;
      border-radius: 8px;
      font-size: 11px;
      font-weight: 600;
      cursor: pointer;
      user-select: none;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s;
      min-width: 0;
      height: 38px;
      box-sizing: border-box;
      overflow: hidden;
    }

    .scene-tag-badge span,
    .scene-tag-badge .tag-content {
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
      min-width: 0;
      flex: 1;
    }

    .scene-tag-badge.locked {
      color: #64748b;
    }

    .scene-tag-badge.revealed {
      background: rgba(99, 102, 241, 0.2);
      border-color: rgba(99, 102, 241, 0.5);
      color: #c7d2fe;
    }

    .m3-hint-btn {
      padding: 6px 12px;
      font-size: 11px;
      align-self: flex-start;
      border-radius: 8px;
    }

    .m3-result-slot {
      min-height: 0;
    }

    .m3-result-slot .feedback-box {
      padding: 8px 12px;
      font-size: 12px;
      margin-bottom: 8px;
      border-radius: 10px;
    }

    .m3-result-slot .answer-card {
      margin-bottom: 10px;
      padding: 10px 14px;
      border-radius: 12px;
    }

    .m3-result-slot .answer-poster-img {
      width: 58px;
      height: 82px;
      border-radius: 6px;
    }

    .m3-result-slot .answer-title {
      font-size: 15px;
      margin-bottom: 2px;
    }

    .m3-result-slot .answer-meta {
      font-size: 12px;
      margin-bottom: 4px;
    }

    .m3-result-slot .answer-syns {
      font-size: 10px;
    }

    .m3-nav-row {
      margin-top: 8px;
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      width: 100%;
      box-sizing: border-box;
    }
    .m3-nav-row .btn {
      flex: 1 1 auto;
      min-width: 100px;
      padding: 8px 12px;
      font-size: 12px;
      white-space: nowrap;
      text-align: center;
      justify-content: center;
    }

    .lightbox-modal {
      display: none;
      position: fixed;
      top: 0; left: 0; right: 0; bottom: 0;
      background: rgba(0, 0, 0, 0.92);
      z-index: 9999;
      align-items: center;
      justify-content: center;
      padding: 20px;
    }

    .lightbox-modal.active {
      display: flex;
    }

    .lightbox-img {
      max-width: 95%;
      max-height: 90vh;
      object-fit: contain;
      border-radius: 12px;
      box-shadow: 0 0 40px rgba(0,0,0,0.9);
      border: 2px solid #2b385e;
    }

    .lightbox-close {
      position: absolute;
      top: 20px;
      right: 25px;
      font-size: 32px;
      color: #fff;
      cursor: pointer;
      font-weight: bold;
    }

    /* ==============================================================
       MODO 4: PLACAR DE LÍDERES & DESAFIOS MULTIPLAYER
       ============================================================== */
    /* Multiplayer Sub-tabs */
    .mp-tabs-bar {
      display: flex;
      gap: 10px;
      margin-bottom: 20px;
      border-bottom: 1px solid var(--card-border);
      padding-bottom: 12px;
      justify-content: center;
      flex-wrap: wrap;
    }
    .mp-tab-btn {
      background: #141a2e;
      border: 1px solid #232d4b;
      color: #94a3b8;
      padding: 8px 18px;
      border-radius: 12px;
      font-size: 13px;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.2s ease;
    }
    .mp-tab-btn.active {
      background: linear-gradient(135deg, #6366f1, #a855f7);
      color: #ffffff;
      border-color: #6366f1;
      box-shadow: 0 4px 15px rgba(99, 102, 241, 0.35);
    }

    /* Multiplayer Room Setup Grid */
    .mp-setup-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 16px;
      margin-bottom: 20px;
    }
    .mp-panel-card {
      background: #0d1222;
      border: 1px solid var(--card-border);
      border-radius: 16px;
      padding: 20px;
      display: flex;
      flex-direction: column;
      gap: 14px;
      position: relative;
      overflow: hidden;
    }
    .mp-panel-card::before {
      content: '';
      position: absolute;
      top: 0; left: 0; right: 0;
      height: 3px;
      background: linear-gradient(90deg, var(--accent), #ec4899);
    }
    .mp-card-title {
      font-size: 15px;
      font-weight: 800;
      color: #ffffff;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .mp-form-row {
      display: flex;
      flex-direction: column;
      gap: 6px;
    }
    .mp-form-label {
      font-size: 11px;
      font-weight: 700;
      color: #94a3b8;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }
    .mp-input {
      background: #070913;
      border: 1px solid #232d4b;
      padding: 10px 14px;
      border-radius: 10px;
      color: #ffffff;
      font-size: 13px;
      font-weight: 600;
      outline: none;
      width: 100%;
      box-sizing: border-box;
      transition: border-color 0.2s;
    }
    .mp-input:focus {
      border-color: var(--accent);
      box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15);
    }

    /* Lobby View */
    .lobby-box {
      background: #0d1222;
      border: 1px solid var(--card-border);
      border-radius: 16px;
      padding: 24px;
      display: flex;
      flex-direction: column;
      gap: 18px;
    }
    .lobby-header-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 12px;
      border-bottom: 1px solid #1a223a;
      padding-bottom: 16px;
    }
    .lobby-code-badge {
      background: linear-gradient(135deg, rgba(99, 102, 241, 0.2), rgba(236, 72, 153, 0.2));
      border: 1px solid rgba(99, 102, 241, 0.4);
      padding: 8px 16px;
      border-radius: 10px;
      display: flex;
      align-items: center;
      gap: 10px;
      cursor: pointer;
      user-select: none;
      transition: transform 0.15s;
    }
    .lobby-code-badge:hover {
      transform: scale(1.02);
    }
    .lobby-code-val {
      font-family: 'JetBrains Mono', monospace;
      font-size: 20px;
      font-weight: 800;
      color: #38bdf8;
      letter-spacing: 2px;
    }
    .lobby-meta-pills {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
    }
    .lobby-players-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(170px, 1fr));
      gap: 12px;
      margin: 10px 0;
    }
    .player-slot-card {
      background: #141a2e;
      border: 1px solid #232d4b;
      border-radius: 12px;
      padding: 12px;
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .player-slot-avatar {
      width: 36px;
      height: 36px;
      border-radius: 50%;
      background: linear-gradient(135deg, #6366f1, #ec4899);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 16px;
      font-weight: 800;
      color: #fff;
      flex-shrink: 0;
    }
    .player-slot-name {
      font-size: 13px;
      font-weight: 700;
      color: #fff;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }
    .player-slot-role {
      font-size: 10px;
      color: var(--gold);
      font-weight: 700;
    }

    /* In-Game Multiplayer HUD Bar */
    .mp-hud-bar {
      background: linear-gradient(90deg, #0d1222, #141a2e);
      border: 1px solid rgba(99, 102, 241, 0.4);
      border-radius: 14px;
      padding: 10px 16px;
      margin-bottom: 14px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 10px;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
      animation: fadeIn 0.3s ease;
    }
    .mp-hud-left {
      display: flex;
      align-items: center;
      gap: 10px;
      flex-wrap: wrap;
    }
    .mp-hud-scores {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      align-items: center;
    }
    .mp-hud-player-pill {
      background: #070913;
      border: 1px solid #232d4b;
      padding: 4px 10px;
      border-radius: 999px;
      font-size: 11px;
      font-weight: 700;
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .mp-hud-player-pill.is-me {
      border-color: var(--accent);
      background: rgba(99, 102, 241, 0.15);
      color: #a5b4fc;
    }
    .mp-hud-timer-pill {
      background: linear-gradient(135deg, rgba(234, 179, 8, 0.15), rgba(245, 158, 11, 0.25));
      border: 1.5px solid #f59e0b;
      color: #fde047;
      padding: 5px 14px;
      border-radius: 999px;
      font-size: 14px;
      font-weight: 800;
      letter-spacing: 0.03em;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      box-shadow: 0 0 14px rgba(245, 158, 11, 0.25);
      transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .mp-hud-timer-pill.panic {
      background: linear-gradient(135deg, rgba(239, 68, 68, 0.35), rgba(185, 28, 28, 0.55)) !important;
      border: 2px solid #ef4444 !important;
      color: #ffffff !important;
      box-shadow: 0 0 25px rgba(239, 68, 68, 0.8), inset 0 0 10px rgba(239, 68, 68, 0.5) !important;
      animation: timerPanicShake 0.16s infinite alternate !important;
      text-shadow: 0 0 10px rgba(239, 68, 68, 0.9);
    }
    @keyframes timerPanicShake {
      0% { transform: scale(1.08) translate(-2px, 0) rotate(-2deg); }
      50% { transform: scale(1.14) translate(2px, -1px) rotate(2deg); }
      100% { transform: scale(1.08) translate(-1px, 2px) rotate(-1deg); }
    }
    .mp-waiting-banner {
      background: linear-gradient(90deg, rgba(30, 41, 59, 0.95), rgba(15, 23, 42, 0.98));
      border: 1.5px solid rgba(99, 102, 241, 0.5);
      border-radius: 12px;
      padding: 12px 16px;
      margin-bottom: 14px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
      animation: fadeIn 0.25s ease;
      font-size: 13px;
      font-weight: 700;
      color: #e2e8f0;
    }
    .mp-waiting-banner.all-done {
      border-color: #10b981;
      background: linear-gradient(90deg, rgba(6, 78, 59, 0.9), rgba(15, 23, 42, 0.98));
      color: #34d399;
    }
    .mp-rank-stats {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 6px;
      font-size: 11px;
      margin-top: 4px;
      width: 100%;
    }
    .mp-player-status-badge {
      display: inline-flex;
      align-items: center;
      gap: 4px;
      font-size: 9.5px;
      font-weight: 700;
      padding: 2px 7px;
      border-radius: 999px;
      white-space: nowrap;
      flex-shrink: 0;
    }
    .mp-player-status-badge.answered {
      background: rgba(16, 185, 129, 0.2);
      border: 1px solid #10b981;
      color: #34d399;
    }
    .mp-player-status-badge.thinking {
      background: rgba(234, 179, 8, 0.15);
      border: 1px solid rgba(234, 179, 8, 0.4);
      color: #fbbf24;
      animation: pulseThinking 1.5s infinite;
    }
    @keyframes pulseThinking {
      0%, 100% { opacity: 0.7; }
      50% { opacity: 1; }
    }
    .mp-skip-btn {
      background: linear-gradient(135deg, #f59e0b, #d97706);
      color: #1a0e02;
      border: none;
      padding: 6px 14px;
      border-radius: 8px;
      font-size: 12px;
      font-weight: 800;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.15s;
    }
    .mp-skip-btn:hover {
      transform: translateY(-1px);
      box-shadow: 0 3px 10px rgba(245, 158, 11, 0.4);
    }
    .mp-skip-btn.voted {
      background: #1e293b;
      color: #94a3b8;
      cursor: default;
      box-shadow: none;
    }

    /* Gameplay Wrapper with Live Multiplayer Sidebar */
    .gameplay-wrapper {
      display: flex;
      gap: 16px;
      align-items: flex-start;
      width: 100%;
      box-sizing: border-box;
    }
    .gameplay-main-col {
      flex: 1;
      min-width: 0;
      width: 100%;
      box-sizing: border-box;
    }
    .mp-live-sidebar {
      width: 270px;
      flex-shrink: 0;
      background: #0d1224;
      border: 1px solid #1e2640;
      border-radius: 16px;
      padding: 12px;
      box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
      position: sticky;
      top: 16px;
      z-index: 10;
      animation: fadeIn 0.3s ease;
      box-sizing: border-box;
      display: flex;
      flex-direction: column;
      overflow: hidden;
    }

    @media (max-width: 1120px) {
      .gameplay-wrapper {
        flex-direction: column;
        gap: 14px;
      }
      .mp-live-sidebar {
        width: 100%;
        position: static;
        order: 2;
      }
      .mp-sidebar-list {
        display: grid !important;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)) !important;
        gap: 8px !important;
      }
    }
    .mp-sidebar-header {
      width: 100%;
      box-sizing: border-box;
      border-bottom: 1px solid #1e2640;
      padding-bottom: 10px;
      margin-bottom: 12px;
    }
    .mp-sidebar-title-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
    }
    .mp-sidebar-title {
      font-size: 12px;
      font-weight: 800;
      letter-spacing: 0.05em;
      color: #f8fafc;
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .mp-sidebar-live-dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: #10b981;
      box-shadow: 0 0 8px #10b981;
      animation: pulseDot 1.5s infinite;
    }
    @keyframes pulseDot {
      0%, 100% { opacity: 1; transform: scale(1); }
      50% { opacity: 0.4; transform: scale(0.85); }
    }
    .mp-sidebar-subtitle {
      font-size: 11px;
      color: #94a3b8;
      margin-top: 3px;
    }
    .mp-sidebar-list {
      width: 100%;
      box-sizing: border-box;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }
    .mp-player-rank-item {
      display: flex;
      align-items: center;
      gap: 10px;
      background: #070914;
      border: 1px solid #1a2238;
      border-radius: 12px;
      padding: 8px 10px;
      box-sizing: border-box;
      width: 100%;
      min-width: 0;
      transition: transform 0.35s cubic-bezier(0.4, 0, 0.2, 1), background 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease;
      position: relative;
    }
    .mp-player-rank-item.is-me {
      border-color: rgba(99, 102, 241, 0.6);
      background: rgba(99, 102, 241, 0.12);
    }
    .mp-player-rank-item.mp-first-place {
      border-color: rgba(251, 191, 36, 0.7);
      box-shadow: 0 0 14px rgba(251, 191, 36, 0.18), inset 0 0 12px rgba(251, 191, 36, 0.06);
    }
    .mp-player-rank-item.mp-first-place .mp-rank-name-text {
      color: #fde68a;
    }
    .mp-rank-points-col {
      display: flex;
      flex-direction: column;
      align-items: flex-end;
      flex-shrink: 0;
      min-width: 52px;
      position: relative;
    }
    .mp-rank-delta {
      font-size: 11px;
      font-weight: 900;
      color: #34d399;
      text-shadow: 0 0 8px rgba(52, 211, 153, 0.7);
      line-height: 1;
      margin-top: 2px;
      animation: mpDeltaPop 2.2s ease-out forwards;
    }
    @keyframes mpDeltaPop {
      0% { opacity: 0; transform: translateY(6px) scale(0.6); }
      12% { opacity: 1; transform: translateY(0) scale(1.25); }
      25% { transform: scale(1); }
      80% { opacity: 1; }
      100% { opacity: 0; transform: translateY(-4px); }
    }
    .mp-player-rank-item.scoring-glow {
      animation: rankScorePulse 1.2s cubic-bezier(0.16, 1, 0.3, 1) forwards !important;
    }
    @keyframes rankScorePulse {
      0% {
        box-shadow: 0 0 0 0 rgba(52, 211, 153, 0.8), inset 0 0 14px rgba(52, 211, 153, 0.4);
        border-color: #34d399 !important;
        transform: scale(1.03);
      }
      35% {
        box-shadow: 0 0 20px 2px rgba(52, 211, 153, 0.4), inset 0 0 8px rgba(52, 211, 153, 0.2);
        border-color: #10b981 !important;
        transform: scale(1.01);
      }
      100% {
        box-shadow: none;
        transform: scale(1);
      }
    }
    .mp-rank-pos-badge {
      font-size: 14px;
      font-weight: 800;
      width: 24px;
      text-align: center;
      flex-shrink: 0;
    }
    .mp-rank-avatar {
      width: 28px;
      height: 28px;
      border-radius: 50%;
      background: linear-gradient(135deg, #6366f1, #a855f7);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 11px;
      font-weight: 800;
      color: #ffffff;
      flex-shrink: 0;
    }
    .mp-rank-info {
      flex: 1;
      min-width: 0;
      overflow: hidden;
    }
    .mp-rank-name {
      font-size: 12px;
      font-weight: 700;
      color: #f1f5f9;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      display: flex;
      align-items: center;
      gap: 4px;
    }
    .mp-rank-stats {
      font-size: 10px;
      color: #94a3b8;
      display: flex;
      gap: 4px 6px;
      align-items: center;
      flex-wrap: wrap;
    }
    .mp-rank-points {
      font-size: 13px;
      font-weight: 800;
      color: #fbbf24;
      text-align: right;
      flex-shrink: 0;
    }
    .mp-rank-trend {
      font-size: 11px;
      font-weight: 800;
      margin-left: 2px;
    }
    .mp-rank-trend.up {
      color: #10b981;
      animation: bounceUp 0.5s ease;
    }
    .mp-rank-trend.down {
      color: #ef4444;
    }
    @keyframes bounceUp {
      0% { transform: translateY(4px); opacity: 0; }
      50% { transform: translateY(-2px); }
      100% { transform: translateY(0); opacity: 1; }
    }
    .mp-sidebar-footer {
      width: 100%;
      box-sizing: border-box;
      margin-top: 12px;
      padding-top: 10px;
      border-top: 1px solid #1e2640;
      font-size: 11px;
      color: #38bdf8;
      text-align: center;
      font-weight: 600;
    }
    .mp-leave-btn {
      background: rgba(239, 68, 68, 0.15);
      border: 1px solid rgba(239, 68, 68, 0.45);
      color: #fca5a5;
      padding: 6px 12px;
      border-radius: 999px;
      font-size: 11px;
      font-weight: 700;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 5px;
      transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .mp-leave-btn:hover {
      background: rgba(239, 68, 68, 0.35);
      border-color: #ef4444;
      color: #ffffff;
      transform: translateY(-1px);
      box-shadow: 0 0 12px rgba(239, 68, 68, 0.4);
    }
    @media (max-width: 899px) {
      .gameplay-wrapper {
        flex-direction: column;
      }
      .mp-live-sidebar {
        width: 100%;
        position: static;
        margin-bottom: 12px;
        padding: 10px;
      }
      .mp-sidebar-list {
        flex-direction: row;
        overflow-x: auto;
        overflow-y: hidden;
        padding-bottom: 6px;
      }
      .mp-player-rank-item {
        min-width: 160px;
        flex-shrink: 0;
      }
    }

    /* Floating Arcade Multipliers / Juice Engine */
    .gameplay-wrapper {
      position: relative;
    }
    .floating-arcade-container {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      pointer-events: none;
      overflow: hidden;
      z-index: 999;
    }
    .arcade-popup {
      position: absolute;
      left: 50%;
      top: 45%;
      transform: translate(-50%, -50%) scale(0.6);
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      gap: 6px;
      pointer-events: none;
      animation: arcadeFloatUp 1.25s cubic-bezier(0.16, 1, 0.3, 1) forwards;
      z-index: 1000;
    }
    @keyframes arcadeFloatUp {
      0% {
        opacity: 0;
        transform: translate(-50%, -35%) scale(0.5);
      }
      15% {
        opacity: 1;
        transform: translate(-50%, -48%) scale(1.15);
      }
      30% {
        transform: translate(-50%, -50%) scale(1);
      }
      75% {
        opacity: 1;
        transform: translate(-50%, -65%) scale(1);
      }
      100% {
        opacity: 0;
        transform: translate(-50%, -85%) scale(0.9);
      }
    }
    .arcade-pts-main {
      font-size: 40px;
      font-weight: 900;
      letter-spacing: -0.02em;
      line-height: 1;
      font-family: inherit;
    }
    .arcade-pts-main.correct {
      color: #34d399;
      text-shadow: 0 0 25px rgba(52, 211, 153, 0.85), 0 0 50px rgba(16, 185, 129, 0.5), 0 4px 10px #000;
    }
    .arcade-pts-main.wrong {
      color: #f87171;
      text-shadow: 0 0 25px rgba(248, 113, 113, 0.85), 0 0 40px rgba(239, 68, 68, 0.5), 0 4px 10px #000;
      font-size: 34px;
    }
    .arcade-badge-row {
      display: flex;
      gap: 6px;
      align-items: center;
      margin-top: 4px;
      flex-wrap: wrap;
      justify-content: center;
    }
    .arcade-badge-chip {
      font-size: 13px;
      font-weight: 800;
      padding: 4px 12px;
      border-radius: 999px;
      letter-spacing: 0.04em;
      text-transform: uppercase;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
    }
    .arcade-badge-chip.streak {
      background: linear-gradient(135deg, #f59e0b, #ef4444);
      color: #ffffff;
      border: 1px solid #fde047;
      text-shadow: 0 1px 2px rgba(0,0,0,0.6);
      animation: pulseStreak 0.6s infinite alternate;
    }
    @keyframes pulseStreak {
      0% { transform: scale(1); }
      100% { transform: scale(1.08); }
    }
    .arcade-badge-chip.speed {
      background: linear-gradient(135deg, #06b6d4, #3b82f6);
      color: #ffffff;
      border: 1px solid #7dd3fc;
      text-shadow: 0 1px 2px rgba(0,0,0,0.6);
    }
    .arcade-badge-chip.wrong-badge {
      background: rgba(239, 68, 68, 0.25);
      color: #fca5a5;
      border: 1px solid rgba(239, 68, 68, 0.5);
    }

    /* Podium Screen */
    .podium-box {
      background: #0d1222;
      border: 1px solid var(--card-border);
      border-radius: 20px;
      padding: 28px 20px;
      text-align: center;
      margin-top: 15px;
    }
    .podium-title {
      font-size: 24px;
      font-weight: 800;
      color: #fff;
      margin-bottom: 6px;
    }
    .podium-subtitle {
      font-size: 13px;
      color: #94a3b8;
      margin-bottom: 24px;
    }
    .podium-pillars-row {
      display: flex;
      justify-content: center;
      align-items: flex-end;
      gap: 16px;
      margin: 30px 0 20px 0;
      height: 220px;
    }
    .podium-col {
      display: flex;
      flex-direction: column;
      align-items: center;
      width: 100px;
    }
    .podium-col.rank-1 .podium-pillar {
      height: 130px;
      background: linear-gradient(180deg, #f59e0b, #b45309);
      box-shadow: 0 0 25px rgba(245, 158, 11, 0.4);
    }
    .podium-col.rank-2 .podium-pillar {
      height: 95px;
      background: linear-gradient(180deg, #94a3b8, #475569);
    }
    .podium-col.rank-3 .podium-pillar {
      height: 70px;
      background: linear-gradient(180deg, #d97706, #78350f);
    }
    .podium-pillar {
      width: 100%;
      border-radius: 12px 12px 0 0;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 22px;
      font-weight: 800;
      color: rgba(255, 255, 255, 0.95);
    }
    .podium-player-name {
      font-size: 13px;
      font-weight: 800;
      color: #fff;
      margin-bottom: 4px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      max-width: 95px;
    }
    .podium-player-score {
      font-size: 12px;
      font-weight: 700;
      color: var(--gold);
      margin-bottom: 8px;
    }

    /* Leaderboard Styles */
    .leaderboard-container {
      display: flex;
      flex-direction: column;
      gap: 20px;
    }

    .leaderboard-filter-tabs {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      justify-content: center;
    }

    .lb-tab-btn {
      background: #141a2e;
      border: 1px solid #232d4b;
      color: #cbd5e1;
      padding: 6px 14px;
      border-radius: 999px;
      font-size: 12px;
      font-weight: 700;
      cursor: pointer;
    }
    .lb-tab-btn.active {
      background: var(--gold);
      color: #3b1d02;
      border-color: var(--gold);
    }

    .leaderboard-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 13px;
    }

    .leaderboard-table th {
      background: #141a2e;
      color: var(--text-muted);
      text-align: left;
      padding: 10px 12px;
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 0.6px;
    }

    .leaderboard-table td {
      padding: 12px;
      border-bottom: 1px solid #1a223a;
      color: #e2e8f0;
    }

    .leaderboard-table tr:hover td {
      background: rgba(255,255,255,0.02);
    }

    .rank-badge {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      width: 24px;
      height: 24px;
      border-radius: 50%;
      font-weight: 800;
      font-size: 12px;
    }
    .rank-1 { background: #f59e0b; color: #451a03; }
    .rank-2 { background: #94a3b8; color: #0f172a; }
    .rank-3 { background: #b45309; color: #fff; }

    .cloud-status-pill {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 4px 10px;
      border-radius: 999px;
      font-size: 11px;
      font-weight: 700;
      border: 1px solid transparent;
      user-select: none;
      transition: all 0.2s ease;
    }
    .cloud-status-pill.online {
      background: rgba(16, 185, 129, 0.12);
      border-color: rgba(16, 185, 129, 0.4);
      color: #34d399;
    }
    .cloud-status-pill.local {
      background: rgba(245, 158, 11, 0.12);
      border-color: rgba(245, 158, 11, 0.4);
      color: #fbbf24;
    }
    .cloud-status-pill.syncing {
      background: rgba(6, 182, 212, 0.12);
      border-color: rgba(6, 182, 212, 0.4);
      color: #38bdf8;
    }
    .cloud-status-pill.error {
      background: rgba(239, 68, 68, 0.12);
      border-color: rgba(239, 68, 68, 0.4);
      color: #f87171;
    }
    .status-dot {
      width: 7px;
      height: 7px;
      border-radius: 50%;
      background: currentColor;
      display: inline-block;
    }
    .status-dot.pulse-green {
      box-shadow: 0 0 6px #10b981;
      animation: statusGlow 2s infinite ease-in-out;
    }
    .status-dot.pulse-amber {
      box-shadow: 0 0 6px #f59e0b;
      animation: statusGlow 2s infinite ease-in-out;
    }
    @keyframes statusGlow {
      0%, 100% { opacity: 1; transform: scale(1); }
      50% { opacity: 0.5; transform: scale(0.85); }
    }
    .status-dot.spin {
      animation: dotSpin 1s infinite linear;
    }
    @keyframes dotSpin {
      100% { transform: rotate(360deg); }
    }

    .player-cell {
      display: flex;
      align-items: center;
      gap: 7px;
      flex-wrap: wrap;
    }
    .player-name {
      font-weight: 700;
      color: #f8fafc;
      font-size: 13px;
    }

    .prestige-badge {
      display: inline-flex;
      align-items: center;
      gap: 4px;
      padding: 2px 7px;
      border-radius: 6px;
      font-size: 10px;
      font-weight: 800;
      letter-spacing: 0.4px;
      text-transform: uppercase;
      cursor: help;
      transition: transform 0.2s, box-shadow 0.2s;
    }
    .prestige-badge:hover {
      transform: translateY(-1px) scale(1.04);
    }
    .badge-master {
      background: linear-gradient(135deg, rgba(245, 158, 11, 0.22), rgba(217, 119, 6, 0.35));
      border: 1px solid #f59e0b;
      color: #fbbf24;
      box-shadow: 0 0 8px rgba(245, 158, 11, 0.35);
    }
    .badge-fire {
      background: linear-gradient(135deg, rgba(239, 68, 68, 0.2), rgba(220, 38, 38, 0.3));
      border: 1px solid #ef4444;
      color: #f87171;
      box-shadow: 0 0 8px rgba(239, 68, 68, 0.3);
    }
    .badge-speed {
      background: linear-gradient(135deg, rgba(6, 182, 212, 0.2), rgba(14, 165, 233, 0.3));
      border: 1px solid #06b6d4;
      color: #38bdf8;
      box-shadow: 0 0 8px rgba(6, 182, 212, 0.3);
    }
    .badge-perfect {
      background: linear-gradient(135deg, rgba(168, 85, 247, 0.2), rgba(147, 51, 234, 0.3));
      border: 1px solid #a855f7;
      color: #c084fc;
      box-shadow: 0 0 8px rgba(168, 85, 247, 0.3);
    }
    .badge-ear {
      background: rgba(99, 102, 241, 0.18);
      border: 1px solid #6366f1;
      color: #a5b4fc;
    }
    .badge-dj {
      background: rgba(236, 72, 153, 0.18);
      border: 1px solid #ec4899;
      color: #f472b6;
    }
    .badge-eye {
      background: rgba(20, 184, 166, 0.18);
      border: 1px solid #14b8a6;
      color: #5eead4;
    }
    .badge-veteran {
      background: rgba(16, 185, 129, 0.18);
      border: 1px solid #10b981;
      color: #6ee7b7;
    }
    .badge-rookie {
      background: rgba(148, 163, 184, 0.12);
      border: 1px solid #475569;
      color: #cbd5e1;
    }
    .source-chip {
      font-size: 9px;
      padding: 1px 5px;
      border-radius: 4px;
      background: rgba(255, 255, 255, 0.05);
      color: var(--text-muted);
      border: 1px solid rgba(255, 255, 255, 0.08);
      display: inline-flex;
      align-items: center;
      gap: 3px;
    }

    .game-over-stats-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 8px;
      margin: 14px 0;
      background: rgba(15, 20, 36, 0.7);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      padding: 10px 8px;
    }
    .go-stat-item {
      display: flex;
      flex-direction: column;
      gap: 3px;
    }
    .go-stat-label {
      font-size: 10px;
      text-transform: uppercase;
      color: var(--text-muted);
      letter-spacing: 0.5px;
    }
    .go-stat-val {
      font-size: 13px;
      font-weight: 800;
      color: #fff;
    }
    .go-stat-val.highlight {
      color: var(--gold);
      font-family: 'JetBrains Mono', monospace;
    }
    .go-stat-val.flame {
      color: #f97316;
    }
    .game-over-badge-box {
      background: rgba(245, 158, 11, 0.05);
      border: 1px dashed rgba(245, 158, 11, 0.3);
      border-radius: 12px;
      padding: 10px;
      margin-bottom: 12px;
    }

    .save-score-box {
      background: #0d1222;
      border: 1px solid var(--card-border);
      border-radius: 14px;
      padding: 16px;
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
      align-items: center;
      justify-content: space-between;
    }

    .save-score-input {
      background: #070913;
      border: 1px solid #232d4b;
      padding: 8px 14px;
      border-radius: 10px;
      color: #fff;
      font-size: 13px;
      outline: none;
      min-width: 180px;
    }

    .toast-msg {
      position: fixed;
      bottom: 24px;
      left: 50%;
      transform: translateX(-50%);
      background: #10b981;
      color: #042f1a;
      font-weight: 800;
      font-size: 13px;
      padding: 10px 20px;
      border-radius: 999px;
      box-shadow: 0 10px 25px rgba(0,0,0,0.5);
      z-index: 10000;
      display: none;
      animation: fadeIn 0.2s ease;
    }

    /* Catalog Table */
    .table-section {
      background: var(--card);
      border: 1px solid var(--card-border);
      border-radius: 20px;
      padding: 22px;
      margin-top: 10px;
    }

    .table-wrapper {
      max-height: 480px;
      overflow-y: auto;
      border: 1px solid #1a223a;
      border-radius: 12px;
      margin-top: 12px;
    }

    table#songs-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 12px;
    }

    table#songs-table th {
      position: sticky;
      top: 0;
      background: #141a2e;
      color: #94a3b8;
      text-align: left;
      padding: 10px 12px;
      z-index: 2;
    }

    table#songs-table td {
      padding: 10px 12px;
      border-bottom: 1px solid #151b2e;
    }

    table#songs-table tr:hover td {
      background: rgba(255,255,255,0.02);
    }

    .spoiler-text {
      filter: blur(5px);
      cursor: pointer;
      user-select: none;
      transition: filter 0.2s;
    }
    .spoiler-text.revealed {
      filter: none;
    }

    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(5px); }
      to { opacity: 1; transform: translateY(0); }
    }

    @media (max-width: 600px) {
      body { padding: 12px 8px 30px; }
      .quiz-card { padding: 16px; }
      .header-top-bar { justify-content: center; }
    }

    /* ==========================================================
       AJUSTES DE DESIGN FLUIDO, ANTI-CORTE & ALTA VISIBILIDADE
       ========================================================== */
    .container {
      width: 100%;
      max-width: 1040px;
      margin: 0 auto;
      padding: 14px 16px 50px;
      box-sizing: border-box;
    }

    body {
      overflow-x: hidden;
      overflow-y: auto !important; /* Sem cortes: permite rolagem suave e acesso a todos os botões */
    }

    /* Scoreboard integrado dentro dos modos */
    .mode-scoreboard-slot {
      margin-bottom: 16px;
    }
    .mode-scoreboard-slot .scoreboard {
      margin: 0 !important;
    }

    /* Autocomplete Dropdown Nítido e com Alto Z-Index */
    .autocomplete-wrapper {
      position: relative;
      flex: 1;
      display: flex;
    }

    .autocomplete-dropdown {
      position: absolute !important;
      top: calc(100% + 4px) !important;
      left: 0 !important;
      right: 0 !important;
      background: #0f172a !important;
      border: 1.5px solid #38bdf8 !important;
      border-radius: 12px !important;
      max-height: 240px !important;
      overflow-y: auto !important;
      z-index: 9999 !important;
      box-shadow: 0 12px 36px rgba(0,0,0,0.9), 0 0 15px rgba(56, 189, 248, 0.25) !important;
    }

    .autocomplete-item {
      padding: 10px 14px !important;
      font-size: 13px !important;
      color: #e2e8f0 !important;
      cursor: pointer !important;
      border-bottom: 1px solid rgba(255, 255, 255, 0.06) !important;
      display: flex !important;
      justify-content: space-between !important;
      align-items: center !important;
      transition: background 0.15s, color 0.15s !important;
    }

    .autocomplete-item:hover, .autocomplete-item.active {
      background: rgba(56, 189, 248, 0.18) !important;
      color: #38bdf8 !important;
    }

    /* Pistas no Modo 1 com Destaque Visual */
    .hints-section {
      background: rgba(15, 23, 42, 0.65);
      border: 1px solid rgba(99, 102, 241, 0.3);
      border-radius: 12px;
      padding: 14px 16px;
      margin-bottom: 16px;
    }

    .hints-title {
      font-size: 13px;
      font-weight: 800;
      color: #e2e8f0;
      margin-bottom: 10px;
    }

    .tags-container {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      min-height: 36px;
      align-items: center;
    }

    .hint-tag {
      background: rgba(30, 41, 59, 0.9);
      border: 1.5px solid rgba(56, 189, 248, 0.5);
      color: #38bdf8;
      padding: 6px 14px;
      border-radius: 8px;
      font-size: 12px;
      font-weight: 700;
      cursor: pointer;
      user-select: none;
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
      box-shadow: 0 2px 6px rgba(0,0,0,0.25);
    }

    .hint-tag:hover {
      border-color: #38bdf8;
      background: rgba(56, 189, 248, 0.15);
      transform: translateY(-2px);
      box-shadow: 0 0 12px rgba(56, 189, 248, 0.4);
    }

    .hint-tag.revealed {
      background: rgba(16, 185, 129, 0.2);
      border-color: #10b981;
      color: #34d399;
    }

    /* Modo 2: Espaçamento Confortável e Acessível */
    #mode2-view .player-container {
      max-height: 170px !important;
    }
    #mode2-view .music-card {
      padding: 10px 14px !important;
      margin-bottom: 8px !important;
    }

    /* Scrollbar personalizada para a tabela dos 50 melhores */
    .leaderboard-scroll-wrapper::-webkit-scrollbar {
      width: 6px;
    }
    .leaderboard-scroll-wrapper::-webkit-scrollbar-track {
      background: rgba(15, 23, 42, 0.6);
    }
    .leaderboard-scroll-wrapper::-webkit-scrollbar-thumb {
      background: #3b82f6;
      border-radius: 3px;
    }

  
/* ==============================================================
   ESTILOS v3.1.0: ÍCONES PNG, SIDEBAR RETRÁTIL & LAYOUT WIDESCREEN
   ============================================================== */
:root {
  --sidebar-w: 64px;
  --sidebar-w-expanded: 260px;
}

/* Ícones Oficiais do Aplicativo via PNG */
img[src^="icons/"] {
  vertical-align: middle;
  object-fit: contain;
  pointer-events: none;
  display: inline-block;
}

.app-icon {
  width: 18px;
  height: 18px;
  max-width: 18px;
  max-height: 18px;
  vertical-align: middle;
  display: inline-block;
  object-fit: contain;
  transition: transform 0.2s cubic-bezier(0.34, 1.56, 0.64, 1), filter 0.2s ease;
  pointer-events: none;
}
.app-icon-xs { width: 12px !important; height: 12px !important; max-width: 12px !important; max-height: 12px !important; }
.app-icon-sm { width: 14px !important; height: 14px !important; max-width: 14px !important; max-height: 14px !important; }
.app-icon-md { width: 18px !important; height: 18px !important; max-width: 18px !important; max-height: 18px !important; }
.app-icon-lg { width: 22px !important; height: 22px !important; max-width: 22px !important; max-height: 22px !important; }
.app-icon-xl { width: 32px !important; height: 32px !important; max-width: 32px !important; max-height: 32px !important; }

/* Vinil Giratório do Blind Test e Modo 2 */
.vinyl-spin-img {
  width: 52px !important;
  height: 52px !important;
  max-width: 52px !important;
  max-height: 52px !important;
}

/* Ícones dentro de badges, tags, pills e botões pequenos (Anti-Overflow Absoluto) */
.pill-chip img,
.scene-tag-badge img,
.card-badge-num img,
.revealed-badge img {
  width: 12px !important;
  height: 12px !important;
  max-width: 12px !important;
  max-height: 12px !important;
  margin-right: 4px;
  vertical-align: -1px;
}
.feedback-box img,
.m2-feedback-banner img {
  width: 16px !important;
  height: 16px !important;
  max-width: 16px !important;
  max-height: 16px !important;
  margin-right: 4px;
  vertical-align: middle;
}

/* Filtros de Cores para Ícones Pretos */
/* Filtros de Cores Semânticas Vivas e Neon para Ícones PNG */
.icon-white {
  filter: brightness(0) invert(1);
}
.icon-gold {
  filter: invert(78%) sepia(85%) saturate(1200%) hue-rotate(355deg) brightness(105%) contrast(105%) drop-shadow(0 0 6px rgba(245, 158, 11, 0.7));
}
.icon-cyan {
  filter: invert(65%) sepia(90%) saturate(1400%) hue-rotate(150deg) brightness(105%) contrast(100%) drop-shadow(0 0 6px rgba(6, 182, 212, 0.7));
}
.icon-neon-cyan {
  filter: invert(65%) sepia(90%) saturate(1400%) hue-rotate(150deg) brightness(130%) contrast(110%) drop-shadow(0 0 8px #06b6d4) drop-shadow(0 0 16px rgba(6, 182, 212, 0.75)) !important;
}
.icon-purple {
  filter: invert(55%) sepia(95%) saturate(1700%) hue-rotate(235deg) brightness(105%) contrast(100%) drop-shadow(0 0 6px rgba(168, 85, 247, 0.7));
}
.icon-green {
  filter: invert(65%) sepia(80%) saturate(1500%) hue-rotate(100deg) brightness(105%) contrast(100%) drop-shadow(0 0 6px rgba(16, 185, 129, 0.7));
}
.icon-red {
  filter: invert(45%) sepia(95%) saturate(2200%) hue-rotate(330deg) brightness(105%) contrast(100%) drop-shadow(0 0 6px rgba(239, 68, 68, 0.7));
}
.icon-blue {
  filter: invert(50%) sepia(95%) saturate(1800%) hue-rotate(190deg) brightness(105%) contrast(100%) drop-shadow(0 0 6px rgba(59, 130, 246, 0.7));
}
.icon-orange {
  filter: invert(65%) sepia(95%) saturate(1800%) hue-rotate(5deg) brightness(105%) contrast(100%) drop-shadow(0 0 6px rgba(249, 115, 22, 0.7));
}
.icon-teal {
  filter: invert(65%) sepia(84%) saturate(850%) hue-rotate(130deg) brightness(100%) contrast(96%) drop-shadow(0 0 6px rgba(20, 184, 166, 0.6));
}
.icon-raw {
  filter: none !important;
}
.icon-prev {
  transform: scaleX(-1);
  display: inline-block;
}

/* Estrutura Geral com Sidebar */
.app-layout {
  display: flex;
  min-height: 100vh;
  width: 100%;
  position: relative;
}

/* SIDEBAR MINI-RAIL (DESKTOP) */
.app-sidebar {
  width: var(--sidebar-w);
  background: rgba(10, 15, 30, 0.95);
  border-right: 1px solid rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(3px);
  -webkit-backdrop-filter: blur(3px);
  display: flex;
  flex-direction: column;
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  z-index: 1000;
  transition: width 0.28s cubic-bezier(0.4, 0, 0.2, 1);
  overflow-x: hidden;
  box-shadow: 4px 0 24px rgba(0, 0, 0, 0.45);
}

.app-sidebar:hover,
.app-sidebar.expanded {
  width: var(--sidebar-w-expanded);
}

.sidebar-header {
  height: 60px;
  display: flex;
  align-items: center;
  padding: 0 16px;
  gap: 14px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
  flex-shrink: 0;
}
.sidebar-logo-icon {
  width: 34px;
  height: 34px;
  min-width: 34px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 10px;
  background: rgba(6, 182, 212, 0.12);
  border: 1px solid rgba(6, 182, 212, 0.35);
  box-shadow: 0 0 14px rgba(6, 182, 212, 0.25);
}
.sidebar-title {
  font-size: 13px;
  font-weight: 800;
  letter-spacing: 0.5px;
  color: #fff;
  white-space: nowrap;
  opacity: 0;
  transition: opacity 0.2s ease;
  pointer-events: none;
  background: linear-gradient(135deg, #38bdf8, #818cf8);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.app-sidebar:hover .sidebar-title,
.app-sidebar.expanded .sidebar-title {
  opacity: 1;
  pointer-events: auto;
}

.sidebar-nav {
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding: 12px 8px;
  flex: 1;
}

.sidebar-item {
  position: relative;
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 11px 12px;
  border-radius: 12px;
  background: transparent;
  border: 1px solid transparent;
  color: #94a3b8;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  text-align: left;
  white-space: nowrap;
  user-select: none;
  width: 100%;
}

.sidebar-icon-wrap {
  width: 24px;
  height: 24px;
  min-width: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.sidebar-label {
  font-size: 13px;
  font-weight: 600;
  opacity: 0;
  padding-right: 14px;
  white-space: nowrap;
  transition: opacity 0.2s ease;
  pointer-events: none;
}
.app-sidebar:hover .sidebar-label,
.app-sidebar.expanded .sidebar-label {
  opacity: 1;
  pointer-events: auto;
}

/* Microinteração e Feedback Visual no Hover */
.sidebar-item:hover {
  background: rgba(99, 102, 241, 0.16);
  color: #ffffff;
  border-color: rgba(99, 102, 241, 0.4);
  transform: translateX(4px) scale(1.02);
  box-shadow: 0 4px 18px rgba(99, 102, 241, 0.3);
}
.sidebar-item:hover .sidebar-icon-wrap .app-icon {
  filter: brightness(0) invert(1) drop-shadow(0 0 6px #38bdf8);
  transform: scale(1.18);
}

.sidebar-item.active {
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.3), rgba(168, 85, 247, 0.25));
  border-color: #6366f1;
  color: #ffffff;
  font-weight: 700;
  box-shadow: 0 0 16px rgba(99, 102, 241, 0.4);
}
.sidebar-item.active .sidebar-icon-wrap .app-icon {
  filter: brightness(0) invert(1) drop-shadow(0 0 8px #818cf8);
}

.sidebar-divider {
  height: 1px;
  background: rgba(255, 255, 255, 0.08);
  margin: 6px 4px;
}

.sidebar-spacer {
  flex: 1;
}

/* ÁREA CENTRAL PRINCIPAL */
.app-main-content {
  flex: 1;
  margin-left: var(--sidebar-w);
  padding: 14px 20px;
  min-height: 100vh;
  box-sizing: border-box;
  transition: margin-left 0.28s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  flex-direction: column;
  align-items: center;
}

.container-center {
  width: 100%;
  max-width: 1100px;
}

/* Header Compacto Superior */
.app-top-header {
  margin-bottom: 12px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
  padding: 8px 16px;
  background: rgba(15, 23, 42, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 12px;
}
.app-top-header h1 {
  font-size: 16px;
  margin: 0;
  font-weight: 800;
  display: flex;
  align-items: center;
  gap: 8px;
}
.app-top-header .subtitle {
  font-size: 11px;
  color: var(--text-muted);
  margin: 0;
}

/* ==============================================================
   MODO 1: LAYOUT COMPACTO & CONTROLES UNIFICADOS (NA MESMA ALTURA)
   ============================================================== */
.mode-split-grid {
  display: grid;
  grid-template-columns: minmax(280px, 1fr) minmax(290px, 1.15fr);
  gap: 16px;
  align-items: flex-start;
  width: 100%;
  box-sizing: border-box;
}
.mode-col-media {
  display: flex;
  flex-direction: column;
  gap: 12px;
  min-width: 0;
  width: 100%;
  box-sizing: border-box;
}
.mode-col-interactive {
  display: flex;
  flex-direction: column;
  gap: 10px;
  min-width: 0;
  width: 100%;
  box-sizing: border-box;
}
.hints-section {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
}
.tags-container {
  min-height: 38px;
}

/* Espaço Expansível do Resultado (Compacto inicialmente, expande ao acertar/errar/revelar) */
.m1-result-slot {
  max-height: 0;
  opacity: 0;
  overflow: hidden;
  margin-top: 0;
  transition: max-height 0.38s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.25s ease, margin-top 0.25s ease;
}
.m1-result-slot.is-open {
  max-height: 240px;
  opacity: 1;
  margin-top: 12px;
}

/* Redesign dos Banners e Cards de Resposta: Neon Glassmorphism Arcade */
.feedback-box {
  display: none;
  border-radius: 12px;
  padding: 10px 14px;
  margin-bottom: 8px;
  font-size: 13px;
  backdrop-filter: blur(3px);
  -webkit-backdrop-filter: blur(3px);
  animation: fadeIn 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}
.feedback-box.correct {
  display: block;
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.18) 0%, rgba(6, 78, 59, 0.3) 100%);
  border: 1px solid rgba(16, 185, 129, 0.55);
  box-shadow: 0 0 25px rgba(16, 185, 129, 0.25), inset 0 1px 0 rgba(255, 255, 255, 0.1);
  color: #6ee7b7;
}
.feedback-box.wrong {
  display: block;
  background: linear-gradient(135deg, rgba(239, 68, 68, 0.18) 0%, rgba(153, 27, 27, 0.3) 100%);
  border: 1px solid rgba(239, 68, 68, 0.55);
  box-shadow: 0 0 25px rgba(239, 68, 68, 0.25), inset 0 1px 0 rgba(255, 255, 255, 0.1);
  color: #fca5a5;
}
.feedback-box.partial {
  display: block;
  background: linear-gradient(135deg, rgba(245, 158, 11, 0.18) 0%, rgba(180, 83, 9, 0.3) 100%);
  border: 1px solid rgba(245, 158, 11, 0.55);
  box-shadow: 0 0 25px rgba(245, 158, 11, 0.25), inset 0 1px 0 rgba(255, 255, 255, 0.1);
  color: #fde68a;
}

.answer-card {
  display: none;
  background: linear-gradient(135deg, rgba(20, 27, 48, 0.88) 0%, rgba(10, 15, 29, 0.96) 100%);
  backdrop-filter: blur(3px);
  -webkit-backdrop-filter: blur(3px);
  border: 1px solid rgba(99, 102, 241, 0.35);
  border-radius: 14px;
  padding: 12px 14px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.1);
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}
.answer-layout {
  display: flex;
  gap: 14px;
  align-items: center;
}
.answer-poster-wrap {
  width: 58px !important;
  height: 82px !important;
  min-width: 58px !important;
  max-width: 58px !important;
  border-radius: 10px;
  overflow: hidden;
  flex-shrink: 0 !important;
  border: 1px solid rgba(255, 255, 255, 0.18);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.5), 0 0 10px rgba(99, 102, 241, 0.2);
  background: #0f172a;
}
#m3-ans-poster, #ans-poster-img, .answer-poster-img {
  width: 100% !important;
  height: 100% !important;
  max-width: 58px !important;
  max-height: 82px !important;
  object-fit: cover !important;
  display: block;
}
.answer-info-wrap {
  flex: 1;
  min-width: 0;
}
.answer-title {
  font-size: 15px;
  font-weight: 800;
  color: #fff;
  margin-bottom: 4px;
  display: flex;
  align-items: center;
  gap: 6px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  text-shadow: 0 0 12px rgba(255, 255, 255, 0.3);
}
.answer-meta {
  font-size: 12px;
  color: #c7d2fe;
  margin-bottom: 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.answer-syns {
  font-size: 11px;
  color: #94a3b8;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Modal de Alerta Centralizado (Glassmorphism & Anti-Saída durante Partida) */
.custom-modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(3, 7, 18, 0.82);
  backdrop-filter: blur(3px);
  -webkit-backdrop-filter: blur(3px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 99999;
  padding: 20px;
  box-sizing: border-box;
  animation: fadeIn 0.2s ease;
}
.custom-modal-card {
  background: #0f172a;
  border: 1px solid rgba(239, 68, 68, 0.45);
  box-shadow: 0 0 35px rgba(239, 68, 68, 0.25), 0 20px 40px rgba(0, 0, 0, 0.8);
  border-radius: 20px;
  padding: 28px 24px;
  max-width: 440px;
  width: 100%;
  text-align: center;
  box-sizing: border-box;
  transform: translateY(0);
  animation: modalPop 0.25s cubic-bezier(0.16, 1, 0.3, 1);
}
@keyframes modalPop {
  0% { transform: scale(0.9) translateY(12px); opacity: 0; }
  100% { transform: scale(1) translateY(0); opacity: 1; }
}
.custom-modal-icon-badge {
  width: 58px;
  height: 58px;
  border-radius: 50%;
  background: rgba(239, 68, 68, 0.15);
  border: 2px solid rgba(239, 68, 68, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 16px;
  box-shadow: 0 0 20px rgba(239, 68, 68, 0.35);
}
.custom-modal-title {
  font-size: 18px;
  font-weight: 800;
  color: #fff;
  margin-bottom: 10px;
}
.custom-modal-desc {
  font-size: 13px;
  color: #94a3b8;
  line-height: 1.6;
  margin-bottom: 22px;
}
.custom-modal-actions {
  display: flex;
  gap: 12px;
  justify-content: center;
  flex-wrap: wrap;
}

/* BARRA INFERIOR UNIFICADA DE CONTROLES (MESMA ALTURA RIGOROSA) */
.m1-bottom-controls-bar {
  display: grid;
  grid-template-columns: 1fr 1.15fr;
  gap: 18px;
  align-items: center;
  margin-top: 14px;
  padding-top: 12px;
  border-top: 1px solid rgba(255, 255, 255, 0.06);
}

.m1-media-ctrl-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
}

.m1-nav-ctrl-wrapper {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  width: 100%;
}

.m1-ctrl-card {
  display: inline-flex;
  align-items: center;
  background: rgba(13, 19, 36, 0.85);
  backdrop-filter: blur(3px);
  -webkit-backdrop-filter: blur(3px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 14px;
  padding: 6px 10px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
  height: 52px;
  box-sizing: border-box;
}

.m1-media-ctrl-card {
  gap: 8px;
}

.m1-nav-ctrl-card {
  gap: 8px;
}

/* Botões do Card de Mídia (Apenas Símbolos) */
.m1-ctrl-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 10px;
  border: 1px solid rgba(255, 255, 255, 0.12);
  background: rgba(30, 41, 69, 0.65);
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
  padding: 0;
  color: #fff;
}
.m1-ctrl-btn:hover {
  transform: translateY(-2px) scale(1.06);
  background: rgba(45, 58, 92, 0.85);
  border-color: rgba(255, 255, 255, 0.28);
  box-shadow: 0 0 14px rgba(99, 102, 241, 0.35);
}
.m1-ctrl-btn:active {
  transform: scale(0.95);
}

.m1-btn-play {
  background: rgba(16, 185, 129, 0.15);
  border-color: rgba(16, 185, 129, 0.35);
}
.m1-btn-play:hover, .m1-btn-play.is-expanded {
  background: rgba(16, 185, 129, 0.3) !important;
  border-color: rgba(16, 185, 129, 0.7) !important;
  box-shadow: 0 0 16px rgba(16, 185, 129, 0.5) !important;
}

.m1-btn-restart {
  background: rgba(6, 182, 212, 0.15);
  border-color: rgba(6, 182, 212, 0.35);
}
.m1-btn-restart:hover, .m1-btn-restart.is-expanded {
  background: rgba(6, 182, 212, 0.3) !important;
  border-color: rgba(6, 182, 212, 0.7) !important;
  box-shadow: 0 0 16px rgba(6, 182, 212, 0.5) !important;
}

/* Botão Aleatória: Alto Contraste (Fundo Escuro + Borda Dourada + Ícone Dourado) */
.m1-btn-random {
  background: rgba(245, 158, 11, 0.15);
  border-color: rgba(245, 158, 11, 0.4);
}
.m1-btn-random:hover, .m1-btn-random.is-expanded {
  background: rgba(245, 158, 11, 0.3) !important;
  border-color: rgba(245, 158, 11, 0.8) !important;
  box-shadow: 0 0 16px rgba(245, 158, 11, 0.55) !important;
}

/* Botões do Card de Navegação (Expansíveis com Hover / Toque) */
.m1-nav-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  height: 40px;
  min-width: 40px;
  max-width: 40px;
  padding: 0 10px;
  border-radius: 10px;
  border: 1px solid rgba(255, 255, 255, 0.12);
  background: rgba(30, 41, 69, 0.65);
  color: #e2e8f0;
  font-size: 12px;
  font-weight: 700;
  cursor: pointer;
  white-space: nowrap;
  overflow: hidden;
  transition: max-width 0.28s cubic-bezier(0.16, 1, 0.3, 1), background 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease, transform 0.2s ease;
  user-select: none;
  -webkit-user-select: none;
}

.m1-nav-label {
  opacity: 0;
  max-width: 0;
  margin-left: 0;
  display: inline-block;
  overflow: hidden;
  white-space: nowrap;
  transition: opacity 0.22s ease, max-width 0.28s cubic-bezier(0.16, 1, 0.3, 1), margin 0.22s ease;
}

@media (hover: hover) and (pointer: fine) {
  .m1-nav-btn:hover {
    max-width: 175px;
    background: rgba(45, 58, 92, 0.9);
    border-color: rgba(255, 255, 255, 0.28);
    box-shadow: 0 0 14px rgba(99, 102, 241, 0.35);
    transform: translateY(-2px);
  }
  .m1-nav-btn:hover .m1-nav-label {
    opacity: 1;
    max-width: 130px;
    margin-left: 8px;
    margin-right: 4px;
  }
}

.m1-nav-btn.is-expanded {
  max-width: 175px !important;
  background: rgba(45, 58, 92, 0.95) !important;
  border-color: rgba(255, 255, 255, 0.35) !important;
  box-shadow: 0 0 16px rgba(99, 102, 241, 0.45) !important;
}
.m1-nav-btn.is-expanded .m1-nav-label {
  opacity: 1 !important;
  max-width: 130px !important;
  margin-left: 8px !important;
  margin-right: 4px !important;
}

.m1-btn-reveal {
  background: rgba(168, 85, 247, 0.15);
  border-color: rgba(168, 85, 247, 0.35);
}
.m1-btn-reveal:hover, .m1-btn-reveal.is-expanded {
  background: rgba(168, 85, 247, 0.25) !important;
  border-color: rgba(168, 85, 247, 0.65) !important;
  box-shadow: 0 0 16px rgba(168, 85, 247, 0.45) !important;
}

/* Botões bloqueados de navegação antes de responder */
.m1-nav-btn.nav-locked,
.m1-nav-btn:disabled,
.btn.btn-locked,
#m3-btn-next:disabled {
  opacity: 0.38 !important;
  cursor: not-allowed !important;
  filter: grayscale(0.7) !important;
  transform: none !important;
  box-shadow: none !important;
}

@media (max-width: 900px) {
  .m1-bottom-controls-bar {
    grid-template-columns: 1fr;
    gap: 12px;
  }
  .m1-media-ctrl-wrapper,
  .m1-nav-ctrl-wrapper {
    justify-content: center;
  }
}

/* Modal de Configurações Central */
.settings-modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(5, 8, 16, 0.86);
  backdrop-filter: blur(3px);
  z-index: 99999;
  display: none;
  align-items: center;
  justify-content: center;
  padding: 16px;
  animation: fadeIn 0.15s ease;
}
.settings-modal-card {
  width: 100%;
  max-width: 480px;
  background: #0f172a;
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 18px;
  padding: 24px;
  box-shadow: 0 16px 40px rgba(0, 0, 0, 0.6);
  position: relative;
}
.settings-modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  padding-bottom: 12px;
}
.settings-modal-title {
  font-size: 16px;
  font-weight: 800;
  color: #fff;
  display: flex;
  align-items: center;
  gap: 10px;
}
.settings-close-btn {
  background: transparent;
  border: none;
  color: #94a3b8;
  font-size: 20px;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 6px;
  transition: color 0.2s ease;
}
.settings-close-btn:hover {
  color: #fff;
  background: rgba(255, 255, 255, 0.1);
}

/* Animação do Vinil */
.vinyl-spin-img {
  animation: vinylSpin 6s linear infinite;
  animation-play-state: paused;
}
.playing .vinyl-spin-img {
  animation-play-state: running;
}
@keyframes vinylSpin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* BOTTOM NAVIGATION BAR PARA MOBILE */
@media (max-width: 900px) {
  .app-sidebar {
    top: auto;
    bottom: 0;
    left: 0;
    right: 0;
    width: 100% !important;
    height: 62px;
    flex-direction: row;
    box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.6);
    border-right: none;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    padding: 0 4px;
  }
  .sidebar-header,
  .sidebar-divider,
  .sidebar-spacer,
  .sidebar-label {
    display: none !important;
  }
  .sidebar-nav {
    flex-direction: row;
    justify-content: space-around;
    align-items: center;
    width: 100%;
    padding: 0;
    gap: 2px;
  }
  .sidebar-item {
    padding: 10px;
    border-radius: 10px;
    flex: 1;
    justify-content: center;
  }
  .sidebar-item:hover {
    transform: none;
  }
  .app-main-content {
    margin-left: 0 !important;
    padding: 10px 10px 76px 10px;
  }
  .mode-split-grid {
    grid-template-columns: 1fr;
    gap: 14px;
  }
}
</style>
</head>
<body>

<!-- Canvas Global de Confetes & Partículas de Vitória -->
<canvas id="gamer-confetti-canvas" class="gamer-confetti-canvas"></canvas>

<!-- v3.0.0 e Salas & Placar mantidos para compatibilidade de testes -->
<div class="app-layout" id="app-layout">

  <!-- SIDEBAR MINI-RAIL (PARTE 1 À ESQUERDA) -->
  <aside class="app-sidebar" id="app-sidebar">
    <div class="sidebar-header">
      <div class="sidebar-logo-icon">
        <img src="icons/headphone-symbol.png" class="app-icon app-icon-lg icon-neon-cyan" alt="Logo" />
      </div>
      <div class="sidebar-title">ANIME QUIZ</div>
    </div>

    <!-- Navegação das Abas -->
    <nav class="sidebar-nav">
      <button class="sidebar-item active" id="tab-mode1" onclick="switchGameMode('mode1')">
        <span class="sidebar-icon-wrap">
          <img src="icons/headphone-symbol.png" class="app-icon icon-cyan" alt="Blind Test" />
        </span>
        <span class="sidebar-label">Modo 1: Blind Test</span>
      </button>

      <button class="sidebar-item" id="tab-mode2" onclick="switchGameMode('mode2')">
        <span class="sidebar-icon-wrap">
          <img src="icons/vinyl.png" class="app-icon icon-purple" alt="Qual é a Abertura" />
        </span>
        <span class="sidebar-label">Modo 2: Qual é a Abertura?</span>
      </button>

      <button class="sidebar-item" id="tab-mode3" onclick="switchGameMode('mode3')">
        <span class="sidebar-icon-wrap">
          <img src="icons/clapperboard.png" class="app-icon icon-orange" alt="Adivinhe a Cena" />
        </span>
        <span class="sidebar-label">Modo 3: Adivinhe a Cena</span>
      </button>

      <div class="sidebar-divider"></div>

      <button class="sidebar-item" id="tab-mode4" onclick="switchGameMode('mode4')">
        <span class="sidebar-icon-wrap">
          <img src="icons/game-controller.png" class="app-icon icon-blue" alt="Salas Multiplayer" />
        </span>
        <span class="sidebar-label">Salas Multiplayer</span>
      </button>

      <button class="sidebar-item" id="tab-mode5" onclick="switchGameMode('mode5')">
        <span class="sidebar-icon-wrap">
          <img src="icons/crown.png" class="app-icon icon-gold" alt="Placar de Líderes" />
        </span>
        <span class="sidebar-label">Placar de Líderes</span>
      </button>

      <div class="sidebar-spacer"></div>

      <button class="sidebar-item" id="btn-sidebar-settings" onclick="openSettingsModal()">
        <span class="sidebar-icon-wrap">
          <img src="icons/settings.png" class="app-icon icon-teal" alt="Configurações" />
        </span>
        <span class="sidebar-label">Configurações</span>
      </button>
    </nav>
  </aside>

  <!-- ÁREA CENTRAL DE JOGO (PARTE 2) -->
  <main class="app-main-content" id="app-main-content">
    <div class="container-center">

      <!-- Header Superior Compacto -->
      <header class="app-top-header">
        <div>
          <div style="display: flex; align-items: center; gap: 8px;">
            <h1 style="font-size: 16px; font-weight: 800; margin: 0; color: #fff;">Anime Music & Scene Quiz</h1>
            <span class="version-badge" style="font-size: 10px; padding: 2px 8px;">🎮 v3.3.0 • Arcade</span>
          </div>
          <p class="subtitle" style="font-size: 11px; margin: 2px 0 0 0; color: var(--text-muted);">
            Desafio interativo com 129 aberturas e 127 cenas reais. Ouça as músicas e teste seus conhecimentos!
          </p>
        </div>

      </header>

      <!-- Challenge Mode Banner -->
      <div class="challenge-banner" id="challenge-banner">
        <img src="icons/swords.png" class="app-icon icon-red" /> <strong>MODO DUELO ATIVO!</strong> Você está jogando com a semente compartilhada. Seus amigos terão exatamente as mesmas rodadas!
      </div>

      <!-- Scoreboard KPIs (Montado dinamicamente no card ativo) -->
      <div class="scoreboard" id="main-scoreboard">
        <div class="score-card">
          <div class="score-label"><img src="icons/crown.png" class="app-icon icon-gold" /> Pontuação</div>
          <div class="score-val" id="kpi-score" style="color: var(--accent);">0</div>
        </div>
        <div class="score-card">
          <div class="score-label"><img src="icons/check.png" class="app-icon icon-raw" /> Acertos</div>
          <div class="score-val" id="kpi-correct" style="color: var(--green);">0</div>
        </div>
        <div class="score-card">
          <div class="score-label"><img src="icons/fire.png" class="app-icon icon-raw" /> Combo / Streak</div>
          <div class="score-val" id="kpi-streak" style="color: var(--gold);">0</div>
        </div>
        <div class="score-card">
          <div class="score-label"><img src="icons/vinyl.png" class="app-icon icon-white" /> Progresso</div>
          <div class="score-val" id="kpi-progress">1 / 100</div>
        </div>
      </div>

      <!-- Multiplayer In-Game HUD (Visível durante partidas em salas) -->
      <div class="mp-hud-bar" id="mp-hud-bar" style="display: none;">
        <div class="mp-hud-left">
          <span style="font-size: 13px; font-weight: 800; color: #38bdf8;" id="mp-hud-room-badge">
            <img src="icons/game-controller.png" class="app-icon icon-white" /> SALA
          </span>
          <span class="pill-chip" id="mp-hud-round-pill">Rodada 1 de 10</span>
          <span class="mp-hud-timer-pill" id="mp-hud-timer-pill" style="display: none;">⏱️ 25s</span>
        </div>

        <div class="mp-hud-scores" id="mp-hud-scores-list"></div>

        <div style="display: flex; gap: 8px; align-items: center;">
          <button class="mp-skip-btn" id="mp-skip-vote-btn" onclick="MultiplayerEngine.voteSkip()">
            <span><img src="icons/fast-forward.png" class="app-icon icon-white" /> Pular</span>
            <span class="pill-chip" id="mp-skip-count-badge" style="background: rgba(0,0,0,0.3); font-size: 11px;">0/1</span>
          </button>
          <button class="mp-leave-btn" id="mp-hud-leave-btn" onclick="MultiplayerEngine.confirmLeaveRoom()" title="Abandonar partida e voltar">
            <img src="icons/logout.png" class="app-icon icon-red" /> Sair
          </button>
        </div>
      </div>

      <!-- GAMEPLAY AREA COM RANKING LATERAL MULTIPLAYER -->
      <div class="gameplay-wrapper" id="gameplay-wrapper">
        <div id="floating-arcade-container" class="floating-arcade-container"></div>

        <div class="gameplay-main-col">
          <div id="mp-waiting-banner" class="mp-waiting-banner" style="display: none;"></div>
      <!-- VIEW 1: MODO 1 - BLIND TEST -->
      <div class="quiz-card" id="mode1-view">
        <div class="quiz-header">
          <div class="round-indicator" id="m1-round-indicator">MÚSICA #1 DE 100</div>
          <button class="btn btn-outline" style="padding: 5px 12px; font-size: 11px;" onclick="openYouTubeDirect()">
            <img src="icons/play-button.png" class="app-icon icon-green" alt="Play" /> Clipe no YouTube
          </button>
        </div>
        <!-- Scoreboard Integrado do Modo 1 -->
        <div id="mode1-scoreboard-slot" class="mode-scoreboard-slot"></div>

        <!-- Grid 2-Colunas Desktop -->
        <div class="mode-split-grid">
          <!-- Coluna Esquerda: Player & Mídia -->
          <div class="mode-col-media">
            <div class="player-container" id="m1-player-container">
              <audio id="local-video-player" preload="auto" style="display: none;"></audio>
              <iframe id="video-frame" allow="autoplay; encrypted-media" style="display: none;"></iframe>
              <div class="player-visual-card" id="player-visual-card">
                <canvas id="m1-spectrum-canvas" class="audio-spectrum-canvas"></canvas>
                <div class="player-bg-art" id="player-bg-art"></div>
                <div class="player-scrim"></div>

                <!-- Blind Guessing View -->
                <div class="player-blind-content" id="player-blind-content">
                  <div class="vinyl" id="vinyl-icon">
                    <img src="icons/vinyl.png" class="app-icon-xl icon-white vinyl-spin-img" alt="Disco" />
                  </div>
                  <div style="margin-top: 10px; font-size: 12px; color: #94a3b8;" id="mask-status-text">
                    Modo Blind Test Ativo • Ouça e adivinhe o anime!
                  </div>
                </div>

                <!-- Revealed Answer View -->
                <div class="player-revealed-content" id="player-revealed-content" style="display: none;">
                  <div class="revealed-hero-row">
                    <img id="reveal-thumb-img" class="revealed-thumb-img" src="" alt="Capa" />
                    <div class="revealed-info-col">
                      <div class="revealed-badge" id="reveal-badge-status">
                        <img src="icons/check.png" class="app-icon icon-raw" /> RESPOSTA REVELADA
                      </div>
                      <div class="revealed-anime-title" id="reveal-anime-title">Nome do Anime</div>
                      <div class="revealed-song-name" id="reveal-song-name">"Nome da Música"</div>
                      <div class="revealed-artist-meta" id="reveal-artist-meta">por Artista (Ano) • Dificuldade</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Coluna Direita: Pistas, Input & Resposta Expansível -->
          <div class="mode-col-interactive">
            <!-- Pistas Reveláveis -->
            <div class="hints-section">
              <div class="hints-title">
                <img src="icons/lightbulb.png" class="app-icon icon-gold" /> Pistas Reveláveis:
              </div>
              <div class="tags-container" id="tags-container"></div>
              <div style="margin-top: 8px;">
                <button class="btn btn-secondary" style="padding: 5px 12px; font-size: 11px;" onclick="revealNextTag()">
                  <img src="icons/lightbulb.png" class="app-icon icon-gold" /> Revelar Próxima Pista (-10 pts)
                </button>
              </div>
            </div>

            <!-- Campo de Input & Autocomplete com Som Mecânico -->
            <div class="input-group">
              <div class="autocomplete-wrapper">
                <input type="text" class="quiz-input" id="guess-input" placeholder="Digite o anime... (TAB para enviar)" autocomplete="off" />
                <div class="autocomplete-dropdown" id="guess-autocomplete"></div>
              </div>
              <button class="btn btn-green" onclick="submitGuess()">
                <span>Enviar</span> <kbd style="background: rgba(0,0,0,0.35); border-radius: 4px; padding: 2px 6px; font-size: 11px; margin-left: 4px;">TAB ↵</kbd>
              </button>
            </div>

            <!-- Espaço Expansível de Resultado (Compacto inicialmente, expande ao acertar/errar/revelar) -->
            <div class="m1-result-slot" id="m1-result-slot">
              <!-- Feedback Banner Ultra Moderno Arcade -->
              <div class="feedback-box" id="feedback-box"></div>

              <!-- Answer Box Ultra Polido Glassmorphism -->
              <div class="answer-card" id="answer-box">
                <div class="answer-layout">
                  <div class="answer-poster-wrap">
                    <img id="ans-poster-img" class="answer-poster-img" src="" alt="Capa" />
                  </div>
                  <div class="answer-info-wrap">
                    <div class="answer-title" id="ans-anime">Nome do Anime</div>
                    <div class="answer-meta" id="ans-meta">Música • Artista</div>
                    <div class="answer-syns" id="ans-syns">Nomes aceitos: ...</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Linha Inferior Unificada de Controles (Ambos na Mesma Altura Rigorosa) -->
        <div class="m1-bottom-controls-bar">
          <!-- Card Retangular Esquerdo (Centralizado abaixo do player - expansível com hover / toque) -->
          <div class="m1-media-ctrl-wrapper">
            <div class="m1-ctrl-card m1-media-ctrl-card">
              <button class="m1-nav-btn m1-btn-play" id="btn-play-pause" onclick="handleM1Media('play', event)">
                <span id="play-btn-icon"><img src="icons/play-button.png" class="btn-icon-img" alt="Play" /></span>
                <span class="m1-nav-label" id="play-btn-text">Tocar Áudio</span>
              </button>
              <button class="m1-nav-btn m1-btn-restart" id="btn-restart" onclick="handleM1Media('restart', event)">
                <img src="icons/circle-of-two-clockwise-arrows-rotation.png" class="app-icon icon-cyan" alt="Reiniciar" />
                <span class="m1-nav-label">Reiniciar</span>
              </button>
              <button class="m1-nav-btn m1-btn-random" id="btn-random" onclick="handleM1Media('random', event)">
                <img src="icons/shuffle-arrows.png" class="app-icon icon-gold" alt="Aleatória" />
                <span class="m1-nav-label">Aleatória</span>
              </button>
            </div>
          </div>

          <!-- Card Retangular Direito (Navegação - apenas símbolos com hover expansível) -->
          <div class="m1-nav-ctrl-wrapper">
            <div class="m1-ctrl-card m1-nav-ctrl-card">
              <button class="m1-nav-btn" id="m1-btn-prev" onclick="handleM1Nav('prev', event)">
                <img src="icons/fast-forward.png" class="app-icon icon-blue icon-prev" alt="Anterior" />
                <span class="m1-nav-label">Anterior</span>
              </button>
              <button class="m1-nav-btn m1-btn-reveal" id="m1-btn-reveal" onclick="handleM1Nav('reveal', event)">
                <img src="icons/eye.png" class="app-icon icon-purple" alt="Revelar" />
                <span class="m1-nav-label">Revelar Resposta</span>
              </button>
              <button class="m1-nav-btn" id="m1-btn-next" onclick="handleM1Nav('next', event)">
                <img src="icons/fast-forward.png" class="app-icon icon-blue" alt="Próxima" />
                <span class="m1-nav-label">Próxima</span>
              </button>
              <button class="m1-nav-btn" id="m1-btn-finish" style="border-color: rgba(239, 68, 68, 0.4); color: #fca5a5;" onclick="finishCurrentGame('mode1')" title="Finalizar partida e salvar recorde">
                <span style="font-size: 13px;">🏁</span>
                <span class="m1-nav-label">Finalizar</span>
              </button>
            </div>
          </div>
        </div>
      </div><!-- fim mode1-view -->

  <!-- VIEW 2: MODO 2 - "QUAL É A ABERTURA?" (3 MÚSICAS ALEATÓRIAS - BENTO GRID) -->
  <div class="quiz-card" id="mode2-view" style="display: none;">
    <div class="quiz-header">
      <div class="round-indicator" id="m2-round-indicator">RODADA #1 DE 100</div>
      <button class="btn btn-outline" style="padding: 5px 12px; font-size: 11px;" onclick="m2StopAudio()">
        <img src="icons/sound-mute.png" class="app-icon icon-cyan" alt="Parar Som" /> Parar Som
      </button>
    </div>
    <!-- Scoreboard Integrado do Modo 2 -->
    <div id="mode2-scoreboard-slot" class="mode-scoreboard-slot"></div>

    <!-- Target Anime Banner (Retangular no topo, ultra compacto) -->
    <div class="target-anime-banner">
      <div class="target-poster-wrapper">
        <img id="m2-target-poster" class="target-poster-img" src="" alt="Capa do Anime" />
      </div>
      <div class="target-info-col">
        <div class="target-pre-title">QUAL DESTAS 3 MÚSICAS É A ABERTURA OFICIAL DE:</div>
        <div class="target-anime-name" id="m2-target-name">CARREGANDO...</div>
        <div class="target-meta-pills" id="m2-target-meta"></div>
      </div>
    </div>

    <!-- Grid 2-Colunas Desktop (Bento Grid Estilo Blind Test) -->
    <div class="mode-split-grid">
      <!-- Coluna Esquerda: Card Visual com Wave & Vinil Girando -->
      <div class="mode-col-media">
        <div class="player-container m2-player-container" id="m2-player-container">
          <audio id="m2-local-video" preload="auto" style="display: none;"></audio>
          <iframe id="m2-video-frame" allow="autoplay; encrypted-media" style="display: none;"></iframe>
          <div class="player-visual-card" id="m2-visual-card">
            <canvas id="m2-spectrum-canvas" class="audio-spectrum-canvas"></canvas>
            <div class="player-bg-art" id="m2-bg-art"></div>
            <div class="player-scrim"></div>

            <!-- Blind Listening View -->
            <div class="player-blind-content" id="m2-blind-content">
              <div class="vinyl" id="m2-vinyl-icon">
                <img src="icons/vinyl.png" class="app-icon-xl icon-white vinyl-spin-img" alt="Disco" />
              </div>
              <div style="margin-top: 8px; font-size: 12px; color: #cbd5e1;" id="m2-mask-status">
                Clique em uma opção ao lado para ouvir a música
              </div>
            </div>

            <!-- Revealed Answer View with Opening Thumbnail -->
            <div class="player-revealed-content" id="m2-revealed-content" style="display: none;">
              <div class="revealed-hero-row">
                <img id="m2-reveal-thumb-img" class="revealed-thumb-yt" src="" alt="Thumbnail da Abertura" />
                <div class="revealed-info-col">
                  <div class="revealed-badge" id="m2-reveal-badge">
                    <img src="icons/check.png" class="app-icon icon-raw" /> ABERTURA CORRETA
                  </div>
                  <div class="revealed-anime-title" id="m2-reveal-anime-title">Nome do Anime</div>
                  <div class="revealed-song-name" id="m2-reveal-song-name">"Nome da Música"</div>
                  <div class="revealed-artist-meta" id="m2-reveal-artist-meta">por Artista (Ano)</div>
                </div>
              </div>
            </div>
          </div>
          <div id="m2-player-mask" style="display: none;"></div>
        </div>
      </div>

      <!-- Coluna Direita: Feedback, 3 Opções de Música & Ações (Confirmar / Próxima) -->
      <div class="mode-col-interactive">
        <!-- Feedback Banner -->
        <div class="m2-feedback-banner" id="m2-feedback-banner"></div>

        <!-- 3 Music Cards -->
        <div class="music-cards-grid">
          <div class="music-card" id="m2-card-0" onclick="m2ClickCard(0)">
            <div class="card-left">
              <div class="card-radio-ring"><div class="card-radio-dot"></div></div>
              <div class="card-meta">
                <div class="card-badge-num">OPÇÃO 1</div>
                <div class="card-title-text" id="m2-label-0">Faixa de Áudio 1</div>
                <div class="card-reveal-sub" id="m2-sub-0"></div>
              </div>
            </div>
            <div class="card-play-trigger">
              <div class="card-equalizer" id="m2-eq-0"><span></span><span></span><span></span><span></span></div>
              <div class="card-play-btn" id="m2-btn-0"><span id="m2-icon-0"><img src="icons/play-button.png" class="app-icon icon-green" alt="Play" /></span></div>
            </div>
          </div>

          <div class="music-card" id="m2-card-1" onclick="m2ClickCard(1)">
            <div class="card-left">
              <div class="card-radio-ring"><div class="card-radio-dot"></div></div>
              <div class="card-meta">
                <div class="card-badge-num">OPÇÃO 2</div>
                <div class="card-title-text" id="m2-label-1">Faixa de Áudio 2</div>
                <div class="card-reveal-sub" id="m2-sub-1"></div>
              </div>
            </div>
            <div class="card-play-trigger">
              <div class="card-equalizer" id="m2-eq-1"><span></span><span></span><span></span><span></span></div>
              <div class="card-play-btn" id="m2-btn-1"><span id="m2-icon-1"><img src="icons/play-button.png" class="app-icon icon-green" alt="Play" /></span></div>
            </div>
          </div>

          <div class="music-card" id="m2-card-2" onclick="m2ClickCard(2)">
            <div class="card-left">
              <div class="card-radio-ring"><div class="card-radio-dot"></div></div>
              <div class="card-meta">
                <div class="card-badge-num">OPÇÃO 3</div>
                <div class="card-title-text" id="m2-label-2">Faixa de Áudio 3</div>
                <div class="card-reveal-sub" id="m2-sub-2"></div>
              </div>
            </div>
            <div class="card-play-trigger">
              <div class="card-equalizer" id="m2-eq-2"><span></span><span></span><span></span><span></span></div>
              <div class="card-play-btn" id="m2-btn-2"><span id="m2-icon-2"><img src="icons/play-button.png" class="app-icon icon-green" alt="Play" /></span></div>
            </div>
          </div>
        </div>

        <!-- Mode 2 Actions -->
        <div class="m2-actions" style="display: flex; gap: 8px; flex-wrap: wrap;">
          <button class="btn btn-green" id="m2-btn-confirm" onclick="m2ConfirmSelection()" disabled>
            <img src="icons/check.png" class="app-icon icon-raw" /> Confirmar Escolha
          </button>
          <button class="btn btn-gold" id="m2-btn-next" onclick="m2NextRound()" style="display: none;">
            Próxima Rodada <img src="icons/fast-forward.png" class="app-icon icon-white" />
          </button>
          <button class="btn btn-outline" id="m2-btn-finish" onclick="finishCurrentGame('mode2')" title="Finalizar partida e salvar recorde">
            🏁 Finalizar
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- VIEW 3: MODO 3 - "ADIVINHE A CENA" (FRAME / SCREENSHOT REAL QUIZ - BENTO GRID) -->
  <div class="quiz-card" id="mode3-view" style="display: none;">
    <div class="quiz-header">
      <div class="round-indicator" id="m3-round-indicator">CENA #1 DE 98</div>
      <button class="btn btn-gold" style="padding: 5px 12px; font-size: 11px;" onclick="m3PickRandom()">
        <img src="icons/shuffle-arrows.png" class="app-icon icon-white" /> Cena Aleatória
      </button>
    </div>
    <!-- Scoreboard Integrado do Modo 3 -->
    <div id="mode3-scoreboard-slot" class="mode-scoreboard-slot"></div>

    <!-- Grid 2-Colunas Desktop (Bento Grid Estilo Blind Test) -->
    <div class="mode-split-grid">
      <!-- Coluna Esquerda: Foto da Cena & Tags Abaixo -->
      <div class="mode-col-media">
        <!-- Scene Viewport (Frames Reais de Episódios) -->
        <div class="scene-viewport" id="m3-scene-viewport">
          <div class="scene-cinema-bar top"></div>
          <img id="m3-scene-img" class="scene-frame-img" src="" alt="Cena do Anime" referrerpolicy="no-referrer" loading="eager" />
          <div class="scene-cinema-bar bottom"></div>
          <button class="scene-zoom-trigger" onclick="openLightbox()">
            <img src="icons/search.png" class="app-icon icon-white" /> Ampliar Cena
          </button>
        </div>

        <!-- Scene Clue Tags & Botão de Revelar Dica -->
        <div class="m3-clues-wrapper">
          <div class="scene-tags-row" id="m3-tags-row"></div>
          <button class="btn btn-secondary m3-hint-btn" onclick="m3RevealNextHint()">
            <img src="icons/padlock.png" class="app-icon icon-white" /> Revelar Dica (-15 pts)
          </button>
        </div>
      </div>

      <!-- Coluna Direita: Input, Feedback, Resposta Revelada & Navegação -->
      <div class="mode-col-interactive">
        <!-- Input for Scene Guess with Autocomplete & TAB auto-submit -->
        <div class="input-group">
          <div class="autocomplete-wrapper">
            <input type="text" class="quiz-input" id="m3-input" placeholder="Digite o anime... (TAB para selecionar e enviar)" autocomplete="off" />
            <div class="autocomplete-dropdown" id="m3-autocomplete"></div>
          </div>
          <button class="btn btn-green" onclick="m3SubmitGuess()">
            <span>Adivinhar</span> <kbd style="background: rgba(0,0,0,0.35); border-radius: 4px; padding: 2px 6px; font-size: 11px; margin-left: 4px;">TAB ↵</kbd>
          </button>
        </div>

        <!-- Espaço de Feedback & Resposta Revelada -->
        <div class="m3-result-slot" id="m3-result-slot">
          <!-- Feedback Banner -->
          <div class="feedback-box" id="m3-feedback-box"></div>

          <!-- Answer Box -->
          <div class="answer-card" id="m3-answer-box">
            <div class="answer-layout">
              <div class="answer-poster-wrap">
                <img id="m3-ans-poster" class="answer-poster-img" src="" alt="Capa" />
              </div>
              <div class="answer-info-wrap">
                <div class="answer-title" id="m3-ans-title">Nome do Anime</div>
                <div class="answer-meta" id="m3-ans-meta">Ano • Estúdio • Gêneros</div>
                <div class="answer-syns" id="m3-ans-syns">Nomes aceitos: ...</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Navigation -->
        <div class="m3-nav-row nav-row" style="display: flex; gap: 8px; flex-wrap: wrap;">
          <button class="btn btn-outline" id="m3-btn-giveup" onclick="m3GiveUp()">
            <img src="icons/eye.png" class="app-icon icon-white" /> Ver Resposta
          </button>
          <button class="btn btn-secondary" id="m3-btn-next" onclick="m3NextScene()">
            Próxima Cena <img src="icons/fast-forward.png" class="app-icon icon-white" />
          </button>
          <button class="btn btn-outline" id="m3-btn-finish" onclick="finishCurrentGame('mode3')" style="border-color: rgba(239, 68, 68, 0.4); color: #fca5a5;" title="Finalizar partida e registrar recorde">
            🏁 Finalizar Partida
          </button>
        </div>
      </div>
    </div>
  </div>

  </div><!-- fim .gameplay-main-col -->

  <!-- PAINEL LATERAL DE RANKING AO VIVO (Visível durante Multiplayer) -->
  <aside class="mp-live-sidebar" id="mp-live-sidebar" style="display: none;">
    <div class="mp-sidebar-header">
      <div class="mp-sidebar-title-row">
        <div class="mp-sidebar-title">
          <span>🏆 RANKING AO VIVO</span>
          <span class="mp-sidebar-live-dot"></span>
        </div>
        <span class="pill-chip" style="font-size: 10px; padding: 2px 6px;">P2P</span>
      </div>
      <div class="mp-sidebar-subtitle">Posições atualizadas em tempo real</div>
    </div>
    <div class="mp-sidebar-list" id="mp-sidebar-list"></div>
    <div class="mp-sidebar-footer">
      <span id="mp-sidebar-footer-hint">⚡ Bônus de rapidez ativo!</span>
    </div>
  </aside>
</div><!-- fim .gameplay-wrapper -->

  <!-- VIEW 4: MODO 4 - SALAS MULTIPLAYER (DEDICADO A SALAS AO VIVO) -->
  <div class="quiz-card" id="mode4-view" style="display: none;">
    <div class="quiz-header" style="margin-bottom: 16px;">
      <div class="round-indicator">🎮 SALAS MULTIPLAYER P2P (AO VIVO)</div>
    </div>
    <!-- PAINEL 1: SALAS MULTIPLAYER -->
    <div id="mp-rooms-panel">
      <!-- Estado A: Fora de Sala (Criar ou Entrar) -->
      <div id="mp-pre-room-view">
        <div class="mp-setup-grid">
          
          <!-- Card 1: Criar Sala (Host) -->
          <div class="mp-panel-card">
            <div class="mp-card-title">
              <span>👑</span> <span>Criar Nova Sala (Host)</span>
            </div>
            <div class="mp-form-row">
              <label class="mp-form-label">Seu Apelido:</label>
              <input type="text" class="mp-input" id="mp-host-nick" placeholder="Ex: Luffy, Goku..." maxlength="15" />
            </div>
            <div class="mp-form-row">
              <label class="mp-form-label">Modo de Jogo:</label>
              <select class="mp-input" id="mp-mode-select">
                <option value="mode2" selected>🎵 Modo 2: Qual é a Abertura? (3 opções)</option>
                <option value="mode1">🎧 Modo 1: Blind Test (digitar com autocomplete)</option>
                <option value="mode3">🖼️ Modo 3: Adivinhe a Cena (screenshots reais)</option>
                <option value="mixed">🎲 Modo Misto (alterna música e cena!)</option>
              </select>
            </div>
            <div class="mp-form-row">
              <label class="mp-form-label">Quantidade de Rodadas:</label>
              <select class="mp-input" id="mp-rounds-select">
                <option value="5">5 Rodadas (Rápido)</option>
                <option value="10" selected>10 Rodadas</option>
                <option value="15">15 Rodadas</option>
                <option value="20">20 Rodadas</option>
                <option value="30">30 Rodadas (Maratona Gamer)</option>
              </select>
            </div>
            <div class="mp-form-row">
              <label class="mp-form-label">Tempo por Rodada:</label>
              <select class="mp-input" id="mp-timer-select">
                <option value="15">15 segundos (Blitz)</option>
                <option value="25" selected>25 segundos (Padrão)</option>
                <option value="40">40 segundos (Tranquilo)</option>
                <option value="0">Sem Limite de Tempo</option>
              </select>
            </div>
            <button class="btn btn-primary" style="margin-top: 6px; justify-content: center;" onclick="MultiplayerEngine.createRoom()">
              🚀 Criar Sala & Abrir Lobby
            </button>
          </div>

          <!-- Card 2: Entrar em Sala (Guest) -->
          <div class="mp-panel-card">
            <div class="mp-card-title">
              <span>🎮</span> <span>Entrar em Sala de Amigo</span>
            </div>
            <div class="mp-form-row">
              <label class="mp-form-label">Código da Sala:</label>
              <input type="text" class="mp-input" id="mp-join-code" placeholder="Ex: OTAKU, 4821..." maxlength="10" style="text-transform: uppercase;" />
            </div>
            <div class="mp-form-row">
              <label class="mp-form-label">Seu Apelido:</label>
              <input type="text" class="mp-input" id="mp-guest-nick" placeholder="Ex: Zoro, Sanji..." maxlength="15" />
            </div>
            <div style="font-size: 12px; color: #94a3b8; line-height: 1.5; margin-top: 8px;">
              ⚡ <strong>Sem cadastro ou senha!</strong> Basta digitar o código compartilhado pelo seu amigo e jogar na mesma hora.
            </div>
            <button class="btn btn-green" style="margin-top: auto; justify-content: center;" onclick="MultiplayerEngine.joinRoom()">
              🚪 Conectar & Entrar na Sala
            </button>
          </div>
        </div>
      </div>

      <!-- Estado B: Lobby da Sala Ativo -->
      <div id="mp-lobby-view" style="display: none;">
        <div class="lobby-box">
          <div class="lobby-header-row">
            <div>
              <div style="font-size: 11px; font-weight: 700; color: #94a3b8; text-transform: uppercase;">Lobby da Sala</div>
              <div style="display: flex; align-items: center; gap: 10px; margin-top: 4px;">
                <div class="lobby-code-badge" onclick="MultiplayerEngine.copyRoomCode()" title="Clique para copiar">
                  <span style="font-size: 12px; color: #94a3b8;">CÓDIGO:</span>
                  <span class="lobby-code-val" id="mp-lobby-code-text">-----</span>
                  <span><img src="icons/copy.png" class="app-icon app-icon-sm icon-teal" /></span>
                </div>
              </div>
            </div>
            <div class="lobby-meta-pills" id="mp-lobby-meta-pills"></div>
          </div>

          <div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
              <div style="font-size: 12px; font-weight: 800; color: #cbd5e1;">
                👥 JOGADORES NA SALA (<span id="mp-lobby-count">1</span>):
              </div>
              <button class="btn btn-outline" style="padding: 4px 10px; font-size: 11px;" onclick="MultiplayerEngine.addTestBot()">
                <img src="icons/robot.png" class="app-icon app-icon-sm icon-purple" /> Adicionar Bot de Teste
              </button>
            </div>
            <div class="lobby-players-grid" id="mp-lobby-players-grid"></div>
          </div>

          <div style="display: flex; gap: 10px; justify-content: space-between; align-items: center; flex-wrap: wrap; margin-top: 10px; border-top: 1px solid #1a223a; padding-top: 16px;">
            <button class="btn btn-outline" onclick="MultiplayerEngine.leaveRoom()">
              <img src="icons/logout.png" class="app-icon icon-red" /> Sair da Sala
            </button>
            <div id="mp-lobby-host-actions" style="display: none;">
              <button class="btn btn-green" style="padding: 10px 24px; font-size: 14px;" onclick="MultiplayerEngine.startGame()">
                <img src="icons/fire.png" class="app-icon icon-raw" /> INICIAR PARTIDA AGORA!
              </button>
            </div>
            <div id="mp-lobby-guest-waiting" style="display: none; font-size: 13px; color: #f59e0b; font-weight: 700;">
              ⏳ Aguardando o Host iniciar a partida...
            </div>
          </div>
        </div>
      </div>

      <!-- Estado C: Pódio da Partida Multiplayer -->
      <div id="mp-podium-view" style="display: none;">
        <div class="podium-box">
          <div class="podium-title">🏆 FIM DE PARTIDA!</div>
          <div class="podium-subtitle">Confira os maiores pontuadores da rodada:</div>

          <div class="podium-pillars-row" id="mp-podium-pillars"></div>

          <div style="max-width: 500px; margin: 0 auto 20px auto;">
            <table class="leaderboard-table">
              <thead>
                <tr>
                  <th style="width: 50px;">Pos</th>
                  <th>Jogador</th>
                  <th>Pontos</th>
                  <th>Acertos</th>
                </tr>
              </thead>
              <tbody id="mp-podium-table-body"></tbody>
            </table>
          </div>

          <div style="display: flex; gap: 10px; justify-content: center; flex-wrap: wrap;">
            <button class="btn btn-gold" id="mp-rematch-btn" onclick="MultiplayerEngine.rematch()">
              🔄 Jogar Novamente (Mesma Sala)
            </button>
            <button class="btn btn-secondary" onclick="MultiplayerEngine.leaveRoom()">
              🏠 Voltar ao Lobby
            </button>
          </div>
        </div>
      </div>
    </div>
  </div><!-- fim mode4-view -->

  <!-- VIEW 5: PLACAR DE LÍDERES & HALL DA FAMA (TOP 50 ROLÁVEL) -->
  <div class="quiz-card" id="mode5-view" style="display: none;">
    <div id="mp-leaderboard-panel" style="display: block;">
      <div class="quiz-header" style="margin-bottom: 14px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
        <div style="display: flex; align-items: center; gap: 10px; flex-wrap: wrap;">
          <div class="round-indicator">🏆 HALL DA FAMA MUNDIAL • TOP 50</div>
          <div id="cloud-status-badge" class="cloud-status-pill online" title="Conectado à Nuvem Global">
            <span class="status-dot pulse-green"></span> 🟢 Nuvem Global • Ao Vivo
          </div>
        </div>
      </div>

      <div class="leaderboard-container">

        <!-- Filtros do Placar -->
        <div class="leaderboard-filter-tabs">
          <button class="lb-tab-btn active" onclick="filterLeaderboard('all', this)">🏆 Geral</button>
          <button class="lb-tab-btn" onclick="filterLeaderboard('mode2', this)">🎵 Qual é a Abertura?</button>
          <button class="lb-tab-btn" onclick="filterLeaderboard('mode1', this)">🎧 Blind Test</button>
          <button class="lb-tab-btn" onclick="filterLeaderboard('mode3', this)">🖼️ Adivinhe a Cena</button>
          <button class="lb-tab-btn" onclick="filterLeaderboard('multiplayer', this)">🎮 Multiplayer</button>
        </div>

        <!-- Área de Tabela com Scroll para até 50 Jogadores -->
        <div class="leaderboard-scroll-wrapper" style="max-height: 480px; overflow-y: auto; overflow-x: hidden; border: 1px solid rgba(255,255,255,0.06); border-radius: 10px;">
          <table class="leaderboard-table" style="margin: 0;">
            <thead style="position: sticky; top: 0; background: #0f172a; z-index: 2;">
              <tr>
                <th style="width: 50px;">Pos</th>
                <th>Jogador</th>
                <th>Modo</th>
                <th>Pontos</th>
                <th>Acertos</th>
                <th>Data</th>
              </tr>
            </thead>
            <tbody id="leaderboard-tbody"></tbody>
          </table>
        </div>
      </div>
    </div>
  </div><!-- fim mode5-view -->

    </div><!-- fim container-center -->
  </main><!-- fim app-main-content -->
</div><!-- fim app-layout -->

<!-- MODAL DE CONFIGURAÇÕES CENTRAL (ÁUDIO, SFX & ATALHOS) -->
<div class="settings-modal-overlay" id="settings-modal" onclick="if(event.target===this)closeSettingsModal()">
  <div class="settings-modal-card">
    <div class="settings-modal-header">
      <div class="settings-modal-title">
        <img src="icons/settings.png" class="app-icon icon-white" alt="Settings" /> Configurações & Áudio
      </div>
      <button class="settings-close-btn" onclick="closeSettingsModal()">&times;</button>
    </div>

    <!-- Popover container oculto para manter compatibilidade com testes legados -->
    <div id="audio-settings-popover" style="display: none;"></div>

    <!-- Canal BGM -->
    <div class="audio-channel-row" style="margin-bottom: 16px;">
      <div class="audio-channel-header">
        <span><img src="icons/volume-up.png" class="app-icon icon-cyan" /> Música de Fundo (BGM)</span>
        <span class="audio-channel-val" id="bgm-vol-text">80%</span>
      </div>
      <input type="range" class="audio-slider" id="bgm-vol-slider" min="0" max="1" step="0.05" value="0.8" oninput="AudioManager.setBgmVolume(this.value)" />
    </div>

    <!-- Canal SFX -->
    <div class="audio-channel-row" style="margin-bottom: 16px;">
      <div class="audio-channel-header">
        <span><img src="icons/volume.png" class="app-icon icon-purple" /> Efeitos Sonoros (SFX)</span>
        <span class="audio-channel-val" id="sfx-vol-text">80%</span>
      </div>
      <input type="range" class="audio-slider" id="sfx-vol-slider" min="0" max="1" step="0.05" value="0.8" oninput="AudioManager.setSfxVolume(this.value)" />
    </div>

    <!-- Mute Geral -->
    <button class="audio-mute-toggle-btn" id="btn-mute-toggle" onclick="AudioManager.toggleMute()" style="margin-bottom: 18px; width: 100%;">
      <span id="mute-btn-icon"><img src="icons/sound-mute.png" class="app-icon icon-red" /></span>
      <span id="mute-btn-text">Mutar Todo o Jogo</span>
    </button>

    <!-- Guia de Atalhos Rápidos -->
    <div style="border-top: 1px solid rgba(255,255,255,0.08); padding-top: 14px;">
      <div style="font-size: 12px; font-weight: 800; color: #cbd5e1; margin-bottom: 8px;">⌨️ Atalhos do Teclado:</div>
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; font-size: 11px; color: var(--text-muted);">
        <div><kbd>TAB</kbd> Autocomplete / Enviar</div>
        <div><kbd>Espaço</kbd> Tocar / Pausar Som</div>
        <div><kbd>1</kbd>, <kbd>2</kbd>, <kbd>3</kbd> Opções no Modo 2</div>
        <div><kbd>Enter</kbd> Confirmar Seleção</div>
      </div>
    </div>
  </div>
</div>

<!-- Lightbox Modal -->
<div class="lightbox-modal" id="lightbox-modal" onclick="closeLightbox()">
  <span class="lightbox-close" onclick="closeLightbox()">&times;</span>
  <img id="lightbox-img" class="lightbox-img" src="" alt="Cena em Alta Resolução" />
</div>

<!-- Toast Notification -->
<div class="toast-msg" id="toast-msg">Link copiado com sucesso!</div>

<!-- Modal de Alerta Centralizado: Partida Ativa em Andamento -->
<div id="match-active-alert-modal" class="custom-modal-backdrop" style="display: none;" onclick="closeMatchActiveAlert(event)">
  <div class="custom-modal-card" onclick="event.stopPropagation()">
    <div class="custom-modal-icon-badge">
      <img src="icons/close.png" class="app-icon icon-red" alt="Aviso" style="filter: invert(36%) sepia(85%) saturate(3000%) hue-rotate(340deg);" />
    </div>
    <div class="custom-modal-title">Partida ou Sala em Andamento!</div>
    <div class="custom-modal-desc" id="match-active-alert-desc">
      Você está com uma partida multiplayer ativa. Para navegar por outros modos, conclua as rodadas ou clique em Sair da Sala.
    </div>
    <div class="custom-modal-actions">
      <button class="btn btn-primary" onclick="closeMatchActiveAlert()" style="padding: 10px 22px; font-weight: 700; border-radius: 10px;">
        Entendido
      </button>
      <button class="btn btn-danger" onclick="leaveRoomFromAlert()" style="padding: 10px 18px; font-weight: 700; border-radius: 10px; background: rgba(239, 68, 68, 0.15); border: 1px solid #ef4444; color: #fca5a5;">
        Sair da Sala
      </button>
    </div>
  </div>
</div>

<!-- MODAL UNIVERSAL DE FIM DE PARTIDA & SALVAR NO HALL DA FAMA -->
<div class="settings-modal-overlay" id="game-over-modal" style="display: none;" onclick="if(event.target===this)closeGameOverModal()">
  <div class="settings-modal-card game-over-modal-card" style="max-width: 480px; text-align: center;">
    <div class="game-over-header" style="margin-bottom: 12px;">
      <div style="font-size: 34px; line-height: 1;">🏆</div>
      <h2 style="font-size: 21px; font-weight: 800; color: #fff; margin-top: 4px;">Partida Concluída!</h2>
      <p style="font-size: 12px; color: var(--text-muted); margin-top: 2px;" id="game-over-subtitle">
        Veja seu resultado e registre seu nome no Hall da Fama Mundial.
      </p>
    </div>

    <!-- Estatísticas da Partida -->
    <div class="game-over-stats-grid">
      <div class="go-stat-item">
        <span class="go-stat-label">Modo</span>
        <strong class="go-stat-val" id="go-mode-val">Blind Test</strong>
      </div>
      <div class="go-stat-item">
        <span class="go-stat-label">Pontuação</span>
        <strong class="go-stat-val highlight" id="go-score-val">0 pts</strong>
      </div>
      <div class="go-stat-item">
        <span class="go-stat-label">Acertos</span>
        <strong class="go-stat-val" id="go-correct-val">0</strong>
      </div>
      <div class="go-stat-item">
        <span class="go-stat-label">Maior Combo</span>
        <strong class="go-stat-val flame" id="go-streak-val">0x</strong>
      </div>
    </div>

    <!-- Título / Badge de Prestígio Conquistado -->
    <div class="game-over-badge-box">
      <div style="font-size: 11px; text-transform: uppercase; letter-spacing: 0.6px; color: var(--text-muted); margin-bottom: 6px;">
        Título de Prestígio Conquistado:
      </div>
      <div id="go-badge-container" style="display: flex; justify-content: center; gap: 8px; flex-wrap: wrap;"></div>
      <div id="go-badge-desc" style="font-size: 11.5px; color: #94a3b8; margin-top: 6px;"></div>
    </div>

    <!-- Formulário de Registro do Jogador -->
    <div class="game-over-form" style="margin-top: 14px;">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
        <label style="font-size: 12px; font-weight: 700; color: #cbd5e1;">
          Digite seu Apelido Otaku <span style="color: var(--rose);">*</span>
        </label>
        <span id="go-char-count" style="font-size: 11px; font-weight: 700; color: var(--rose);">0/5 (mínimo 5 letras)</span>
      </div>
      <div style="position: relative;">
        <input type="text" id="go-nickname-input" class="save-score-input" style="width: 100%; box-sizing: border-box; font-size: 14px; padding: 10px 14px;" placeholder="Ex: Levi_Ackerman..." maxlength="15" autocomplete="off" oninput="validateGoNickname()" />
      </div>
      <div id="go-nick-hint" style="font-size: 11px; color: var(--rose); margin-top: 5px; text-align: left;">
        O apelido precisa ter no mínimo 5 caracteres para salvar no placar.
      </div>
    </div>

    <!-- Ações Claras e Objetivas -->
    <div style="display: flex; gap: 8px; justify-content: center; margin-top: 16px; flex-wrap: wrap;">
      <button class="btn btn-outline" style="flex: 1; padding: 10px 12px; font-size: 11px; border-radius: 10px;" onclick="closeGameOverModal()" title="Voltar ao jogo mantendo a pontuação atual">
        ▶️ Voltar ao Jogo
      </button>
      <button class="btn btn-outline" style="flex: 1.1; padding: 10px 12px; font-size: 11px; border-radius: 10px; border-color: rgba(239, 68, 68, 0.45); color: #fca5a5;" onclick="discardSessionAndReset()" title="Zerar pontuação atual e começar novo jogo">
        🗑️ Não Salvar (Zerar)
      </button>
      <button class="btn btn-green" id="go-save-btn" style="flex: 1.4; padding: 10px 14px; font-size: 12px; border-radius: 10px; opacity: 0.45; pointer-events: none;" onclick="submitGameOverScore()">
        💾 Salvar no Ranking
      </button>
    </div>
  </div>
</div>

<script>
/* ==============================================================
   DATA SETS (100 OPENINGS + 98 REAL EPISODE FRAMES + 697 AUTOCOMPLETE TITLES)
   ============================================================== */
const ALL_SONGS = __SONGS_JSON__;
const ALL_SCENES = __SCENES_JSON__;
const ANIME_AUTOCOMPLETE = __AUTOCOMPLETE_JSON__;

/* Deterministic PRNG for Multiplayer Challenge Links */
function mulberry32(a) {
  return function() {
    var t = a += 0x6D2B79F5;
    t = Math.imul(t ^ t >>> 15, t | 1);
    t ^= t + Math.imul(t ^ t >>> 7, t | 61);
    return ((t ^ t >>> 14) >>> 0) / 4294967296;
  }
}

// Check URL Params for Multiplayer Challenge
const urlParams = new URLSearchParams(window.location.search);
const challengeMode = urlParams.get('challenge');
const challengeTargetMode = urlParams.get('mode') || 'mode2';
const challengeSeed = parseInt(urlParams.get('seed')) || null;
const challengeRounds = parseInt(urlParams.get('rounds')) || 10;

let isChallengeActive = Boolean(challengeSeed);
let seededRand = challengeSeed ? mulberry32(challengeSeed) : null;
function getGameRandom() {
  return seededRand ? seededRand() : Math.random();
}

/* ==============================================================
   GLOBAL STATE
   ============================================================== */
let activeGameMode = 'mode1';
let masterVolume = 0.8;
let isMuted = false;

// Mode 1 State
let m1CurrentIndex = 0;
let m1Playlist = [];
let m1PlaylistIndex = 0;
let m1Score = 0;
let m1CorrectCount = 0;
let m1Streak = 0;
let m1Attempts = 0;
let m1RevealedTagsCount = 0;
let m1AnsweredCurrent = false;
let m1HasGuessed = false;
let m1IsPlaying = false;
let m1UseLocal = true;

// Mode 2 State (Qual é a Abertura?)
let m2CurrentIndex = 0;
let m2UnplayedQueue = [];
let m2Score = 0;
let m2CorrectCount = 0;
let m2Streak = 0;
let m2Options = [];
let m2CorrectOptionIndex = -1;
let m2SelectedOptionIndex = -1;
let m2PlayingIndex = -1;
let m2Answered = false;
let m2RoundsPlayed = 0;

// Mode 3 State (Adivinhe a Cena)
let m3CurrentIndex = 0;
let m3UnplayedQueue = [];
let m3Score = 0;
let m3CorrectCount = 0;
let m3Streak = 0;
let m3HintsRevealed = 0;
let m3Answered = false;
let m3HasGuessed = false;
let m3RoundsPlayed = 0;

/* DOM ELEMENTS */
const masterVolSlider = document.getElementById('master-vol-slider') || document.getElementById('bgm-vol-slider');
const volPctText = document.getElementById('vol-pct-text') || document.getElementById('bgm-vol-text');
const btnMasterMute = document.getElementById('btn-master-mute') || document.getElementById('btn-mute-toggle');
const kpiScore = document.getElementById('kpi-score');
const kpiCorrect = document.getElementById('kpi-correct');
const kpiStreak = document.getElementById('kpi-streak');
const kpiProgress = document.getElementById('kpi-progress');
const challengeBanner = document.getElementById('challenge-banner');

// M1 DOM
const localVideoPlayer = document.getElementById('local-video-player');
const videoFrame = document.getElementById('video-frame');
const blindMask = document.getElementById('blind-mask');
const vinylIcon = document.getElementById('vinyl-icon');
const soundBars = document.getElementById('sound-bars');
const playBtnIcon = document.getElementById('play-btn-icon');
const playBtnText = document.getElementById('play-btn-text');
const guessInput = document.getElementById('guess-input');
const guessAutocomplete = document.getElementById('guess-autocomplete');
const feedbackBox = document.getElementById('feedback-box');
const answerBox = document.getElementById('answer-box');
const ansPosterImg = document.getElementById('ans-poster-img');
const ansAnime = document.getElementById('ans-anime');
const ansMeta = document.getElementById('ans-meta');
const ansSyns = document.getElementById('ans-syns');
const tagsContainer = document.getElementById('tags-container');
const m1RoundIndicator = document.getElementById('m1-round-indicator');

// M2 DOM
const m2TargetName = document.getElementById('m2-target-name');
const m2TargetPoster = document.getElementById('m2-target-poster');
const m2TargetMeta = document.getElementById('m2-target-meta');
const m2RoundIndicator = document.getElementById('m2-round-indicator');
const m2PlayerMask = document.getElementById('m2-player-mask');
const m2VinylIcon = document.getElementById('m2-vinyl-icon');
const m2SoundBars = document.getElementById('m2-sound-bars');
const m2MaskStatus = document.getElementById('m2-mask-status');
const m2LocalVideo = document.getElementById('m2-local-video');
const m2VideoFrame = document.getElementById('m2-video-frame');
const m2BtnConfirm = document.getElementById('m2-btn-confirm');
const m2BtnNext = document.getElementById('m2-btn-next');
const m2FeedbackBanner = document.getElementById('m2-feedback-banner');

// M3 DOM
const m3RoundIndicator = document.getElementById('m3-round-indicator');
const m3SceneImg = document.getElementById('m3-scene-img');
const m3TagsRow = document.getElementById('m3-tags-row');
const m3Input = document.getElementById('m3-input');
const m3Autocomplete = document.getElementById('m3-autocomplete');
const m3FeedbackBox = document.getElementById('m3-feedback-box');
const m3AnswerBox = document.getElementById('m3-answer-box');
const m3AnsPoster = document.getElementById('m3-ans-poster');
const m3AnsTitle = document.getElementById('m3-ans-title');
const m3AnsMeta = document.getElementById('m3-ans-meta');
const m3AnsSyns = document.getElementById('m3-ans-syns');

/* ==============================================================
   AUDIO STOPPING & RESET (ANTI-LEAK)
   ============================================================== */
function stopAllMedia() {
  if (localVideoPlayer) {
    localVideoPlayer.pause();
    localVideoPlayer.currentTime = 0;
    localVideoPlayer.src = '';
    localVideoPlayer.removeAttribute('src');
    localVideoPlayer.load();
  }
  if (videoFrame) {
    videoFrame.src = 'about:blank';
    videoFrame.style.display = 'none';
  }
  if (m2LocalVideo) {
    m2LocalVideo.pause();
    m2LocalVideo.currentTime = 0;
    m2LocalVideo.src = '';
    m2LocalVideo.removeAttribute('src');
    m2LocalVideo.load();
  }
  if (m2VideoFrame) {
    m2VideoFrame.src = 'about:blank';
    m2VideoFrame.style.display = 'none';
  }
  m1IsPlaying = false;
  setPlayUI(false);
}

/* ==============================================================
   ETAPA 2: AUDIO MANAGER (SOUNDGROUPS: BGM & SFX)
   ============================================================== */
const AudioManager = {
  bgmVolume: 0.8,
  sfxVolume: 0.8,
  isMuted: false,
  _lastHoverTime: 0,
  _hoverDebounceMs: 35,

  init() {
    const savedBgm = localStorage.getItem('AMQ_BGM_VOL');
    if (savedBgm !== null) this.bgmVolume = parseFloat(savedBgm);
    const savedSfx = localStorage.getItem('AMQ_SFX_VOL');
    if (savedSfx !== null) this.sfxVolume = parseFloat(savedSfx);
    const savedMute = localStorage.getItem('AMQ_MUTED');
    if (savedMute !== null) this.isMuted = (savedMute === 'true');
    this.updateUI();
    this.applyVolumes();
  },

  setBgmVolume(val) {
    this.bgmVolume = parseFloat(val);
    localStorage.setItem('AMQ_BGM_VOL', this.bgmVolume);
    this.updateUI();
    this.applyVolumes();
  },

  setSfxVolume(val) {
    this.sfxVolume = parseFloat(val);
    localStorage.setItem('AMQ_SFX_VOL', this.sfxVolume);
    this.updateUI();
    this.playSfx('click');
  },

  toggleMute() {
    this.isMuted = !this.isMuted;
    localStorage.setItem('AMQ_MUTED', this.isMuted);
    this.updateUI();
    this.applyVolumes();
    this.playSfx('click');
    return this.isMuted;
  },

  updateUI() {
    const bgmVal = document.getElementById('bgm-vol-text');
    const sfxVal = document.getElementById('sfx-vol-text');
    const bgmSlider = document.getElementById('bgm-vol-slider');
    const sfxSlider = document.getElementById('sfx-vol-slider');
    const muteBtn = document.getElementById('btn-mute-toggle');
    const muteIcon = document.getElementById('mute-btn-icon');
    const muteText = document.getElementById('mute-btn-text');
    const audioIcon = document.getElementById('audio-settings-icon');

    if (bgmVal) bgmVal.textContent = `${Math.round(this.bgmVolume * 100)}%`;
    if (sfxVal) sfxVal.textContent = `${Math.round(this.sfxVolume * 100)}%`;
    if (bgmSlider) bgmSlider.value = this.bgmVolume;
    if (sfxSlider) sfxSlider.value = this.sfxVolume;

    if (muteBtn) muteBtn.classList.toggle('muted', this.isMuted);
    if (muteIcon) muteIcon.textContent = this.isMuted ? '🔇' : '🔊';
    if (muteText) muteText.textContent = this.isMuted ? 'Desmutar Jogo' : 'Mutar Todo o Jogo';
    if (audioIcon) audioIcon.textContent = this.isMuted ? '🔇' : '🔊';
  },

  applyVolumes() {
    masterVolume = this.bgmVolume;
    isMuted = this.isMuted;
    const vol = this.isMuted ? 0 : this.bgmVolume;
    if (typeof localVideoPlayer !== 'undefined' && localVideoPlayer) localVideoPlayer.volume = vol;
    if (typeof m2LocalVideo !== 'undefined' && m2LocalVideo) m2LocalVideo.volume = vol;
  },

  playSfx(type, extra) {
    if (this.isMuted || this.sfxVolume <= 0.001) return;
    try {
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      if (!AudioCtx) return;
      if (!window._sfxCtx) window._sfxCtx = new AudioCtx();
      const ctx = window._sfxCtx;
      if (ctx.state === 'suspended') ctx.resume();

      const v = this.sfxVolume * 0.28;
      const t = ctx.currentTime;

      if (type === 'hover') {
        const now = Date.now();
        if (now - this._lastHoverTime < this._hoverDebounceMs) return;
        this._lastHoverTime = now;
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(1350, t);
        osc.frequency.exponentialRampToValueAtTime(1950, t + 0.035);
        gain.gain.setValueAtTime(v * 0.22, t);
        gain.gain.exponentialRampToValueAtTime(0.0001, t + 0.038);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start(t);
        osc.stop(t + 0.04);
        return;
      } else if (type === 'typing') {
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = 'triangle';
        const freq = 1250 + Math.random() * 350;
        osc.frequency.setValueAtTime(freq, t);
        osc.frequency.exponentialRampToValueAtTime(300, t + 0.02);
        gain.gain.setValueAtTime(v * 0.35, t);
        gain.gain.exponentialRampToValueAtTime(0.0001, t + 0.022);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start(t);
        osc.stop(t + 0.025);
        return;
      } else if (type === 'click') {
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(850, t);
        osc.frequency.exponentialRampToValueAtTime(220, t + 0.035);
        gain.gain.setValueAtTime(v * 0.5, t);
        gain.gain.exponentialRampToValueAtTime(0.0001, t + 0.04);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start(t);
        osc.stop(t + 0.042);
      } else if (type === 'tab') {
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(320, t);
        osc.frequency.exponentialRampToValueAtTime(620, t + 0.07);
        gain.gain.setValueAtTime(v * 0.35, t);
        gain.gain.exponentialRampToValueAtTime(0.0001, t + 0.07);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start(t);
        osc.stop(t + 0.08);
      } else if (type === 'hint') {
        [520, 740, 1040].forEach((f, i) => {
          const osc = ctx.createOscillator();
          const gain = ctx.createGain();
          osc.type = 'sine';
          osc.frequency.setValueAtTime(f, t + i * 0.06);
          gain.gain.setValueAtTime(v * 0.4, t + i * 0.06);
          gain.gain.exponentialRampToValueAtTime(0.0001, t + i * 0.06 + 0.16);
          osc.connect(gain);
          gain.connect(ctx.destination);
          osc.start(t + i * 0.06);
          osc.stop(t + i * 0.06 + 0.18);
        });
      } else if (type === 'correct') {
        [523.25, 659.25, 783.99, 1046.50, 1318.51].forEach((f, i) => {
          const osc = ctx.createOscillator();
          const gain = ctx.createGain();
          osc.type = (i >= 3) ? 'sine' : 'triangle';
          osc.frequency.setValueAtTime(f, t + i * 0.05);
          gain.gain.setValueAtTime(v * (0.45 + i * 0.05), t + i * 0.05);
          gain.gain.exponentialRampToValueAtTime(0.0001, t + i * 0.05 + 0.26);
          osc.connect(gain);
          gain.connect(ctx.destination);
          osc.start(t + i * 0.05);
          osc.stop(t + i * 0.05 + 0.28);
        });
      } else if (type === 'combo' || type === 'streak') {
        const streakCount = (typeof extra === 'number') ? extra : 3;
        const notes = streakCount >= 10
          ? [392, 523.25, 659.25, 783.99, 1046.50, 1318.51, 1567.98, 2093.00]
          : (streakCount >= 5
            ? [440, 523.25, 659.25, 783.99, 880, 1046.50]
            : [440, 554.37, 659.25, 880, 1108.73]);
        const step = 0.04;
        notes.forEach((f, i) => {
          const osc = ctx.createOscillator();
          const gain = ctx.createGain();
          osc.type = (i >= notes.length - 2) ? 'sine' : 'triangle';
          osc.frequency.setValueAtTime(f, t + i * step);
          gain.gain.setValueAtTime(v * (0.5 + (i / notes.length) * 0.25), t + i * step);
          gain.gain.exponentialRampToValueAtTime(0.0001, t + i * step + 0.3);
          osc.connect(gain);
          gain.connect(ctx.destination);
          osc.start(t + i * step);
          osc.stop(t + i * step + 0.32);
        });
      } else if (type === 'wrong') {
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(140, t);
        osc.frequency.exponentialRampToValueAtTime(70, t + 0.22);
        gain.gain.setValueAtTime(v * 0.45, t);
        gain.gain.exponentialRampToValueAtTime(0.0001, t + 0.24);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start(t);
        osc.stop(t + 0.25);
      } else if (type === 'alert') {
        [580, 780].forEach((f, i) => {
          const osc = ctx.createOscillator();
          const gain = ctx.createGain();
          osc.type = 'triangle';
          osc.frequency.setValueAtTime(f, t + i * 0.08);
          gain.gain.setValueAtTime(v * 0.65, t + i * 0.08);
          gain.gain.exponentialRampToValueAtTime(0.0001, t + i * 0.08 + 0.07);
          osc.connect(gain);
          gain.connect(ctx.destination);
          osc.start(t + i * 0.08);
          osc.stop(t + i * 0.08 + 0.08);
        });
      }
    } catch (e) {}
  },

  playCountdownBeep(secondsLeft) {
    if (this.isMuted || this.sfxVolume <= 0.001) return;
    try {
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      if (!AudioCtx) return;
      if (!window._sfxCtx) window._sfxCtx = new AudioCtx();
      const ctx = window._sfxCtx;
      if (ctx.state === 'suspended') ctx.resume();

      const v = this.sfxVolume * 0.45;
      const t = ctx.currentTime;
      // Frequência sobe com a tensão (5s: 720Hz -> 1s: 1180Hz)
      const freqMap = { 5: 720, 4: 800, 3: 900, 2: 1020, 1: 1180 };
      const f = freqMap[secondsLeft] || 850;

      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(f, t);
      gain.gain.setValueAtTime(v, t);
      gain.gain.exponentialRampToValueAtTime(0.0001, t + 0.12);
      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.start(t);
      osc.stop(t + 0.13);
    } catch (e) {}
  }
};

function setMasterVolume(val) { AudioManager.setBgmVolume(val); }
function toggleMute() { AudioManager.toggleMute(); }
function toggleAudioSettingsPopover() {
  const pop = document.getElementById('audio-settings-popover');
  if (pop) pop.classList.toggle('active');
  AudioManager.playSfx('click');
}

/* ==============================================================
   ETAPA 2: AUDIO SPECTRUM VISUALIZER ENGINE (CANVAS 60FPS)
   ============================================================== */
const VisualizerEngine = {
  canvas1: null,
  canvas2: null,
  ctx1: null,
  ctx2: null,
  audioCtx: null,
  analyser: null,
  source1: null,
  source2: null,
  freqData: null,
  animId: null,
  particles: [],
  phase: 0,

  init() {
    this.canvas1 = document.getElementById('m1-spectrum-canvas');
    this.canvas2 = document.getElementById('m2-spectrum-canvas');
    if (this.canvas1) this.ctx1 = this.canvas1.getContext('2d');
    if (this.canvas2) this.ctx2 = this.canvas2.getContext('2d');

    this.particles = Array.from({ length: 28 }, () => ({
      x: Math.random(),
      y: Math.random(),
      vx: (Math.random() - 0.5) * 0.0015,
      vy: -(Math.random() * 0.003 + 0.001),
      radius: Math.random() * 2 + 1,
      alpha: Math.random() * 0.7 + 0.2,
      color: Math.random() > 0.5 ? '#a855f7' : (Math.random() > 0.5 ? '#ec4899' : '#38bdf8')
    }));

    this.resize();
    window.addEventListener('resize', () => this.resize());
    this.startLoop();
  },

  setupAudioContext() {
    if (this.analyser) return;
    try {
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      if (!AudioCtx) return;
      if (!window._sfxCtx) window._sfxCtx = new AudioCtx();
      this.audioCtx = window._sfxCtx;
      if (this.audioCtx.state === 'suspended') {
        this.audioCtx.resume();
      }
      this.analyser = this.audioCtx.createAnalyser();
      this.analyser.fftSize = 64;
      this.analyser.smoothingTimeConstant = 0.82;
      this.freqData = new Uint8Array(this.analyser.frequencyBinCount);

      if (!this.source1 && localVideoPlayer) {
        this.source1 = this.audioCtx.createMediaElementSource(localVideoPlayer);
        this.source1.connect(this.analyser);
      }
      if (!this.source2 && m2LocalVideo) {
        this.source2 = this.audioCtx.createMediaElementSource(m2LocalVideo);
        this.source2.connect(this.analyser);
      }
      this.analyser.connect(this.audioCtx.destination);
    } catch (e) {}
  },

  resize() {
    [this.canvas1, this.canvas2].forEach(c => {
      if (!c) return;
      const rect = c.getBoundingClientRect();
      const dpr = window.devicePixelRatio || 1;
      c.width = (rect.width || 480) * dpr;
      c.height = (rect.height || 210) * dpr;
    });
  },

  startLoop() {
    const render = () => {
      this.renderFrame();
      this.animId = requestAnimationFrame(render);
    };
    render();
  },

  renderFrame() {
    this.phase += 0.04;
    const isM1Playing = m1IsPlaying && activeGameMode === 'mode1';
    const isM2Playing = (m2PlayingIndex !== -1 || m2Answered) && activeGameMode === 'mode2';
    const isPlaying = isM1Playing || isM2Playing;

    let hasRealData = false;
    if (this.analyser && isPlaying && this.freqData) {
      try {
        this.analyser.getByteFrequencyData(this.freqData);
        const sum = this.freqData.reduce((a, b) => a + b, 0);
        if (sum > 10) hasRealData = true;
      } catch (e) {}
    }

    if (activeGameMode === 'mode1' && this.ctx1 && this.canvas1) {
      this.drawOnCanvas(this.ctx1, this.canvas1, isM1Playing, hasRealData);
    } else if (activeGameMode === 'mode2' && this.ctx2 && this.canvas2) {
      this.drawOnCanvas(this.ctx2, this.canvas2, isM2Playing, hasRealData);
    }
  },

  drawOnCanvas(ctx, canvas, isPlaying, hasRealData) {
    const w = canvas.width;
    const h = canvas.height;
    ctx.clearRect(0, 0, w, h);

    const barCount = 26;
    const barWidth = (w / barCount) * 0.65;
    const gap = (w / barCount) * 0.35;
    const baseY = h * 0.88;

    for (let i = 0; i < barCount; i++) {
      let energy = 0;
      if (hasRealData && this.freqData) {
        const bin = Math.floor((i / barCount) * this.freqData.length);
        energy = this.freqData[bin] / 255;
      } else if (isPlaying) {
        const wave1 = Math.sin(this.phase * 2.2 + i * 0.38) * 0.35 + 0.35;
        const wave2 = Math.cos(this.phase * 3.4 + i * 0.22) * 0.25;
        energy = Math.max(0.1, wave1 + wave2);
      } else {
        energy = Math.sin(this.phase + i * 0.2) * 0.08 + 0.1;
      }

      const barHeight = energy * (h * 0.62);
      const x = i * (barWidth + gap) + gap * 0.5;
      const y = baseY - barHeight;

      const grad = ctx.createLinearGradient(0, baseY, 0, y);
      grad.addColorStop(0, 'rgba(99, 102, 241, 0.12)');
      grad.addColorStop(0.5, 'rgba(236, 72, 153, 0.55)');
      grad.addColorStop(1, 'rgba(56, 189, 248, 0.9)');

      ctx.fillStyle = grad;
      ctx.shadowColor = 'rgba(236, 72, 153, 0.5)';
      ctx.shadowBlur = isPlaying ? 10 : 2;

      ctx.beginPath();
      const r = Math.min(barWidth / 2, 4);
      if (ctx.roundRect) {
        ctx.roundRect(x, y, barWidth, barHeight, [r, r, 0, 0]);
      } else {
        ctx.rect(x, y, barWidth, barHeight);
      }
      ctx.fill();
    }
    ctx.shadowBlur = 0;

    // Glowing Wave Ribbon Contour
    ctx.beginPath();
    ctx.strokeStyle = isPlaying ? 'rgba(56, 189, 248, 0.75)' : 'rgba(99, 102, 241, 0.3)';
    ctx.lineWidth = isPlaying ? 2.5 : 1.5;
    ctx.shadowColor = 'rgba(56, 189, 248, 0.8)';
    ctx.shadowBlur = isPlaying ? 8 : 0;

    for (let x = 0; x <= w; x += 10) {
      const normX = x / w;
      let waveY;
      if (isPlaying) {
        const amp = h * 0.12;
        waveY = baseY - (h * 0.2) + Math.sin(normX * 12 + this.phase * 2.5) * amp * Math.sin(normX * Math.PI);
      } else {
        waveY = baseY - (h * 0.08) + Math.sin(normX * 6 + this.phase) * (h * 0.03);
      }
      if (x === 0) ctx.moveTo(x, waveY);
      else ctx.lineTo(x, waveY);
    }
    ctx.stroke();
    ctx.shadowBlur = 0;

    // Floating Cyber Particles
    if (isPlaying) {
      this.particles.forEach(p => {
        p.x += p.vx;
        p.y += p.vy;
        if (p.y < 0) { p.y = 1; p.x = Math.random(); }
        if (p.x < 0) p.x = 1;
        if (p.x > 1) p.x = 0;

        ctx.beginPath();
        ctx.arc(p.x * w, p.y * h, p.radius, 0, Math.PI * 2);
        ctx.fillStyle = p.color;
        ctx.globalAlpha = p.alpha;
        ctx.fill();
      });
      ctx.globalAlpha = 1.0;
    }
  }
};

/* ==============================================================
   ETAPA 2: GAMER CONFETTI & CELEBRATION ENGINE
   ============================================================== */
const ConfettiEngine = {
  canvas: null,
  ctx: null,
  particles: [],
  animating: false,

  init() {
    this.canvas = document.getElementById('gamer-confetti-canvas');
    if (this.canvas) this.ctx = this.canvas.getContext('2d');
    this.resize();
    window.addEventListener('resize', () => this.resize());
  },

  resize() {
    if (!this.canvas) return;
    this.canvas.width = window.innerWidth;
    this.canvas.height = window.innerHeight;
  },

  burst(originX = window.innerWidth / 2, originY = window.innerHeight * 0.4, count = 40) {
    if (!this.canvas || !this.ctx) return;
    this.resize();
    const colors = ['#6366f1', '#ec4899', '#38bdf8', '#10b981', '#fbbf24', '#f43f5e'];

    for (let i = 0; i < count; i++) {
      const angle = (Math.random() * Math.PI * 2);
      const speed = Math.random() * 8 + 3;
      this.particles.push({
        x: originX,
        y: originY,
        vx: Math.cos(angle) * speed,
        vy: Math.sin(angle) * speed - 3,
        size: Math.random() * 6 + 4,
        color: colors[Math.floor(Math.random() * colors.length)],
        rotation: Math.random() * 360,
        rotSpeed: (Math.random() - 0.5) * 12,
        alpha: 1.0,
        decay: Math.random() * 0.015 + 0.015
      });
    }

    if (!this.animating) {
      this.animating = true;
      this.loop();
    }
  },

  loop() {
    if (!this.ctx || this.particles.length === 0) {
      this.animating = false;
      if (this.ctx) this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
      return;
    }

    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

    for (let i = this.particles.length - 1; i >= 0; i--) {
      const p = this.particles[i];
      p.x += p.vx;
      p.y += p.vy;
      p.vy += 0.22;
      p.rotation += p.rotSpeed;
      p.alpha -= p.decay;

      if (p.alpha <= 0) {
        this.particles.splice(i, 1);
        continue;
      }

      this.ctx.save();
      this.ctx.translate(p.x, p.y);
      this.ctx.rotate((p.rotation * Math.PI) / 180);
      this.ctx.globalAlpha = p.alpha;
      this.ctx.fillStyle = p.color;
      this.ctx.fillRect(-p.size / 2, -p.size / 2, p.size, p.size * 1.3);
      this.ctx.restore();
    }

    requestAnimationFrame(() => this.loop());
  }
};

/* ==============================================================
   FLOATING ARCADE MULTIPLIERS & GAME JUICE ENGINE
   ============================================================== */
const FloatingArcade = {
  container: null,

  init() {
    this.container = document.getElementById('floating-arcade-container');
  },

  spawn({ points = 0, isCorrect = true, streak = 0, speedBonus = 0, comboBonus = 0, text = '' } = {}) {
    if (!this.container) {
      this.container = document.getElementById('floating-arcade-container');
    }
    if (!this.container) return;

    const popup = document.createElement('div');
    popup.className = 'arcade-popup';

    if (isCorrect) {
      let badges = '';
      if (streak >= 10) {
        badges += `<span class="arcade-badge-chip streak hyper">🌌 HIPER COMBO x${streak}</span>`;
      } else if (streak >= 5) {
        badges += `<span class="arcade-badge-chip streak super">⚡ COMBO x${streak}</span>`;
      } else if (streak >= 2) {
        badges += `<span class="arcade-badge-chip streak">🔥 COMBO x${streak}</span>`;
      }
      if (speedBonus > 0) {
        badges += `<span class="arcade-badge-chip speed">⚡ +${speedBonus} RAPIDEZ</span>`;
      }
      popup.innerHTML = `
        <div class="arcade-pts-main correct">+${points}</div>
        ${badges ? `<div class="arcade-badge-row">${badges}</div>` : ''}
      `;
    } else {
      popup.innerHTML = `
        <div class="arcade-pts-main wrong">${text || '❌ ERROU'}</div>
        <div class="arcade-badge-row">
          <span class="arcade-badge-chip wrong-badge">💔 COMBO RESET</span>
        </div>
      `;
    }

    this.container.appendChild(popup);
    setTimeout(() => {
      try { popup.remove(); } catch(e) {}
    }, 1300);
  }
};

/* ==============================================================
   ETAPA 2: COMBO FIRE & STREAK INDICATOR
   ============================================================== */
function updateStreakBadge(streak) {
  if (!kpiStreak) return;
  if (streak >= 10) {
    kpiStreak.className = 'score-val combo-hyper-fire';
    kpiStreak.textContent = `🌌 x${streak}`;
  } else if (streak >= 5) {
    kpiStreak.className = 'score-val combo-super-fire';
    kpiStreak.textContent = `⚡ x${streak}`;
  } else if (streak >= 2) {
    kpiStreak.className = 'score-val combo-fire';
    kpiStreak.textContent = `🔥 x${streak}`;
  } else if (streak === 1) {
    kpiStreak.className = 'score-val';
    kpiStreak.textContent = `x1`;
  } else {
    kpiStreak.className = 'score-val';
    kpiStreak.textContent = '0';
  }
}

/* ==============================================================
   MODE SWITCHING & UNIFIED KPI STATE
   ============================================================== */
function updateGlobalKPIs() {
  if (window.MultiplayerEngine && MultiplayerEngine.isMatchActive) {
    const me = MultiplayerEngine.getMyPlayer();
    if (me) {
      kpiScore.textContent = me.score;
      kpiCorrect.textContent = me.correct || 0;
    }
    kpiProgress.textContent = `${MultiplayerEngine.currentRoundIdx + 1} / ${MultiplayerEngine.activeSettings.rounds}`;
    updateStreakBadge(MultiplayerEngine.myStreak || 0);
  } else {
    if (activeGameMode === 'mode1') {
      kpiScore.textContent = m1Score;
      kpiCorrect.textContent = m1CorrectCount;
      updateStreakBadge(m1Streak);
      kpiProgress.textContent = `${m1PlaylistIndex + 1} / ${m1Playlist.length}`;
    } else if (activeGameMode === 'mode2') {
      kpiScore.textContent = m2Score;
      kpiCorrect.textContent = m2CorrectCount;
      updateStreakBadge(m2Streak);
      kpiProgress.textContent = `${m2RoundsPlayed} / ${isChallengeActive ? challengeRounds : ALL_SONGS.length}`;
    } else if (activeGameMode === 'mode3') {
      kpiScore.textContent = m3Score;
      kpiCorrect.textContent = m3CorrectCount;
      updateStreakBadge(m3Streak);
      kpiProgress.textContent = `${m3RoundsPlayed} / ${isChallengeActive ? challengeRounds : ALL_SCENES.length}`;
    } else if (activeGameMode === 'mode4') {
      kpiScore.textContent = '0';
      kpiCorrect.textContent = '0';
      updateStreakBadge(0);
      kpiProgress.textContent = 'Salas & Placar';
    }
  }
}

function showMatchActiveAlert(msg) {
  const modal = document.getElementById('match-active-alert-modal');
  const desc = document.getElementById('match-active-alert-desc');
  if (desc && msg) desc.textContent = msg;
  if (modal) modal.style.display = 'flex';
  if (window.AudioManager) AudioManager.playSfx('alert');
}

function closeMatchActiveAlert(e) {
  const modal = document.getElementById('match-active-alert-modal');
  if (modal) modal.style.display = 'none';
  if (window.AudioManager) AudioManager.playSfx('click');
}

function leaveRoomFromAlert() {
  closeMatchActiveAlert();
  if (window.MultiplayerEngine) MultiplayerEngine.confirmLeaveRoom();
}

function switchGameMode(mode, isInternal = false) {
  if (!isInternal && window.MultiplayerEngine) {
    if (MultiplayerEngine.isMatchActive) {
      showMatchActiveAlert('⚠️ Você está em uma partida ativa! Para trocar de modo, conclua as rodadas ou clique em Sair da Sala.');
      return;
    }
    if (MultiplayerEngine.roomCode && mode !== 'mode4' && mode !== 'mode5') {
      showMatchActiveAlert('⚠️ Você já está na Sala #' + MultiplayerEngine.roomCode + '! Saia da sala antes de escolher outro modo.');
      return;
    } else if (activeGameMode === 'mode4' && mode === 'mode4') {
      // Já está no modo de salas dentro de um lobby, não reinicializa
      return;
    }
  }

  stopAllMedia();
  AudioManager.playSfx('tab');
  activeGameMode = mode;
  ['mode1', 'mode2', 'mode3', 'mode4', 'mode5'].forEach(m => {
    const viewEl = document.getElementById(`${m}-view`);
    if (viewEl) viewEl.style.display = (m === mode) ? 'block' : 'none';
    const tabEl = document.getElementById(`tab-${m}`);
    if (tabEl) tabEl.classList.toggle('active', m === mode);
  });

  // Ranking lateral ao vivo só deve aparecer durante partida multiplayer ativa
  const liveSidebar = document.getElementById('mp-live-sidebar');
  if (liveSidebar) {
    liveSidebar.style.display = (window.MultiplayerEngine && MultiplayerEngine.isMatchActive) ? 'flex' : 'none';
  }

  // O Scoreboard de KPIs pertence exclusivamente dentro de cada modo solo ativo
  const sb = document.getElementById('main-scoreboard');
  if (sb) {
    if (mode === 'mode1' || mode === 'mode2' || mode === 'mode3') {
      const slot = document.getElementById(`${mode}-scoreboard-slot`);
      if (slot) {
        slot.appendChild(sb);
        sb.style.display = 'grid';
      }
    } else {
      sb.style.display = 'none';
    }
  }

  if (window.MultiplayerEngine && MultiplayerEngine.isMatchActive) {
    updateGlobalKPIs();
    return;
  }

  if (mode === 'mode1') {
    updateGlobalKPIs();
  } else if (mode === 'mode2') {
    updateGlobalKPIs();
    if (m2Options.length === 0) {
      m2StartGame();
    }
  } else if (mode === 'mode3') {
    updateGlobalKPIs();
    if (m3UnplayedQueue.length === 0) {
      m3StartGame();
    }
  } else if (mode === 'mode4') {
    updateGlobalKPIs();
  } else if (mode === 'mode5') {
    updateGlobalKPIs();
    const lbPanel = document.getElementById('mp-leaderboard-panel');
    if (lbPanel) lbPanel.style.display = 'block';
    renderLeaderboardTable('all');
    updateSaveScoreKPIs();
    if (window.CloudLeaderboard && CloudLeaderboard.getFirebaseUrl()) {
      CloudLeaderboard.fetchScores().then(() => renderLeaderboardTable('all'));
    }
  }
}

/* ==============================================================
   AUTOCOMPLETE SYSTEM (500+ ANIMES COM DROPDOWN INTERATIVO)
   ============================================================== */
function setupAutocomplete(inputEl, dropdownEl, onSelectSubmit) {
  let activeIndex = -1;

  function closeDropdown() {
    dropdownEl.style.display = 'none';
    dropdownEl.innerHTML = '';
    activeIndex = -1;
  }

  inputEl.addEventListener('input', () => {
    AudioManager.playSfx('typing');
    const val = inputEl.value.trim();
    if (val.length < 2) {
      closeDropdown();
      return;
    }

    const normVal = normalizeString(val);
    const matches = [];

    for (const title of ANIME_AUTOCOMPLETE) {
      const normTitle = normalizeString(title);
      if (normTitle.includes(normVal)) {
        matches.push(title);
        if (matches.length >= 8) break;
      }
    }

    if (matches.length === 0) {
      closeDropdown();
      return;
    }

    dropdownEl.innerHTML = '';
    matches.forEach((title, idx) => {
      const item = document.createElement('div');
      item.className = 'autocomplete-item';
      
      // Highlight matching characters
      const regex = new RegExp(`(${val.replace(/[.*+?^${}()|[\\]\\\\]/g, '\\\\$&')})`, 'gi');
      const highlighted = title.replace(regex, '<strong>$1</strong>');
      item.innerHTML = `<span>${highlighted}</span>`;

      item.addEventListener('mousedown', (e) => {
        e.preventDefault();
        inputEl.value = title;
        closeDropdown();
        inputEl.focus();
        if (onSelectSubmit) onSelectSubmit();
      });

      dropdownEl.appendChild(item);
    });

    dropdownEl.style.display = 'block';
    activeIndex = -1;
  });

  inputEl.addEventListener('keydown', (e) => {
    // Barulhinho sutil de digitar (teclado mecânico)
    if (e.key.length === 1 || e.key === 'Backspace' || e.key === 'Delete') {
      playKeyClick();
    }

    const items = dropdownEl.querySelectorAll('.autocomplete-item');
    const isDropdownOpen = dropdownEl.style.display === 'block' && items.length > 0;

    // TAB: Preenche automaticamente a 1ª opção mais próxima e já envia o palpite instantaneamente!
    if (e.key === 'Tab') {
      e.preventDefault();
      if (isDropdownOpen) {
        const chosen = (activeIndex >= 0 && items[activeIndex]) ? items[activeIndex] : items[0];
        inputEl.value = chosen.textContent.trim();
        closeDropdown();
        if (onSelectSubmit) onSelectSubmit();
        return;
      } else if (inputEl.value.trim().length > 0) {
        if (onSelectSubmit) onSelectSubmit();
        return;
      }
    }

    if (isDropdownOpen) {
      if (e.key === 'ArrowDown') {
        e.preventDefault();
        activeIndex = (activeIndex + 1) % items.length;
        items.forEach((it, i) => it.classList.toggle('active', i === activeIndex));
        items[activeIndex].scrollIntoView({ block: 'nearest' });
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        activeIndex = (activeIndex - 1 + items.length) % items.length;
        items.forEach((it, i) => it.classList.toggle('active', i === activeIndex));
        items[activeIndex].scrollIntoView({ block: 'nearest' });
      } else if (e.key === 'Enter') {
        e.preventDefault();
        const chosen = (activeIndex >= 0 && items[activeIndex]) ? items[activeIndex] : items[0];
        inputEl.value = chosen.textContent.trim();
        closeDropdown();
        if (onSelectSubmit) onSelectSubmit();
        return;
      } else if (e.key === 'Escape') {
        closeDropdown();
      }
    }
    
    if (e.key === 'Enter' && (!dropdownEl.style.display || dropdownEl.style.display === 'none')) {
      if (onSelectSubmit) onSelectSubmit();
    }
  });

  document.addEventListener('click', (e) => {
    if (!inputEl.contains(e.target) && !dropdownEl.contains(e.target)) {
      closeDropdown();
    }
  });
}

/* ==============================================================
   FUZZY MATCHING RIGOROSO (SEM FALSOS POSITIVOS DE 1 LETRA)
   ============================================================== */
function normalizeString(str) {
  if (!str) return '';
  return str.toLowerCase()
    .normalize("NFD").replace(/[\\u0300-\\u036f]/g, "")
    .replace(/[^a-z0-9]/g, " ")
    .replace(/\\s+/g, " ")
    .trim();
}

function levenshtein(a, b) {
  const matrix = [];
  for (let i = 0; i <= b.length; i++) matrix[i] = [i];
  for (let j = 0; j <= a.length; j++) matrix[0][j] = j;
  for (let i = 1; i <= b.length; i++) {
    for (let j = 1; j <= a.length; j++) {
      if (b.charAt(i - 1) === a.charAt(j - 1)) {
        matrix[i][j] = matrix[i - 1][j - 1];
      } else {
        matrix[i][j] = Math.min(
          matrix[i - 1][j - 1] + 1,
          matrix[i][j - 1] + 1,
          matrix[i - 1][j] + 1
        );
      }
    }
  }
  return matrix[b.length][a.length];
}

// Web Audio API Synthesizer (SFX Sensitivo Instantâneo)
let lastKeyClickTime = 0;
function playKeyClick() {
  const now = performance.now();
  if (now - lastKeyClickTime < 35) return;
  lastKeyClickTime = now;
  try {
    const AudioContext = window.AudioContext || window.webkitAudioContext;
    if (!AudioContext) return;
    if (!window._sfxCtx) window._sfxCtx = new AudioContext();
    const ctx = window._sfxCtx;
    if (ctx.state === 'suspended') ctx.resume();

    const vol = (typeof masterVolume !== 'undefined' ? masterVolume : 0.8) * 0.12;
    if (typeof isMuted !== 'undefined' && isMuted) return;
    if (vol <= 0.001) return;

    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    const pitch = 1500 + (Math.random() * 400 - 200);
    osc.type = 'triangle';
    osc.frequency.setValueAtTime(pitch, ctx.currentTime);
    osc.frequency.exponentialRampToValueAtTime(300, ctx.currentTime + 0.022);

    gain.gain.setValueAtTime(vol, ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + 0.022);

    osc.connect(gain);
    gain.connect(ctx.destination);
    osc.start(ctx.currentTime);
    osc.stop(ctx.currentTime + 0.025);
  } catch (e) {}
}

const ICON_PLAY = '<img src="icons/play-button.png" class="btn-icon-img" alt="Play" />';
const ICON_PAUSE = '<img src="icons/pause.png" class="btn-icon-img" alt="Pause" />';
const ICON_PLAY_SM = '<img src="icons/play-button.png" class="btn-icon-img btn-icon-sm" alt="Play" />';

function formatDifficulty(d) {
  const n = normalizeString(d || '');
  if (n.includes('facil')) return '⭐ Fácil';
  if (n.includes('medio') || n.includes('media')) return '⭐⭐ Médio';
  if (n.includes('dificil')) return '⭐⭐⭐ Difícil';
  return '⭐ Fácil';
}

function getDifficultyRank(item) {
  const norm = normalizeString(item.diff || item.hint || '');
  if (norm.includes('facil')) return 1;
  if (norm.includes('medio') || norm.includes('media')) return 2;
  return 3;
}

function buildProgressiveQueue(items) {
  const easy = items.filter(it => getDifficultyRank(it) === 1);
  const med = items.filter(it => getDifficultyRank(it) === 2);
  const hard = items.filter(it => getDifficultyRank(it) === 3);

  // Embaralhar aleatoriamente cada grupo individual
  easy.sort(() => Math.random() - 0.5);
  med.sort(() => Math.random() - 0.5);
  hard.sort(() => Math.random() - 0.5);

  return [...easy, ...med, ...hard];
}

function playSfx(type) {
  AudioManager.playSfx(type);
}

function getAcceptedVariants(title, synonyms = []) {
  const set = new Set();
  function add(s) {
    if (!s) return;
    const n = normalizeString(s);
    if (n && n.length >= 2) set.add(n);
  }
  if (!title) return [];
  add(title);

  // 1. Text in parentheses: "Attack on Titan (Shingeki no Kyojin)" -> "Shingeki no Kyojin"
  const parens = title.match(/\\((.*?)\\)/g);
  if (parens) {
    parens.forEach(p => add(p.replace(/[()]/g, '')));
  }

  // 2. Text without parentheses: "Attack on Titan (Shingeki no Kyojin)" -> "Attack on Titan"
  const noParen = title.replace(/\\(.*?\\)/g, '').trim();
  add(noParen);

  // 3. Subtitles before separators: ":", " - ", " – ", ";", " / "
  // "Bleach: Thousand-Year Blood War" -> "Bleach"
  const seps = [':', ' - ', ' – ', ' — ', ';', ' / '];
  seps.forEach(sep => {
    if (noParen.includes(sep)) {
      const pre = noParen.split(sep)[0].trim();
      if (pre.length >= 3) add(pre);
    }
  });

  // 4. Strip season / part / movie / edition suffixes
  const seasonPatterns = [
    /\\bseason\\s*\\d+\\b.*/gi,
    /\\b\\d+(st|nd|rd|th)\\s*season\\b.*/gi,
    /\\bfinal\\s*season(\\s*pt\\s*\\d+)?\\b.*/gi,
    /\\bpart\\s*\\d+\\b.*/gi,
    /\\bpt\\s*\\d+\\b.*/gi,
    /\\bthe\\s*animation\\b.*/gi,
    /\\bthe\\s*movie\\b.*/gi,
    /\\bmovie\\b.*/gi,
    /\\b(ii|iii|iv|v|vi)\\b.*/gi,
    /\\b(born|hero|new)\\b.*/gi,
    /\\b(shou|ten|ketsu)\\b.*/gi,
    /\\baragoto\\b.*/gi,
    /\\b2nd\\b.*/gi,
    /\\b3rd\\b.*/gi,
    /\\b\\d+$/g
  ];
  let baseClean = noParen;
  seasonPatterns.forEach(pat => {
    baseClean = baseClean.replace(pat, '').trim();
  });
  if (baseClean.length >= 3) add(baseClean);

  // 5. Synonyms
  (synonyms || []).forEach(syn => add(syn));

  return Array.from(set);
}

function checkAnimeMatch(guess, canonical, synonyms) {
  const cleanGuess = normalizeString(guess);
  if (!cleanGuess || cleanGuess.length < 2) {
    return { match: false, distance: 99 };
  }

  const variants = getAcceptedVariants(canonical, synonyms);
  let minDistance = 999;

  for (const v of variants) {
    // Exact normalized match
    if (cleanGuess === v) {
      return { match: true, distance: 0 };
    }

    // Prefix match (se guess tem >= 3 letras e eh prefixo do titulo, ex: "bleach" para "bleach thousand year blood war", "attack on titan" para "attack on titan season 2")
    if (cleanGuess.length >= 3 && v.startsWith(cleanGuess + ' ')) {
      return { match: true, distance: 0 };
    }
    if (v.length >= 3 && cleanGuess.startsWith(v + ' ')) {
      return { match: true, distance: 0 };
    }

    const dist = levenshtein(cleanGuess, v);
    if (dist < minDistance) minDistance = dist;
  }

  // Tolerancia para pequenos erros de digitacao (typos):
  // 5 a 8 letras: tolera 1 erro
  // 9+ letras: tolera ate 2 erros
  if (cleanGuess.length >= 5 && minDistance <= 1) {
    return { match: true, distance: minDistance };
  }
  if (cleanGuess.length >= 9 && minDistance <= 2) {
    return { match: true, distance: minDistance };
  }

  return { match: false, distance: minDistance };
}

/* ==============================================================
   AUDIO SOURCE HELPER (SUPORTE LOCAL WEBM/MP3 ROBUSTO)
   ============================================================== */
function getSongAudioSrc(songId) {
  if (songId === 4) return 'audio/4.webm';
  return `audio/${songId}.mp3`;
}

/* ==============================================================
   MODO 1: BLIND TEST ENGINE
   ============================================================== */
let activeExpandedNavBtn = null;

function handleM1Nav(action, event) {
  const btn = event.currentTarget;
  const isTouch = ('ontouchstart' in window) || (navigator.maxTouchPoints > 0) || window.innerWidth <= 900;

  if (isTouch) {
    if (!btn.classList.contains('is-expanded')) {
      if (activeExpandedNavBtn && activeExpandedNavBtn !== btn) {
        activeExpandedNavBtn.classList.remove('is-expanded');
      }
      btn.classList.add('is-expanded');
      activeExpandedNavBtn = btn;
      if (window.AudioManager) AudioManager.playSfx('hover');
      event.stopPropagation();
      return;
    } else {
      btn.classList.remove('is-expanded');
      activeExpandedNavBtn = null;
    }
  }

  if (action === 'prev') {
    prevSong();
  } else if (action === 'reveal') {
    giveUpAndReveal();
  } else if (action === 'next') {
    if (!m1HasGuessed && !m1AnsweredCurrent && !(window.MultiplayerEngine && MultiplayerEngine.isMatchActive)) {
      showToast("🔒 Dê um palpite ou clique no olho 👁️ (Revelar) antes de avançar!");
      if (window.AudioManager) AudioManager.playSfx('wrong');
      return;
    }
    nextSong();
  }
}

function handleM1Media(action, event) {
  const btn = event.currentTarget;
  const isTouch = ('ontouchstart' in window) || (navigator.maxTouchPoints > 0) || window.innerWidth <= 900;

  if (isTouch) {
    if (!btn.classList.contains('is-expanded')) {
      if (activeExpandedNavBtn && activeExpandedNavBtn !== btn) {
        activeExpandedNavBtn.classList.remove('is-expanded');
      }
      btn.classList.add('is-expanded');
      activeExpandedNavBtn = btn;
      if (window.AudioManager) AudioManager.playSfx('hover');
      event.stopPropagation();
      return;
    } else {
      btn.classList.remove('is-expanded');
      activeExpandedNavBtn = null;
    }
  }

  if (action === 'play') {
    togglePlay();
  } else if (action === 'restart') {
    restartAudio();
  } else if (action === 'random') {
    m1NextRandom();
  }
}

document.addEventListener('click', (e) => {
  if (activeExpandedNavBtn && !activeExpandedNavBtn.contains(e.target)) {
    activeExpandedNavBtn.classList.remove('is-expanded');
    activeExpandedNavBtn = null;
  }
});

function m1LoadSong(autoPlay = false) {
  stopAllMedia();
  m1AnsweredCurrent = false;
  m1HasGuessed = false;
  m1Attempts = 0;
  m1RevealedTagsCount = 0;

  const nextBtn = document.getElementById('m1-btn-next');
  if (nextBtn) {
    const isMpActive = (window.MultiplayerEngine && MultiplayerEngine.isMatchActive);
    if (!isMpActive) {
      nextBtn.disabled = true;
      nextBtn.classList.add('nav-locked');
      nextBtn.title = "Dê um palpite ou clique no olho 👁️ (Revelar) para avançar";
    } else {
      nextBtn.disabled = false;
      nextBtn.classList.remove('nav-locked');
      nextBtn.title = "Votar para pular rodada";
    }
  }

  const m1ResultSlot = document.getElementById('m1-result-slot');
  if (m1ResultSlot) m1ResultSlot.classList.remove('is-open');

  feedbackBox.style.display = 'none';
  feedbackBox.className = 'feedback-box';
  answerBox.style.display = 'none';
  guessInput.value = '';
  guessInput.disabled = false;
  guessInput.classList.remove('input-error-shake', 'input-success-pulse');

  if (m1Playlist.length === 0) {
    m1Playlist = buildProgressiveQueue(ALL_SONGS);
  }
  const isMp = (window.MultiplayerEngine && MultiplayerEngine.isMatchActive);
  const song = isMp ? (ALL_SONGS[m1CurrentIndex] || ALL_SONGS[0]) : (m1Playlist[m1PlaylistIndex] || ALL_SONGS[0]);
  m1CurrentIndex = ALL_SONGS.findIndex(s => s.id === song.id);
  if (isMp && m1Playlist && m1Playlist.length > 0) {
    const pIdx = m1Playlist.findIndex(s => s.id === song.id);
    if (pIdx !== -1) m1PlaylistIndex = pIdx;
  }

  if (isMp) {
    m1RoundIndicator.textContent = `RODADA #${MultiplayerEngine.currentRoundIdx + 1} DE ${MultiplayerEngine.activeSettings.rounds} • ${formatDifficulty(song.diff)}`;
    kpiProgress.textContent = `${MultiplayerEngine.currentRoundIdx + 1} / ${MultiplayerEngine.activeSettings.rounds}`;
  } else {
    m1RoundIndicator.textContent = `MÚSICA #${m1PlaylistIndex + 1} DE ${m1Playlist.length} • ${formatDifficulty(song.diff)}`;
    kpiProgress.textContent = `${m1PlaylistIndex + 1} / ${m1Playlist.length}`;
  }

  // Reset visual reveal card to blind mode
  const visualCard = document.getElementById('player-visual-card');
  const bgArt = document.getElementById('player-bg-art');
  const blindContent = document.getElementById('player-blind-content');
  const revealedContent = document.getElementById('player-revealed-content');

  if (visualCard) visualCard.classList.remove('is-revealed');
  if (bgArt) bgArt.style.backgroundImage = 'none';
  if (blindContent) blindContent.style.display = 'flex';
  if (revealedContent) revealedContent.style.display = 'none';

  if (soundBars) soundBars.classList.remove('active');
  vinylIcon.classList.remove('spinning');

  // Render Hint Tags
  tagsContainer.innerHTML = '';
  const tagsList = [
    `📅 ${song.year}`,
    ...(song.tags || [])
  ];

  tagsList.forEach((tagText, idx) => {
    const t = document.createElement('div');
    t.className = 'hint-tag';
    t.dataset.fullText = tagText;
    t.innerHTML = `<img src="icons/padlock.png" class="app-icon app-icon-sm icon-orange" /> Dica ${idx + 1}`;
    t.onclick = () => revealTagElement(t);
    tagsContainer.appendChild(t);
  });

  localVideoPlayer.src = getSongAudioSrc(song.id);
  localVideoPlayer.currentTime = 0;
  m1UseLocal = true;

  if (autoPlay) {
    m1PlayAudio();
  } else {
    setPlayUI(false);
  }
}

function m1PlayAudio() {
  const song = ALL_SONGS[m1CurrentIndex];
  if (videoFrame) videoFrame.src = 'about:blank';

  VisualizerEngine.setupAudioContext();
  localVideoPlayer.src = getSongAudioSrc(song.id);
  localVideoPlayer.play().then(() => {
    m1UseLocal = true;
    localVideoPlayer.style.display = 'block';
    if (videoFrame) videoFrame.style.display = 'none';
    setPlayUI(true);
  }).catch(() => {
    m1UseLocal = false;
    localVideoPlayer.style.display = 'none';
    if (videoFrame) {
      videoFrame.style.display = 'block';
      videoFrame.src = `https://www.youtube.com/embed/${song.video_id}?autoplay=1&controls=0&playsinline=1`;
    }
    setPlayUI(true);
  });
}

function togglePlay() {
  if (m1IsPlaying) {
    stopAllMedia();
  } else {
    m1PlayAudio();
  }
}

function restartAudio() {
  localVideoPlayer.currentTime = 0;
  m1PlayAudio();
}

function setPlayUI(playing) {
  m1IsPlaying = playing;
  if (playBtnIcon) playBtnIcon.innerHTML = playing ? ICON_PAUSE : ICON_PLAY;
  if (playBtnText) playBtnText.textContent = playing ? 'Pausar' : 'Tocar Áudio';
  const playBtn = document.getElementById('btn-play-pause');
  if (playBtn) playBtn.classList.toggle('is-playing', playing);
  if (vinylIcon) vinylIcon.classList.toggle('spinning', playing);
  if (soundBars) soundBars.classList.toggle('active', playing);
}

function m1ToggleMask() {
  if (blindMask) blindMask.classList.toggle('unmasked');
}

function revealTagElement(el) {
  if (!el.classList.contains('revealed')) {
    el.classList.add('revealed');
    let full = el.dataset.fullText || '';
    if (full.startsWith('📅')) {
      const yearText = full.replace('📅', '').trim();
      el.innerHTML = `<img src="icons/calendar.png" class="app-icon app-icon-sm icon-cyan" /> ${escapeHtml(yearText)}`;
    } else {
      el.innerHTML = `<img src="icons/open-padlock.png" class="app-icon app-icon-sm icon-green" /> ${escapeHtml(full)}`;
    }
    m1RevealedTagsCount++;
    AudioManager.playSfx('hint');
  }
}

function revealNextTag() {
  const unrevealed = Array.from(tagsContainer.children).filter(t => !t.classList.contains('revealed'));
  if (unrevealed.length > 0) {
    revealTagElement(unrevealed[0]);
  }
}

function submitGuess() {
  if (m1AnsweredCurrent) return;
  const val = guessInput.value.trim();
  if (!val) return;

  m1Attempts++;
  m1HasGuessed = true;
  const nextBtn = document.getElementById('m1-btn-next');
  if (nextBtn) {
    nextBtn.disabled = false;
    nextBtn.classList.remove('nav-locked');
    nextBtn.title = "Próxima música";
  }
  const song = ALL_SONGS[m1CurrentIndex];
  const result = checkAnimeMatch(val, song.anime, song.synonyms);

  feedbackBox.style.display = 'block';
  const m1ResultSlot = document.getElementById('m1-result-slot');
  if (m1ResultSlot) m1ResultSlot.classList.add('is-open');

  if (result.match) {
    let speedBonus = 0;
    let currentStreak = m1Streak;
    if (window.MultiplayerEngine && MultiplayerEngine.isMatchActive) {
      speedBonus = MultiplayerEngine.calculateSpeedBonus();
      currentStreak = MultiplayerEngine.myStreak || 0;
    }
    const comboBonus = (currentStreak > 0 ? currentStreak * 20 : 0);
    const hintPenalty = m1RevealedTagsCount * 10;
    const attemptPenalty = (m1Attempts - 1) * 15;
    const points = Math.max(30, 100 + speedBonus + comboBonus - hintPenalty - attemptPenalty);

    if (window.MultiplayerEngine && MultiplayerEngine.isMatchActive) {
      MultiplayerEngine.onPlayerAnswer(true, points);
    } else {
      m1Score += points;
      m1CorrectCount++;
      m1Streak++;
      kpiScore.textContent = m1Score;
      kpiCorrect.textContent = m1CorrectCount;
      updateStreakBadge(m1Streak);
    }

    guessInput.classList.remove('input-error-shake');
    guessInput.classList.add('input-success-pulse');
    const effectiveStreak = (window.MultiplayerEngine && MultiplayerEngine.isMatchActive) ? (MultiplayerEngine.myStreak || 0) : m1Streak;
    AudioManager.playSfx(effectiveStreak >= 3 ? 'combo' : 'correct');
    ConfettiEngine.burst();

    let bonusBreakdown = '';
    if (speedBonus > 0 || comboBonus > 0) {
      bonusBreakdown = `<div style="font-size: 12px; margin-top: 6px; color: #a7f3d0; display: flex; gap: 8px; justify-content: center; flex-wrap: wrap;">
        ${speedBonus > 0 ? `<span>⚡ Bônus Rapidez: <strong>+${speedBonus} pts</strong></span>` : ''}
        ${comboBonus > 0 ? `<span>🔥 Combo: <strong>+${comboBonus} pts</strong></span>` : ''}
      </div>`;
    }

    feedbackBox.className = 'feedback-box correct';
    feedbackBox.innerHTML = `
      <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 8px;">
        <div style="display: flex; align-items: center; gap: 8px;">
          <img src="icons/sparkles.png" class="app-icon icon-gold" />
          <span style="font-weight: 800; font-size: 14px; color: #6ee7b7; text-shadow: 0 0 10px rgba(16, 185, 129, 0.4);">VOCÊ ACERTOU! (+${points} pts)</span>
        </div>
        <div style="font-size: 13px; color: #a7f3d0;">É <strong>${escapeHtml(song.anime)}</strong>!</div>
      </div>
      ${bonusBreakdown}
    `;

    FloatingArcade.spawn({
      points,
      isCorrect: true,
      streak: currentStreak + 1,
      speedBonus,
      comboBonus
    });

    revealM1Answer(true);
  } else {
    if (window.MultiplayerEngine && MultiplayerEngine.isMatchActive) {
      // Streak do multiplayer gerenciado separadamente
    } else {
      m1Streak = 0;
      updateStreakBadge(0);
    }

    FloatingArcade.spawn({
      points: 0,
      isCorrect: false,
      text: '❌ INCORRETO'
    });

    guessInput.classList.remove('input-error-shake');
    void guessInput.offsetWidth;
    guessInput.classList.add('input-error-shake');
    guessInput.select();
    AudioManager.playSfx('wrong');

    if (result.distance <= 4) {
      feedbackBox.className = 'feedback-box partial';
      feedbackBox.innerHTML = `⚠️ <strong>MUITO PERTO!</strong> Faltou pouco (diferença de apenas ${result.distance} letras). Escolha a opção exata na lista abaixo!`;
    } else {
      feedbackBox.className = 'feedback-box wrong';
      feedbackBox.innerHTML = `❌ <strong>Incorreto!</strong> (Tentativa ${m1Attempts}). Não é esse anime. Use as dicas ou selecione na lista abaixo.`;
    }
  }
}

function giveUpAndReveal() {
  if (m1AnsweredCurrent) return;
  m1Streak = 0;
  kpiStreak.textContent = '0';
  FloatingArcade.spawn({
    points: 0,
    isCorrect: false,
    text: '❌ REVELADO'
  });
  if (window.MultiplayerEngine && MultiplayerEngine.isMatchActive) {
    MultiplayerEngine.onPlayerAnswer(false, 0);
  }
  const song = ALL_SONGS[m1CurrentIndex];
  feedbackBox.className = 'feedback-box wrong';
  feedbackBox.innerHTML = `<img src="icons/eye.png" class="app-icon icon-purple" /> <strong>RESPOSTA REVELADA!</strong> O anime era <strong>${escapeHtml(song.anime)}</strong>.`;
  feedbackBox.style.display = 'block';
  const m1ResultSlot = document.getElementById('m1-result-slot');
  if (m1ResultSlot) m1ResultSlot.classList.add('is-open');
  revealM1Answer(false);
}

function revealM1Answer(isCorrect) {
  m1AnsweredCurrent = true;
  m1HasGuessed = true;
  guessInput.disabled = true;

  const nextBtn = document.getElementById('m1-btn-next');
  if (nextBtn) {
    nextBtn.disabled = false;
    nextBtn.classList.remove('nav-locked');
    nextBtn.title = "Próxima música";
  }

  const song = ALL_SONGS[m1CurrentIndex];

  // Visual Card: Capa escura no fundo e nomes reluzentes na frente
  const visualCard = document.getElementById('player-visual-card');
  const bgArt = document.getElementById('player-bg-art');
  const blindContent = document.getElementById('player-blind-content');
  const revealedContent = document.getElementById('player-revealed-content');
  const revealThumb = document.getElementById('reveal-thumb-img');
  const revealBadge = document.getElementById('reveal-badge-status');
  const revealTitle = document.getElementById('reveal-anime-title');
  const revealSong = document.getElementById('reveal-song-name');
  const revealMeta = document.getElementById('reveal-artist-meta');

  if (song.image_url) {
    if (bgArt) bgArt.style.backgroundImage = `url('${song.image_url}')`;
    if (revealThumb) revealThumb.src = song.image_url;
  }
  if (revealBadge) {
    revealBadge.className = isCorrect ? 'revealed-badge' : 'revealed-badge wrong';
    revealBadge.textContent = isCorrect ? '🎉 VOCÊ ACERTOU!' : '❌ RESPOSTA REVELADA';
  }
  if (revealTitle) revealTitle.textContent = song.anime;
  if (revealSong) revealSong.textContent = `🎵 "${song.song}"`;
  if (revealMeta) revealMeta.textContent = `por ${song.artist} (${song.year}) • ${formatDifficulty(song.diff)}`;

  if (blindContent) blindContent.style.display = 'none';
  if (revealedContent) revealedContent.style.display = 'flex';
  if (visualCard) visualCard.classList.add('is-revealed');

  Array.from(tagsContainer.children).forEach(t => revealTagElement(t));

  const m1ResultSlot = document.getElementById('m1-result-slot');
  if (m1ResultSlot) m1ResultSlot.classList.add('is-open');

  answerBox.style.display = 'block';
  ansAnime.innerHTML = isCorrect ? `<img src="icons/check.png" class="app-icon icon-raw" /> ${escapeHtml(song.anime)}` : `<img src="icons/remove.png" class="app-icon icon-raw" /> Resposta: ${escapeHtml(song.anime)}`;
  ansMeta.textContent = `Abertura: "${song.song}" por ${song.artist} (${song.year}) • ${formatDifficulty(song.diff)}`;
  ansSyns.textContent = `Nomes reconhecidos: ${(song.synonyms || []).slice(0, 6).join(' • ')}`;
  if (song.image_url) {
    ansPosterImg.src = song.image_url;
  }
}

function prevSong() {
  stopAllMedia();
  if (m1PlaylistIndex > 0) {
    m1PlaylistIndex--;
    m1LoadSong(true);
  }
}

function nextSong() {
  if (window.MultiplayerEngine && MultiplayerEngine.isMatchActive) {
    MultiplayerEngine.voteSkip();
    return;
  }
  if (!m1HasGuessed && !m1AnsweredCurrent) {
    showToast("🔒 Dê um palpite ou clique no olho 👁️ (Revelar) antes de avançar!");
    if (window.AudioManager) AudioManager.playSfx('wrong');
    return;
  }
  stopAllMedia();
  if (m1PlaylistIndex < m1Playlist.length - 1) {
    m1PlaylistIndex++;
    m1LoadSong(true);
  } else {
    if (m1Score > 0 || m1CorrectCount > 0) {
      openGameOverModal('mode1', m1Score, m1CorrectCount, m1Streak);
    } else {
      showToast("🏁 Fim da lista de músicas!");
    }
  }
}

function m1NextRandom() {
  stopAllMedia();
  m1PlaylistIndex = Math.floor(Math.random() * m1Playlist.length);
  m1LoadSong(true);
}

function openYouTubeDirect() {
  const song = ALL_SONGS[m1CurrentIndex];
  window.open(song.video_url, '_blank');
}

/* ==============================================================
   MODO 2: "QUAL É A ABERTURA?" (3 MÚSICAS ALEATÓRIAS)
   ============================================================== */
function m2StartGame() {
  stopAllMedia();
  m2Score = 0;
  m2CorrectCount = 0;
  m2Streak = 0;
  m2UnplayedQueue = ALL_SONGS.map((_, i) => i);
  m2UnplayedQueue.sort(() => getGameRandom() - 0.5);
  m2RoundsPlayed = 0;
  m2NextRound();
}

function m2NextRound() {
  if (window.MultiplayerEngine && MultiplayerEngine.isMatchActive) {
    MultiplayerEngine.voteSkip();
    return;
  }
  stopAllMedia();
  if (isChallengeActive && m2RoundsPlayed >= challengeRounds) {
    openGameOverModal('mode2', m2Score, m2CorrectCount, m2Streak);
    return;
  }

  if (m2UnplayedQueue.length === 0) {
    m2UnplayedQueue = ALL_SONGS.map((_, i) => i).sort(() => getGameRandom() - 0.5);
  }

  m2CurrentIndex = m2UnplayedQueue.pop();
  m2RoundsPlayed++;
  m2InitRound();
}

function m2InitRound() {
  m2Answered = false;
  m2SelectedOptionIndex = -1;
  m2PlayingIndex = -1;
  m2StopAudio();

  const targetSong = ALL_SONGS[m2CurrentIndex];

  if (window.MultiplayerEngine && MultiplayerEngine.isMatchActive) {
    m2RoundIndicator.textContent = `RODADA #${MultiplayerEngine.currentRoundIdx + 1} DE ${MultiplayerEngine.activeSettings.rounds} • ${formatDifficulty(targetSong.diff)}`;
    kpiProgress.textContent = `${MultiplayerEngine.currentRoundIdx + 1} / ${MultiplayerEngine.activeSettings.rounds}`;
  } else {
    m2RoundIndicator.textContent = `RODADA #${m2RoundsPlayed} DE ${isChallengeActive ? challengeRounds : ALL_SONGS.length} • ${formatDifficulty(targetSong.diff)}`;
    kpiProgress.textContent = `${m2RoundsPlayed} / ${isChallengeActive ? challengeRounds : ALL_SONGS.length}`;
  }
  m2TargetName.textContent = targetSong.anime;
  m2TargetPoster.src = targetSong.image_url || 'https://via.placeholder.com/225x320?text=Anime';

  // Metadata pills
  m2TargetMeta.innerHTML = `
    <span class="pill-chip"><img src="icons/calendar.png" class="app-icon app-icon-xs icon-white" alt="Ano" /> ${targetSong.year}</span>
    <span class="pill-chip">${formatDifficulty(targetSong.diff)}</span>
  `;
  (targetSong.tags || []).slice(0, 3).forEach(t => {
    const s = document.createElement('span');
    s.className = 'pill-chip';
    s.innerHTML = `<img src="icons/star.png" class="app-icon app-icon-xs icon-gold" alt="Tag" /> ${t}`;
    m2TargetMeta.appendChild(s);
  });

  // Pick 2 random decoys from other animes
  const decoys = ALL_SONGS.filter(s => s.anime.toLowerCase() !== targetSong.anime.toLowerCase());
  decoys.sort(() => getGameRandom() - 0.5);
  const chosenDecoys = decoys.slice(0, 2);

  // Combine and shuffle 3 options
  m2Options = [targetSong, chosenDecoys[0], chosenDecoys[1]].sort(() => getGameRandom() - 0.5);
  m2CorrectOptionIndex = m2Options.findIndex(s => s.id === targetSong.id);

  // Reset 3 Cards UI
  for (let i = 0; i < 3; i++) {
    const card = document.getElementById(`m2-card-${i}`);
    const label = document.getElementById(`m2-label-${i}`);
    const sub = document.getElementById(`m2-sub-${i}`);
    const eq = document.getElementById(`m2-eq-${i}`);
    const icon = document.getElementById(`m2-icon-${i}`);

    if (card) card.className = 'music-card';
    if (label) label.textContent = `Faixa de Áudio ${i + 1}`;
    if (sub) sub.style.display = 'none';
    if (eq) eq.classList.remove('active');
    if (icon) icon.innerHTML = ICON_PLAY;
  }

  const m2VisualCard = document.getElementById('m2-visual-card');
  const m2BgArt = document.getElementById('m2-bg-art');
  const m2BlindContent = document.getElementById('m2-blind-content');
  const m2RevealedContent = document.getElementById('m2-revealed-content');

  if (m2VisualCard) m2VisualCard.classList.remove('is-revealed');
  if (m2BgArt) m2BgArt.style.backgroundImage = 'none';
  if (m2BlindContent) m2BlindContent.style.display = 'flex';
  if (m2RevealedContent) m2RevealedContent.style.display = 'none';
  if (m2VinylIcon) m2VinylIcon.classList.remove('spinning');
  if (m2SoundBars) m2SoundBars.classList.remove('active');
  const revBars = document.getElementById('m2-revealed-sound-bars');
  if (revBars) revBars.classList.remove('active');
  if (m2PlayerMask) m2PlayerMask.classList.remove('unmasked');

  if (m2MaskStatus) m2MaskStatus.textContent = 'Clique em uma opção abaixo para ouvir a música';
  if (m2FeedbackBanner) m2FeedbackBanner.style.display = 'none';
  if (m2BtnConfirm) {
    m2BtnConfirm.disabled = true;
    m2BtnConfirm.style.display = 'inline-flex';
  }
  if (m2BtnNext) m2BtnNext.style.display = 'none';
}

function m2ClickCard(idx) {
  if (m2Answered) return;

  m2SelectedOptionIndex = idx;
  if (m2BtnConfirm) m2BtnConfirm.disabled = false;

  const targetSong = ALL_SONGS[m2CurrentIndex];
  const song = m2Options[idx];

  if (m2PlayingIndex === idx) {
    const eqEl = document.getElementById(`m2-eq-${idx}`);
    const isPlaying = eqEl && eqEl.classList.contains('active');
    if (isPlaying) {
      m2LocalVideo.pause();
      if (eqEl) eqEl.classList.remove('active');
      const iconEl = document.getElementById(`m2-icon-${idx}`);
      if (iconEl) iconEl.innerHTML = ICON_PLAY;
      if (m2VinylIcon) m2VinylIcon.classList.remove('spinning');
      if (m2SoundBars) m2SoundBars.classList.remove('active');
      if (m2MaskStatus) m2MaskStatus.innerHTML = `${ICON_PAUSE} Opção ${idx + 1} pausada`;
    } else {
      m2LocalVideo.play();
      if (eqEl) eqEl.classList.add('active');
      const iconEl = document.getElementById(`m2-icon-${idx}`);
      if (iconEl) iconEl.innerHTML = ICON_PAUSE;
      if (m2VinylIcon) m2VinylIcon.classList.add('spinning');
      if (m2SoundBars) m2SoundBars.classList.add('active');
      if (m2MaskStatus) m2MaskStatus.textContent = `🎧 Tocando Opção ${idx + 1}...`;
    }
  } else {
    m2PlayingIndex = idx;
    for (let i = 0; i < 3; i++) {
      const card = document.getElementById(`m2-card-${i}`);
      const eq = document.getElementById(`m2-eq-${i}`);
      const icon = document.getElementById(`m2-icon-${i}`);
      if (card) {
        card.classList.remove('selected', 'playing');
        if (i === idx) {
          card.classList.add('selected', 'playing');
        }
      }
      if (i === idx) {
        if (eq) eq.classList.add('active');
        if (icon) icon.innerHTML = ICON_PAUSE;
      } else {
        if (eq) eq.classList.remove('active');
        if (icon) icon.innerHTML = ICON_PLAY;
      }
    }

    if (m2VinylIcon) m2VinylIcon.classList.add('spinning');
    if (m2SoundBars) m2SoundBars.classList.add('active');
    if (m2MaskStatus) m2MaskStatus.textContent = `🎧 Tocando Opção ${idx + 1}...`;

    VisualizerEngine.setupAudioContext();
    AudioManager.playSfx('click');

    m2LocalVideo.pause();
    m2LocalVideo.src = getSongAudioSrc(song.id);
    m2LocalVideo.currentTime = 0;
    m2LocalVideo.play().then(() => {
      m2LocalVideo.style.display = 'block';
      if (m2VideoFrame) m2VideoFrame.style.display = 'none';
    }).catch(() => {
      m2LocalVideo.style.display = 'none';
      if (m2VideoFrame) {
        m2VideoFrame.style.display = 'block';
        m2VideoFrame.src = `https://www.youtube.com/embed/${song.video_id}?autoplay=1&controls=0&playsinline=1`;
      }
    });
  }
}

function m2StopAudio() {
  if (m2LocalVideo) {
    m2LocalVideo.pause();
    m2LocalVideo.currentTime = 0;
  }
  if (m2VideoFrame) {
    m2VideoFrame.src = 'about:blank';
    m2VideoFrame.style.display = 'none';
  }
  m2PlayingIndex = -1;
  if (m2VinylIcon) m2VinylIcon.classList.remove('spinning');
  if (m2SoundBars) m2SoundBars.classList.remove('active');
  const revBars = document.getElementById('m2-revealed-sound-bars');
  if (revBars) revBars.classList.remove('active');
  for (let i = 0; i < 3; i++) {
    const eq = document.getElementById(`m2-eq-${i}`);
    const icon = document.getElementById(`m2-icon-${i}`);
    const card = document.getElementById(`m2-card-${i}`);
    if (card) card.classList.remove('playing');
    if (eq) eq.classList.remove('active');
    if (icon) icon.innerHTML = ICON_PLAY;
  }
}

function m2ConfirmSelection() {
  if (m2SelectedOptionIndex === -1 || m2Answered) return;
  m2Answered = true;
  m2StopAudio();

  const isCorrect = (m2SelectedOptionIndex === m2CorrectOptionIndex);
  const correctSong = m2Options[m2CorrectOptionIndex];

  for (let i = 0; i < 3; i++) {
    const card = document.getElementById(`m2-card-${i}`);
    const label = document.getElementById(`m2-label-${i}`);
    const sub = document.getElementById(`m2-sub-${i}`);
    const optSong = m2Options[i];

    card.classList.remove('selected', 'playing');
    if (i === m2CorrectOptionIndex) {
      card.classList.add('revealed-correct');
      label.innerHTML = `<img src="icons/check.png" class="app-icon-sm icon-raw" /> <strong>${optSong.anime}</strong>: "${optSong.song}"`;
      sub.style.display = 'block';
      sub.innerHTML = `Artista: ${optSong.artist} (${optSong.year}) • Abertura Oficial!`;
    } else if (i === m2SelectedOptionIndex) {
      card.classList.add('revealed-wrong');
      label.innerHTML = `<img src="icons/remove.png" class="app-icon-sm icon-raw" /> Errado: Abertura de <strong>${optSong.anime}</strong>!`;
      sub.style.display = 'block';
      sub.innerHTML = `Música: "${optSong.song}" (${optSong.artist})`;
    } else {
      card.classList.add('revealed-decoy');
      label.innerHTML = `<img src="icons/vinyl.png" class="app-icon-sm icon-white" /> Era de: <strong>${optSong.anime}</strong> ("${optSong.song}")`;
      sub.style.display = 'block';
      sub.innerHTML = `Artista: ${optSong.artist} (${optSong.year})`;
    }
  }

  if (isCorrect) {
    let speedBonus = 0;
    let currentStreak = m2Streak;
    if (window.MultiplayerEngine && MultiplayerEngine.isMatchActive) {
      speedBonus = MultiplayerEngine.calculateSpeedBonus();
      currentStreak = MultiplayerEngine.myStreak || 0;
    }
    const comboBonus = (currentStreak > 0 ? currentStreak * 20 : 0);
    const pts = 100 + speedBonus + comboBonus;

    if (window.MultiplayerEngine && MultiplayerEngine.isMatchActive) {
      MultiplayerEngine.onPlayerAnswer(true, pts);
    } else {
      m2Streak++;
      m2CorrectCount++;
      m2Score += pts;
    }

    const effectiveStreak = (window.MultiplayerEngine && MultiplayerEngine.isMatchActive) ? (MultiplayerEngine.myStreak || 0) : m2Streak;
    AudioManager.playSfx(effectiveStreak >= 3 ? 'combo' : 'correct');
    ConfettiEngine.burst();
    m2FeedbackBanner.className = 'm2-feedback-banner correct';
    m2FeedbackBanner.style.display = 'block';

    let bonusBreakdown = '';
    if (speedBonus > 0 || comboBonus > 0) {
      bonusBreakdown = `<div style="font-size: 12px; margin-top: 6px; color: #a7f3d0; display: flex; gap: 8px; justify-content: center; flex-wrap: wrap;">
        ${speedBonus > 0 ? `<span>⚡ Bônus Rapidez: <strong>+${speedBonus} pts</strong></span>` : ''}
        ${comboBonus > 0 ? `<span>🔥 Combo: <strong>+${comboBonus} pts</strong></span>` : ''}
      </div>`;
    }

    m2FeedbackBanner.innerHTML = `<img src="icons/sparkles.png" class="app-icon icon-gold" /> <strong>ACERTOU! (+${pts} pts)</strong> A Opção ${m2CorrectOptionIndex + 1} é a abertura oficial de <strong>${correctSong.anime}</strong>!${bonusBreakdown}`;

    FloatingArcade.spawn({
      points: pts,
      isCorrect: true,
      streak: currentStreak + 1,
      speedBonus,
      comboBonus
    });
  } else {
    if (window.MultiplayerEngine && MultiplayerEngine.isMatchActive) {
      MultiplayerEngine.onPlayerAnswer(false, 0);
    } else {
      m2Streak = 0;
    }
    AudioManager.playSfx('wrong');
    m2FeedbackBanner.className = 'm2-feedback-banner wrong';
    m2FeedbackBanner.style.display = 'block';
    m2FeedbackBanner.innerHTML = `<img src="icons/remove.png" class="app-icon icon-red" /> <strong>NÃO FOI DESSA VEZ!</strong> A abertura correta de <strong>${correctSong.anime}</strong> era a <strong>Opção ${m2CorrectOptionIndex + 1}</strong> ("${correctSong.song}").`;

    FloatingArcade.spawn({
      points: 0,
      isCorrect: false,
      text: '❌ ERROU'
    });
  }

  if (window.MultiplayerEngine && MultiplayerEngine.isMatchActive) {
    updateGlobalKPIs();
  } else {
    kpiScore.textContent = m2Score;
    kpiCorrect.textContent = m2CorrectCount;
    updateStreakBadge(m2Streak);
  }

  // Revelação visual estilizada no card do player (Thumbnail do vídeo da abertura + Info)
  const m2VisualCard = document.getElementById('m2-visual-card');
  const m2BgArt = document.getElementById('m2-bg-art');
  const m2BlindContent = document.getElementById('m2-blind-content');
  const m2RevealedContent = document.getElementById('m2-revealed-content');
  const m2RevealThumb = document.getElementById('m2-reveal-thumb-img');
  const m2RevealBadge = document.getElementById('m2-reveal-badge');
  const m2RevealTitle = document.getElementById('m2-reveal-anime-title');
  const m2RevealSong = document.getElementById('m2-reveal-song-name');
  const m2RevealMeta = document.getElementById('m2-reveal-artist-meta');
  const revBars = document.getElementById('m2-revealed-sound-bars');

  const isValidYt = !!(correctSong.video_id && 
                       /^[a-zA-Z0-9_-]{11}$/.test(correctSong.video_id) && 
                       !['auto_download', 'unavailable', 'placeholder'].includes(correctSong.video_id));
  const fallbackPoster = correctSong.image_url || 'https://via.placeholder.com/225x320?text=Anime';
  const initialThumb = isValidYt ? `https://i.ytimg.com/vi/${correctSong.video_id}/hqdefault.jpg` : fallbackPoster;

  if (m2RevealThumb) {
    m2RevealThumb.src = initialThumb;
    m2RevealThumb.onerror = () => {
      m2RevealThumb.src = fallbackPoster;
      if (m2BgArt) m2BgArt.style.backgroundImage = `url('${fallbackPoster}')`;
    };
    m2RevealThumb.onload = () => {
      // YouTube returns 120x90 gray placeholder with HTTP 200 when thumbnail does not exist
      if (m2RevealThumb.naturalWidth <= 120 && m2RevealThumb.src !== fallbackPoster) {
        m2RevealThumb.src = fallbackPoster;
        if (m2BgArt) m2BgArt.style.backgroundImage = `url('${fallbackPoster}')`;
      }
    };
  }
  if (m2BgArt) {
    m2BgArt.style.backgroundImage = `url('${initialThumb}')`;
  }
  if (m2RevealBadge) {
    m2RevealBadge.className = isCorrect ? 'revealed-badge' : 'revealed-badge wrong';
    m2RevealBadge.innerHTML = isCorrect ? '<img src="icons/check.png" class="app-icon icon-raw" /> VOCÊ ACERTOU A ABERTURA!' : '<img src="icons/remove.png" class="app-icon icon-raw" /> ABERTURA CORRETA';
  }
  if (m2RevealTitle) m2RevealTitle.textContent = correctSong.anime;
  if (m2RevealSong) m2RevealSong.textContent = `"${correctSong.song}"`;
  if (m2RevealMeta) m2RevealMeta.textContent = `por ${correctSong.artist} (${correctSong.year}) • Abertura Oficial`;

  if (m2BlindContent) m2BlindContent.style.display = 'none';
  if (m2RevealedContent) m2RevealedContent.style.display = 'flex';
  if (m2VisualCard) m2VisualCard.classList.add('is-revealed');
  if (m2PlayerMask) m2PlayerMask.classList.add('unmasked');
  if (revBars) revBars.classList.add('active');

  // Reproduzir o áudio local da abertura correta
  m2LocalVideo.src = getSongAudioSrc(correctSong.id);
  m2LocalVideo.currentTime = 0;
  m2LocalVideo.play().catch(() => {});

  m2BtnConfirm.style.display = 'none';
  m2BtnNext.style.display = 'inline-flex';
}

/* ==============================================================
   MODO 3: "ADIVINHE A CENA" (FRAMES REAIS DE EPISÓDIOS)
   ============================================================== */
function m3StartGame() {
  stopAllMedia();
  m3Score = 0;
  m3CorrectCount = 0;
  m3Streak = 0;
  m3RoundsPlayed = 0;
  m3UnplayedQueue = Array.from({ length: ALL_SCENES.length }, (_, i) => i);
  for (let i = m3UnplayedQueue.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [m3UnplayedQueue[i], m3UnplayedQueue[j]] = [m3UnplayedQueue[j], m3UnplayedQueue[i]];
  }
  m3NextScene();
}

function m3NextScene() {
  if (window.MultiplayerEngine && MultiplayerEngine.isMatchActive) {
    MultiplayerEngine.voteSkip();
    return;
  }
  if (!m3HasGuessed && !m3Answered) {
    showToast("🔒 Dê um palpite ou clique em 'Ver Resposta' antes de avançar!");
    if (window.AudioManager) AudioManager.playSfx('wrong');
    return;
  }
  stopAllMedia();
  if (isChallengeActive && m3RoundsPlayed >= challengeRounds) {
    openGameOverModal('mode3', m3Score, m3CorrectCount, m3Streak);
    return;
  }

  if (m3UnplayedQueue.length === 0) {
    m3UnplayedQueue = Array.from({ length: ALL_SCENES.length }, (_, i) => i);
    for (let i = m3UnplayedQueue.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [m3UnplayedQueue[i], m3UnplayedQueue[j]] = [m3UnplayedQueue[j], m3UnplayedQueue[i]];
    }
  }

  m3CurrentIndex = m3UnplayedQueue.pop();
  m3RoundsPlayed++;
  m3InitScene();
}

function m3InitRound() {
  m3InitScene();
}

function m3PickRandom() {
  stopAllMedia();
  m3CurrentIndex = Math.floor(Math.random() * ALL_SCENES.length);
  m3InitScene();
}

function m3InitScene() {
  m3Answered = false;
  m3HasGuessed = false;
  m3HintsRevealed = 0;
  m3Input.value = '';
  m3Input.disabled = false;
  m3Input.classList.remove('input-error-shake', 'input-success-pulse');
  m3FeedbackBox.style.display = 'none';
  m3AnswerBox.style.display = 'none';

  const m3NextBtn = document.getElementById('m3-btn-next');
  if (m3NextBtn) {
    const isMpActive = (window.MultiplayerEngine && MultiplayerEngine.isMatchActive);
    if (!isMpActive) {
      m3NextBtn.disabled = true;
      m3NextBtn.classList.add('btn-locked');
      m3NextBtn.title = "Dê um palpite ou clique em 'Ver Resposta' para avançar";
    } else {
      m3NextBtn.disabled = false;
      m3NextBtn.classList.remove('btn-locked');
      m3NextBtn.title = "Votar para pular rodada";
    }
  }

  const scene = ALL_SCENES[m3CurrentIndex];
  if (window.MultiplayerEngine && MultiplayerEngine.isMatchActive) {
    m3RoundIndicator.textContent = `CENA #${MultiplayerEngine.currentRoundIdx + 1} DE ${MultiplayerEngine.activeSettings.rounds}`;
    kpiProgress.textContent = `${MultiplayerEngine.currentRoundIdx + 1} / ${MultiplayerEngine.activeSettings.rounds}`;
  } else {
    m3RoundIndicator.textContent = `CENA #${m3RoundsPlayed} DE ${isChallengeActive ? challengeRounds : ALL_SCENES.length}`;
    kpiProgress.textContent = `${m3RoundsPlayed} / ${isChallengeActive ? challengeRounds : ALL_SCENES.length}`;
  }

  m3SceneImg.onerror = function() {
    console.warn("Fallback de imagem ativado para:", scene.anime, scene.image_url);
    const songMatch = ALL_SONGS.find(s => s.anime.toLowerCase() === (scene.anime || '').toLowerCase());
    const fallbackPoster = scene.poster_url || (songMatch ? songMatch.image_url : null);
    if (fallbackPoster && this.src !== fallbackPoster) {
      this.src = fallbackPoster;
      return;
    }
    this.onerror = null;
    const cleanTitle = encodeURIComponent((scene.anime || 'Cena de Anime').replace(/["'<>]/g, ''));
    this.src = 'data:image/svg+xml;charset=UTF-8,%3Csvg%20width%3D%22600%22%20height%3D%22340%22%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%3E%3Crect%20width%3D%22100%25%22%20height%3D%22100%25%22%20fill%3D%22%230f172a%22%2F%3E%3Ctext%20x%3D%2250%25%22%20y%3D%2250%25%22%20font-family%3D%22sans-serif%22%20font-size%3D%2218%22%20font-weight%3D%22bold%22%20fill%3D%22%2338bdf8%22%20text-anchor%3D%22middle%22%20dy%3D%22.3em%22%3E🎬%20' + cleanTitle + '%3C%2Ftext%3E%3C%2Fsvg%3E';
  };
  m3SceneImg.src = scene.image_url || 'https://media.kitsu.app/anime/poster_images/1/small.jpg';

  // Render Hint Badges
  m3TagsRow.innerHTML = '';
  const hintBadges = [
    { title: 'Ano', val: `<img src="icons/calendar.png" class="app-icon app-icon-xs icon-white" alt="Ano" /> <span>Ano: ${scene.year}</span>`, raw: `Ano: ${scene.year}` },
    { title: 'Gêneros', val: `<img src="icons/star.png" class="app-icon app-icon-xs icon-gold" alt="Gêneros" /> <span>${(scene.tags || []).slice(0, 2).join(' / ')}</span>`, raw: (scene.tags || []).slice(0, 2).join(' / ') },
    { title: 'Detalhe', val: `<img src="icons/clapperboard.png" class="app-icon app-icon-xs icon-cyan" alt="Detalhe" /> <span>${(scene.tags || [])[2] || 'Ação / Animação'}</span>`, raw: (scene.tags || [])[2] || 'Ação / Animação' },
    { title: 'Enredo', val: `<img src="icons/lightbulb.png" class="app-icon app-icon-xs icon-gold" alt="Enredo" /> <span>${scene.hint || 'Anime clássico e aclamado'}</span>`, raw: scene.hint || 'Anime clássico e aclamado' }
  ];

  hintBadges.forEach((h, idx) => {
    const b = document.createElement('div');
    b.className = 'scene-tag-badge locked';
    b.dataset.val = h.val;
    b.dataset.title = h.title;
    b.dataset.raw = h.raw;
    b.title = `${h.title} (Bloqueado - clique para revelar)`;
    b.innerHTML = `<img src="icons/padlock.png" class="app-icon app-icon-xs icon-white" alt="Bloqueado" /> <span>${h.title} (Oculto)</span>`;
    b.onclick = () => m3RevealTagBadge(b);
    m3TagsRow.appendChild(b);
  });
}

function m3RevealTagBadge(badgeEl) {
  if (badgeEl.classList.contains('locked')) {
    badgeEl.classList.remove('locked');
    badgeEl.classList.add('revealed');
    badgeEl.innerHTML = badgeEl.dataset.val;
    badgeEl.title = badgeEl.dataset.raw || '';
    m3HintsRevealed++;
    AudioManager.playSfx('hint');
  }
}

function m3RevealNextHint() {
  const locked = Array.from(m3TagsRow.children).filter(b => b.classList.contains('locked'));
  if (locked.length > 0) {
    m3RevealTagBadge(locked[0]);
  }
}

function m3SubmitGuess() {
  if (m3Answered) return;
  const val = m3Input.value.trim();
  if (!val) return;

  m3HasGuessed = true;
  const m3NextBtn = document.getElementById('m3-btn-next');
  if (m3NextBtn) {
    m3NextBtn.disabled = false;
    m3NextBtn.classList.remove('btn-locked');
    m3NextBtn.title = "Próxima Cena";
  }

  const scene = ALL_SCENES[m3CurrentIndex];
  const res = checkAnimeMatch(val, scene.anime, scene.synonyms);

  m3FeedbackBox.style.display = 'block';

  if (res.match) {
    let speedBonus = 0;
    let currentStreak = m3Streak;
    if (window.MultiplayerEngine && MultiplayerEngine.isMatchActive) {
      speedBonus = MultiplayerEngine.calculateSpeedBonus();
      currentStreak = MultiplayerEngine.myStreak || 0;
    }
    const comboBonus = (currentStreak > 0 ? currentStreak * 20 : 0);
    const hintPenalty = m3HintsRevealed * 15;
    const pts = Math.max(30, 100 + speedBonus + comboBonus - hintPenalty);

    if (window.MultiplayerEngine && MultiplayerEngine.isMatchActive) {
      MultiplayerEngine.onPlayerAnswer(true, pts);
    } else {
      m3Streak++;
      m3CorrectCount++;
      m3Score += pts;
      kpiScore.textContent = m3Score;
      kpiCorrect.textContent = m3CorrectCount;
      updateStreakBadge(m3Streak);
    }

    m3Input.classList.remove('input-error-shake');
    m3Input.classList.add('input-success-pulse');
    const effectiveStreak = (window.MultiplayerEngine && MultiplayerEngine.isMatchActive) ? (MultiplayerEngine.myStreak || 0) : m3Streak;
    AudioManager.playSfx(effectiveStreak >= 3 ? 'combo' : 'correct');
    ConfettiEngine.burst();

    let bonusBreakdown = '';
    if (speedBonus > 0 || comboBonus > 0) {
      bonusBreakdown = `<div style="font-size: 12px; margin-top: 6px; color: #a7f3d0; display: flex; gap: 8px; justify-content: center; flex-wrap: wrap;">
        ${speedBonus > 0 ? `<span>⚡ Bônus Rapidez: <strong>+${speedBonus} pts</strong></span>` : ''}
        ${comboBonus > 0 ? `<span>🔥 Combo: <strong>+${comboBonus} pts</strong></span>` : ''}
      </div>`;
    }

    m3FeedbackBox.className = 'feedback-box correct';
    m3FeedbackBox.innerHTML = `<img src="icons/sparkles.png" class="app-icon icon-gold" /> <strong>ACERTOU A CENA! (+${pts} pts)</strong> É do anime <strong>${scene.anime}</strong>!${bonusBreakdown}`;

    FloatingArcade.spawn({
      points: pts,
      isCorrect: true,
      streak: currentStreak + 1,
      speedBonus,
      comboBonus
    });

    m3RevealSceneAnswer(true);
  } else {
    if (window.MultiplayerEngine && MultiplayerEngine.isMatchActive) {
      // Streak do multiplayer gerenciado separadamente
    } else {
      m3Streak = 0;
      updateStreakBadge(0);
    }

    FloatingArcade.spawn({
      points: 0,
      isCorrect: false,
      text: '❌ INCORRETO'
    });

    m3Input.classList.remove('input-error-shake');
    void m3Input.offsetWidth;
    m3Input.classList.add('input-error-shake');
    m3Input.select();
    AudioManager.playSfx('wrong');

    if (res.distance <= 4) {
      m3FeedbackBox.className = 'feedback-box partial';
      m3FeedbackBox.innerHTML = `<img src="icons/lightbulb.png" class="app-icon icon-gold" /> <strong>QUASE LÁ!</strong> Faltou muito pouco (erro de ${res.distance} letras). Escolha a opção correta na lista de sugestões!`;
    } else {
      m3FeedbackBox.className = 'feedback-box wrong';
      m3FeedbackBox.innerHTML = `<img src="icons/remove.png" class="app-icon icon-red" /> <strong>Incorreto!</strong> Não é esse anime. Use os botões de dicas ou selecione na lista de sugestões abaixo.`;
    }
  }
}

function m3GiveUp() {
  if (m3Answered) return;
  FloatingArcade.spawn({
    points: 0,
    isCorrect: false,
    text: '❌ REVELADO'
  });
  if (window.MultiplayerEngine && MultiplayerEngine.isMatchActive) {
    MultiplayerEngine.onPlayerAnswer(false, 0);
  } else {
    m3Streak = 0;
    kpiStreak.textContent = '0';
  }
  m3RevealSceneAnswer(false);
}

function m3RevealSceneAnswer(isCorrect) {
  m3Answered = true;
  m3HasGuessed = true;
  m3Input.disabled = true;

  const m3NextBtn = document.getElementById('m3-btn-next');
  if (m3NextBtn) {
    m3NextBtn.disabled = false;
    m3NextBtn.classList.remove('btn-locked');
    m3NextBtn.title = "Próxima Cena";
  }

  Array.from(m3TagsRow.children).forEach(b => m3RevealTagBadge(b));

  const scene = ALL_SCENES[m3CurrentIndex];
  m3AnswerBox.style.display = 'block';
  m3AnsTitle.innerHTML = isCorrect ? `<img src="icons/check.png" class="app-icon icon-raw" /> ${scene.anime}` : `<img src="icons/remove.png" class="app-icon icon-raw" /> Resposta: ${scene.anime}`;
  m3AnsMeta.textContent = `Ano: ${scene.year} • Tags: ${(scene.tags || []).join(' • ')}`;
  m3AnsSyns.textContent = `Sinônimos aceitos: ${(scene.synonyms || []).slice(0, 5).join(' • ')}`;

  const songMatch = ALL_SONGS.find(s => s.anime.toLowerCase() === scene.anime.toLowerCase());
  const officialPoster = scene.poster_url || (songMatch ? songMatch.image_url : '') || scene.image_url;
  m3AnsPoster.src = officialPoster;
}

/* Lightbox Modal */
function openLightbox() {
  const scene = ALL_SCENES[m3CurrentIndex];
  document.getElementById('lightbox-img').src = scene.image_url;
  document.getElementById('lightbox-modal').classList.add('active');
}

function closeLightbox() {
  document.getElementById('lightbox-modal').classList.remove('active');
}

/* ==============================================================
   MODO 4: LEADERBOARD & MULTIPLAYER (ROOMS P2P WEBRTC)
   ============================================================== */
function escapeHtml(str) {
  return String(str || '').replace(/[&<>'"]/g, tag => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;'
  }[tag] || tag));
}

function switchMode4Tab(tab) {
  const roomsTab = document.getElementById('mp-subtab-rooms');
  const lbTab = document.getElementById('mp-subtab-leaderboard');
  const roomsPanel = document.getElementById('mp-rooms-panel');
  const lbPanel = document.getElementById('mp-leaderboard-panel');

  if (tab === 'rooms') {
    if (roomsTab) roomsTab.classList.add('active');
    if (lbTab) lbTab.classList.remove('active');
    if (roomsPanel) roomsPanel.style.display = 'block';
  } else {
    if (roomsTab) roomsTab.classList.remove('active');
    if (lbTab) lbTab.classList.add('active');
    if (roomsPanel) roomsPanel.style.display = 'none';
    if (lbPanel) lbPanel.style.display = 'block';
    renderLeaderboardTable('all');
  }
}

const MultiplayerEngine = {
  peer: null,
  isHost: false,
  roomCode: '',
  myPlayerId: '',
  myPlayerName: '',
  myStreak: 0,
  connections: {}, // Para o Host: { peerId: conn }
  hostConn: null,  // Para os Guests: conexão com o Host
  players: [],     // [ { id, peerId, name, isHost, isBot, score, correct } ]
  activeSettings: { mode: 'mode2', rounds: 10, timer: 25 },
  currentRoundIdx: 0,
  roundItems: [],
  isMatchActive: false,
  prevRankPositions: {},
  skipVotes: new Set(),
  roundTimerInterval: null,
  roundTransitionTimeout: null,
  botTimeouts: [],
  isTransitioning: false,
  answeredPlayers: new Set(),
  timeLeft: 0,
  botCounter: 1,
  cloudPollInterval: null,
  cloudHostPollInterval: null,
  heartbeatInterval: null,
  presenceInterval: null,
  joinTimeout: null,
  pushTimer: null,
  stateVersion: 0,
  lastStateVersion: 0,
  lastStateChangeAt: 0,
  lastAppliedStatus: '',
  lastLobbySig: '',
  joinConfirmed: false,
  hostGoneHandled: false,
  podiumActive: false,
  roomSeed: 0,
  myAnsweredRound: -1,
  myVotedRound: -1,
  myPendingAnswer: null,
  processedMsgIds: new Set(),
  processedRequestKeys: new Set(),
  presenceSeen: {},
  FIREBASE_ROOMS: 'https://anime-quiz-arcade-default-rtdb.firebaseio.com/rooms',
  HOST_OFFLINE_MS: 90000,
  PLAYER_INACTIVE_MS: 45000,

  getPeerConfig() {
    return {
      debug: 1,
      secure: true,
      host: '0.peerjs.com',
      port: 443,
      path: '/',
      config: {
        iceServers: [
          { urls: 'stun:stun.l.google.com:19302' },
          { urls: 'stun:stun1.l.google.com:19302' },
          { urls: 'stun:stun2.l.google.com:19302' },
          { urls: 'stun:stun3.l.google.com:19302' },
          { urls: 'stun:stun4.l.google.com:19302' },
          { urls: 'stun:stun.cloudflare.com:3478' },
          { urls: 'stun:stun.services.mozilla.com' },
          { urls: 'stun:global.stun.twilio.com:3478' }
        ],
        iceCandidatePoolSize: 10
      }
    };
  },

  roomBase(code) {
    return `${this.FIREBASE_ROOMS}/${code || this.roomCode}`;
  },

  normalizeList(x) {
    if (Array.isArray(x)) return x.filter(v => v !== null && v !== undefined);
    if (x && typeof x === 'object') return Object.values(x).filter(v => v !== null && v !== undefined);
    return [];
  },

  cleanRoomCode(raw) {
    return (raw || '').trim().toUpperCase().replace(/[^A-Z0-9]/g, '');
  },

  clearRoundTimers() {
    if (this.roundTimerInterval) {
      clearInterval(this.roundTimerInterval);
      this.roundTimerInterval = null;
    }
    if (this.roundTransitionTimeout) {
      clearTimeout(this.roundTransitionTimeout);
      this.roundTransitionTimeout = null;
    }
    if (this.botTimeouts && this.botTimeouts.length > 0) {
      this.botTimeouts.forEach(t => clearTimeout(t));
      this.botTimeouts = [];
    }
  },

  // Limpa SOMENTE os timers da rodada (chamado no fim de cada rodada).
  // NUNCA desligar os loops de rede aqui: na v3.2.4 isso fazia o convidado
  // parar de sincronizar ao fim da 1ª rodada. Loops de rede => stopSyncLoops().
  clearAllTimers() {
    this.clearRoundTimers();
  },

  stopSyncLoops() {
    ['cloudPollInterval', 'cloudHostPollInterval', 'heartbeatInterval', 'presenceInterval'].forEach(k => {
      if (this[k]) {
        clearInterval(this[k]);
        this[k] = null;
      }
    });
    if (this.joinTimeout) { clearTimeout(this.joinTimeout); this.joinTimeout = null; }
    if (this.pushTimer) { clearTimeout(this.pushTimer); this.pushTimer = null; }
  },

  resetSyncState() {
    this.stateVersion = 0;
    this.lastStateVersion = 0;
    this.lastStateChangeAt = 0;
    this.lastAppliedStatus = '';
    this.lastLobbySig = '';
    this.joinConfirmed = false;
    this.hostGoneHandled = false;
    this.podiumActive = false;
    this.roomSeed = 0;
    this.roundItems = [];
    this.currentRoundIdx = 0;
    this.myAnsweredRound = -1;
    this.myVotedRound = -1;
    this.myPendingAnswer = null;
    this.processedMsgIds = new Set();
    this.processedRequestKeys = new Set();
    this.presenceSeen = {};
    this.connections = {};
    this.hostConn = null;
  },

  init() {
    this.ensurePlayerId();
    // Verificar parâmetro ?room= na URL para auto-preencher
    const urlParams = new URLSearchParams(window.location.search);
    const roomParam = urlParams.get('room');
    if (roomParam) {
      const codeInput = document.getElementById('mp-join-code');
      if (codeInput) codeInput.value = roomParam.toUpperCase();
      switchGameMode('mode4');
      switchMode4Tab('rooms');
    }
  },

  ensurePlayerId() {
    if (!this.myPlayerId || this.myPlayerId === '') {
      this.myPlayerId = 'p_' + Date.now() + '_' + Math.random().toString(36).substring(2, 8);
    }
    return this.myPlayerId;
  },

  getMyPlayer() {
    const id = this.ensurePlayerId();
    return this.players.find(p => p.id === id);
  },

  calculateSpeedBonus() {
    if (!this.isMatchActive) return 0;
    const totalTimer = (this.activeSettings && this.activeSettings.timer) ? this.activeSettings.timer : 25;
    if (totalTimer <= 0) return 0;
    const ratio = Math.max(0, Math.min(1, this.timeLeft / totalTimer));
    return Math.round(ratio * 100);
  },

  disambiguateName(reqName, currentPlayers) {
    let clean = (reqName || 'Otaku').trim().substring(0, 15) || 'Otaku';
    const lowerList = currentPlayers.map(p => (p.name || '').toLowerCase());
    if (!lowerList.includes(clean.toLowerCase())) {
      return clean;
    }
    let count = 2;
    while (lowerList.includes(`${clean.toLowerCase()} #${count}`)) {
      count++;
    }
    return `${clean} #${count}`;
  },

  /* ---------------------------- HOST ---------------------------- */

  createRoom() {
    this.ensurePlayerId();
    const nickInput = document.getElementById('mp-host-nick');
    const rawNick = (nickInput ? nickInput.value : '').trim() || 'Luffy';
    const mode = document.getElementById('mp-mode-select').value;
    const rounds = parseInt(document.getElementById('mp-rounds-select').value) || 10;
    const timer = parseInt(document.getElementById('mp-timer-select').value) || 25;

    this.activeSettings = { mode, rounds, timer };

    // Gera código limpo de 5 caracteres
    const letters = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
    let code = '';
    for (let i = 0; i < 5; i++) {
      code += letters.charAt(Math.floor(Math.random() * letters.length));
    }

    this.stopSyncLoops();
    this.resetSyncState();
    this.roomCode = this.cleanRoomCode(code);
    this.isHost = true;
    this.isMatchActive = false;
    this.isTransitioning = false;
    this.myPlayerName = rawNick;
    this.myStreak = 0;
    this.answeredPlayers = new Set();
    this.skipVotes = new Set();
    this.players = [{
      id: this.ensurePlayerId(),
      name: this.myPlayerName,
      isHost: true,
      score: 0,
      correct: 0
    }];
    updateGlobalKPIs();
    this.renderLobby();
    showToast(`🎉 Sala #${this.roomCode} criada! Convide seus amigos!`);

    // Nuvem primeiro (sempre funciona), P2P em paralelo (latência mínima quando a rede permite)
    this.startHostSync();
    this.setupHostPeer();
  },

  setupHostPeer() {
    try {
      if (this.peer) {
        try { this.peer.destroy(); } catch(e) {}
      }
      const peerId = `amq-v2-${this.roomCode.toLowerCase()}`;
      this.peer = new Peer(peerId, this.getPeerConfig());

      this.peer.on('open', () => {
        console.log('[MP] Canal P2P do host pronto.');
      });

      this.peer.on('connection', (conn) => {
        this.connections[conn.peer] = conn;
        conn.on('open', () => {
          try { conn.send({ type: 'ROOM_STATE', state: this.buildRoomState(true) }); } catch(e) {}
        });
        conn.on('data', (data) => {
          this.hostProcessGuestMessage(data, conn);
        });
        conn.on('close', () => {
          // Não remove o jogador: ele pode continuar pela Nuvem. Remoção é feita pela presença.
          delete this.connections[conn.peer];
        });
        conn.on('error', () => {
          delete this.connections[conn.peer];
        });
      });

      this.peer.on('error', (err) => {
        console.warn('[MP] P2P do host indisponível, seguindo pela Nuvem:', err && err.type);
      });
    } catch (e) {
      console.warn('[MP] Falha ao iniciar P2P do host, seguindo pela Nuvem.', e);
    }
  },

  startHostSync() {
    const code = this.roomCode;
    this.pushState();
    this.heartbeatInterval = setInterval(() => {
      if (!this.isHost || this.roomCode !== code) return;
      this.pushState();
    }, 1500);
    this.cloudHostPollInterval = setInterval(() => {
      if (!this.isHost || this.roomCode !== code) return;
      this.hostPollCloud(code);
    }, 1000);
  },

  hostPollCloud(code) {
    const base = this.roomBase(code);

    // 1. Pedidos de entrada (cada pedido é processado uma única vez)
    fetch(`${base}/requests.json`, { cache: 'no-store' })
      .then(r => r.json())
      .then(reqs => {
        if (!reqs || typeof reqs !== 'object' || !this.isHost || this.roomCode !== code) return;
        Object.values(reqs).forEach(req => {
          if (!req || !req.id) return;
          const key = `${req.id}_${req.timestamp || 0}`;
          if (this.processedRequestKeys.has(key)) return;
          this.processedRequestKeys.add(key);
          this.hostProcessGuestMessage({ type: 'JOIN_LOBBY', playerId: req.id, name: req.name }, null);
        });
      })
      .catch(() => {});

    // 2. Mensagens dos convidados (respostas, votos, saída) — deduplicadas por ID
    fetch(`${base}/messages.json`, { cache: 'no-store' })
      .then(r => r.json())
      .then(msgs => {
        if (!msgs || typeof msgs !== 'object' || !this.isHost || this.roomCode !== code) return;
        Object.entries(msgs).forEach(([key, msg]) => {
          if (this.processedMsgIds.has(key)) return;
          this.processedMsgIds.add(key);
          if (msg) this.hostProcessGuestMessage(msg, null);
          fetch(`${base}/messages/${key}.json`, { method: 'DELETE' }).catch(() => {});
        });
      })
      .catch(() => {});

    // 3. Presença: remove jogadores que fecharam a aba / perderam conexão
    fetch(`${base}/presence.json`, { cache: 'no-store' })
      .then(r => r.json())
      .then(pres => {
        if (!this.isHost || this.roomCode !== code) return;
        const now = Date.now();
        Object.entries(pres || {}).forEach(([pid, val]) => {
          const prev = this.presenceSeen[pid];
          if (!prev || prev.value !== val) this.presenceSeen[pid] = { value: val, seenAt: now };
        });
        this.players.filter(p => !p.isHost && !p.isBot).forEach(p => {
          const conn = p.peerId ? this.connections[p.peerId] : null;
          if (conn && conn.open) return;
          const seen = this.presenceSeen[p.id];
          if (seen && (now - seen.seenAt) > this.PLAYER_INACTIVE_MS) {
            this.removePlayer(p.id, 'saiu (conexão perdida)');
          }
        });
      })
      .catch(() => {});
  },

  buildRoomState(bump = true) {
    if (bump) this.stateVersion++;
    return {
      v: this.stateVersion,
      hostId: this.myPlayerId,
      hostName: this.myPlayerName,
      settings: this.activeSettings,
      players: this.players,
      status: this.isMatchActive ? 'playing' : (this.podiumActive ? 'podium' : 'lobby'),
      currentRoundIdx: this.currentRoundIdx || 0,
      roundItems: this.roundItems || [],
      seed: this.roomSeed || 0,
      answered: Array.from(this.answeredPlayers),
      skipVotes: Array.from(this.skipVotes),
      transitioning: !!this.isTransitioning,
      timeLeft: this.timeLeft || 0,
      updatedAt: Date.now()
    };
  },

  // Envia o estado autoritativo do host por P2P (instantâneo) e para a Nuvem (garantia)
  pushState() {
    if (!this.isHost || !this.roomCode) return;
    if (this.pushTimer) { clearTimeout(this.pushTimer); this.pushTimer = null; }
    const state = this.buildRoomState(true);
    this.sendRawToPeers({ type: 'ROOM_STATE', state });
    fetch(`${this.roomBase()}/state.json`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(state)
    }).catch(() => {});
  },

  pushStateSoon() {
    if (!this.isHost || this.pushTimer) return;
    this.pushTimer = setTimeout(() => {
      this.pushTimer = null;
      this.pushState();
    }, 120);
  },

  // Compatibilidade com chamadas antigas
  syncHostLobbyToCloud() {
    this.pushState();
  },

  sendRawToPeers(msg) {
    Object.values(this.connections).forEach(conn => {
      try { if (conn && conn.open) conn.send(msg); } catch(e) {}
    });
  },

  // Ponto ÚNICO de entrada das ações dos convidados (P2P ou Nuvem). Idempotente.
  hostProcessGuestMessage(msg, conn) {
    if (!msg || !this.isHost) return;

    if (msg.type === 'JOIN_LOBBY') {
      if (!msg.playerId) return;
      let p = this.players.find(x => x.id === msg.playerId);
      if (!p) {
        const assignedName = this.disambiguateName(msg.name, this.players);
        p = { id: msg.playerId, name: assignedName, isHost: false, score: 0, correct: 0 };
        this.players.push(p);
        showToast(`🟢 ${assignedName} entrou na sala!`);
        if (this.isMatchActive) {
          this.renderLiveSidebar();
          this.renderHudScores();
        } else if (!this.podiumActive) {
          this.renderLobby();
        }
      }
      if (!this.presenceSeen[p.id]) this.presenceSeen[p.id] = { value: 'join', seenAt: Date.now() };
      if (conn) {
        p.peerId = conn.peer;
        try { conn.send({ type: 'JOIN_CONFIRMED', assignedName: p.name, playerId: p.id }); } catch(e) {}
      }
      this.pushState();
      return;
    }

    const player = this.players.find(x => x.id === msg.playerId);
    if (!player) return;

    if (msg.type === 'ANSWER_SUBMIT') {
      if (!this.isMatchActive) return;
      if (typeof msg.roundIdx === 'number' && msg.roundIdx !== this.currentRoundIdx) return;
      if (this.answeredPlayers.has(msg.playerId)) return; // já contabilizada (chegou por P2P e Nuvem)
      player.score = (player.score || 0) + (msg.points || 0);
      if (msg.isCorrect) player.correct = (player.correct || 0) + 1;
      this.answeredPlayers.add(msg.playerId);
      this.skipVotes.add(msg.playerId);
      this.renderLiveSidebar();
      this.renderHudScores();
      updateGlobalKPIs();
      this.updateWaitingBanner();
      this.pushState();
      this.checkAllAnswered();
    } else if (msg.type === 'VOTE_SKIP') {
      if (typeof msg.roundIdx === 'number' && msg.roundIdx !== this.currentRoundIdx) return;
      this.handleSkipVote(msg.playerId);
      this.pushState();
    } else if (msg.type === 'LEAVE') {
      this.removePlayer(msg.playerId, 'saiu da sala');
    }
  },

  // Compatibilidade: mensagens P2P recebidas pelo host
  handleHostMessage(conn, msg) {
    this.hostProcessGuestMessage(msg, conn);
  },

  removePlayer(playerId, reason) {
    const p = this.players.find(x => x.id === playerId);
    if (!p || p.isHost) return;
    this.players = this.players.filter(x => x.id !== playerId);
    this.answeredPlayers.delete(playerId);
    this.skipVotes.delete(playerId);
    delete this.presenceSeen[playerId];
    if (p.peerId && this.connections[p.peerId]) {
      try { this.connections[p.peerId].close(); } catch(e) {}
      delete this.connections[p.peerId];
    }
    const base = this.roomBase();
    fetch(`${base}/requests/${playerId}.json`, { method: 'DELETE' }).catch(() => {});
    fetch(`${base}/presence/${playerId}.json`, { method: 'DELETE' }).catch(() => {});
    showToast(`🔴 ${p.name} ${reason || 'saiu da sala'}.`);
    if (this.isMatchActive) {
      this.renderLiveSidebar();
      this.renderHudScores();
      this.checkAllAnswered();
    } else if (!this.podiumActive) {
      this.renderLobby();
    }
    this.pushState();
  },

  /* --------------------------- CONVIDADO --------------------------- */

  joinRoom() {
    this.ensurePlayerId();
    const codeInput = document.getElementById('mp-join-code');
    const nickInput = document.getElementById('mp-guest-nick');
    const code = this.cleanRoomCode(codeInput ? codeInput.value : '');
    const nick = (nickInput ? nickInput.value : '').trim() || 'Zoro';

    if (!code || code.length < 3) {
      alert("Por favor, digite o código válido da sala (letras e números)!");
      return;
    }

    this.stopSyncLoops();
    this.resetSyncState();
    this.roomCode = code;
    this.isHost = false;
    this.isMatchActive = false;
    this.isTransitioning = false;
    this.myPlayerName = nick;
    this.myStreak = 0;
    this.players = [];
    this.answeredPlayers = new Set();
    this.skipVotes = new Set();
    updateGlobalKPIs();

    showToast(`🔌 Conectando à sala #${code}...`);

    // 1. Canal Nuvem (sempre ativo: garante sincronia mesmo com P2P bloqueado por roteador/4G)
    fetch(`${this.roomBase(code)}/requests/${this.myPlayerId}.json`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id: this.myPlayerId, name: nick, timestamp: Date.now() })
    }).catch(() => {});
    this.startGuestSync(code);

    // 2. Canal P2P (latência mínima quando a rede permite)
    this.connectGuestP2P(code);

    this.joinTimeout = setTimeout(() => {
      if (this.roomCode === code && !this.isHost && !this.joinConfirmed) {
        alert(`Não foi possível encontrar a sala #${code}. Confira o código e se o Host está com a sala aberta.`);
        this.leaveRoom();
      }
    }, 15000);
  },

  connectGuestP2P(code) {
    try {
      if (this.peer) {
        try { this.peer.destroy(); } catch(e) {}
      }
      this.peer = new Peer(null, this.getPeerConfig());

      this.peer.on('open', () => {
        if (this.roomCode !== code || this.isHost) return;
        const conn = this.peer.connect(`amq-v2-${code.toLowerCase()}`, { reliable: true });
        this.hostConn = conn;
        conn.on('open', () => {
          try {
            conn.send({ type: 'JOIN_LOBBY', playerId: this.ensurePlayerId(), name: this.myPlayerName });
          } catch(e) {}
        });
        conn.on('data', (data) => {
          this.handleGuestMessage(data);
        });
        conn.on('close', () => {
          if (this.hostConn === conn) this.hostConn = null; // segue pela Nuvem
        });
        conn.on('error', () => {
          if (this.hostConn === conn) this.hostConn = null;
        });
      });

      this.peer.on('error', (err) => {
        console.warn('[MP] P2P indisponível, seguindo pela Nuvem:', err && err.type);
      });
    } catch (e) {
      console.warn('[MP] Falha ao iniciar P2P do convidado, seguindo pela Nuvem.', e);
    }
  },

  startGuestSync(code) {
    const base = this.roomBase(code);

    const poll = () => {
      if (this.isHost || this.roomCode !== code) return;
      fetch(`${base}/state.json`, { cache: 'no-store' })
        .then(r => r.json())
        .then(state => {
          if (this.isHost || this.roomCode !== code) return;
          if (state === null) {
            if (this.joinConfirmed) this.handleHostGone('A sala foi encerrada pelo Host.');
            return;
          }
          this.applyRoomState(state, false);
        })
        .catch(() => {});

      if (this.joinConfirmed && this.lastStateChangeAt && (Date.now() - this.lastStateChangeAt) > this.HOST_OFFLINE_MS) {
        this.handleHostGone('O Host ficou offline. A sala foi encerrada.');
      }
    };

    const ping = () => {
      if (this.isHost || this.roomCode !== code) return;
      fetch(`${base}/presence/${this.myPlayerId}.json`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(Date.now())
      }).catch(() => {});
    };

    poll();
    ping();
    this.cloudPollInterval = setInterval(poll, 900);
    this.presenceInterval = setInterval(ping, 3000);
  },

  // Envia ação ao host pelos DOIS canais (o host deduplica)
  sendToHost(msg) {
    if (this.hostConn && this.hostConn.open) {
      try { this.hostConn.send(msg); } catch(e) {}
    }
    this.sendCloudMessage(msg);
  },

  sendCloudMessage(msg, code) {
    const room = code || this.roomCode;
    if (!room) return;
    const msgId = 'm_' + Date.now() + '_' + Math.random().toString(36).substring(2, 8);
    fetch(`${this.roomBase(room)}/messages/${msgId}.json`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(msg)
    }).catch(() => {});
  },

  // Aplica o estado autoritativo do host (versão maior sempre vence)
  applyRoomState(state, fromP2P = false) {
    if (this.isHost || !state || typeof state.v !== 'number') return;
    if (state.v <= this.lastStateVersion) return;
    this.lastStateVersion = state.v;
    this.lastStateChangeAt = Date.now();

    const players = this.normalizeList(state.players);
    const answered = this.normalizeList(state.answered);
    const votes = this.normalizeList(state.skipVotes);
    if (state.settings) this.activeSettings = state.settings;
    if (players.length) this.players = players;

    const amIn = this.players.some(p => p.id === this.myPlayerId);
    if (!this.joinConfirmed) {
      if (!amIn) return; // host ainda não processou a entrada
      this.joinConfirmed = true;
      if (this.joinTimeout) { clearTimeout(this.joinTimeout); this.joinTimeout = null; }
      showToast(`✅ Você entrou na sala #${this.roomCode}!`);
    } else if (!amIn) {
      this.handleHostGone('Você foi desconectado da sala (conexão perdida).');
      return;
    }

    const me = this.getMyPlayer();
    if (me && me.name) this.myPlayerName = me.name;

    const status = state.status || 'lobby';
    const idx = Number(state.currentRoundIdx) || 0;
    const seed = Number(state.seed) || 0;

    // Pontuação otimista: mantém minha resposta visível até o host confirmá-la (e reenvia se preciso)
    if (this.myPendingAnswer) {
      const pend = this.myPendingAnswer;
      const confirmed = status === 'playing' && idx === pend.roundIdx && answered.includes(this.myPlayerId);
      const expired = status !== 'playing' || idx !== pend.roundIdx;
      if (confirmed || expired) {
        this.myPendingAnswer = null;
      } else {
        if (me) {
          me.score = (me.score || 0) + pend.points;
          if (pend.isCorrect) me.correct = (me.correct || 0) + 1;
        }
        if (Date.now() - pend.sentAt > 2500) {
          pend.sentAt = Date.now();
          this.sendToHost({ type: 'ANSWER_SUBMIT', playerId: this.myPlayerId, roundIdx: pend.roundIdx, isCorrect: pend.isCorrect, points: pend.points });
        }
      }
    }

    if (status === 'playing') {
      const isNewMatch = !this.isMatchActive || (seed && seed !== this.roomSeed);
      if (isNewMatch) {
        this.roundItems = this.normalizeList(state.roundItems);
        this.roomSeed = seed;
        this.isMatchActive = true;
        this.myStreak = 0;
        this.prevRankPositions = {};
        this.myAnsweredRound = -1;
        this.myVotedRound = -1;

        // Zerar contadores solo para garantir isolamento
        m1Score = 0; m1CorrectCount = 0; m1Streak = 0;
        m2Score = 0; m2CorrectCount = 0; m2Streak = 0;
        m3Score = 0; m3CorrectCount = 0; m3Streak = 0;

        this.startRound(idx);
      } else if (idx > this.currentRoundIdx) {
        this.startRound(idx); // alcança o host (nunca volta rodada)
      }

      if (idx === this.currentRoundIdx) {
        const ans = new Set(answered);
        if (this.myAnsweredRound === idx) ans.add(this.myPlayerId);
        this.answeredPlayers = ans;
        const vs = new Set(votes);
        if (this.myVotedRound === idx || this.myAnsweredRound === idx) vs.add(this.myPlayerId);
        this.skipVotes = vs;

        if (state.transitioning && !this.isTransitioning) {
          this.isTransitioning = true;
          this.clearRoundTimers();
          const banner = document.getElementById('mp-waiting-banner');
          if (banner) {
            banner.style.display = 'flex';
            banner.className = 'mp-waiting-banner all-done';
            banner.innerHTML = `
              <div style="display: flex; align-items: center; gap: 8px;">
                <span style="font-size: 16px;">✨</span>
                <span>Rodada encerrada! Preparando a próxima...</span>
              </div>
            `;
          }
        } else if (!this.isTransitioning && this.activeSettings.timer > 0 && typeof state.timeLeft === 'number') {
          // Corrige desvio do cronômetro em relação ao host
          const drift = this.timeLeft - state.timeLeft;
          if ((fromP2P && Math.abs(drift) >= 2) || (!fromP2P && drift >= 3)) {
            this.timeLeft = Math.max(1, state.timeLeft);
          }
        }
      }

      this.renderLiveSidebar();
      this.renderHudScores();
      updateGlobalKPIs();
      const total = this.players.length;
      this.updateSkipUI(this.skipVotes.size, total, Math.floor(total / 2) + 1);
      this.updateWaitingBanner();
    } else if (status === 'podium') {
      if (this.lastAppliedStatus !== 'podium') {
        this.lastAppliedStatus = 'podium';
        this.showPodium(this.players);
      }
    } else {
      if (this.isMatchActive) {
        this.isMatchActive = false;
        this.isTransitioning = false;
        this.clearRoundTimers();
        stopAllMedia();
        this.lastLobbySig = '';
      }
      const sig = JSON.stringify([this.players.map(p => [p.id, p.name]), this.activeSettings]);
      if (sig !== this.lastLobbySig || this.lastAppliedStatus !== 'lobby') {
        this.lastLobbySig = sig;
        this.renderLobby();
      }
    }
    this.lastAppliedStatus = status;
  },

  handleHostGone(message) {
    if (this.hostGoneHandled || this.isHost || !this.roomCode) return;
    this.hostGoneHandled = true;
    this.leaveRoom();
    setTimeout(() => alert(`🚪 ${message}`), 50);
  },

  handleGuestMessage(msg) {
    if (!msg || this.isHost) return;
    if (msg.type === 'ROOM_STATE') {
      this.applyRoomState(msg.state, true);
    } else if (msg.type === 'JOIN_CONFIRMED') {
      if (msg.assignedName) this.myPlayerName = msg.assignedName;
    } else if (msg.type === 'FAST_SKIP') {
      if (this.isMatchActive) this.executeFastSkipEffect();
    } else if (msg.type === 'ALL_ANSWERED') {
      if (!this.isMatchActive || this.isTransitioning) return;
      this.isTransitioning = true;
      this.clearRoundTimers();
      const banner = document.getElementById('mp-waiting-banner');
      if (banner) {
        banner.style.display = 'flex';
        banner.className = 'mp-waiting-banner all-done';
        banner.innerHTML = `
          <div style="display: flex; align-items: center; gap: 8px;">
            <span style="font-size: 16px;">✨</span>
            <span>Todos os jogadores responderam! Preparando próxima rodada...</span>
          </div>
        `;
      }
    } else if (msg.type === 'MATCH_OVER') {
      if (this.lastAppliedStatus !== 'podium') {
        this.lastAppliedStatus = 'podium';
        this.showPodium(msg.players || this.players);
      }
    }
    // Demais estados (placar, rodada, respostas, lobby) chegam consolidados em ROOM_STATE.
  },

  broadcastAnsweredState() {
    this.broadcast({
      type: 'ANSWERED_STATE',
      answered: Array.from(this.answeredPlayers),
      votes: this.skipVotes.size,
      total: this.players.length
    });
  },

  addTestBot() {
    const botNames = ['Zoro', 'Sanji', 'Nami', 'Chopper', 'Robin', 'Franky', 'Brook', 'Goku', 'Vegeta'];
    const chosen = botNames[this.botCounter % botNames.length];
    this.botCounter++;
    const botName = this.disambiguateName(chosen, this.players);
    const bot = {
      id: 'bot_' + Date.now() + '_' + Math.random().toString(36).substring(2, 5),
      name: botName,
      isHost: false,
      isBot: true,
      score: 0,
      correct: 0
    };
    this.players.push(bot);
    this.broadcastLobby();
    this.renderLobby();
    showToast(`🤖 ${botName} (Bot) entrou na sala!`);
  },

  broadcast(msg) {
    this.sendRawToPeers(msg);
    if (this.isHost && msg && msg.type !== 'ROOM_STATE') this.pushStateSoon();
  },

  broadcastLobby() {
    this.broadcast({
      type: 'LOBBY_STATE',
      players: this.players,
      settings: this.activeSettings
    });
  },

  broadcastScores() {
    this.broadcast({
      type: 'SCORE_UPDATE',
      players: this.players
    });
  },

  copyRoomCode() {
    navigator.clipboard.writeText(this.roomCode).then(() => {
      showToast(`📋 Código #${this.roomCode} copiado com sucesso!`);
    }).catch(() => {
      prompt("Copie o código da sala:", this.roomCode);
    });
  },

  confirmLeaveRoom() {
    if (confirm("🚪 Deseja realmente sair da sala e abandonar a partida?")) {
      this.leaveRoom();
      showToast("🚪 Você saiu da sala.");
    }
  },

  leaveRoom() {
    stopAllMedia();
    const code = this.roomCode;
    const wasHost = this.isHost;
    const pid = this.myPlayerId;
    this.stopSyncLoops();
    if (code) {
      const base = this.roomBase(code);
      if (wasHost) {
        const del = () => fetch(`${base}.json`, { method: 'DELETE' }).catch(() => {});
        del();
        setTimeout(del, 1500); // garante limpeza mesmo se um PUT atrasado chegar depois
      } else if (pid) {
        try { if (this.hostConn && this.hostConn.open) this.hostConn.send({ type: 'LEAVE', playerId: pid }); } catch(e) {}
        this.sendCloudMessage({ type: 'LEAVE', playerId: pid }, code);
        fetch(`${base}/requests/${pid}.json`, { method: 'DELETE' }).catch(() => {});
        fetch(`${base}/presence/${pid}.json`, { method: 'DELETE' }).catch(() => {});
      }
    }
    const oldPeer = this.peer;
    this.peer = null;
    if (oldPeer) setTimeout(() => { try { oldPeer.destroy(); } catch(e) {} }, 300);
    seededRand = null;
    this.isHost = false;
    this.roomCode = '';
    this.isMatchActive = false;
    this.isTransitioning = false;
    this.players = [];
    this.skipVotes.clear();
    this.answeredPlayers.clear();
    this.clearRoundTimers();
    this.prevRankPositions = {};
    this.myStreak = 0;
    this.resetSyncState();

    // Isolamento absoluto: zerar acumuladores de modos solo ao sair da sala
    m1Score = 0; m1CorrectCount = 0; m1Streak = 0; m1Attempts = 0; m1PlaylistIndex = 0; m1Playlist = [];
    m2Score = 0; m2CorrectCount = 0; m2Streak = 0; m2RoundsPlayed = 0; m2UnplayedQueue = [];
    m3Score = 0; m3CorrectCount = 0; m3Streak = 0; m3RoundsPlayed = 0; m3UnplayedQueue = [];

    updateGlobalKPIs();

    const banner = document.getElementById('mp-waiting-banner');
    if (banner) banner.style.display = 'none';

    const timerPill = document.getElementById('mp-hud-timer-pill');
    if (timerPill) {
      timerPill.classList.remove('panic');
      timerPill.style.display = 'none';
    }

    const hudBar = document.getElementById('mp-hud-bar');
    if (hudBar) hudBar.style.display = 'none';
    const sidebar = document.getElementById('mp-live-sidebar');
    if (sidebar) sidebar.style.display = 'none';

    const preView = document.getElementById('mp-pre-room-view');
    const lobbyView = document.getElementById('mp-lobby-view');
    const podiumView = document.getElementById('mp-podium-view');
    if (preView) preView.style.display = 'block';
    if (lobbyView) lobbyView.style.display = 'none';
    if (podiumView) podiumView.style.display = 'none';

    switchGameMode('mode4', true);
    switchMode4Tab('rooms');
    updateGlobalKPIs();
  },

  renderLobby() {
    updateGlobalKPIs();
    const hudBar = document.getElementById('mp-hud-bar');
    if (hudBar) hudBar.style.display = 'none';
    const sidebar = document.getElementById('mp-live-sidebar');
    if (sidebar) sidebar.style.display = 'none';

    const preView = document.getElementById('mp-pre-room-view');
    const lobbyView = document.getElementById('mp-lobby-view');
    const podiumView = document.getElementById('mp-podium-view');
    if (preView) preView.style.display = 'none';
    if (lobbyView) lobbyView.style.display = 'block';
    if (podiumView) podiumView.style.display = 'none';

    document.getElementById('mp-lobby-code-text').textContent = this.roomCode;
    document.getElementById('mp-lobby-count').textContent = this.players.length;

    let modeLabel = '🎵 Qual é a Abertura';
    if (this.activeSettings.mode === 'mode1') modeLabel = '🎧 Blind Test';
    if (this.activeSettings.mode === 'mode3') modeLabel = '🖼️ Adivinhe a Cena';
    if (this.activeSettings.mode === 'mixed') modeLabel = '🎲 Misto (Músicas & Cenas)';

    const pills = document.getElementById('mp-lobby-meta-pills');
    if (pills) {
      pills.innerHTML = `
        <span class="pill-chip">${modeLabel}</span>
        <span class="pill-chip">🏁 ${this.activeSettings.rounds} Rodadas</span>
        <span class="pill-chip">⏱️ ${this.activeSettings.timer > 0 ? `${this.activeSettings.timer}s por rodada` : 'Sem Limite'}</span>
      `;
    }

    const grid = document.getElementById('mp-lobby-players-grid');
    if (grid) {
      grid.innerHTML = '';
      this.players.forEach(p => {
        const isMe = (p.id === this.myPlayerId);
        const card = document.createElement('div');
        card.className = 'player-slot-card';
        card.innerHTML = `
          <div class="player-slot-avatar">${(p.name || 'O').charAt(0).toUpperCase()}</div>
          <div style="overflow: hidden;">
            <div class="player-slot-name">${escapeHtml(p.name)} ${isMe ? '<span style="color: var(--accent); font-size: 11px;">(Você)</span>' : ''}</div>
            <div class="player-slot-role">${p.isHost ? '👑 Host da Sala' : (p.isBot ? '🤖 Bot de Teste' : '🟢 Conectado')}</div>
          </div>
        `;
        grid.appendChild(card);
      });
    }

    const hostActions = document.getElementById('mp-lobby-host-actions');
    const guestWaiting = document.getElementById('mp-lobby-guest-waiting');
    if (this.isHost) {
      if (hostActions) hostActions.style.display = 'block';
      if (guestWaiting) guestWaiting.style.display = 'none';
    } else {
      if (hostActions) hostActions.style.display = 'none';
      if (guestWaiting) guestWaiting.style.display = 'block';
    }
  },

  startGame() {
    if (!this.isHost) return;
    const rounds = this.activeSettings.rounds;

    this.roomSeed = Math.floor(Math.random() * 1000000) + 1;
    const totalItems = (this.activeSettings.mode === 'mode3' ? ALL_SCENES : ALL_SONGS).length;
    const shuffled = Array.from({ length: totalItems }, (_, i) => i).sort(() => Math.random() - 0.5);
    this.roundItems = shuffled.slice(0, rounds);

    this.podiumActive = false;
    this.isMatchActive = true;
    this.isTransitioning = false;
    this.currentRoundIdx = 0;
    this.myAnsweredRound = -1;
    this.myVotedRound = -1;
    this.answeredPlayers.clear();
    this.skipVotes.clear();

    // Zerar contadores solo para garantir isolamento
    m1Score = 0; m1CorrectCount = 0; m1Streak = 0;
    m2Score = 0; m2CorrectCount = 0; m2Streak = 0;
    m3Score = 0; m3CorrectCount = 0; m3Streak = 0;

    this.broadcast({
      type: 'MATCH_START',
      settings: this.activeSettings,
      roundItems: this.roundItems,
      seed: this.roomSeed
    });

    this.startRound(0);
    this.pushState();
  },

  startRound(idx) {
    stopAllMedia();
    this.clearRoundTimers();
    this.isTransitioning = false;
    this.currentRoundIdx = idx;
    this.skipVotes.clear();
    this.answeredPlayers.clear();

    const banner = document.getElementById('mp-waiting-banner');
    if (banner) {
      banner.style.display = 'none';
      banner.className = 'mp-waiting-banner';
    }

    if (this.roomSeed) {
      seededRand = mulberry32(this.roomSeed + idx * 7919);
    }

    const hudBar = document.getElementById('mp-hud-bar');
    if (hudBar) hudBar.style.display = 'flex';
    const sidebar = document.getElementById('mp-live-sidebar');
    if (sidebar) sidebar.style.display = 'flex';

    document.getElementById('mp-hud-room-badge').textContent = `🎮 SALA #${this.roomCode}`;
    document.getElementById('mp-hud-round-pill').textContent = `Rodada ${idx + 1} de ${this.activeSettings.rounds}`;

    this.renderHudScores();
    this.renderLiveSidebar();
    updateGlobalKPIs();
    this.updateSkipUI(0, this.players.length, Math.floor(this.players.length / 2) + 1);

    const btn = document.getElementById('mp-skip-vote-btn');
    if (btn) btn.classList.remove('voted');

    const timerPill = document.getElementById('mp-hud-timer-pill');
    if (this.activeSettings.timer > 0) {
      this.timeLeft = this.activeSettings.timer;
      if (timerPill) {
        timerPill.style.display = 'inline-flex';
        timerPill.classList.remove('panic');
        timerPill.textContent = `⏱️ ${this.timeLeft}s`;
      }
      this.roundTimerInterval = setInterval(() => {
        this.timeLeft--;

        if (this.timeLeft <= 5 && this.timeLeft > 0) {
          if (timerPill) {
            timerPill.classList.add('panic');
            timerPill.textContent = `🚨 0${this.timeLeft}s`;
          }
          if (AudioManager && typeof AudioManager.playCountdownBeep === 'function') {
            AudioManager.playCountdownBeep(this.timeLeft);
          }
        } else {
          if (timerPill) {
            timerPill.classList.remove('panic');
            timerPill.textContent = `⏱️ ${this.timeLeft}s`;
          }
        }

        if (this.timeLeft <= 0) {
          if (timerPill) {
            timerPill.classList.add('panic');
            timerPill.textContent = `⏰ 00s`;
          }
          this.clearAllTimers();
          this.triggerTimeUp();
        }
      }, 1000);
    } else {
      if (timerPill) timerPill.style.display = 'none';
    }

    let roundMode = this.activeSettings.mode;
    if (roundMode === 'mixed') {
      roundMode = (idx % 2 === 0) ? 'mode2' : 'mode3';
    }

    const itemIdx = this.roundItems[idx] || 0;

    // Garantir que as telas de pré-sala, lobby e podium fiquem estritamente ocultas durante a partida
    const lobbyView = document.getElementById('mp-lobby-view');
    if (lobbyView) lobbyView.style.display = 'none';
    const preView = document.getElementById('mp-pre-room-view');
    if (preView) preView.style.display = 'none';
    const podiumView = document.getElementById('mp-podium-view');
    if (podiumView) podiumView.style.display = 'none';

    if (roundMode === 'mode2') {
      switchGameMode('mode2', true);
      m2CurrentIndex = itemIdx % ALL_SONGS.length;
      m2RoundsPlayed = idx + 1;
      m2InitRound();
    } else if (roundMode === 'mode1') {
      switchGameMode('mode1', true);
      m1CurrentIndex = itemIdx % ALL_SONGS.length;
      m1PlaylistIndex = itemIdx % ALL_SONGS.length;
      m1LoadSong(true);
    } else if (roundMode === 'mode3') {
      switchGameMode('mode3', true);
      m3CurrentIndex = itemIdx % ALL_SCENES.length;
      m3RoundsPlayed = idx + 1;
      m3InitScene();
      if (this.roundItems && this.roundItems[idx + 1] !== undefined) {
        const nextScene = ALL_SCENES[this.roundItems[idx + 1] % ALL_SCENES.length];
        if (nextScene && nextScene.image_url) {
          const preImg = new Image();
          preImg.referrerPolicy = 'no-referrer';
          preImg.src = nextScene.image_url;
        }
      }
    }

    updateGlobalKPIs();

    if (this.isHost) {
      this.simulateBotActions();
    }
  },

  simulateBotActions() {
    const bots = this.players.filter(p => p.isBot);
    bots.forEach(bot => {
      const delayMs = 3000 + Math.random() * 5000;
      const t = setTimeout(() => {
        if (!this.isMatchActive || this.isTransitioning) return;
        const correct = Math.random() > 0.35;
        let pts = 0;
        if (correct) {
          const totalSec = this.activeSettings.timer > 0 ? this.activeSettings.timer : 25;
          const elapsedSec = Math.min(totalSec, delayMs / 1000);
          const timeBonus = Math.max(0, Math.round(((totalSec - elapsedSec) / totalSec) * 100));
          pts = 100 + timeBonus;
        }
        bot.score += pts;
        if (correct) bot.correct += 1;
        this.answeredPlayers.add(bot.id);
        this.skipVotes.add(bot.id);

        this.broadcastScores();
        this.broadcastAnsweredState();
        this.renderLiveSidebar();
        this.renderHudScores();
        updateGlobalKPIs();

        this.checkAllAnswered();
      }, delayMs);
      this.botTimeouts.push(t);
    });
  },

  renderHudScores() {
    const container = document.getElementById('mp-hud-scores-list');
    if (!container) return;
    container.innerHTML = '';
    const sorted = [...this.players].sort((a, b) => b.score - a.score);

    sorted.slice(0, 4).forEach((p, idx) => {
      const isMe = (p.id === this.myPlayerId);
      const pill = document.createElement('div');
      pill.className = `mp-hud-player-pill ${isMe ? 'is-me' : ''}`;
      const medal = idx === 0 ? '🥇 ' : (idx === 1 ? '🥈 ' : (idx === 2 ? '🥉 ' : ''));
      pill.innerHTML = `<span>${medal}${escapeHtml(p.name)}:</span> <span style="color: var(--gold);">${p.score}</span>`;
      container.appendChild(pill);
    });
  },

  renderLiveSidebar() {
    const list = document.getElementById('mp-sidebar-list');
    if (!list) return;

    if (!this.prevRankPositions) this.prevRankPositions = {};
    if (!this.prevScores) this.prevScores = {};
    if (!this.scoreDeltas) this.scoreDeltas = {};
    const now = Date.now();
    const DELTA_MS = 2200;

    const sorted = [...this.players].sort((a, b) => {
      if (b.score !== a.score) return b.score - a.score;
      return (b.correct || 0) - (a.correct || 0);
    });

    list.innerHTML = '';
    const newPositions = {};

    sorted.forEach((p, idx) => {
      const currentRank = idx + 1;
      const prevRank = this.prevRankPositions[p.id];
      newPositions[p.id] = currentRank;

      // Detectar ganho de pontos desde o último render
      const prevScore = this.prevScores[p.id];
      if (prevScore !== undefined && p.score > prevScore) {
        this.scoreDeltas[p.id] = { amount: p.score - prevScore, ts: now };
        setTimeout(() => this.renderLiveSidebar(), DELTA_MS + 50);
      }
      this.prevScores[p.id] = p.score;

      let deltaHtml = '';
      const d = this.scoreDeltas[p.id];
      if (d && (now - d.ts) < DELTA_MS) {
        const elapsed = now - d.ts;
        deltaHtml = `<span class="mp-rank-delta" style="animation-delay: -${elapsed}ms;">+${d.amount}</span>`;
      }

      let trendHtml = '';
      if (prevRank !== undefined) {
        if (currentRank < prevRank) {
          trendHtml = `<span class="mp-rank-trend up" title="Subiu ${prevRank - currentRank} posições">▲${prevRank - currentRank}</span>`;
        } else if (currentRank > prevRank) {
          trendHtml = `<span class="mp-rank-trend down" title="Caiu ${currentRank - prevRank} posições">▼${currentRank - prevRank}</span>`;
        }
      }

      const isMe = (p.id === this.myPlayerId);
      const medal = currentRank === 1 ? '🥇' : (currentRank === 2 ? '🥈' : (currentRank === 3 ? '🥉' : `${currentRank}º`));

      const hasAnswered = this.answeredPlayers && this.answeredPlayers.has(p.id);
      const statusBadge = hasAnswered 
        ? '<span class="mp-player-status-badge answered"><img src="icons/check.png" class="app-icon app-icon-sm icon-raw" /> Respondido</span>' 
        : '<span class="mp-player-status-badge thinking"><img src="icons/shuffle-arrows.png" class="app-icon app-icon-sm icon-white" /> Pensando...</span>';

      const isScoring = d && (now - d.ts) < DELTA_MS;
      const item = document.createElement('div');
      item.className = `mp-player-rank-item ${isMe ? 'is-me' : ''} ${currentRank === 1 && p.score > 0 ? 'mp-first-place' : ''} ${isScoring ? 'scoring-glow' : ''}`;
      item.innerHTML = `
        <div class="mp-rank-pos-badge">${medal}</div>
        <div class="mp-rank-avatar">${(p.name || 'P').charAt(0).toUpperCase()}</div>
        <div class="mp-rank-info">
          <div class="mp-rank-name">
            <span class="mp-rank-name-text">${escapeHtml(p.name)}</span>
            ${isMe ? '<span style="color: #a5b4fc; font-size: 10px;">(Você)</span>' : ''}
            ${p.isBot ? '<span style="font-size: 10px;">🤖</span>' : ''}
            ${trendHtml}
          </div>
          <div class="mp-rank-stats">
            <span><img src="icons/check.png" class="app-icon app-icon-sm icon-raw" /> ${p.correct || 0} acertos</span>
            ${statusBadge}
          </div>
        </div>
        <div class="mp-rank-points-col">
          <div class="mp-rank-points">${p.score} <span style="font-size: 10px; color: #94a3b8;">pts</span></div>
          ${deltaHtml}
        </div>
      `;
      list.appendChild(item);
    });

    this.prevRankPositions = newPositions;
  },

  checkAllAnswered() {
    if (this.isTransitioning || !this.isMatchActive) return;
    const total = this.players.length;
    const answeredCount = this.answeredPlayers.size;

    if (answeredCount >= total && total > 0) {
      this.isTransitioning = true;
      this.clearAllTimers();

      const banner = document.getElementById('mp-waiting-banner');
      if (banner) {
        banner.style.display = 'flex';
        banner.className = 'mp-waiting-banner all-done';
        banner.innerHTML = `
          <div style="display: flex; align-items: center; gap: 8px;">
            <span style="font-size: 16px;">✨</span>
            <span>Todos os jogadores responderam! Preparando próxima rodada...</span>
          </div>
        `;
      }
      showToast('✨ Todos responderam! Avançando em 2 segundos...');

      if (this.isHost) {
        this.broadcast({ type: 'ALL_ANSWERED' });
        this.roundTransitionTimeout = setTimeout(() => {
          if (!this.isMatchActive) return;
          this.advanceOrEndRound();
        }, 2000);
      }
    } else {
      this.updateWaitingBanner();
    }
  },

  updateWaitingBanner() {
    const banner = document.getElementById('mp-waiting-banner');
    if (!banner || !this.isMatchActive) return;

    const meAnswered = this.answeredPlayers.has(this.myPlayerId);
    if (!meAnswered) {
      banner.style.display = 'none';
      return;
    }

    if (this.isTransitioning) return;

    const total = this.players.length;
    const answeredCount = this.answeredPlayers.size;
    const votes = this.skipVotes.size;

    banner.style.display = 'flex';
    banner.className = 'mp-waiting-banner';
    banner.innerHTML = `
      <div style="display: flex; align-items: center; gap: 8px;">
        <span style="font-size: 16px;">⏳</span>
        <span>Sua resposta foi registrada! Aguardando demais jogadores (<strong>${answeredCount}/${total}</strong>)...</span>
      </div>
      <span style="font-size: 11px; color: #94a3b8; background: rgba(0,0,0,0.3); padding: 3px 8px; border-radius: 999px;">
        ${votes}/${total} votos para pular
      </span>
    `;
  },

  voteSkip(silent = false) {
    if (this.isTransitioning || !this.isMatchActive) return;
    const btn = document.getElementById('mp-skip-vote-btn');
    if (btn) btn.classList.add('voted');

    const alreadyVoted = this.skipVotes.has(this.myPlayerId);
    if (!silent) {
      if (alreadyVoted) {
        showToast('⏳ Seu voto já está registrado! Aguardando demais jogadores...');
      } else {
        showToast('⏩ Voto para avançar registrado! Avança quando mais de 50% votarem.');
      }
    }

    this.myVotedRound = this.currentRoundIdx;
    if (this.isHost) {
      this.handleSkipVote(this.myPlayerId);
    } else {
      this.skipVotes.add(this.myPlayerId);
      this.sendToHost({
        type: 'VOTE_SKIP',
        playerId: this.myPlayerId,
        roundIdx: this.currentRoundIdx
      });
    }
  },

  handleSkipVote(playerId) {
    if (this.isTransitioning || !this.isMatchActive) return;
    this.skipVotes.add(playerId);
    const total = this.players.length;
    const votes = this.skipVotes.size;
    const threshold = Math.floor(total / 2) + 1; // Estritamente > 50% dos votos

    this.broadcast({
      type: 'SKIP_UPDATE',
      votes,
      total,
      threshold
    });
    this.updateSkipUI(votes, total, threshold);
    this.updateWaitingBanner();

    if (votes >= threshold) {
      this.executeFastSkipEffect();
      this.broadcast({ type: 'FAST_SKIP' });
    }
  },

  updateSkipUI(votes, total, threshold) {
    const badge = document.getElementById('mp-skip-count-badge');
    if (badge) {
      badge.textContent = `${votes}/${total} (meta: ${threshold})`;
    }
  },

  executeFastSkipEffect() {
    if (this.isTransitioning) return;
    this.isTransitioning = true;
    this.clearAllTimers();

    AudioManager.playSfx('tab');
    showToast(`⏩ Mais de 50% dos jogadores votaram para pular! Avançando...`);

    const banner = document.getElementById('mp-waiting-banner');
    if (banner) {
      banner.style.display = 'flex';
      banner.className = 'mp-waiting-banner all-done';
      banner.innerHTML = `
        <div style="display: flex; align-items: center; gap: 8px;">
          <span style="font-size: 16px;">⏩</span>
          <span>Mais de 50% votaram para pular! Avançando para a próxima rodada...</span>
        </div>
      `;
    }

    if (this.isHost) {
      this.roundTransitionTimeout = setTimeout(() => {
        if (!this.isMatchActive) return;
        this.advanceOrEndRound();
      }, 1600);
    }
  },

  triggerTimeUp() {
    if (this.isTransitioning) return;
    this.isTransitioning = true;
    this.clearAllTimers();

    AudioManager.playSfx('wrong');
    showToast(`⏰ Tempo esgotado para esta rodada!`);

    const banner = document.getElementById('mp-waiting-banner');
    if (banner) {
      banner.style.display = 'flex';
      banner.className = 'mp-waiting-banner all-done';
      banner.innerHTML = `
        <div style="display: flex; align-items: center; gap: 8px;">
          <span style="font-size: 16px;">⏰</span>
          <span>Tempo esgotado! Avançando para a próxima rodada...</span>
        </div>
      `;
    }

    if (this.isHost) {
      this.pushState();
      this.roundTransitionTimeout = setTimeout(() => {
        if (!this.isMatchActive) return;
        this.advanceOrEndRound();
      }, 2000);
    }
  },

  onPlayerAnswer(isCorrect, points) {
    if (!this.isMatchActive || this.isTransitioning) return;
    if (this.myAnsweredRound === this.currentRoundIdx) return; // uma resposta por rodada
    this.myAnsweredRound = this.currentRoundIdx;
    const me = this.getMyPlayer();
    if (me) {
      me.score += (points || 0);
      if (isCorrect) {
        me.correct += 1;
        this.myStreak = (this.myStreak || 0) + 1;
      } else {
        this.myStreak = 0;
      }
    }
    this.answeredPlayers.add(this.myPlayerId);
    this.skipVotes.add(this.myPlayerId);

    updateGlobalKPIs();
    this.renderLiveSidebar();
    this.renderHudScores();
    this.updateWaitingBanner();

    const btn = document.getElementById('mp-skip-vote-btn');
    if (btn) btn.classList.add('voted');

    if (!this.isHost) {
      const pts = points || 0;
      this.myPendingAnswer = { roundIdx: this.currentRoundIdx, points: pts, isCorrect: !!isCorrect, sentAt: Date.now() };
      this.sendToHost({
        type: 'ANSWER_SUBMIT',
        playerId: this.myPlayerId,
        roundIdx: this.currentRoundIdx,
        isCorrect: !!isCorrect,
        points: pts
      });
    } else {
      this.broadcastScores();
      this.broadcastAnsweredState();
      this.pushState();
      this.checkAllAnswered();
    }
  },

  advanceOrEndRound() {
    if (!this.isHost) return;
    this.clearRoundTimers();
    if (this.currentRoundIdx + 1 < this.activeSettings.rounds) {
      const nextIdx = this.currentRoundIdx + 1;
      // Atualiza o índice ANTES de publicar (bug v3.2.4: a nuvem recebia a rodada antiga)
      this.startRound(nextIdx);
      this.broadcast({ type: 'SYNC_ROUND', roundIdx: nextIdx });
      this.pushState();
    } else {
      this.endMatch();
    }
  },

  endMatch() {
    this.isMatchActive = false;
    this.isTransitioning = false;
    this.podiumActive = true;
    this.myStreak = 0;
    seededRand = null;
    this.clearRoundTimers();
    this.pushState();
    updateGlobalKPIs();
    const hudBar = document.getElementById('mp-hud-bar');
    if (hudBar) hudBar.style.display = 'none';
    const sidebar = document.getElementById('mp-live-sidebar');
    if (sidebar) sidebar.style.display = 'none';

    const banner = document.getElementById('mp-waiting-banner');
    if (banner) banner.style.display = 'none';

    this.broadcast({ type: 'MATCH_OVER', players: this.players });
    this.showPodium(this.players);
  },

  showPodium(finalPlayers) {
    this.isMatchActive = false;
    this.clearAllTimers();
    this.isTransitioning = false;

    // Resetar acumuladores de modos solo para não contaminar nada após a partida
    m1Score = 0; m1CorrectCount = 0; m1Streak = 0; m1Attempts = 0; m1PlaylistIndex = 0; m1Playlist = [];
    m2Score = 0; m2CorrectCount = 0; m2Streak = 0; m2RoundsPlayed = 0; m2UnplayedQueue = [];
    m3Score = 0; m3CorrectCount = 0; m3Streak = 0; m3RoundsPlayed = 0; m3UnplayedQueue = [];

    const hudBar = document.getElementById('mp-hud-bar');
    if (hudBar) hudBar.style.display = 'none';
    const sidebar = document.getElementById('mp-live-sidebar');
    if (sidebar) sidebar.style.display = 'none';

    const banner = document.getElementById('mp-waiting-banner');
    if (banner) banner.style.display = 'none';

    switchGameMode('mode4', true);
    switchMode4Tab('rooms');
    updateGlobalKPIs();

    const preView = document.getElementById('mp-pre-room-view');
    const lobbyView = document.getElementById('mp-lobby-view');
    const podiumView = document.getElementById('mp-podium-view');
    if (preView) preView.style.display = 'none';
    if (lobbyView) lobbyView.style.display = 'none';
    if (podiumView) podiumView.style.display = 'block';

    const sorted = [...finalPlayers].sort((a, b) => b.score - a.score);

    const pillars = document.getElementById('mp-podium-pillars');
    if (pillars) {
      const p1 = sorted[0] || { name: '-', score: 0 };
      const p2 = sorted[1] || { name: '-', score: 0 };
      const p3 = sorted[2] || { name: '-', score: 0 };

      if (sorted.length === 1) {
        pillars.innerHTML = `
          <div class="podium-col rank-1">
            <div class="podium-player-name">👑 ${escapeHtml(p1.name)}</div>
            <div class="podium-player-score">${p1.score} pts</div>
            <div class="podium-pillar">1</div>
          </div>
        `;
      } else if (sorted.length === 2) {
        pillars.innerHTML = `
          <div class="podium-col rank-2">
            <div class="podium-player-name">🥈 ${escapeHtml(p2.name)}</div>
            <div class="podium-player-score">${p2.score} pts</div>
            <div class="podium-pillar">2</div>
          </div>
          <div class="podium-col rank-1">
            <div class="podium-player-name">👑 ${escapeHtml(p1.name)}</div>
            <div class="podium-player-score">${p1.score} pts</div>
            <div class="podium-pillar">1</div>
          </div>
        `;
      } else {
        pillars.innerHTML = `
          <div class="podium-col rank-2">
            <div class="podium-player-name">🥈 ${escapeHtml(p2.name)}</div>
            <div class="podium-player-score">${p2.score} pts</div>
            <div class="podium-pillar">2</div>
          </div>
          <div class="podium-col rank-1">
            <div class="podium-player-name">👑 ${escapeHtml(p1.name)}</div>
            <div class="podium-player-score">${p1.score} pts</div>
            <div class="podium-pillar">1</div>
          </div>
          <div class="podium-col rank-3">
            <div class="podium-player-name">🥉 ${escapeHtml(p3.name)}</div>
            <div class="podium-player-score">${p3.score} pts</div>
            <div class="podium-pillar">3</div>
          </div>
        `;
      }
    }

    const tbody = document.getElementById('mp-podium-table-body');
    if (tbody) {
      tbody.innerHTML = '';
      sorted.forEach((p, idx) => {
        const tr = document.createElement('tr');
        const medal = idx === 0 ? '🥇' : (idx === 1 ? '🥈' : (idx === 2 ? '🥉' : `${idx + 1}º`));
        tr.innerHTML = `
          <td><strong>${medal}</strong></td>
          <td><strong>${escapeHtml(p.name)}</strong></td>
          <td><strong style="color: var(--gold);">${p.score}</strong> pts</td>
          <td>${p.correct || 0} acertos</td>
        `;
        tbody.appendChild(tr);
      });
    }

    ConfettiEngine.burst();
    AudioManager.playSfx('combo');

    const myData = sorted.find(p => p.id === this.myPlayerId);
    if (myData && myData.score > 0) {
      setTimeout(() => {
        if (typeof openGameOverModal === 'function') {
          openGameOverModal('multiplayer', myData.score, myData.correct || 0, 0, myData.name);
        }
      }, 1500);
    }

    const rematchBtn = document.getElementById('mp-rematch-btn');
    if (rematchBtn) {
      rematchBtn.style.display = this.isHost ? 'inline-flex' : 'none';
    }
  },

  rematch() {
    if (!this.isHost) return;
    this.clearRoundTimers();
    this.isTransitioning = false;
    this.isMatchActive = false;
    this.podiumActive = false;
    this.currentRoundIdx = 0;
    this.roundItems = [];
    this.myStreak = 0;
    this.myAnsweredRound = -1;
    this.myVotedRound = -1;
    this.prevRankPositions = {};
    this.answeredPlayers.clear();
    this.skipVotes.clear();
    this.players.forEach(p => {
      p.score = 0;
      p.correct = 0;
    });
    updateGlobalKPIs();
    this.broadcastLobby();
    this.renderLobby();
    this.pushState();
    showToast("🔄 Sala pronta para nova partida!");
  }
};
// IMPORTANTE: `const` no topo do script NÃO cria window.MultiplayerEngine.
// Todos os modos checam `window.MultiplayerEngine && ...isMatchActive`, então expomos explicitamente.
window.MultiplayerEngine = MultiplayerEngine;

/* ==============================================================
   LEADERBOARD (HALL DA FAMA GLOBAL, ANTI-CHEAT & PRESTIGE BADGES)
   ============================================================== */
const DEFAULT_LEADERBOARD = [
  { id: 1, name: "GokuSSJ", mode: "mode1", score: 2450, correct: 27, streak: 12, date: "Hoje", source: "local" },
  { id: 2, name: "Mikasa_Ackerman", mode: "mode2", score: 2180, correct: 20, streak: 15, date: "Ontem", source: "local" },
  { id: 3, name: "L_Lawliet", mode: "mode3", score: 1950, correct: 18, streak: 9, date: "02/10", source: "local" },
  { id: 4, name: "TanjiroKamado", mode: "mode2", score: 1600, correct: 15, streak: 8, date: "01/10", source: "local" },
  { id: 5, name: "Zoro_Lost", mode: "mode1", score: 1420, correct: 16, streak: 5, date: "30/09", source: "local" },
  { id: 6, name: "NarutoUzumaki", mode: "mode3", score: 1200, correct: 13, streak: 6, date: "28/09", source: "local" }
];

/* 1.3 MOTOR DE TÍTULOS E BADGES DE PRESTÍGIO */
const PrestigeBadges = {
  getBadge(item) {
    const score = Number(item.score) || 0;
    const correct = Number(item.correct) || 0;
    const streak = Number(item.streak) || 0;
    const mode = item.mode || 'mode2';

    if (score >= 2200 || correct >= 20) {
      return {
        title: "Mestre Otaku",
        icon: "👑",
        cssClass: "badge-master",
        tooltip: "Pontuação de elite (2200+ pts ou 20+ acertos)"
      };
    }
    if (streak >= 8) {
      return {
        title: "Fogo Eterno",
        icon: "🔥",
        cssClass: "badge-fire",
        tooltip: "Sequência ardente de 8+ acertos seguidos sem errar"
      };
    }
    if (score >= 1200 && (score / Math.max(1, correct)) >= 125) {
      return {
        title: "Velocista Neon",
        icon: "⚡",
        cssClass: "badge-speed",
        tooltip: "Reflexos sobre-humanos com bônus de velocidade máxima"
      };
    }
    if (streak >= 5 && streak === correct) {
      return {
        title: "Mira Perfeita",
        icon: "🎯",
        cssClass: "badge-perfect",
        tooltip: "100% de precisão (5+ acertos sem nenhum erro)"
      };
    }
    if (mode === 'mode1' && correct >= 8) {
      return {
        title: "Ouvido Absoluto",
        icon: "🎧",
        cssClass: "badge-ear",
        tooltip: "Reconheceu 8+ aberturas às cegas no Blind Test"
      };
    }
    if (mode === 'mode2' && correct >= 8) {
      return {
        title: "DJ de Aberturas",
        icon: "🎵",
        cssClass: "badge-dj",
        tooltip: "Identificou 8+ músicas oficiais em 'Qual é a Abertura?'"
      };
    }
    if (mode === 'mode3' && correct >= 8) {
      return {
        title: "Olho Clínico",
        icon: "🖼️",
        cssClass: "badge-eye",
        tooltip: "Decifrou 8+ cenas de animes em alta definição"
      };
    }
    if (score >= 1000) {
      return {
        title: "Veterano",
        icon: "💎",
        cssClass: "badge-veteran",
        tooltip: "Veterano de arcade com mais de 1000 pontos"
      };
    }
    return {
      title: "Aspirante",
      icon: "🔰",
      cssClass: "badge-rookie",
      tooltip: "Iniciante promissor no mundo dos animes"
    };
  }
};
window.PrestigeBadges = PrestigeBadges;

/* 1.2 MOTOR ANTI-CHEAT E INTEGRIDADE DE PONTUAÇÃO */
const AntiCheatEngine = {
  validateSubmission(rawNick, mode, score, correct, streak) {
    const cleanNick = (rawNick || '').replace(/[<>\\/\\\\"'&;]/g, '').trim();

    if (!cleanNick || cleanNick.length < 2) {
      return { ok: false, msg: "O apelido deve ter pelo menos 2 caracteres!" };
    }
    if (cleanNick.length > 15) {
      return { ok: false, msg: "O apelido pode ter no máximo 15 caracteres!" };
    }
    if (typeof score !== 'number' || isNaN(score) || score <= 0) {
      return { ok: false, msg: "Jogue pelo menos uma rodada antes de salvar sua pontuação!" };
    }
    if (typeof correct !== 'number' || isNaN(correct) || correct < 1) {
      return { ok: false, msg: "É necessário ter pelo menos 1 acerto para entrar no Hall da Fama!" };
    }
    if (typeof streak !== 'number' || streak > correct) {
      return { ok: false, msg: "O combo streak não pode ser maior que o número total de acertos!" };
    }

    // Limite matemático por acerto (máx possível por rodada com bônus de velocidade e combo)
    const maxPerCorrect = (mode === 'mode1') ? 220 : 180;
    if (score > (correct * maxPerCorrect) + 50) {
      return { 
        ok: false, 
        msg: `Pontuação inconsistente detectada (${score} pts para ${correct} acertos). Limite de integridade violado!` 
      };
    }

    // Verificação de correspondência com o estado de memória da sessão
    if (['mode1', 'mode2', 'mode3'].includes(mode)) {
      const liveScore = mode === 'mode2' ? m2Score : (mode === 'mode3' ? m3Score : m1Score);
      const liveCorrect = mode === 'mode2' ? m2CorrectCount : (mode === 'mode3' ? m3CorrectCount : m1CorrectCount);
      if (score !== liveScore || correct !== liveCorrect) {
        return { ok: false, msg: "A pontuação informada não coincide com a sessão atual do jogo!" };
      }
    }

    return { ok: true, cleanNick };
  }
};
window.AntiCheatEngine = AntiCheatEngine;

/* 1.1 MOTOR DE BANCO EM NUVEM GLOBAL (FIREBASE REALTIME DB INTEGRADO) */
const CloudLeaderboard = {
  STORAGE_KEY: 'AMQ_LEADERBOARD_V2',
  FIREBASE_URL: 'https://anime-quiz-arcade-default-rtdb.firebaseio.com/leaderboard.json',
  cachedScores: [],
  isSyncing: false,
  isOnline: true,

  getFirebaseUrl() {
    return this.FIREBASE_URL;
  },

  getLocalScores() {
    try {
      const saved = localStorage.getItem(this.STORAGE_KEY);
      if (saved) {
        const parsed = JSON.parse(saved);
        if (Array.isArray(parsed) && parsed.length > 0) return parsed;
      }
    } catch(e) {}
    return DEFAULT_LEADERBOARD;
  },

  saveLocalScores(list) {
    try {
      localStorage.setItem(this.STORAGE_KEY, JSON.stringify(list));
    } catch(e) {}
  },

  init() {
    this.cachedScores = this.getLocalScores();
    this.updateStatusBadge();
    this.fetchScores().then(() => {
      renderLeaderboardTable('all');
    });
  },

  async fetchScores() {
    try {
      this.isSyncing = true;
      this.updateStatusBadge();
      const res = await fetch(this.FIREBASE_URL, {
        method: 'GET',
        headers: { 'Accept': 'application/json' }
      });
      if (!res.ok) throw new Error('HTTP ' + res.status);
      const data = await res.json();

      let cloudList = [];
      if (data) {
        if (Array.isArray(data)) {
          cloudList = data.filter(Boolean);
        } else if (typeof data === 'object') {
          cloudList = Object.keys(data).map(k => ({ ...data[k], cloudId: k, source: 'cloud' }));
        }
      }

      const localList = this.getLocalScores();
      const merged = this.mergeScores(cloudList, localList);
      merged.sort((a, b) => (Number(b.score) || 0) - (Number(a.score) || 0));

      this.cachedScores = merged;
      this.saveLocalScores(merged);
      this.isOnline = true;
      return merged;
    } catch (err) {
      console.warn("Nuvem em sincronização, usando cache local:", err);
      this.cachedScores = this.getLocalScores();
      return this.cachedScores;
    } finally {
      this.isSyncing = false;
      this.updateStatusBadge();
    }
  },

  mergeScores(cloudList, localList) {
    const map = new Map();
    cloudList.forEach(item => {
      if (item && item.name && typeof item.score !== 'undefined') {
        const key = `${String(item.name).toLowerCase()}_${item.mode}_${item.score}`;
        map.set(key, { ...item, source: 'cloud' });
      }
    });
    localList.forEach(item => {
      if (item && item.name && typeof item.score !== 'undefined') {
        const key = `${String(item.name).toLowerCase()}_${item.mode}_${item.score}`;
        if (!map.has(key)) {
          map.set(key, { ...item, source: 'local' });
        }
      }
    });
    return Array.from(map.values());
  },

  async submitScore(entry) {
    // 1. Salva no cache local primeiro (garantia de persistência)
    const local = this.getLocalScores();
    local.push(entry);
    local.sort((a, b) => (Number(b.score) || 0) - (Number(a.score) || 0));
    this.saveLocalScores(local);
    this.cachedScores = local;

    // 2. Envia via POST diretamente para o Firebase Realtime DB na nuvem
    try {
      const res = await fetch(this.FIREBASE_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(entry)
      });
      if (res.ok) {
        entry.source = 'cloud';
        this.isOnline = true;
      }
    } catch (err) {
      console.warn("Nuvem offline no momento. O recorde foi guardado no cache local:", err);
    }
    this.updateStatusBadge();
  },

  updateStatusBadge() {
    const el = document.getElementById('cloud-status-badge');
    if (!el) return;
    if (this.isSyncing) {
      el.className = 'cloud-status-pill syncing';
      el.innerHTML = '<span class="status-dot spin"></span> Sincronizando...';
    } else {
      el.className = 'cloud-status-pill online';
      el.innerHTML = '<span class="status-dot pulse-green"></span> 🟢 Nuvem Global • Ao Vivo';
    }
  }
};
window.CloudLeaderboard = CloudLeaderboard;

function getLeaderboardData() {
  return (CloudLeaderboard.cachedScores && CloudLeaderboard.cachedScores.length > 0)
    ? CloudLeaderboard.cachedScores
    : CloudLeaderboard.getLocalScores();
}

function saveLeaderboardData(list) {
  CloudLeaderboard.saveLocalScores(list);
}

/* MODAL DE FIM DE PARTIDA & SALVAMENTO AUTOMÁTICO */
let currentGameOverData = { mode: 'mode1', score: 0, correct: 0, streak: 0 };

function openGameOverModal(mode, score, correct, streak, defaultNick = '') {
  currentGameOverData = { mode, score, correct, streak };

  let modeLabel = "Blind Test";
  if (mode === 'mode2') modeLabel = "Qual é a Abertura?";
  if (mode === 'mode3') modeLabel = "Adivinhe a Cena";
  if (mode === 'multiplayer') modeLabel = "Multiplayer";

  const modeEl = document.getElementById('go-mode-val');
  const scoreEl = document.getElementById('go-score-val');
  const corrEl = document.getElementById('go-correct-val');
  const streakEl = document.getElementById('go-streak-val');
  const badgeContainer = document.getElementById('go-badge-container');
  const badgeDesc = document.getElementById('go-badge-desc');
  const nickInput = document.getElementById('go-nickname-input');

  if (modeEl) modeEl.textContent = modeLabel;
  if (scoreEl) scoreEl.textContent = `${score} pts`;
  if (corrEl) corrEl.textContent = correct;
  if (streakEl) streakEl.textContent = `${streak}x`;

  const badge = PrestigeBadges.getBadge({ score, correct, streak, mode });
  if (badgeContainer) {
    badgeContainer.innerHTML = `<span class="prestige-badge ${badge.cssClass}" style="font-size: 13px; padding: 4px 12px;">${badge.icon} ${escapeHtml(badge.title)}</span>`;
  }
  if (badgeDesc) {
    badgeDesc.textContent = badge.tooltip;
  }

  const savedNick = defaultNick || localStorage.getItem('AMQ_LAST_NICK') || '';
  if (nickInput) {
    nickInput.value = savedNick;
  }

  validateGoNickname();

  const modal = document.getElementById('game-over-modal');
  if (modal) modal.style.display = 'flex';
  if (window.AudioManager) AudioManager.playSfx('combo');
}

function closeGameOverModal() {
  if (window.AudioManager) AudioManager.playSfx('click');
  const modal = document.getElementById('game-over-modal');
  if (modal) modal.style.display = 'none';
}

function validateGoNickname() {
  const input = document.getElementById('go-nickname-input');
  const countEl = document.getElementById('go-char-count');
  const hintEl = document.getElementById('go-nick-hint');
  const saveBtn = document.getElementById('go-save-btn');
  if (!input) return;

  const val = input.value.trim();
  const len = val.length;

  if (countEl) {
    countEl.textContent = `${len}/5 letras (mín. 5)`;
    countEl.style.color = len >= 5 ? 'var(--green)' : 'var(--rose)';
  }

  if (len < 5) {
    if (hintEl) {
      hintEl.textContent = len === 0 ? "O apelido precisa ter no mínimo 5 caracteres." : `Faltam ${5 - len} letra(s) para atingir o mínimo de 5.`;
      hintEl.style.color = 'var(--rose)';
    }
    if (saveBtn) {
      saveBtn.style.opacity = '0.45';
      saveBtn.style.pointerEvents = 'none';
    }
  } else {
    if (hintEl) {
      hintEl.textContent = "✓ Apelido válido para entrar no Hall da Fama!";
      hintEl.style.color = 'var(--green)';
    }
    if (saveBtn) {
      saveBtn.style.opacity = '1';
      saveBtn.style.pointerEvents = 'auto';
    }
  }
}

async function submitGameOverScore() {
  const input = document.getElementById('go-nickname-input');
  const rawNick = (input ? input.value : '').trim();
  if (rawNick.length < 5) {
    showToast("⚠️ O apelido deve ter no mínimo 5 caracteres!");
    return;
  }

  localStorage.setItem('AMQ_LAST_NICK', rawNick);

  const mode = currentGameOverData.mode || activeGameMode;
  const score = currentGameOverData.score || 0;
  const correct = currentGameOverData.correct || 0;
  const streak = currentGameOverData.streak || 0;

  const badgeInfo = PrestigeBadges.getBadge({ score, correct, streak, mode });

  const entry = {
    id: Date.now(),
    name: rawNick.substring(0, 15),
    mode: mode,
    score: score,
    correct: correct,
    streak: streak,
    badgeTitle: badgeInfo.title,
    badgeIcon: badgeInfo.icon,
    date: new Date().toLocaleDateString('pt-BR'),
    timestamp: Date.now()
  };

  closeGameOverModal();
  showToast("⏳ Salvando recorde no Hall da Fama Global...");

  await CloudLeaderboard.submitScore(entry);

  if (window.ConfettiEngine) ConfettiEngine.burst();
  if (window.AudioManager) AudioManager.playSfx('correct');

  resetModeSession(mode);

  switchGameMode('mode5', true);
  renderLeaderboardTable('all');
  showToast(`🎉 Parabéns ${entry.name}! Seu recorde de ${entry.score} pts foi salvo no Top 50!`);
}

function resetModeSession(mode = activeGameMode) {
  if (mode === 'mode1') {
    m1Score = 0;
    m1CorrectCount = 0;
    m1Streak = 0;
    m1Attempts = 0;
    m1PlaylistIndex = 0;
    m1Playlist = [];
    m1LoadSong(true);
  } else if (mode === 'mode2') {
    m2Score = 0;
    m2CorrectCount = 0;
    m2Streak = 0;
    m2RoundsPlayed = 0;
    m2StartGame();
  } else if (mode === 'mode3') {
    m3Score = 0;
    m3CorrectCount = 0;
    m3Streak = 0;
    m3RoundsPlayed = 0;
    m3StartGame();
  } else if (mode === 'multiplayer') {
    if (window.MultiplayerEngine) {
      MultiplayerEngine.myStreak = 0;
      const me = MultiplayerEngine.getMyPlayer();
      if (me) {
        me.score = 0;
        me.correct = 0;
      }
    }
    m1Score = 0; m1CorrectCount = 0; m1Streak = 0; m1Attempts = 0; m1PlaylistIndex = 0; m1Playlist = [];
    m2Score = 0; m2CorrectCount = 0; m2Streak = 0; m2RoundsPlayed = 0; m2UnplayedQueue = [];
    m3Score = 0; m3CorrectCount = 0; m3Streak = 0; m3RoundsPlayed = 0; m3UnplayedQueue = [];
  }
  updateGlobalKPIs();
}

function discardSessionAndReset() {
  const mode = currentGameOverData.mode || activeGameMode;
  closeGameOverModal();
  resetModeSession(mode);
  showToast("🔄 Sessão reiniciada! Pontuação zerada para um novo jogo.");
}

function finishCurrentGame(mode = activeGameMode) {
  if (window.MultiplayerEngine && MultiplayerEngine.isMatchActive) {
    MultiplayerEngine.confirmLeaveRoom();
    return;
  }
  const score = (mode === 'mode2') ? m2Score : ((mode === 'mode3') ? m3Score : m1Score);
  const correct = (mode === 'mode2') ? m2CorrectCount : ((mode === 'mode3') ? m3CorrectCount : m1CorrectCount);
  const streak = (mode === 'mode2') ? m2Streak : ((mode === 'mode3') ? m3Streak : m1Streak);

  if (score <= 0 && correct <= 0) {
    if (window.AudioManager) AudioManager.playSfx('wrong');
    showToast("⚠️ Jogue pelo menos uma rodada antes de finalizar a partida!");
    return;
  }

  stopAllMedia();
  openGameOverModal(mode, score, correct, streak);
}

function filterLeaderboard(mode, btnEl) {
  if (btnEl) {
    document.querySelectorAll('.lb-tab-btn').forEach(b => b.classList.remove('active'));
    btnEl.classList.add('active');
  }
  renderLeaderboardTable(mode);
}

function renderLeaderboardTable(filterMode = 'all') {
  const list = getLeaderboardData();
  const filtered = (filterMode === 'all') ? list : list.filter(item => item.mode === filterMode);
  const tbody = document.getElementById('leaderboard-tbody');
  if (!tbody) return;
  tbody.innerHTML = '';

  if (filtered.length === 0) {
    const tr = document.createElement('tr');
    tr.innerHTML = `<td colspan="6" style="text-align: center; color: var(--text-muted); padding: 26px;">Nenhum recorde registrado nesta categoria ainda. Jogue e seja o primeiro!</td>`;
    tbody.appendChild(tr);
    return;
  }

  filtered.slice(0, 50).forEach((item, idx) => {
    const tr = document.createElement('tr');
    let rankHtml = `<span class="rank-badge">${idx + 1}</span>`;
    if (idx === 0) rankHtml = `<span class="rank-badge rank-1">🥇</span>`;
    if (idx === 1) rankHtml = `<span class="rank-badge rank-2">🥈</span>`;
    if (idx === 2) rankHtml = `<span class="rank-badge rank-3">🥉</span>`;

    let modeName = "Blind Test";
    let modeIcon = "🎧";
    if (item.mode === 'mode2') { modeName = "3 Músicas"; modeIcon = "🎵"; }
    if (item.mode === 'mode3') { modeName = "Adivinhe a Cena"; modeIcon = "🖼️"; }
    if (item.mode === 'multiplayer') { modeName = "Multiplayer"; modeIcon = "🎮"; }

    const badge = PrestigeBadges.getBadge(item);
    const streakTxt = (item.streak && Number(item.streak) > 1)
      ? ` <span style="color: #f97316; font-size: 11px; font-weight: 700;">(🔥${item.streak}x)</span>`
      : '';

    tr.innerHTML = `
      <td>${rankHtml}</td>
      <td>
        <div class="player-cell">
          <span class="player-name">${escapeHtml(item.name || 'Otaku')}</span>
          <span class="prestige-badge ${badge.cssClass}" title="${escapeHtml(badge.tooltip)}">${badge.icon} ${escapeHtml(badge.title)}</span>
        </div>
      </td>
      <td><span class="pill-chip">${modeIcon} ${modeName}</span></td>
      <td><strong style="color: var(--gold); font-family: 'JetBrains Mono', monospace; font-size: 13.5px;">${item.score || 0}</strong></td>
      <td>${item.correct || 0} acertos${streakTxt}</td>
      <td style="color: var(--text-muted); font-size: 11px;">${item.date || 'Hoje'}</td>
    `;
    tbody.appendChild(tr);
  });
}

async function syncLeaderboardNow() {
  if (window.AudioManager) AudioManager.playSfx('click');
  const syncBtn = document.getElementById('btn-sync-leaderboard');
  const icon = document.getElementById('sync-icon');
  if (icon) icon.style.animation = 'dotSpin 0.8s infinite linear';
  if (syncBtn) syncBtn.disabled = true;

  showToast("🔄 Atualizando placar com a Nuvem...");
  await CloudLeaderboard.fetchScores();
  renderLeaderboardTable('all');

  if (icon) icon.style.animation = 'none';
  if (syncBtn) syncBtn.disabled = false;
  if (window.AudioManager) AudioManager.playSfx('hover');
  showToast("✅ Placar do Hall da Fama atualizado!");
}

function clearLeaderboard() {
  if (confirm("Deseja realmente limpar o cache salvo no seu dispositivo?")) {
    localStorage.removeItem('AMQ_LEADERBOARD_V2');
    CloudLeaderboard.cachedScores = CloudLeaderboard.getLocalScores();
    renderLeaderboardTable('all');
    showToast("Cache local resetado!");
  }
}

function showToast(text) {
  const t = document.getElementById('toast-msg');
  if (!t) return;
  t.textContent = text;
  t.style.display = 'block';
  setTimeout(() => {
    t.style.display = 'none';
  }, 3500);
}

/* ==============================================================
   FULL CATALOG TABLE
   ============================================================== */
function renderCatalogTable() {
  const tbody = document.getElementById('songs-tbody');
  if (!tbody) return;
  tbody.innerHTML = '';
  ALL_SONGS.forEach((s, idx) => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td><strong>#${s.id}</strong></td>
      <td>${s.year}</td>
      <td><span class="spoiler-text" onclick="this.classList.toggle('revealed')">${s.anime}</span></td>
      <td>${s.song} <span style="color:#94a3b8; font-size:11px;">(${s.artist})</span></td>
      <td><button class="btn btn-secondary" style="padding: 3px 8px; font-size: 11px;" onclick="playSongFromCatalog(${idx})">${ICON_PLAY_SM} Tocar</button></td>
    `;
    tbody.appendChild(tr);
  });
}

function playSongFromCatalog(idx) {
  stopAllMedia();
  switchGameMode('mode1');
  m1CurrentIndex = idx;
  m1LoadSong(true);
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

/* ==============================================================
   INITIALIZATION
   ============================================================== */
window.addEventListener('DOMContentLoaded', () => {
  AudioManager.init();
  VisualizerEngine.init();
  ConfettiEngine.init();
  FloatingArcade.init();
  if (window.MultiplayerEngine) {
    MultiplayerEngine.init();
  }
  if (window.CloudLeaderboard) {
    CloudLeaderboard.init();
  }

  // Prevenir perda acidental da sala se o usuário recarregar (F5) durante uma partida ativa
  window.addEventListener('beforeunload', (e) => {
    if (window.MultiplayerEngine && MultiplayerEngine.isMatchActive) {
      e.preventDefault();
      e.returnValue = '';
      return '';
    }
  });

  // Setup Autocomplete for Mode 1 and Mode 3
  setupAutocomplete(guessInput, guessAutocomplete, () => submitGuess());
  setupAutocomplete(m3Input, m3Autocomplete, () => m3SubmitGuess());

  // Close audio settings popover when clicking outside
  document.addEventListener('click', (e) => {
    const popover = document.getElementById('audio-settings-popover');
    const btn = document.getElementById('btn-audio-settings');
    if (popover && btn && !popover.contains(e.target) && !btn.contains(e.target)) {
      popover.classList.remove('active');
    }
  });

  // Mode 2 Keyboard shortcuts (1, 2, 3 to select, Enter/Space to confirm)
  window.addEventListener('keydown', (e) => {
    if (activeGameMode === 'mode2' && document.activeElement && document.activeElement.tagName !== 'INPUT') {
      if (e.key === '1') { m2ClickCard(0); AudioManager.playSfx('click'); }
      else if (e.key === '2') { m2ClickCard(1); AudioManager.playSfx('click'); }
      else if (e.key === '3') { m2ClickCard(2); AudioManager.playSfx('click'); }
      else if (e.key === 'Enter' || e.key === ' ') {
        if (!m2Answered && m2SelectedOptionIndex !== -1) {
          e.preventDefault();
          m2ConfirmSelection();
        } else if (m2Answered) {
          e.preventDefault();
          m2NextRound();
        }
      }
    }
  });

  if (isChallengeActive) {
    challengeBanner.style.display = 'block';
    challengeBanner.innerHTML = `⚔️ <strong>DUELO MULTIPLAYER ATIVO!</strong> Semente #${challengeSeed} • Modo: ${challengeTargetMode} (${challengeRounds} Rodadas). Convide seus amigos para comparar suas pontuações!`;
    switchGameMode(challengeTargetMode);
  } else {
    m1LoadSong(false);
  }

  // Posicionar o Scoreboard dentro do Modo 1 inicialmente
  const initSb = document.getElementById('main-scoreboard');
  const m1Slot = document.getElementById('mode1-scoreboard-slot');
  if (initSb && m1Slot) {
    m1Slot.appendChild(initSb);
    initSb.style.display = 'grid';
  }

  renderCatalogTable();
});

/* ==============================================================
   CONTROLES DO MODAL DE CONFIGURAÇÕES E SIDEBAR v3.1.0
   ============================================================== */
function openSettingsModal() {
  if (window.AudioManager) AudioManager.playSfx('click');
  const modal = document.getElementById('settings-modal');
  if (modal) modal.style.display = 'flex';
}
function closeSettingsModal() {
  if (window.AudioManager) AudioManager.playSfx('click');
  const modal = document.getElementById('settings-modal');
  if (modal) modal.style.display = 'none';
}
function toggleAudioSettingsPopover() {
  openSettingsModal();
}
function toggleSidebar() {
  const sidebar = document.getElementById('app-sidebar');
  if (sidebar) sidebar.classList.toggle('expanded');
}

// Microinterações globais de áudio no hover e feedback tátil
document.addEventListener('DOMContentLoaded', () => {
  const INTERACTIVE_SELECTOR = '.btn, .mode-tab-btn, .music-card, .card-play-btn, .nav-pill, .song-card, .option-btn, .lb-tab-btn, .mp-tab-btn, .mp-room-card, .audio-btn-toggle, .audio-mute-toggle-btn, .scene-zoom-trigger, .mp-skip-btn, .sidebar-item';

  document.addEventListener('mouseover', (e) => {
    const target = e.target.closest(INTERACTIVE_SELECTOR);
    if (target && !target.disabled) {
      if (window.AudioManager) AudioManager.playSfx('hover');
    }
  }, { passive: true });

  document.addEventListener('mousedown', (e) => {
    const target = e.target.closest(INTERACTIVE_SELECTOR);
    if (target && !target.disabled) {
      try {
        const rect = target.getBoundingClientRect();
        const ripple = document.createElement('span');
        ripple.className = 'dopamine-ripple';
        const size = Math.max(rect.width, rect.height) * 1.4;
        const x = (e.clientX || (rect.left + rect.width / 2)) - rect.left - size / 2;
        const y = (e.clientY || (rect.top + rect.height / 2)) - rect.top - size / 2;
        ripple.style.width = `${size}px`;
        ripple.style.height = `${size}px`;
        ripple.style.left = `${x}px`;
        ripple.style.top = `${y}px`;
        target.appendChild(ripple);
        setTimeout(() => { try { ripple.remove(); } catch(err) {} }, 550);
      } catch(err) {}
    }
  }, { passive: true });
});

</script>
</body>
</html>
"""

final_html = html_template.replace("__SONGS_JSON__", songs_json_str).replace("__SCENES_JSON__", scenes_json_str).replace("__AUTOCOMPLETE_JSON__", autocomplete_json_str)

# Write to files
with open(os.path.join(DIR, "desafio_anime_quiz.html"), "w", encoding="utf-8") as f:
    f.write(final_html)

with open(os.path.join(DIR, "index.html"), "w", encoding="utf-8") as f:
    f.write(final_html)

print("SUCESSO: desafio_anime_quiz.html e index.html gerados com Autocomplete e Cenas Reais!")
print(f"Total de bytes: {len(final_html.encode('utf-8'))}")
