from http.server import HTTPServer, CGIHTTPRequestHandler


def main():
    server_address = ("", 8000)
    httpd = HTTPServer(server_address, CGIHTTPRequestHandler)
    httpd.serve_forever()


if __name__ == "__main__":  # If run as a script, create a test object
    main()
