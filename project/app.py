from flask import Flask, render_template, request, send_file
import socket
import os
from utils import sha256_file

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

SERVER_HOST = 'localhost'
SERVER_PORT = 65432

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)

            # Tính hash trước khi gửi
            original_hash = sha256_file(filepath)

            # Gửi file qua socket
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((SERVER_HOST, SERVER_PORT))
                with open(filepath, 'rb') as f:
                    while chunk := f.read(4096):
                        s.sendall(chunk)

            # So sánh hash
            received_path = os.path.join(UPLOAD_FOLDER, 'received_file')
            received_hash = sha256_file(received_path)

            if original_hash == received_hash:
                result = f"✅ File hợp lệ! Hash: {original_hash}"
            else:
                result = f"❌ File bị lỗi! Hash gốc: {original_hash} | Hash nhận: {received_hash}"

    return render_template('index.html', result=result)

@app.route('/download')
def download():
    path = os.path.join(UPLOAD_FOLDER, 'received_file')
    return send_file(path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
