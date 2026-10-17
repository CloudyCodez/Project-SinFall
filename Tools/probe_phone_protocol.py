import socket,threading,time
from pathlib import Path
root=Path('E:/7DS-Offline/Research/PhoneProtocol');root.mkdir(exist_ok=True)
listener=socket.socket();listener.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1);listener.bind(('127.0.0.1',5002));listener.listen()
print('Protocol capture proxy ready',flush=True)
def pipe(src,dst,name):
 with (root/name).open('wb') as file:
  try:
   while True:
    b=src.recv(1048576)
    if not b:break
    file.write(b);file.flush();print(name,len(b),b[:48].hex(),flush=True);dst.sendall(b)
  except OSError as e: print(name,str(e),flush=True)
while True:
 c,_=listener.accept();s=socket.create_connection(('127.0.0.1',5001));stamp=str(time.time_ns())
 threading.Thread(target=pipe,args=(c,s,stamp+'-client.bin'),daemon=True).start()
 threading.Thread(target=pipe,args=(s,c,stamp+'-server.bin'),daemon=True).start()
