""" Tests for getting/setting log files. """
from logger import logger

log_path = "tests/test_log.log"
log_name = "Test Log"

class TestLogging:
    #Test initialization of default logger
    def test_default_init(self):
        log = logger.Log(Name=log_name)
        assert log.name == log_name
        assert log.save_error is False
        assert log.save_warning is False
        assert log.save_ok is False
        assert log.save_info is False
        assert log.file_path is None
        assert log.enabled is True
        assert log.level == 0

    #Test if initializing Log() instance updates parameters as expected
    def test_disable_enable(self):
        log = logger.Log(Name=log_name)
        assert log.enabled is True
        log.disable()
        assert log.enabled is False
        log.enable()
        assert log.enabled is True

    #Test that disabling the logger will not output any statements or increase log_count
    def test_disabled_messages(self):
        log = logger.Log(Name=log_name)
        log.disable()
        log.log_count = 0
        assert log.ok("test") is None
        assert log.log_count == 0
        assert log.info("test") is None
        assert log.log_count == 0
        assert log.warning("test") is None
        assert log.log_count == 0
        assert log.error("test") is None
        assert log.log_count == 0
    
    #Test that an enabled logger will try to output statements + increase log_count
    def test_enabled_messages(self):
        log = logger.Log(Name=log_name)
        log.log_count = 0
        assert log.ok("Testing OK") is None
        assert log.log_count == 1
        assert log.info("Testing INFO") is None
        assert log.log_count == 2
        assert log.warning("Testing WARNING") is None
        assert log.log_count == 3
        assert log.error("Testing ERROR") is None
        assert log.log_count == 4


    def test_set_log_file(self):
        log = logger.Log(Name=log_name)
        assert log.set_log_file(log_path) is True
        assert log.file_path == log_path
        log = logger.Log(Name=log_name, FilePath=log_path)
        assert log.file_path == log_path

    """
    #test that saving strings into a specified file works as expected
    def test_save_to_file(self):
        log = logger.Log(Name=log_name)
    """

    #attempt to change log level without setting a log path
    #and without using int() datatype
    def test_set_log_level(self):
        log = logger.Log(Name=log_name, Level=0)
        assert log.level == 0
        assert log.set_log_level(1) is False
        assert log.set_log_level(2) is False
        assert log.set_log_level(3) is False
        assert log.set_log_level(None) is False
        assert log.set_log_level("a") is False
        assert log.set_log_level(33) is False
