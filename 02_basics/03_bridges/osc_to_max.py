"""Send and receive Open Sound Control (OSC) between Python and Max.

In Max:
    [udpreceive 9000] -> [route /pluck /damp] -> ...     (Python -> Max)
    ... -> [prepend /fromMax] -> [udpsend 127.0.0.1 9001] (Max -> Python)

Install:  pip install python-osc
Run:      python osc_to_max.py
"""
import math
import threading
import time

from pythonosc.udp_client import SimpleUDPClient
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import ThreadingOSCUDPServer

MAX_IP, MAX_PORT = "127.0.0.1", 9000      # Max listens here
PY_PORT = 9001                            # Python listens here

client = SimpleUDPClient(MAX_IP, MAX_PORT)

def on_message(address, *args):
    print(f"from Max  {address}  {args}")

dispatcher = Dispatcher()
dispatcher.set_default_handler(on_message)
server = ThreadingOSCUDPServer(("127.0.0.1", PY_PORT), dispatcher)
threading.Thread(target=server.serve_forever, daemon=True).start()

# A slow sine sweeps the damping while a pluck is sent twice a second.
t0 = time.time()
try:
    while True:
        t = time.time() - t0
        client.send_message("/damp", 0.5 + 0.5 * math.sin(2 * math.pi * 0.1 * t))
        if int(t * 2) != int((t - 0.02) * 2):
            client.send_message("/pluck", [110.0, 0.8])   # frequency, velocity
        time.sleep(0.02)                                 # 50 messages per second
except KeyboardInterrupt:
    server.shutdown()
