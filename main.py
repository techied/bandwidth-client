from selenium import webdriver
import socketio
import subprocess
import json

server_address = '192.168.1.10'
server_port = 3001


def init():
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

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)

    @sio.on('connect')
    def on_connect():
        print('Reconnected')
        sio.emit('client mac', mac)

    @sio.on('iperf3')
    def on_iperf3(data):
        if mac in data:
            print('iperf3')
            stdout = subprocess.run(["iperf3", "-Jc", server_address], capture_output=True, text=True).stdout
            json_obj = json.loads(stdout)
            bits_per_second = json_obj['end']['sum_received']['bits_per_second']
            sio.emit('iperf3 results', {"mac": mac, "bits_per_second": bits_per_second})

    @sio.on('webtest')
    def on_webtest(data):
        if mac in data['macs']:
            print('webtest')
            results = []
            total_load_time = 0
            for site in data['sites']:
                hyperlink = site['url']
                driver.get(hyperlink)
                # navigation_start = driver.execute_script("return window.performance.timing.navigationStart")
                # response_start = driver.execute_script("return window.performance.timing.responseStart")
                # dom_complete = driver.execute_script("return window.performance.timing.domComplete")
                # load_event_end = driver.execute_script("return window.performance.timing.loadEventEnd")

                fetch_time = driver.execute_script(
                    "return window.performance.timing.responseEnd - window.performance.timing.responseStart")

                results.append({"url": site['url'], "performance": fetch_time})
                total_load_time += fetch_time

            sio.emit('webtest results', {"mac": mac, "results": results, "totalLoadTime": total_load_time})

    @sio.on('client remove')
    def client_remove(data):
        print(data)


if __name__ == '__main__':
    run()
