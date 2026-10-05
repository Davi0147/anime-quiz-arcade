import os
import glob
import subprocess
import time

FFMPEG_EXE = r"C:\Users\luizd\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg.Essentials_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.1-essentials_build\bin\ffmpeg.exe"
AUDIO_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "audio")

def convert_all():
    mp4_files = sorted(glob.glob(os.path.join(AUDIO_DIR, "*.mp4")), key=lambda p: int(os.path.basename(p).split('.')[0]) if os.path.basename(p).split('.')[0].isdigit() else p)
    print(f"Encontrados {len(mp4_files)} arquivos MP4 para conversao em MP3...")
    
    total_original_bytes = 0
    total_mp3_bytes = 0
    converted_count = 0

    t0 = time.time()
    for i, mp4_path in enumerate(mp4_files, 1):
        mp3_path = mp4_path[:-4] + ".mp3"
        orig_size = os.path.getsize(mp4_path)
        total_original_bytes += orig_size

        if os.path.exists(mp3_path) and os.path.getsize(mp3_path) > 10000:
            total_mp3_bytes += os.path.getsize(mp3_path)
            continue

        cmd = [
            FFMPEG_EXE,
            "-y",
            "-i", mp4_path,
            "-vn",
            "-acodec", "libmp3lame",
            "-b:a", "128k",
            "-ar", "44100",
            mp3_path
        ]
        res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if res.returncode == 0 and os.path.exists(mp3_path):
            mp3_size = os.path.getsize(mp3_path)
            total_mp3_bytes += mp3_size
            converted_count += 1
            if converted_count % 10 == 0 or converted_count == len(mp4_files):
                print(f"[{i}/{len(mp4_files)}] Convertido {os.path.basename(mp3_path)} ({mp3_size // 1024} KB)")
        else:
            print(f"[ERRO] Falha ao converter {os.path.basename(mp4_path)}")

    elapsed = time.time() - t0
    orig_mb = total_original_bytes / (1024 * 1024)
    mp3_mb = total_mp3_bytes / (1024 * 1024)
    savings_pct = ((orig_mb - mp3_mb) / orig_mb * 100) if orig_mb > 0 else 0

    print("=" * 60)
    print(f"CONVERSAO CONCLUIDA EM {elapsed:.1f}s!")
    print(f"Total MP4 original: {orig_mb:.1f} MB")
    print(f"Total MP3 otimizado: {mp3_mb:.1f} MB")
    print(f"Economia de espaco: {savings_pct:.1f}% ({orig_mb - mp3_mb:.1f} MB a menos)")
    print("=" * 60)

if __name__ == "__main__":
    convert_all()
