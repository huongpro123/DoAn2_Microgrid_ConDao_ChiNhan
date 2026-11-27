import subprocess
import os

filter_script = """[0:v]loop=loop=-1:size=1:start=0,scale=1280:720,fps=30,trim=duration=19.0,setpts=PTS-STARTPTS[v0];[1:v]trim=start=3:end=45,setpts=PTS-STARTPTS,setpts=43/42*PTS,scale=1280:720,fps=30[v1];[1:v]trim=start=45:end=85,setpts=PTS-STARTPTS,setpts=51/40*PTS,scale=1280:720,fps=30[v2];[1:v]trim=start=85:end=120,setpts=PTS-STARTPTS,setpts=58/35*PTS,scale=1280:720,fps=30[v3];[1:v]trim=start=120:end=160,setpts=PTS-STARTPTS,setpts=53/40*PTS,scale=1280:720,fps=30[v4];[1:v]trim=start=160:end=205,setpts=PTS-STARTPTS,setpts=42/45*PTS,scale=1280:720,fps=30[v5];[1:v]trim=start=205:end=248,setpts=PTS-STARTPTS,setpts=57/43*PTS,scale=1280:720,fps=30[v6];[2:v]loop=loop=-1:size=1:start=0,scale=1280:720,fps=30,trim=duration=16.14,setpts=PTS-STARTPTS[v7];[v0][v1][v2][v3][v4][v5][v6][v7]concat=n=8:v=1:a=0[vcat]"""

cmd = [
    'ffmpeg', '-y',
    '-i', 'd:/chinhan/video_frames/slide_00.png',
    '-i', 'd:/chinhan/2026-10-31 23-12-31.mp4',
    '-i', 'd:/chinhan/video_frames/slide_10.png',
    '-i', 'd:/chinhan/audio_clean.m4a',
    '-filter_complex', filter_script,
    '-map', '[vcat]',
    '-map', '3:a',
    '-c:v', 'libx264',
    '-preset', 'fast',
    '-crf', '18',
    '-c:a', 'copy',
    '-shortest',
    'd:/chinhan/Video_Bao_Cao_HOMER_Chuan_Khop_Tieng.mp4'
]

print('Running ffmpeg to generate synchronized video...')
res = subprocess.run(cmd, capture_output=True, text=True)
if res.returncode == 0:
    print('SUCCESS! Video generated: Video_Bao_Cao_HOMER_Chuan_Khop_Tieng.mp4')
else:
    print('ERROR:', res.stderr[-800:])
