#/usr/bin/env python3
import socket, ssl
import re
import getpass

# check why I always get  len(body) < content length

def read_page(s):

    if not hasattr(s, 'recv'):
        s.recv=s.read
        # yeah great! sock and ssl_sock do not have the same APIs 

    # 1. Get the content length
    buf = s.recv(4096)
    while True:
        m = re.search(b'Content-Length: (\d+)',buf)
        if m:
            content_length = int(m.groups()[0])
            break
        else:
            buf += s.recv(4096)

    # 2. Find the empty line
    while True:
        m = re.search(b'\\r\\n\\r\\n',buf)
        if m:
            hdr, body = buf[:m.start()], buf[:m.end()]
            break
        else:
            buf += s.recv(4096)

    remaining = content_length - len(body)

    # 3. Read exactly "content length" bytes, 
    while remaining>0 and len(buf)!=0:   # why can't recv exactly the content length !
        buf = s.recv(4096 if remaining > 4096 else remaining)
        remaining -= len(buf)
        body += buf
    s.close()
    return (hdr, body)

def getpage(path):
    # Read a page
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('lwn.net',80))

    req = """GET %s HTTP/1.1
Host: lwn.net 

""" % (path)

    s.send(bytes(req, 'ascii'))
    return read_page(s)


def get_auth_cookie(username='RobWilco'):
    # 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssl_sock = ssl.wrap_socket(s,
                           ca_certs=None,
                           cert_reqs=ssl.CERT_NONE)
    ssl_sock.connect(('lwn.net',443))

    req = """POST /login HTTP/1.1
Host: lwn.net
Content-Type: application/x-www-form-urlencoded
Content-Length: 37

Username=%s&Password=%s""" % (username, getpass.getpass())

    print req

    ssl_sock.write(req.decode('ascii'))
    hdr, body = read_page(ssl_sock)
    m = re.search(b'Set-Cookie: (.*?);',hdr)
    if m:
        return m.groups()[0] 
    else:
        print('Could not find the cookie')

def getpage_auth(path, cookie):

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('lwn.net',80))

    req = """GET %s HTTP/1.1
Host: lwn.net
Cookie: %s

""" % (path, cookie.decode('ascii'))

    s.send(req.decode('ascii'))
    return read_page(s)

cookie = get_auth_cookie()
print(cookie.decode('ascii'))
print(getpage_auth('/Articles/402512/', cookie)[0].decode('ascii'))

