import socket
import time
import random
from threading import Thread
from multiprocessing import Process, Queue
import logging, sys

import os
from _thread import *

def setup_custom_logger(name):
    # adapted from https://stackoverflow.com/a/28330410
    # set up logging to file - see previous section for more details
    formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')
    # handler = logging.FileHandler('log.txt', mode='w')
    handler = logging.FileHandler(name+'.log', mode='w')
    handler.setFormatter(formatter)
    screen_handler = logging.StreamHandler(stream=sys.stdout)
    screen_handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    logger.addHandler(screen_handler)
    return logger

def consumer(conn):
    # each machine listens on its own consumer thread, which initializes its queue

    print("consumer accepted connection" + str(conn)+"\n")
    while True:
        data = conn.recv(1024)
        dataVal = data.decode('ascii')
        msg_queue.append(dataVal)
 

def producer(portVal1, portVal2):
    # tries to initiate connection to another port

    host = "127.0.0.1" # localhots
    port_first = int(portVal1)
    port_second = int(portVal2)
    s1 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s2 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sleepVal = 1.0/clock_rate
    # print(sleepVal)

    #sema acquire
    try:
        s1.connect((host,port_first))
        print("Client-side connection success to port val:" + str(portVal1) + "\n")
        s2.connect((host,port_second))
        print("Client-side connection success to port val:" + str(portVal2) + "\n")

        while True:
            # update clock value immediately
            global clock_value
            clock_value += 1


            # if msg_queue is not empty, then read the first message in the queue
            if len(msg_queue) > 0:
                msg = msg_queue.pop(0)
                # if msg is greater than clock_value, then update clock_value
                if int(msg) > clock_value:
                    clock_value = int(msg)
                    # print("clock updated:", clock_value)
                # else:
                    # print("clock not updated:", clock_value)
                
                logger.info("msg received, logical clock time: "+str(clock_value)+" queue length: "+str(len(msg_queue)))

            # if msg_queue empty, generate own event and follow instructions   
            else:
                prob = random.randint(1, events_prob)
                # if prob == 1, then send message to first other process
                if prob == 1:
                    # print("msg sent 1", clock_value)
                    codeVal = str(clock_value)
                    s1.send(codeVal.encode('ascii'))
                    logger.info("msg sent, logical clock time: "+str(clock_value))
                # if prob == 2, then send message to second other process
                if prob == 2:
                    # print("msg sent 2", clock_value)
                    codeVal = str(clock_value)
                    s2.send(codeVal.encode('ascii'))
                    logger.info("msg sent, logical clock time: "+str(clock_value))
                # if prob == 3, then send message to both processes
                if prob == 3:
                    # print("msg sent BOTH", clock_value)
                    codeVal = str(clock_value)
                    s1.send(codeVal.encode('ascii'))
                    s2.send(codeVal.encode('ascii'))
                    logger.info("msg sent, logical clock time: "+str(clock_value))
                # else, internal event
                else:
                    logger.info("internal event, logical clock time: "+str(clock_value)) 
            
            # wait before next action
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

    # initialize the probability of an event
    global events_prob
    events_prob = 10

    # initialize the logging for the process
    global logger
    logger = setup_custom_logger('process'+str(config[1]-5550))
    logger.info("Log set up for process "+str(config[1]-5550)+" with clock rate "+str(clock_rate))
    # print("logging initialized for process", config[1]-5550)

    # initialize listeners
    init_thread = Thread(target=init_machine, args=(config,)) # start a thread for the consumer, to listen
    init_thread.start()

    #add delay to initialize the server-side logic on all processes
    time.sleep(5)

    # extensible to multiple producers, we just use one producer that connects to two threads though
    prod_thread = Thread(target=producer, args=(config[2], config[3],)) # start a thread for the producer, to send
    prod_thread.start()
 
    # while True:
    #     time.sleep(1)
    #     print("Machine:", int(config[1])-5550, "(clock rate %d)"%(clock_rate), "logical clock value:", clock_value)


localHost= "127.0.0.1"
    

if __name__ == '__main__':
    port1 = 5551
    port2 = 5552
    port3 = 5553
    

    # each config is structured as [host, listening port, sending port 1, sending port 2]
    config1=[localHost, port1, port2, port3]
    p1 = Process(target=machine, args=(config1,))
    config2=[localHost, port2, port3, port1]
    p2 = Process(target=machine, args=(config2,))
    config3=[localHost, port3, port1, port2]
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