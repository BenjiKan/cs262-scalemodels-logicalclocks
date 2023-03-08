import socket
import time
import random
import os
import unittest
from unittest.mock import patch

from models import *


class TestMachine(unittest.TestCase):
    @patch('models.socket.socket')
    def test_init_machine(self, mock_socket):
        localHost= "127.0.0.1"
        port1 = 5551
        port2 = 5552
        port3 = 5553
        
        config1=[localHost, port1, port2, port3]

        global clock_rate 
        clock_rate = 1

        init_machine(config1)
        mock_socket.assert_called_once_with(socket.AF_INET, socket.SOCK_STREAM)
        mock_socket().bind.assert_called_once_with((host, port1))
        mock_socket().listen.assert_called_once()

    
    @patch('models.socket.socket')
    def test_machine(self, mock_socket):
        localHost= "127.0.0.1"
        port1 = 5551
        port2 = 5552
        port3 = 5553
        
        config1=[localHost, port1, port2, port3]

        machine(config1)
        # global variables
        unittest.assertTrue(len(msg_queue) == 0)
        unittest.assertTrue(clock_value >= 0)

        init_machine.assert_called_once_with(config1)
        producer.assert_called_once_with(config1[2], config1[3])

    @patch('models.socket.socket')
    def test_consumer(self, mock_socket):
        localHost= "127.0.0.1"
        port1 = 5551
        port2 = 5552
        port3 = 5553

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        test_prod = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        test_prod.bind((localHost, port1))
        test_prod.listen()

        s.connect(localHost, port1)
        conn, addr = test_prod.accept()

        consumer(conn)
        
        unittest.assertTrue(len(msg_queue)==0)
        s.send("test")
        unittest.assertTrue(len(msg_queue)==1)


    @patch('models.socket.socket')
    def test_producer(self, mock_socket):
        localHost= "127.0.0.1"
        port1 = 5551
        port2 = 5552
        port3 = 5553
        
        global s1, s2
        producer(port1, port2)

        s1.connect.assert_called_once_with((localHost, port1))
        s2.connect.assert_called_once_with((localHost, port2))
        unittest.assertTrue(events_prob>0)
        unittest.assertTrue(events_prob<=10)   

class TestLogger(unittest.TestCase):
    def test_setup_custom_logger(self):
        logger_name = 'test_logger'
        setup_custom_logger(logger_name)
        # logger = logging.getLogger(logger_name)

        # check that log file
        self.assertTrue(os.path.exists(logger_name+'.log'))

    def delete(self):
        os.remove(logger_name+'.log')


if __name__ == '__main__':
    unittest.main()
