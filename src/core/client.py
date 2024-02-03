import socketio
import time

sio = socketio.Client(reconnection=True)

@sio.event
def connect():
    print("Connected to the server")

@sio.event
def disconnect():
    print("Disconnected from the server")

@sio.event
def update_location(data):
    print('Received location', data)


@sio.event
def update_block(data):
    print('Received block', data)

@sio.event
def x(data):
    print('Received x', data)

def main():
    try:
        sio.connect('http://localhost:8080', namespaces=['/'])
        sio.wait()
    except KeyboardInterrupt:
        print("Shutting down client.")
        sio.disconnect()

if __name__ == "__main__":
    main()
