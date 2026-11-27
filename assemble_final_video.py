import subprocess
import os

print('Rendering intro & outro...')
# Intro: 1280x720 matching user video
cmd_intro = [
    'ffmpeg', '-y', '-loop', '1', '-i', 'video_frames/slide_00.png',
    '-vf', 'scale=1280:720', '-t', '4', '-r', '30', '-pix_fmt', 'yuv420p',
    '-c:v', 'libx264', 'intro_clip.mp4'
]
subprocess.run(cmd_intro, check=True)

# Outro: 1280x720 matching user video
cmd_outro = [
    'ffmpeg', '-y', '-loop', '1', '-i', 'video_frames/slide_10.png',
    '-vf', 'scale=1280:720', '-t', '4', '-r', '30', '-pix_fmt', 'yuv420p',
    '-c:v', 'libx264', 'outro_clip.mp4'
]
subprocess.run(cmd_outro, check=True)

print('Trimming main video...')
cmd_main = [
    'ffmpeg', '-y', '-ss', '00:00:03', '-to', '00:04:08', '-i', '2026-10-31 23-12-31.mp4',
    '-c:v', 'libx264', '-crf', '18', '-pix_fmt', 'yuv420p', '-r', '30', 'main_trimmed.mp4'
]
subprocess.run(cmd_main, check=True)

print('Concatenating clips...')
with open('concat_final.txt', 'w', encoding='utf-8') as f:
    f.write("file 'intro_clip.mp4'\nfile 'main_trimmed.mp4'\nfile 'outro_clip.mp4'\n")

cmd_concat = [
    'ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', 'concat_final.txt',
    '-c:v', 'libx264', '-crf', '18', '-pix_fmt', 'yuv420p', 'Video_Thuyet_Trinh_HOMER_Chinh_Thuc.mp4'
]
subprocess.run(cmd_concat, check=True)

print('ALL DONE: Video_Thuyet_Trinh_HOMER_Chinh_Thuc.mp4 created successfully!')

