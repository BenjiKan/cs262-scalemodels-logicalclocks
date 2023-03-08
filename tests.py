import unittest
import unittest.mock
from io import StringIO
import logging, sys
import time
import socket
import random

from models import *
import models

class TestHelpers(unittest.TestCase):
    def test_logger(self):
        name = "TestingLog"
        logger = models.setup_custom_logger(name)
        with unittest.mock.patch('sys.stdout', new = StringIO()) as out:
            logger.handlers.clear() # remove file creation
            logging.getLogger(name).addHandler(logging.StreamHandler(out)) # add to output

            strings_to_test = [
                "This is a test INFO logger call",
                "This is another test logger call, status INFO",
                "Test debug call"
            ]
            for i in range(len(strings_to_test)): # test that strings are logged correctly
                logger.info(strings_to_test[i])
                self.assertEqual(out.getvalue(),\
                                  "".join(list(map(lambda s: s + '\n', strings_to_test[:i+1]))))

class TestModel(unittest.TestCase):

    def test_producer_connections(self):
        port1 = 5551
        port2 = 5552
        port3 = 5553
        # each config is structured as [host, listening port, sending port 1, sending port 2]
        config1=[models.localHost, port1, port2, port3]
        with unittest.mock.patch("socket.socket") as mock_socket:
            

            logger = models.setup_custom_logger('process'+str(config1[1]-5550))
            logger.handlers.clear() # just to make output more condensed
            try:
                prod1 = models.producer(logger, config1[2], config1[3])
            except KeyboardInterrupt:
                pass
            mock_socket.return_value.connect.raiseError.side_effect = unittest.mock.Mock(side_effect = socket.error("TestSocketError"))
            # Assert that sockets are created and called
            mock_socket.assert_has_calls([unittest.mock.call(socket.AF_INET,socket.SOCK_STREAM), unittest.mock.call(socket.AF_INET,socket.SOCK_STREAM)])

    def test_init_machine(self):
        port1 = 5551
        port2 = 5552
        port3 = 5553
        # each config is structured as [host, listening port, sending port 1, sending port 2]
        config1=[models.localHost, port1, port2, port3]
        with unittest.mock.patch("socket.socket") as mock_socket:
            try:
                init_machine(config1)
            except KeyboardInterrupt:
                pass
            except ValueError:
                pass
            mock_socket.assert_called_once_with(socket.AF_INET,socket.SOCK_STREAM)
            mock_socket.return_value.bind.assert_called()
    
    def test_random_event_1(self):
        # Tests when prob resolves to 1
        logger = models.setup_custom_logger('blah')
        logger.handlers.clear()
        with unittest.mock.patch.object(random, "randint", unittest.mock.Mock(return_value=1)):
            mock1 = unittest.mock.Mock()
            mock1.send = unittest.mock.Mock(return_value = None)
            mock2 = unittest.mock.Mock()
            mock2.send = unittest.mock.Mock(return_value = None)
            t = producer_run_random_event(logger, mock1, mock2)
            mock1.send.assert_called_once()
            mock2.send.assert_not_called()

    def test_random_event_2(self):
        # Tests when prob resolves to 2
        logger = models.setup_custom_logger('blah')
        logger.handlers.clear()
        with unittest.mock.patch.object(random, "randint", unittest.mock.Mock(return_value=2)):
            mock1 = unittest.mock.Mock()
            mock1.send = unittest.mock.Mock(return_value = None)
            mock2 = unittest.mock.Mock()
            mock2.send = unittest.mock.Mock(return_value = None)
            t = producer_run_random_event(logger, mock1, mock2)
            mock1.send.assert_not_called()
            mock2.send.assert_called_once()
    
    def test_random_event_3(self):
        # Tests when prob resolves to 3
        logger = models.setup_custom_logger('blah')
        logger.handlers.clear()
        with unittest.mock.patch.object(random, "randint", unittest.mock.Mock(return_value=3)):
            mock1 = unittest.mock.Mock()
            mock1.send = unittest.mock.Mock(return_value = None)
            mock2 = unittest.mock.Mock()
            mock2.send = unittest.mock.Mock(return_value = None)
            t = producer_run_random_event(logger, mock1, mock2)
            mock1.send.assert_called_once()
            mock2.send.assert_called_once()

    def test_random_event_internal(self):
        # Tests when prob resolves to an internal event
        logger = models.setup_custom_logger('blah')
        logger.handlers.clear()
        with unittest.mock.patch.object(random, "randint", unittest.mock.Mock(return_value=5)):
            mock1 = unittest.mock.Mock()
            mock1.send = unittest.mock.Mock(return_value = None)
            mock2 = unittest.mock.Mock()
            mock2.send = unittest.mock.Mock(return_value = None)
            t = producer_run_random_event(logger, mock1, mock2)
            mock1.send.assert_not_called()
            mock2.send.assert_not_called()


if __name__=="__main__":
    print('\033[1m' + '\033[96m' + "\nUse Ctrl-C for KeyboardInterrupts\n" + '\033[0m')
    unittest.main()