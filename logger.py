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
        #self.logger.close()

    def __init__(self, Name:str, Level:int=None, FilePath:str=None):
        self.log_count = 0

        #Enable/Disable the logger
        self.enabled = True
        self.name = Name
        logging.basicConfig()
        self.logger = logging.getLogger(self.name)
        #flags set to save specific logging-types to a file.
        self.save_ok = False
        self.save_info = False
        self.save_warning = False
        self.save_error = False

        if FilePath is None:
            Level = 0 #set level to None since no filepath will be written to.
            self.warning(Message=f"Log path was not specified/found. Log file will not be set for {self.name}.")
        else:
            if path.isfile(FilePath):
                if self.set_log_file(FilePath):
                    self.info(Message=f"Log file has been set.")
                else:
                    self.error(Message=f"Log file was unable to be configured properly. Please make sure the log file exists.")
            else:
                Level = 0 #do not try to save anything if the file is set.
                self.warning(Message=f"Specified file was not found. Log file will not be set for {self.name}")

        if Level is not None and (Level >= 0 and Level <= 3):
            self.level = Level
            if self.level == 1:
                self.save_error = True
            elif self.level == 2:
                self.save_error = True
                self.save_warning = True
            elif self.level == 3 or self.level == 4:
                self.save_ok = True
                self.save_info = True
                self.save_warning = True
                self.save_error = True
            #logger level always set to
            #DEBUG since this class will handle whether a file goes to
            #terminal or file.
            self.logger.setLevel(10)
            self.info(Message=f"Log level set to: {self.level}")
        else:
            self.level = 0
            self.error(Message=f"Log level out of bounds: {self.level}")

        self.info(Message=f"Sucessfuly started logging instance for: {self.name}")


    def get_current_time(self):
        return datetime.now().time()


    def set_log_file(self, FilePath:str):
        if path.isfile(FilePath):
            file_handler = logging.FileHandler(
                    filename=FilePath,
                    mode="a",
                    encoding="utf-8"
                    )
            formatter = logging.Formatter("%(message)s")
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
            return True
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
        self.logger.log(level=10, msg=formatted_msg)
        self.log_count += 1

    def info_to_file(self, Message:str):
        """ TODO """
        level = 10
        header = "INFO"
        self.log_to_file(Header=header, Level=level, Message=Message)


    def ok_to_file(self, Message:str):
        """ TODO """
        level = 10
        header = "OK"
        #header = "OK"
        self.log_to_file(Header=header, Level=level, Message=Message)
    
    def warning_to_file(self, Message:str):
        header = "WARNING"
        level = 10
        self.log_to_file(Header=header, Level=level, Message=Message)


    def error_to_file(self, Message:str):
        header = "ERROR"
        level = 10
        self.log_to_file(Header=header, Level=level, Message=Message)


    def warning_to_terminal(self, Message:str):
        header = "WARNING"
        color = Colors.WARNING
        style = Styles.BOLD
        self.log_to_terminal(Message=Message, Header=header, Color=color, Style=style)


    def error_to_terminal(self, Message:str):
        header = "ERROR"
        color = Colors.ERROR
        style = Styles.BOLD
        self.log_to_terminal(Message=Message, Header=header, Color=color, Style=style)


    def ok_to_terminal(self, Message:str):
        header = "OK"
        color = Colors.OKBLUE
        style = Styles.BOLD
        self.log_to_terminal(Message=Message, Header=header, Color=color, Style=style)


    def info_to_terminal(self, Message:str):
        header = "INFO"
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
