import requests
import socketio
import time

# Create HTTP sessions
session_tdk = requests.Session()
session_lvh = requests.Session()

# Login
session_tdk.post('http://127.0.0.1:5000/', data={'username': 'tdk', 'password': '123456'})
session_lvh.post('http://127.0.0.1:5000/', data={'username': 'lvh', 'password': '123456'})

cookie_tdk = '; '.join([f"{k}={v}" for k, v in session_tdk.cookies.items()])
cookie_lvh = '; '.join([f"{k}={v}" for k, v in session_lvh.cookies.items()])

sio_tdk1 = socketio.Client()
sio_tdk2 = socketio.Client()
sio_lvh = socketio.Client()

@sio_tdk2.on('receive_message')
def msg_tdk2(data):
    print("tdk2 RECEIVED message:", data['plaintext'])

# Connect tdk1 and lvh
sio_tdk1.connect('http://127.0.0.1:5000', headers={'Cookie': cookie_tdk})
sio_lvh.connect('http://127.0.0.1:5000', headers={'Cookie': cookie_lvh})
time.sleep(1)

# Connect tdk2 (overlapping connection, e.g. same user opening another tab or refreshing)
print("\n--- Connecting tdk2 (overlapping) ---")
sio_tdk2.connect('http://127.0.0.1:5000', headers={'Cookie': cookie_tdk})
time.sleep(1)

# Now disconnect the old tdk1 (tab closed / old connection times out)
print("\n--- Disconnecting tdk1 ---")
sio_tdk1.disconnect()
time.sleep(2)

print("\n--- Current Server State ---")
r = requests.get('http://127.0.0.1:5000/debug')
print(r.json())

# Now try to send message from lvh to tdk
print("\n--- Sending message from lvh to tdk (should go to tdk2) ---")
sio_lvh.emit('send_message', {'receiver': 'tdk', 'message': 'Hello tdk2!'})

time.sleep(2)

sio_tdk2.disconnect()
sio_lvh.disconnect()
