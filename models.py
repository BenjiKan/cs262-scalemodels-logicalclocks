import socket
import time
import random
from threading import Thread
from multiprocessing import Process, Queue
import logging

import os
from _thread import *

# class Clock


# def machine(config):
#     # virtual machine that starts a clock
#     # config is a dictionary with the following keys:
#     #   'name' - name of the machine
#     #   'ip' - ip address of the machine
#     #   'port' - port number of the machine
#     #   'clock' - clock type
#     #   'offset' - offset of the clock
#     #   'drift' - drift of the clock

#     # create a socket

#     # bind the socket to the ip and port
#     # listen for connections
#     # accept connections
#     # receive data
#     # send data
#     # close the socket
#     pass

def consumer(conn):
    # each machine listens on its own consumer thread, which initializes its queue

    print("consumer accepted connection" + str(conn)+"\n")
    # msg_queue=[]
    sleepVal = 0.900 # proxy for clock rate
    while True:
        time.sleep(sleepVal)
        data = conn.recv(1024)
        print("msg received\n")
        dataVal = data.decode('ascii')
        print("msg received:", dataVal)
        msg_queue.append(dataVal)
 

def producer(portVal):
    # tries to initiate connection to another port

    host = "127.0.0.1" # localhots
    port = int(portVal)
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sleepVal = 1.0/clock_rate
    print(sleepVal)

    #sema acquire
    try:
        s.connect((host,port))
        print("Client-side connection success to port val:" + str(portVal) + "\n")
 

        while True:
            # update clock value immediately
            clock_value += 1
            
            # if msg_queue is not empty, then read the first message in the queue
            if len(msg_queue) > 0:
                msg = msg_queue.pop(0)
                print("msg received:", msg)
                # if msg is greater than clock_value, then update clock_value
                if int(msg) > clock_value:
                    clock_value = int(msg)
                    print("clock updated:", clock_value)
                else:
                    print("clock not updated:", clock_value)

            # if msg_queue empty, generate own event and follow instructions   
            else:
                prob = random.randint(1, 10)
                # if prob == 1, then send message to first other process
                if prob == 1:
                    print("msg sent", clock_value)
                    codeVal = str(clock_value)
                    s.send(codeVal.encode('ascii'))
                # if prob == 2, then send message to second other process
                if prob == 2:
                    print("msg sent", clock_value)
                    codeVal = str(clock_value)
                    s.send(codeVal.encode('ascii'))
                # if prob == 3, then send message to both processes
                if prob == 3:
                    print("msg sent", clock_value)
                    codeVal = str(clock_value)
                    s.send(codeVal.encode('ascii'))
                    print("msg sent", clock_value)
                    codeVal = str(clock_value)
                    s.send(codeVal.encode('ascii'))
                # else, internal event
                else:
                    pass 


                    
                

            codeVal = str(clock_value)
            s.send(codeVal.encode('ascii'))
            print("msg sent", codeVal)

            time.sleep(sleepVal)

    

    except socket.error as e:
        print ("Error connecting producer: %s" % e)
 

def init_machine(config):
    HOST = str(config[0])
    PORT = int(config[1])
    print("starting server| port val:", PORT, "clock rate:", clock_rate)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen()
    while True:
        conn, addr = s.accept()
        start_new_thread(consumer, (conn,))
 

def machine(config):
    config.append(os.getpid())
    # initialize the logical clock value for the process
    global clock_value 
    clock_value = 0

    # initialize the queue for the process
    global msg_queue
    msg_queue = []

    # initialize clock rate for process
    global clock_rate
    clock_rate = random.randint(1, 6)

    # initialize the logging for the process
    # TODO
    # logging.basicConfig(filename='process'+str(config[3])+'.log',level=logging.DEBUG)

    
    # initialize listeners
    init_thread = Thread(target=init_machine, args=(config,)) # start a thread for the consumer, to listen
    init_thread.start()

    #add delay to initialize the server-side logic on all processes
    time.sleep(5)

    # extensible to multiple producers
    prod_thread = Thread(target=producer, args=(config[2],)) # start a thread for the producer, to send
    prod_thread.start()
 
    while True:
        time.sleep(1)
        print("Machine:", int(config[1])-5550, "(clock rate %d)"%(clock_rate), "logical clock value:", clock_value)
        # print("msg queue:", msg_queue)



localHost= "127.0.0.1"
    

if __name__ == '__main__':
    port1 = 5551
    port2 = 5552
    port3 = 5553
    

    # each connection is bidirectional, so only need three connections
    config1=[localHost, port1, port2,]
    p1 = Process(target=machine, args=(config1,))
    config2=[localHost, port2, port3]
    p2 = Process(target=machine, args=(config2,))
    config3=[localHost, port3, port1]
    p3 = Process(target=machine, args=(config3,))
    

    p1.start()
    p2.start()
    p3.start()
    

    p1.join()
    p2.join()
    p3.join()


# if __name__ == '__main__':
    
    # set up logging to file - see previous section for more details
    
    # initialize the clocks

    # start the clocks