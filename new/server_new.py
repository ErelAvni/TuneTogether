import socket
import threading


def start_server(host='127.0.0.1', port=65432):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()
        print(f"Server started. Listening on {host}:{port}...")
        
        while True:
            conn, addr = server_socket.accept()
            threading.Thread(target=handle_client_request, args=(conn, addr)).start()
            with conn:
                print(f"Connected by {addr}")


def handle_client_request(conn, addr):
    with conn:
        print(f"Connected by {addr}")
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    break
                request = data.decode('utf-8')
                print(f"Received request from {addr}: {request}")
                # Process the ServerRequest here
                


            except Exception as e:
                print(f"Error handling request from {addr}: {e}")
                break
            

def add_comment(comment : str):
    pass


if __name__ == "__main__":
    start_server()