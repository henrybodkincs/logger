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


    #Test if initializing Log() instance updates parameters as expected
    def test_disable_enable(self):
        log = logger.Log(Name=log_name)
        self.assertEqual(log.enabled, True)
        log.disable()
        self.assertEqual(log.enabled, False)
        log.enable()
        self.assertEqual(log.enabled, True)

    #Test that disabling the logger will not output any statements or increase log_count
    def test_disabled_messages(self):
        log = logger.Log(Name=log_name)
        log.disable()
        log.log_count = 0
        self.assertEqual(log.ok("test"), None)
        self.assertEqual(log.log_count, 0)
        self.assertEqual(log.info("test"), None)
        self.assertEqual(log.log_count, 0)
        self.assertEqual(log.warning("test"), None)
        self.assertEqual(log.log_count, 0)
        self.assertEqual(log.error("test"), None)
        self.assertEqual(log.log_count, 0)

    
    #Test that an enabled logger will try to output statements + increase log_count
    def test_enabled_messages(self):
        log = logger.Log(Name=log_name)
        log.log_count = 0
        self.assertEqual(log.ok("Testing OK"), None)
        self.assertEqual(log.log_count, 1)
        self.assertEqual(log.info("Testing INFO"), None)
        self.assertEqual(log.log_count, 2)
        self.assertEqual(log.warning("Testing WARNING"), None)
        self.assertEqual(log.log_count, 3)
        self.assertEqual(log.error("Testing ERROR"), None)
        self.assertEqual(log.log_count, 4)


    def test_set_log_file(self):
        log = logger.Log(Name=log_name)
        log.disable()
        self.assertEqual(log.set_log_file(log_path), True)
        self.assertEqual(log.file_path, log_path)
        log = logger.Log(Name=log_name, FilePath=log_path)
        self.assertEqual(log.file_path, log_path)

    """
    #test that saving strings into a specified file works as expected
    def test_save_to_file(self):
        log = logger.Log(Name=log_name)
    """

    def test_set_log_level(self):
        log = logger.Log(Name=log_name, Level=0)
        log.disable()
        self.assertEqual(log.level, 0)
        self.assertEqual(log.set_log_level(1), False)
        self.assertEqual(log.set_log_level(2), False)
        self.assertEqual(log.set_log_level(None), False)
        self.assertEqual(log.set_log_level("a"), False)
        self.assertEqual(log.set_log_level(3), False)

    
