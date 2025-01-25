import os
import zipfile
import shlex
import subprocess
from flask import Flask, render_template, request, send_file, jsonify

app = Flask(__name__)
UPLOAD_FOLDER = './uploads'
DOWNLOAD_FOLDER = './downloads'
EXIFTOOL_PATH = 'exiftool'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    # Ambil data dari form
    files = request.files.getlist('images')
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    keywords = request.form.get('keywords', '').strip()

    # Validasi data
    if not files or not title or not description or not keywords:
        return jsonify({'error': 'Semua kolom harus diisi!'}), 400

    # Proses setiap file
    processed_files = []
    for file in files:
        if file.filename == '':
            continue
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        # Tambahkan metadata menggunakan ExifTool
        try:
            command = [
                EXIFTOOL_PATH,
                '-overwrite_original',
                f"-XMP-dc:Title={shlex.quote(title)}",
                f"-XMP-dc:Description={shlex.quote(description)}",
                f"-XMP-dc:Subject={shlex.quote(keywords)}",
                file_path
            ]
            result = subprocess.run(command, capture_output=True, text=True)
            if result.returncode == 0:
                processed_files.append(file_path)
        except Exception as e:
            return jsonify({'error': f"Gagal memproses file {file.filename}: {e}"}), 500

    # Buat file zip jika ada banyak file
    zip_path = os.path.join(DOWNLOAD_FOLDER, 'processed_images.zip')
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for file in processed_files:
            zipf.write(file, os.path.basename(file))

    return jsonify({'message': 'Proses selesai!', 'download_url': '/download/processed_images.zip'})


@app.route('/download/<path:filename>')
def download(filename):
    file_path = os.path.join(DOWNLOAD_FOLDER, filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return "File tidak ditemukan!", 404


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5151)
