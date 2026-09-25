# Persistent HTTP Calculator Server

A simple calculator server implemented using raw Python sockets and HTTP/1.1 persistent connections.

## Features

* Raw TCP sockets
* No frameworks
* HTTP/1.1 support
* Persistent connections (keep-alive)
* Arithmetic operations

Supported routes:

```text
/add?a=2&b=3
/sub?a=10&b=4
/mul?a=6&b=7
/div?a=9&b=3
```

## Status Codes

### 200 OK

Valid request.

### 400 Bad Request

Invalid parameters.

Example:

```text
/add?a=x&b=3
```

### 404 Not Found

Invalid route.

Example:

```text
/pow?a=2&b=8
```

### 405 Method Not Allowed

Any method other than GET.

Example:

```text
POST /add
```

## Run

```bash
python server.py
```

Output:

```text
Listening on 0.0.0.0:8080
```

## Test

Open browser:

```text
http://localhost:8080/add?a=2&b=3
```

or

```bash
python test_client.py
```

## Example

Request:

```http
GET /add?a=2&b=3 HTTP/1.1
```

Response:

```http
HTTP/1.1 200 OK

5
```

## Concepts Demonstrated

* TCP sockets
* HTTP request parsing
* Query parameters
* Persistent connections
* Keep-Alive
* HTTP response formatting
* Status codes
* Server architecture
