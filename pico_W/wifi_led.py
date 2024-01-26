import network
import socket
from time import sleep
from machine import Pin

pico_led=Pin(0, Pin.OUT)

ssid = 'Gearbox Members'
password = 'Members@Gearbox'

def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip


def open_socket(ip):
    # Open a socket
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    print(connection)
    return connection

def webpage(state):
    #Template HTML
    html = f"""
            <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">
    <title>Document</title>
</head>
<body>
<div class="row">
    <div class = "col-sm-12">
       <form action="./lighton">
            <div class="mb-0 mt-5 mx-5">
                <button type="submit"  class="btn btn-danger" value="Light on">Light on</button>
            </div>
        </form>
    </div>
    <div class = "col-sm-12">
       <form action="./lightoff">
            <div class="mb-0 mt-2 mx-5">
                <button type="submit"  class="btn btn-primary" value="Light off">Light off</button>
            </div>
        </form>
    </div>
        <div class="mx-5">
        <p>LED is {state}</p>
        </div>
    </div>
    
            
           
            
</body>
</html>
            """
    return str(html)

def serve(connection):
    #Start a web server
    state = 'OFF'
    pico_led.off()
    temperature = 0
    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        try:
            request = request.split()[1]
        except IndexError:
            pass
        if request == '/lighton?':
            pico_led.on()
            state = 'ON'
        elif request =='/lightoff?':
            pico_led.off()
            state = 'OFF'
        
        html = webpage(state)
        client.send(html)
        client.close()
try:
    ip = connect()
    connection = open_socket(ip)
    serve(connection)
except KeyboardInterrupt:
    machine.reset()