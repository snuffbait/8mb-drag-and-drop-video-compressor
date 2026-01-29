import os
import sys
import subprocess

def durr(file):
    cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', file]
    return float(subprocess.check_output(cmd).decode().strip())

def bitss(duration, size):
    bits = size * 8 * 1024 * 1024
    audio = 128 * 1024
    video = (bits / duration) - audio
    return max(int(video / 1024), 100)

def compress(filez):
    output = filez.replace('.mp4', '_snuff_compressed.mp4')
    duration = durr(filez)
    bitrate = bitss(duration, 7.5)
    
    cmd = [
        'ffmpeg', '-i', filez,
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
