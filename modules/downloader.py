import yt_dlp
import os


def download_song(url, title):
    try:
        if not os.path.exists('downloads'):
            os.makedirs('downloads')
            
        safe_title = "".join([c for c in title if c.isalnum() or c in (' ', '-', '_')]).rstrip()
        output_file = os.path.join('downloads', f"{safe_title}.mp3")
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output_file,
            'progress_hooks': [progress_hook],
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }],
            'quiet': False,
            'no_warnings': False
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
        return output_file
        
    except Exception as e:
        raise Exception(f"Error al descargar: {str(e)}")