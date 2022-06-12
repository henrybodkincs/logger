""" Tests for getting/setting log files. """
import logging

from logger import logger

log_path = "tests/test_log.log"
log_name = "Test Logger"

class TestLogging:
    def test_default_init(self):
        log = logger.Log(Name=log_name)
        assert log.name == log_name
        assert log.save_error is False
        assert log.save_warning is False
        assert log.save_ok is False
        assert log.save_info is False
        assert log.file_path is None
        assert log.log_file_set is False
        assert log.log_level_set is False
        assert log.enabled is True
        assert log.level == 0


    def test_disable_enable(self):
        log = logger.Log(Name=log_name)
        assert log.enabled is True
        log.disable()
        assert log.enabled is False
        log.enable()
        assert log.enabled is True


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


    def test_set_log_file(self, caplog):
        other_log = logger.Log(Name=log_name, FilePath=log_path)
        log = logger.Log(Name=log_name)
        assert other_log.file_path == log_path
        assert log.set_log_file(log_path) is True
        assert log.file_path == log_path


    """
    def test_save_to_file(self, caplog):
        msg = "Testing test_save_to_file"
        log = logger.Log(Name=log_name, Level=2, FilePath=log_path)
        log.error(msg)
        logging.getLogger()
        assert caplog.records != []
        assert msg in caplog.text
    """

    def test_set_log_level(self):
        log = logger.Log(Name=log_name, Level=0)
        #test 0 flags
        assert log.level == 0
        assert log.save_error is False
        assert log.save_ok is False
        assert log.save_info is False
        assert log.save_warning is False
        #test 1 flags
        assert log.set_log_level(1) is True
        assert log.level == 1
        assert log.save_error is True
        assert log.save_ok is False
        assert log.save_info is False
        assert log.save_warning is False
        #test 2 flags
        assert log.set_log_level(2) is True
        assert log.level == 2
        assert log.save_error is True
        assert log.save_ok is False
        assert log.save_info is False
        assert log.save_warning is True
        #test 3 flags
        assert log.set_log_level(3) is True
        assert log.level == 3
        assert log.save_error is True
        assert log.save_ok is True
        assert log.save_info is True
        assert log.save_warning is True
        #test that flags/levels aren't reset on invalid inputs
        assert log.set_log_level(None) is False
        assert log.level == 3
        assert log.set_log_level("a") is False
        assert log.level == 3
        assert log.set_log_level(33) is False
        assert log.level == 3
        assert log.save_error is True
        assert log.save_ok is True
        assert log.save_info is True
        assert log.save_warning is True

