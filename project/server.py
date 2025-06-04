import socket
import os

HOST = 'localhost'
PORT = 65432
BUFFER_SIZE = 4096
SAVE_PATH = 'uploads/received_file'

os.makedirs('uploads', exist_ok=True)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("🔌 Server đang chờ file...")

    conn, addr = s.accept()
    with conn:
        print(f"📥 Kết nối từ {addr}")
        with open(SAVE_PATH, 'wb') as f:
            while True:
                data = conn.recv(BUFFER_SIZE)
                if not data:
                    break
                f.write(data)
        print("✅ Đã nhận file xong!")
