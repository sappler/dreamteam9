#!/usr/bin/env python3

import bluetooth
import subprocess
import sys
import time
import io
try:
        subprocess.call(['sudo', 'hciconfig', 'hci0', 'piscan'])
except:
        print("shell call didn't work")
        sys.exit()

server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
server_sock.bind(("", bluetooth.PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = "8ce255c0-200a-11e0-ac64-0800200c9a66"

bluetooth.advertise_service(server_sock, "piServer", service_id=uuid,
                            service_classes=[uuid, bluetooth.SERIAL_PORT_CLASS],
                            profiles=[bluetooth.SERIAL_PORT_PROFILE],
                            # protocols=[bluetooth.OBEX_UUID]
                           )

def transfer(f):
    print('opened file')
    
    print('sent opcode for sending file')
    bytes=1
    while bytes:
        time.sleep(0.5)
        #prevent sending data too quickly. Android can't handle it for some reason
        #this just makes sure for every 1000 bytes sent, we get a response at least once
        data = client_sock.recv(1024)
        print('phone received data')
        bytes=f.read(1000)
        print(len(bytes))
        client_sock.send(bytes)
        print('sent')
    print('finished sending')
    client_sock.send(str.encode('\x04'))



while True:
    print("Waiting for connection on RFCOMM channel", port)
    client_sock, client_info = server_sock.accept()
    print("Accepted connection from", client_info)
    try:
        while True:
            data = client_sock.recv(1024)
            if not data:
                break
            code=str(data)[2]
            #print(data)
            if code=='1': # change settings
                with open('/home/pi/dreamteam9/StateMachine/config.txt','r') as f:
                    settings=f.read()
                with open('/home/pi/dreamteam9/StateMachine/config.txt','w') as f:
                    f.write(str(data)[4:-1])
                    
                print('changed settings to: ' + str(data)[4:-1])
                client_sock.send(str.encode('1'))
            elif code=='2': # requested file
                try:
                    with open("/home/pi/dreamteam9/StateMachine/states_output.txt","rb") as f:
                        client_sock.send(str.encode('2'))
                        transfer(f)
                    with open("/home/pi/dreamteam9/StateMachine/datasets/accel.txt","rb") as f: 
                        transfer(f)
                except OSError as err:
                        print("OS error: {0}".format(err))
                        client_sock.send(str.encode('3'))
    except OSError as err:
        print("OS error: {0}".format(err))
    client_sock.close()
    print("All closed.")
