
import socketio
import eventlet  # 如果你选择使用gevent，请相应地导入gevent

sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(
    sio, static_files={"/": {"content_type": "text/html", "filename": "index.html"}}
)

class SocketIOEventsHandler:
    def __init__(self, sio):
        self.sio = sio
        self.register_events()

    def register_events(self):
        @self.sio.event
        def connect(sid, environ):
            print('Client connected', sid)

        @self.sio.event
        def disconnect(sid):
            print('Client disconnected', sid)

        @self.sio.event
        def location(sid, data):
            print('Received location:', data)
            self.process_location(sid, data)

        @self.sio.event
        def block(sid, data):
            print('Received block event:', data)
            self.process_block(sid, data)

    def process_location(self, location):
        # 处理位置数据
        print(f'Processing location data')

    def process_block(self, tag):
        # 处理block事件
        print(f'Processing block data')
