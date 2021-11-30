import selenium
import socketio
import subprocess
import json

server_address = '192.168.1.10'
server_port = 3001


def init():
    mac = '00:00:00:00:00:00'
    with open('/sys/class/net/eth0/address') as f:
        lines = f.readlines()
        mac = lines[0].strip()
    return mac


def run():
    mac = init()
    print('MAC: %s' % mac)
    sio = socketio.Client()
    sio.connect('http://%s:%i' % (server_address, server_port))

    sio.emit('client mac', mac)

    @sio.on('iperf3')
    def on_iperf3(data):
        print(data)
        if mac in data:
            print('iperf3')
            stdout = subprocess.run(["iperf3", "-Jc", server_address], capture_output=True, text=True).stdout
            json_obj = json.loads(stdout)
            bits_per_second = json_obj['end']['sum_received']['bits_per_second']
            print('bits per second: %d' % bits_per_second)
            sio.emit('iperf3 results', {"mac": mac, "bits_per_second": bits_per_second})

    @sio.on('client remove')
    def client_remove(data):
        print(data)


if __name__ == '__main__':
    run()
