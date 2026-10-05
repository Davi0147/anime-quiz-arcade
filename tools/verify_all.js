const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');

console.log('============================================');
console.log('   VERIFICACAO COMPLETA DO JOGO (v2.4.0)   ');
console.log('============================================');

// 1. Data sizes
const songsMatch = html.match(/const ALL_SONGS = (\[[\s\S]*?\]);/);
const scenesMatch = html.match(/const ALL_SCENES = (\[[\s\S]*?\]);/);
const autoMatch = html.match(/const ANIME_AUTOCOMPLETE = (\[[\s\S]*?\]);/);

const songs = JSON.parse(songsMatch[1]);
const scenes = JSON.parse(scenesMatch[1]);
const autocomplete = JSON.parse(autoMatch[1]);

console.log('1. Total de Musicas no Jogo:', songs.length);
console.log('2. Total de Cenas Reais no Modo 3:', scenes.length);
console.log('3. Total de Animes no Autocomplete Limpo:', autocomplete.length);

// 2. Autocomplete sanity check
const atta = autocomplete.filter(t => t.toLowerCase().includes('atta'));
console.log('4. Sugestoes para "Atta":', atta);
const bleach = autocomplete.filter(t => t.toLowerCase().includes('bleach'));
console.log('5. Sugestoes para "Bleach":', bleach);

// 3. Audio & SFX
console.log('6. Player usa MP3:', html.includes('localVideoPlayer.src = `audio/${song.id}.mp3`'));
console.log('7. SFX Synthesizer presente:', html.includes('function playSfx'));
console.log('8. Animacao Shake de Erro presente:', html.includes('input-error-shake'));
console.log('9. Animacao Pulse de Sucesso presente:', html.includes('input-success-pulse'));
console.log('10. Feedback display block corrigido:', html.includes("m3FeedbackBox.style.display = 'block'") && html.includes("feedbackBox.style.display = 'block'"));

// 4. Test logic execution directly in node
const scriptContent = html.match(/<script>([\s\S]*?)<\/script>/)[1];
const sandbox = {
  document: {
    addEventListener: () => {},
    getElementById: () => ({ style: {}, classList: { add: ()=>{}, remove: ()=>{} }, appendChild: ()=>{} }),
    querySelectorAll: () => []
  },
  window: { addEventListener: () => {}, location: { search: '' } },
  URLSearchParams: URLSearchParams,
  navigator: {},
  localStorage: { getItem: () => null, setItem: () => {} }
};

const vm = require('vm');
const context = vm.createContext(sandbox);
vm.runInContext(scriptContent, context);

const test1 = context.checkAnimeMatch('Bleach', 'Bleach: Thousand-Year Blood War', ['bleach tybw']);
const test2 = context.checkAnimeMatch('Attack on Titan', 'Attack on Titan (Shingeki no Kyojin)');
const test3 = context.checkAnimeMatch('Shingeki no Kyojin', 'Attack on Titan (Shingeki no Kyojin)');
const test4 = context.checkAnimeMatch('Attack on Titan', 'Attack on Titan Final Season Pt 2');
const test5 = context.checkAnimeMatch('k', 'Bocchi the Rock!');

console.log('11. Teste Bleach -> Bleach TYBW:', test1.match ? 'ACERTOU (OK)' : 'ERRO');
console.log('12. Teste AoT -> AoT (Shingeki):', test2.match ? 'ACERTOU (OK)' : 'ERRO');
console.log('13. Teste Shingeki -> AoT (Shingeki):', test3.match ? 'ACERTOU (OK)' : 'ERRO');
console.log('14. Teste AoT -> Final Season Pt 2:', test4.match ? 'ACERTOU (OK)' : 'ERRO');
console.log('15. Teste anti-cheat k -> Bocchi:', !test5.match ? 'BLOQUEADO (OK)' : 'FALHA');
console.log('============================================');
