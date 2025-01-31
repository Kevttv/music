import requests
import json
import re
from urllib.parse import quote

def search_songs(query):
    try:
        search_url = f"https://www.youtube.com/results?search_query={quote(query)}&sp=EgIQAQ%253D%253D"
        response = requests.get(search_url)
        
        if response.status_code != 200:
            return []

        pattern = r'var ytInitialData = ({.*?});'
        matches = re.search(pattern, response.text)
        
        if not matches:
            return []

        data = json.loads(matches.group(1))
        videos = data['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents']
        
        results = []
        for video in videos[:5]:
            if 'videoRenderer' not in video:
                continue
                
            video_data = video['videoRenderer']
            video_id = video_data.get('videoId', '')
            
            if not video_id:
                continue
                
            title = video_data.get('title', {}).get('runs', [{}])[0].get('text', 'Sin título')
            duration_str = video_data.get('lengthText', {}).get('simpleText', '0:00')
            preview_url = f"https://music.youtube.com/watch?v={video_id}"
            
            results.append({
                'title': title,
                'url': f'https://youtube.com/watch?v={video_id}',
                'preview_url': preview_url,
                'duration_str': duration_str,
                'thumbnail': f'https://img.youtube.com/vi/{video_id}/maxresdefault.jpg'
            })
            
        return results

    except Exception as e:
        print(f"Error en la búsqueda: {str(e)}")
        return []