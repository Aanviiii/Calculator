import socket
import threading
from urllib.parse import urlparse, parse_qs

HOST = "0.0.0.0"
PORT = 8080


def build_response(status_code, body):
    reasons = {
        200: "OK",
        400: "Bad Request",
        404: "Not Found",
        405: "Method Not Allowed",
        500: "Internal Server Error"
    }

    body = str(body)

    response = (
        f"HTTP/1.1 {status_code} {reasons.get(status_code, 'Unknown')}\r\n"
        f"Content-Type: text/plain\r\n"
        f"Content-Length: {len(body.encode())}\r\n"
        f"Connection: keep-alive\r\n"
        f"\r\n"
        f"{body}"
    )

    return response.encode()


def perform_calculation(path, query):
    try:
        a = float(query["a"][0])
        b = float(query["b"][0])
    except (KeyError, ValueError, IndexError):
        return 400, "Invalid or missing parameters"

    if path == "/add":
        return 200, a + b

    elif path == "/sub":
        return 200, a - b

    elif path == "/mul":
        return 200, a * b

    elif path == "/div":
        if b == 0:
            return 400, "Division by zero"

        return 200, a / b

    return 404, "Route not found"


def handle_request(request_text):
    try:
        lines = request_text.split("\r\n")

        if not lines:
            return build_response(400, "Bad Request")

        request_line = lines[0]

        try:
            method, target, version = request_line.split()
        except ValueError:
            return build_response(400, "Malformed Request")

        if method != "GET":
            return build_response(405, "Method Not Allowed")

        parsed = urlparse(target)

        status, body = perform_calculation(
            parsed.path,
            parse_qs(parsed.query)
        )

        return build_response(status, body)

    except Exception as e:
        print("Request processing error:", e)
        return build_response(500, "Internal Server Error")


def handle_client(conn, addr):
    print(f"[CONNECTED] {addr}")

    buffer = b""

    try:
        while True:
            data = conn.recv(4096)

            if not data:
                break

            buffer += data

            while b"\r\n\r\n" in buffer:

                request_bytes, buffer = buffer.split(
                    b"\r\n\r\n",
                    1
                )

                request_text = request_bytes.decode(
                    "utf-8",
                    errors="ignore"
                )

                first_line = request_text.split("\r\n")[0]
                print(f"[REQUEST] {addr} -> {first_line}")

                response = handle_request(request_text)

                conn.sendall(response)

    except ConnectionResetError:
        print(f"[DISCONNECTED] {addr}")

    except Exception as e:
        print(f"[ERROR] {addr}: {e}")

    finally:
        conn.close()


def main():
    server = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    server.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_REUSEADDR,
        1
    )

    server.bind((HOST, PORT))
    server.listen()

    print("=" * 50)
    print(f"Calculator Server Running")
    print(f"Listening on {HOST}:{PORT}")
    print("=" * 50)

    while True:
        conn, addr = server.accept()

        thread = threading.Thread(
            target=handle_client,
            args=(conn, addr),
            daemon=True
        )

        thread.start()


if __name__ == "__main__":
    main()