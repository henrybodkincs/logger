import logging

from datetime import datetime
from os import path

class Colors:
    """ Class to be used for setting logging colors. """
    WARNING = "\033[93m"
    ERROR = "\033[91m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    ENDC  = "\033[0m"

class Styles:
    """ Class to be used for setting different font types. """
    HEADER = "\033[95m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

class Headers:
    """ Class for quickly accessing headers. """
    INFO = "INFO"
    OK = "OK"
    WARNING = "WARNING"
    ERROR = "ERROR"

class Levels:
    """ Quick access to logger.Logging() levels. """
    NOTSET = 0
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50


class Log:
    """ Logging class for managing the formatting, storage and output of logs.

    Logging Types:
        [ERROR] = raised for issues that return application-breaking responses that occured while handling some request
        [WARNING] = raised for unexpected actions or processing some request
        [INFO] = raised for notifying the admins of something
        [OK] = raised when a process executed as expected (good for tests!)

    Logging Levels:
        Level 0:
            Logs everything to the Terminal.
        Level 1:
            Logs ERROR to Files. Logs WARNING/INFO/OK messages to Terminal.
        Level 2:
            Logs ERROR/WARNING to Files. - Logs INFO/OK to Terminal.
        Level 3:
            Logs everything to Files.
    """
    def __enter__(self):
        self.info("Opening logger.")
        return self

    def __exit__(self, *args):
        self.info("Closing logger.")

    def __init__(self, Name:str, Level:int=None, FilePath:str=None):
        self.log_count = 0
        self.file_path = None
        self.level = None

        #flags for logging
        self.save_ok = False
        self.save_info = False
        self.save_warning = False
        self.save_error = False

        #Enable/Disable the logger
        self.enabled = True
        self.name = Name
        logging.basicConfig()
        self.logger = logging.getLogger(self.name)
        
        self.log_file_worked = False
        self.log_level_worked = False

        if FilePath is not None:
            self.log_file_worked = self.set_log_file(FilePath)
        else:
            self.log_file_worked = True

        if Level is None or isinstance(Level, int) is False:
            Level = 0
        self.log_level_worked = self.set_log_level(Level)

        if self.log_level_worked and self.log_file_worked:
            self.info(Message=f"Sucessfuly started logging instance.")
        else:
            self.error(Message=f"Error occurred while initializing logging instance.")

    def disable(self):
        """ Disables all logging. """
        self.enabled = False
        self.logger.disabled = True #just in case


    def enable(self):
        """ Enables all logging """
        self.enabled = True
        self.logger.disabled = False #just in case


    def get_current_time(self):
        return datetime.now().time()

    def set_log_level(self, Level:int):
        """
            Updates the logging level if it is in range and sets the flags for
            logging into a file or terminal based off the new value.
            Use this function instead of manually updating Log().level
            as it will correctly update your flags for writing to files.
        """
        if not isinstance(Level, int):
            self.error("Level must be an int() type. Please specify a valid log level.")
            return False
        if Level > 0 and self.file_path is None:
            self.error("No FilePath has been specified for this log. Please use set_log_file(FilePath) to set a file path then call this function.")
            return False

        #executes exception when level is set to something other than an int/exists
        if self.level is not None and self.level == Level:
            self.warning(f"The specified level {Level} is already chosen. Please refer to the documentation/source code for more details on the available levels.")
            return False
        tmp = self.level
        #reset the save flags 
        self.save_ok = False
        self.save_info = False
        self.save_warning = False
        self.save_error = False

        if Level >= 0 and Level <= 3:
            self.level = Level
            if self.level == 1:
                self.save_error = True
            elif self.level == 2:
                self.save_error = True
                self.save_warning = True
            elif self.level == 3:
                self.save_ok = True
                self.save_info = True
                self.save_warning = True
                self.save_error = True

            #logger level will always be set to DEBUG since
            #the class itself will handle whether a file goes to terminal or file.
            self.logger.setLevel(level=logging.DEBUG)
            self.info(f"Log level successfully set to {self.level}.")
            return True
        else:
            self.warning(f"Specified level {Level} is not a valid range. Please refer to the documentation for more details.")
            return False

    def set_log_file(self, FilePath:str):
        try:
            if FilePath is None:
                self.warning(f"No file path has been specified for this log.")
                return False
            if path.isfile(FilePath):
                file_handler = logging.FileHandler(
                        filename=FilePath,
                        mode="a",
                        encoding="utf-8"
                        )
                formatter = logging.Formatter("%(message)s")
                file_handler.setFormatter(formatter)
                self.logger.addHandler(file_handler)
                self.file_path = FilePath
                self.ok(f"Successfully set file path for logger to: {FilePath}")
                return True
            else:
                self.error(f"The specified file path is not an existing file. Please create it to set the new log path.")
        except Exception as e:
            self.error(f"An error occurred while setting the log file: {e}")
        return False


    def log_to_terminal(self, Message:str, Header:str=None, Color:str=None, Style:str=None):
        current_time = self.get_current_time()
        if Header is None:
            Header = "LOG"
        if Color is None and Style is None:
            print(f"[{Header}] [{self.name} - {self.log_count}]: {current_time} - {Message}")
        else:
        #pass formatting appropiately:
            if Color is not None and Style is not None:
                #color and style
                print(f"[{current_time}] [{Color}{Style}{Header}{Colors.ENDC}] [{self.name}] [{self.log_count}] - {Message}")
            elif Color is not None and Style is None:
                #only color
                print(f"[{current_time}] [{Color}{Header}{Colors.ENDC}] [{self.name}] [{self.log_count}] - {Message}")
            else:
                #only style
                print(f"[{current_time}] [{Style}{Header}{Colors.ENDC}] [{self.name}] [{self.log_count}] - {Message}")

        self.log_count += 1


    def log_to_file(self, Header:str, Level:int, Message:str):
        """ Logs the specific message into the log file(assuming the file path was set and the logger is enabled."""
        current_time = self.get_current_time()
        if Header is None:
            Header = "LOG"
        formatted_msg = f"[{current_time}] [{Header}] [{self.name}] [{self.log_count}] - {Message}"
        self.logger.propagate = False
        self.logger.log(level=logging.DEBUG, msg=formatted_msg)
        self.logger.propagate = True
        self.log_count += 1

    def info_to_file(self, Message:str):
        level = Levels.DEBUG
        header = "INFO"
        self.log_to_file(Header=header, Level=level, Message=Message)


    def ok_to_file(self, Message:str):
        level = Levels.DEBUG
        header = Headers.OK
        self.log_to_file(Header=header, Level=level, Message=Message)
    
    def warning_to_file(self, Message:str):
        header = Headers.WARNING
        level = Levels.DEBUG
        self.log_to_file(Header=header, Level=level, Message=Message)


    def error_to_file(self, Message:str):
        header = Headers.ERROR
        level = Levels.DEBUG
        self.log_to_file(Header=header, Level=level, Message=Message)


    def warning_to_terminal(self, Message:str):
        header = Headers.WARNING
        color = Colors.WARNING
        style = Styles.BOLD
        self.log_to_terminal(Message=Message, Header=header, Color=color, Style=style)


    def error_to_terminal(self, Message:str):
        header = Headers.ERROR
        color = Colors.ERROR
        style = Styles.BOLD
        self.log_to_terminal(Message=Message, Header=header, Color=color, Style=style)


    def ok_to_terminal(self, Message:str):
        header = Headers.OK
        color = Colors.OKBLUE
        style = Styles.BOLD
        self.log_to_terminal(Message=Message, Header=header, Color=color, Style=style)


    def info_to_terminal(self, Message:str):
        header = Headers.INFO
        color = Colors.OKCYAN
        style = Styles.BOLD
        self.log_to_terminal(Message=Message, Header=header, Color=color, Style=style)


    def ok(self, Message:str):
        """ Logs [OK] messages to either the terminal or file depending on self.level """
        if not self.enabled:
            return
        if self.save_ok:
            self.ok_to_file(Message)
        else:
            self.ok_to_terminal(Message)


    def error(self, Message:str):
        """ Logs [ERROR] messages to either the terminal or file depending on self.level """
        if not self.enabled:
            return
        if self.save_error:
            self.error_to_file(Message)
        else:
            self.error_to_terminal(Message)


    def info(self, Message:str):
        """ Logs [INFO] messages to either the terminal or file depending on self.level """
        if not self.enabled:
            return
        if self.save_info:
            self.info_to_file(Message)
        else:
            self.info_to_terminal(Message)


    def warning(self, Message:str):
        """ Logs [WARNING] messages to either the terminal or file depending on self.level """
        if not self.enabled:
            return
        if self.save_warning:
            self.warning_to_file(Message)
        else:
            self.warning_to_terminal(Message)
