import socket
from urllib.parse import urlparse, parse_qs


HOST = "0.0.0.0"
PORT = 8080


def http_response(status_code, body):
    reasons = {
        200: "OK",
        400: "Bad Request",
        404: "Not Found",
        405: "Method Not Allowed",
    }

    body = str(body)

    response = (
        f"HTTP/1.1 {status_code} {reasons[status_code]}\r\n"
        f"Content-Type: text/plain\r\n"
        f"Content-Length: {len(body.encode())}\r\n"
        f"Connection: keep-alive\r\n"
        f"\r\n"
        f"{body}"
    )

    return response.encode()


def calculate(path, query):
    try:
        a = int(query.get("a", [None])[0])
        b = int(query.get("b", [None])[0])
    except Exception:
        return 400, "invalid numbers"

    if path == "/add":
        return 200, str(a + b)

    elif path == "/sub":
        return 200, str(a - b)

    elif path == "/mul":
        return 200, str(a * b)

    elif path == "/div":
        if b == 0:
            return 400, "division by zero"

        return 200, str(a // b)

    return 404, "route not found"


def handle_request(request_text):
    lines = request_text.split("\r\n")

    if not lines:
        return http_response(400, "bad request")

    try:
        method, target, version = lines[0].split()
    except ValueError:
        return http_response(400, "bad request")

    if method != "GET":
        return http_response(405, "method not allowed")

    parsed = urlparse(target)

    status, body = calculate(
        parsed.path,
        parse_qs(parsed.query)
    )

    return http_response(status, body)


def handle_client(conn):
    buffer = b""

    while True:
        try:
            data = conn.recv(4096)

            if not data:
                break

            buffer += data

            while b"\r\n\r\n" in buffer:
                request, buffer = buffer.split(
                    b"\r\n\r\n",
                    1
                )

                response = handle_request(
                    request.decode()
                )

                conn.sendall(response)

        except ConnectionResetError:
            break
        except Exception as e:
            print("Client error:", e)
            break

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

    print(f"Listening on {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()

        print(
            f"Client connected: "
            f"{addr[0]}:{addr[1]}"
        )

        handle_client(conn)


if __name__ == "__main__":
    main()