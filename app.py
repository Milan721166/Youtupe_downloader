from flask import Flask, render_template, request, send_file
import os
import yt_dlp

app = Flask(__name__)

# Directory to save downloaded videos
DOWNLOAD_FOLDER = "downloads"

# Create the downloads folder if it doesn't exist
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    try:
        # Get the URL and type (audio/video) from the form
        video_url = request.form['url']
        file_type = request.form['file_type']  # audio or video

        # Define yt-dlp options based on file type
        if file_type == "video":
            ydl_opts = {'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s')}
        elif file_type == "audio":
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
            }
        else:
            return render_template('index.html', error="Invalid file type selection.")

        # Use yt-dlp to download the video or audio
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            file_path = ydl.prepare_filename(info_dict)

        # Send the downloaded file to the user
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            return render_template('index.html', error="File not found after download.")
    except yt_dlp.utils.DownloadError as e:
        return render_template('index.html', error=f"Download Error: {e}")
    except Exception as e:
        return render_template('index.html', error=f"Unexpected Error: {e}")

if __name__ == '__main__':
    app.run(debug=True)
