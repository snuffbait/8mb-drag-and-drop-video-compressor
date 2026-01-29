import os
import sys
import subprocess

def get_duration(file):
    cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', file]
    return float(subprocess.check_output(cmd).decode().strip())

def get_bitrate(duration, size):
    bits = size * 8 * 1024 * 1024
    audio = 128 * 1024
    video = (bits / duration) - audio
    return max(int(video / 1024), 100)

def compress(input_file):
    output = input_file.replace('.mp4', '_compressed.mp4')
    duration = get_duration(input_file)
    bitrate = get_bitrate(duration, 7.5)
    
    cmd = [
        'ffmpeg', '-i', input_file,
        '-c:v', 'libx264',
        '-b:v', f'{bitrate}k',
        '-preset', 'medium',
        '-c:a', 'aac',
        '-b:a', '128k',
        '-y',
        output
    ]
    
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

compress(sys.argv[1])
