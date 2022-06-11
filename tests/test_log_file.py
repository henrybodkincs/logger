""" Tests for getting/setting log files. """
import logging
import unittest

import logger

log_path = "tests/test_log.log"
log_name = "Test Log"

class Test(unittest.TestCase):
    #Test initialization of default logger
    def test_default_init(self):
        log = logger.Log(Name=log_name)
        self.assertEqual(log.name, log_name)
        self.assertEqual(log.save_error, False)
        self.assertEqual(log.save_warning, False)
        self.assertEqual(log.save_ok, False)
        self.assertEqual(log.save_info, False)
        self.assertEqual(log.file_path, None)
        self.assertEqual(log.enabled, True)
        self.assertEqual(log.level, 0)
    
    def test_set_log_file(self):
        log = logger.Log(Name=log_name)
        self.assertEqual(log.set_log_file(log_path), True)
        self.assertEqual(log.file_path, log_path)

    #test that saving strings into a specified file works as expected
    """
    def test_save_to_file(self):
        log = logger.Log(Name=log_name)
    """

    #Test if initializing Log() instance updates parameters as expected
    def test_disable_enable(self):
        log = logger.Log(Name=log_name)
        self.assertEqual(log.enabled, True)
        log.disable()
        self.assertEqual(log.enabled, False)
        log.enable()
        self.assertEqual(log.enabled, True)

