import logging
from typing import Optional
from datetime import datetime
from os import path


class Colors:
    """Class to be used for setting logging colors."""

    YELLOW = "\033[93m"
    RED = "\033[91m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    ENDC = "\033[0m"


class Styles:
    """Class to be used for setting different font types."""

    HEADER = "\033[95m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


class Headers:
    """Class for quickly accessing headers."""

    INFO = "INFO"
    OK = "OK"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class Log:
    """Logging class for managing the formatting, storage and output of logs.

    Logging Types: CRITICAL, ERROR, WARNING, INFO, OK

    Logging Levels:
        Level 0:
            Logs everything to the Terminal.
        Level 1:
            Logs CRITICAL to files. Logs ERROR/WARNING/INFO/OK messages to Terminal.
        Level 2:
            Logs ERROR/CRITICAL to files. Logs WARNING/INFO/OK to Terminal.
        Level 3:
            Logs ERROR/CRITICAL/WARNING to files.  Logs INFO/OK to Terminal
        Level 4:
            Logs everything to Files.
    """

    def __enter__(self):
        self.info("Opening logger.")
        return self

    def __exit__(self, *args):
        self.info("Closing logger.")

    def __init__(self, Name: str, Level: int = None, FilePath: str = None):
        self.name = Name
        self.logger = logging.getLogger(self.name)
        self.log_count = 0
        self.level = 0
        self.enabled = True
        self.file_path = None

        # flags for logging
        self.save_ok = False
        self.save_info = False
        self.save_warning = False
        self.save_error = False
        self.save_critical = False

        self.set_log_file(FilePath)
        self.set_log_level(Level)

    def disable(self) -> None:
        """Disables all logging."""
        self.enabled = False
        self.logger.disabled = True

    def enable(self) -> None:
        """Enables all logging"""
        self.enabled = True
        self.logger.disabled = False

    def get_current_time(self) -> datetime:
        return datetime.today()

    def set_log_level(self, Level: int) -> bool:
        """
        Updates the logging level if it is in range and sets the flags for
        logging into a file or terminal based off the new value.
        Use this function instead of manually updating Log().level
        as it will correctly update your flags for writing to files.
        """
        if not isinstance(Level, int):
            return False
        if Level > 0 and self.file_path is None:
            self.error(
                "No FilePath has been specified for this log. Please use set_log_file(FilePath) to set a file path then call this function."
            )
            return False

        if Level >= 0 and Level <= 4:
            # reset the save flags
            self.save_ok = False
            self.save_info = False
            self.save_warning = False
            self.save_error = False
            self.save_critical = False
            self.level = Level
            if self.level == 1:
                self.save_critical = True
            elif self.level == 2:
                self.save_error = True
                self.save_critical = True
            elif self.level == 3:
                self.save_warning = True
                self.save_error = True
                self.save_critical = True
            elif self.level == 4:
                self.save_warning = True
                self.save_error = True
                self.save_critical = True
                self.save_ok = True
                self.save_info = True

            # logger level will always be set to DEBUG since
            # the class itself will handle whether a file goes to terminal or file.
            self.info(f"Log level set to {self.level}.")
            return True
        else:
            self.warning(
                f"Specified level {Level} is not a valid range. Please refer to the documentation for more details."
            )
            return False

    def set_log_file(self, FilePath: str) -> bool:
        try:
            if FilePath is None:
                self.warning(f"No file path has been specified for this log.")
            elif path.isfile(FilePath):
                file_handler = logging.FileHandler(
                    filename=FilePath, mode="a", encoding="utf-8"
                )
                self.logger.addHandler(file_handler)
                self.file_path = FilePath
                self.logger.setLevel(level=logging.DEBUG)
                self.ok(f"Pointing to new file path for logger: {FilePath}")
                return True
            else:
                self.error(
                    f"The specified file path {FilePath} is not an existing file. Please create it to set the new log path."
                )
        except Exception as e:
            self.error(f"An error occurred while setting the log file: {e}")
        return False

    def log_to_terminal(
        self, Message: str, Header: str = None, Color: str = None, Style: str = None
    ) -> None:
        current_time = self.get_current_time()
        if Header is None:
            Header = "LOG"
        if Color is None and Style is None:
            print(
                f"[{Header}] [{self.name} - {self.log_count}]: {current_time} - {Message}"
            )
        else:
            # pass formatting appropiately:
            if Color is not None and Style is not None:
                # color and style
                print(
                    f"[{current_time}] [{Color}{Style}{Header}{Colors.ENDC}] [{self.name}] [{self.log_count}] - {Message}"
                )
            elif Color is not None and Style is None:
                # only color
                print(
                    f"[{current_time}] [{Color}{Header}{Colors.ENDC}] [{self.name}] [{self.log_count}] - {Message}"
                )
            else:
                # only style
                print(
                    f"[{current_time}] [{Style}{Header}{Colors.ENDC}] [{self.name}] [{self.log_count}] - {Message}"
                )

        self.log_count += 1

    def log_to_file(self, Header: str, Level: int, Message: str) -> None:
        """Logs the specific message into the log file(assuming the file path was set and the logger is enabled."""
        current_time = self.get_current_time()
        if Header is None:
            Header = "LOG"
        formatted_msg = (
            f"[{current_time}] [{Header}] [{self.name}] [{self.log_count}] - {Message}"
        )
        self.logger.propagate = False
        self.logger.log(level=logging.CRITICAL, msg=formatted_msg)
        self.logger.propagate = True
        self.log_count += 1

    def info_to_file(self, Message: str) -> None:
        level = logging.DEBUG
        header = "INFO"
        self.log_to_file(Header=header, Level=level, Message=Message)

    def ok_to_file(self, Message: str) -> None:
        level = Logging.DEBUG
        header = Headers.OK
        self.log_to_file(Header=header, Level=level, Message=Message)

    def warning_to_file(self, Message: str) -> None:
        header = Headers.WARNING
        level = logging.DEBUG
        self.log_to_file(Header=header, Level=level, Message=Message)

    def error_to_file(self, Message: str) -> None:
        header = Headers.ERROR
        level = logging.DEBUG
        self.log_to_file(Header=header, Level=level, Message=Message)

    def critical_to_file(self, Message: str) -> None:
        header = Headers.CRITICAL
        level = logging.DEBUG
        self.log_to_file(Header=header, Level=level, Message=Message)

    def warning_to_terminal(self, Message: str) -> None:
        header = Headers.WARNING
        color = Colors.YELLOW
        style = Styles.BOLD
        self.log_to_terminal(Message=Message, Header=header, Color=color, Style=style)

    def error_to_terminal(self, Message: str) -> None:
        header = Headers.ERROR
        color = Colors.RED
        style = Styles.BOLD
        self.log_to_terminal(Message=Message, Header=header, Color=color, Style=style)

    def critical_to_terminal(self, Message: str) -> None:
        header = Headers.CRITICAL
        color = Colors.RED
        style = Styles.BOLD
        self.log_to_terminal(Message=Message, Header=header, Color=color, Style=style)

    def ok_to_terminal(self, Message: str) -> None:
        header = Headers.OK
        color = Colors.BLUE
        style = Styles.BOLD
        self.log_to_terminal(Message=Message, Header=header, Color=color, Style=style)

    def info_to_terminal(self, Message: str) -> None:
        header = Headers.INFO
        color = Colors.CYAN
        style = Styles.BOLD
        self.log_to_terminal(Message=Message, Header=header, Color=color, Style=style)

    def ok(self, Message: str) -> Optional[int]:
        """Logs [OK] messages to either the terminal or file depending on self.level"""
        if not self.enabled:
            return 1
        if self.save_ok:
            self.ok_to_file(Message)
        else:
            self.ok_to_terminal(Message)

    def error(self, Message: str) -> Optional[int]:
        """Logs [ERROR] messages to either the terminal or file depending on self.level"""
        if not self.enabled:
            return 1
        if self.save_error:
            self.error_to_file(Message)
        else:
            self.error_to_terminal(Message)

    def info(self, Message: str) -> Optional[int]:
        """Logs [INFO] messages to either the terminal or file depending on self.level"""
        if not self.enabled:
            return 1
        if self.save_info:
            self.info_to_file(Message)
        else:
            self.info_to_terminal(Message)

    def warning(self, Message: str) -> Optional[int]:
        """Logs [WARNING] messages to either the terminal or file depending on self.level"""
        if not self.enabled:
            return 1
        if self.save_warning:
            self.warning_to_file(Message)
        else:
            self.warning_to_terminal(Message)

    def critical(self, Message: str) -> Optional[int]:
        """Logs [CRITICAL] messages to either the terminal or file depending on self.level"""
        if not self.enabled:
            return 1
        if self.save_critical:
            self.critical_to_file(Message)
        else:
            self.critical_to_terminal(Message)
