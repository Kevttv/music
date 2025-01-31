from flask import Flask, render_template, request, send_file, jsonify
from modules.searcher import search_songs
from modules.downloader import download_song
import os

app = Flask(__name__)
app.config['STATIC_FOLDER'] = 'static'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query')
    if not query:
        return render_template('index.html', error='Se requiere un término de búsqueda')
    
    results = search_songs(query)
    return render_template('index.html', results=results)

@app.route('/download', methods=['POST'])
def download():
    try:
        url = request.form['url']
        title = request.form['title']
        file_path = download_song(url, title)
        return send_file(
            file_path, 
            as_attachment=True,
            download_name=os.path.basename(file_path)
        )
    except Exception as e:
        return render_template('index.html', error=str(e))

if __name__ == '__main__':
    app.run(debug=True)