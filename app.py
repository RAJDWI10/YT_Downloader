from flask import Flask, request, send_file, jsonify, send_from_directory
from yt_dlp import YoutubeDL
import os
import uuid

app = Flask(__name__)

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/download', methods=['POST'])
def download_video():
    data = request.json
    url = data.get('url')

    if not url:
        return jsonify({'error': 'URL missing'}), 400

    try:
        # Temporary output filename
        filename = f"/tmp/{uuid.uuid4()}.mp4"
        ydl_opts = {
            'format': 'best',
            'outtmpl': filename
        }

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        return send_file(filename, as_attachment=True)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Required for Render
    app.run(host='0.0.0.0', port=port)
