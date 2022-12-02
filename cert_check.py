import ssl, socket, datetime


def get_cert(host, port: int=443):
    ctx = ssl.create_default_context()
    with ctx.wrap_socket(socket.socket(), server_hostname=host) as s:
        s.connect((host, port))
        cert = s.getpeercert()
    return cert

def get_cert_left(host):

    d = get_cert(host)['notAfter']


    dt = datetime.datetime.strptime(d, "%b %d %H:%M:%S %Y GMT")
    delta = dt-datetime.datetime.now()
    return delta.days

def main():
    checks = [
        'google.com',
        'bing.com',
        'example.com'
    ]
    max_len = max([len(c) for c in checks])
    results = []
    for c in checks:
        results.append((c,  get_cert_left(c)))

    # Sort by days, then names
    results.sort(key=lambda x: (x[1], x[0]))

    for r in results:
        print(f"{r[0]:<{max_len+1}}", r[1], sep="")

if __name__ == '__main__':
    main()
