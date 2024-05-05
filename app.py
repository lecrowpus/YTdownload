from flask import Flask, render_template, request, send_file
from pytube import YouTube, Playlist
import os
import shutil

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download_video', methods=['POST'])
def download_video():
    try:
        video_url = request.form['video_url']
        yt = YouTube(video_url)
        video_stream = yt.streams.get_highest_resolution()
        output_folder = os.path.join('static', 'downloads', 'videos')
        os.makedirs(output_folder, exist_ok=True)
        video_path = os.path.join(output_folder, f'{yt.title}.mp4')
        video_stream.download(output_folder)
        zip_file_path = os.path.join('static', 'downloads', 'videos.zip')
        shutil.make_archive(zip_file_path[:-4], 'zip', output_folder)
        return render_template('success.html', title=yt.title, url='/download/videos.zip')
    except Exception as e:
        return render_template('error.html', error_message=str(e))

@app.route('/download_playlist', methods=['POST'])
def download_playlist():
    try:
        playlist_url = request.form['playlist_url']
        playlist = Playlist(playlist_url)
        output_folder = os.path.join('static', 'downloads', 'playlist')
        os.makedirs(output_folder, exist_ok=True)

        for video_url in playlist.video_urls:
            yt = YouTube(video_url)
            video_stream = yt.streams.get_highest_resolution()
            video_stream.download(output_folder)

        zip_file_path = os.path.join('static', 'downloads', 'playlist.zip')
        shutil.make_archive(zip_file_path[:-4], 'zip', output_folder)

        return render_template('success_playlist.html', playlist_title=playlist.title, url='/download/playlist.zip')
    except Exception as e:
        return render_template('error.html', error_message=str(e))

@app.route('/download/<filename>')
def download(filename):
    return send_file(os.path.join('static', 'downloads', filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
