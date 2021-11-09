import selenium
import socketio


def run():
    sio = socketio.Client()
    sio.connect('http://192.168.1.10:3001')

    @sio.on('client remove')
    def client_remove(data):
        print(data)


if __name__ == '__main__':
    run()
