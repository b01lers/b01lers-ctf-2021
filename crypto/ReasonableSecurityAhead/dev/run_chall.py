import socket, sys, subprocess


port = int(sys.argv[1])  if len(sys.argv) > 1   else  13371
host = sys.argv[2]       if len(sys.argv) > 2   else  "localhost"
arg  = sys.argv[3]       if len(sys.argv) > 3   else  "0"


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
   s.bind((host, port))
   s.listen()
   #s.listen(200)
   while True:
      conn, addr = s.accept()
      with conn:
         print(addr[0], "connected on port", addr[1])
         subprocess.run(["python3.7", "server.py", arg], stdin = conn, stdout = conn)
         # close connection - FIXME: this does not make vanilla netcat (nc) terminate...
         conn.shutdown(socket.SHUT_RDWR)
         conn.close()


