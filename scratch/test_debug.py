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

sio_tdk = socketio.Client()
sio_lvh = socketio.Client()

sio_tdk.connect('http://127.0.0.1:5000', headers={'Cookie': cookie_tdk})
sio_lvh.connect('http://127.0.0.1:5000', headers={'Cookie': cookie_lvh})

print("State immediately after connection:")
r = requests.get('http://127.0.0.1:5000/debug')
print(r.json())

# Wait for 5 seconds
time.sleep(5)

print("State after 5 seconds:")
r = requests.get('http://127.0.0.1:5000/debug')
print(r.json())

# Disconnect one client and connect again (simulate page refresh)
print("\n--- Simulating tdk page refresh ---")
sio_tdk.disconnect()
time.sleep(1)

sio_tdk = socketio.Client()
sio_tdk.connect('http://127.0.0.1:5000', headers={'Cookie': cookie_tdk})
time.sleep(2)

print("State after tdk refresh:")
r = requests.get('http://127.0.0.1:5000/debug')
print(r.json())

# Now try to send message from lvh to tdk
print("\n--- Sending message from lvh to tdk ---")
sio_lvh.emit('send_message', {'receiver': 'tdk', 'message': 'Hello tdk!'})

time.sleep(2)

sio_tdk.disconnect()
sio_lvh.disconnect()
