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

class CountFilter(logging.Filter):
    """ This count filter is applied to the logger for displaying messages correctly. """
    def filter(self, record):
        record.count = counter
        return True

class Log:
    """ Logging class for managing the formatting, storage and output of logs.

    Logging Types:
        [ERROR] = raised for issues that return application-breaking responses that occured while handling some request
        [WARNING] = raised for unexpected actions or processing some request
        [INFO] = raised for notifying the admins of something
        [OK] = raised when a process executed as expected (good for tests!)

    Logging Levels:
        Level 0/1:
            Logs all messages to Terminal.
        Level 2:
            Logs ERROR to Files. Logs WARNING/INFO/OK to Terminal.
        Level 3:
            Logs ERROR/WARNING to Files. - Logs INFO/OK to Terminal.
        Level 4/5:
            Logs everything to Files.
    """
    def __enter__(self):
        self.info("Opening logger.")
        return self

    def __exit__(self, *args):
        self.info("Closing logger.")
        #self.logger.close()

    def __init__(self, Name:str, Level:int=None, LogPath:str=None):
        #Enable/Disable the logger
        self.enabled = True
        self.name = Name

        logging.basicConfig()
        self.logger = logging.getLogger(self.name)
        formatter = logging.Formatter("[%(levelname)s] [%(name)s - %(count)s] [%(asctime)s] - %(message)s", "%F")
        self.logger.addFilter(CountFilter())
        self.count = 0

        #flags set to save specific logging-types to a file.
        self.save_ok = False
        self.save_info = False
        self.save_warning = False
        self.save_error = False

        if LogPath is None:
            Level = 0 #set level to None since no filepath will be written to.
            self.warning_to_terminal(Message=f"Log path was not specified/found. Log file will not be set for {self.name}.")
        else:
            if path.isfile(LogPath):
                self.log_path = LogPath
                file_handler = logging.FileHandler(
                        filename=self.log_path,
                        mode="a",
                        encoding="utf-8"
                        )
                #self.logger.addHandler(file_handler)
                self.ok_to_terminal(Message=f"Log file will be set to: {self.LogPath}")
            else:
                Level = 0 #do not try to save anything if the file is set.
                self.warning_to_terminal(Message=f"Specified file was not found. Log file will not be set for {self.name}")

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
            self.info_to_terminal(Message=f"Log level set to: {self.level}")
        else:
            self.level = 0
            self.error_to_terminal(Message=f"Log level out of bounds: {self.level}")

        self.info_to_terminal(Message=f"Sucessfuly started logging instance for: {self.name}")

    def get_current_time(self):
        return datetime.now().time()

    def log_to_terminal(self, Message:str, Header:str=None, Color:str=None, Style:str=None):
        current_time = self.get_current_time()
        if Header is None:
            Header = "LOG"
        if Color is None and Style is None:
            print(f"[{Header}] [{self.name} - {self.count}]: {current_time} - {Message}")
        else:
        #pass formatting appropiately:
            if Color is not None and Style is not None:
                #color and style
                print(f"[{Color}{Style}{Header}{Colors.ENDC}] [{self.name} - {self.count}] [{current_time}] - {Message}")
            elif Color is not None and Style is None:
                #only color
                print(f"[{Color}{Header}{Colors.ENDC}] [{self.name} - {self.count}] [{current_time}] - {Message}")
            else:
                #only style
                print(f"[{Style}{Header}{Colors.ENDC}] [{self.name} - {self.count}] [{current_time}] - {Message}")

        self.count += 1

    def log_to_file(self, Level:int, Message:str):
        """ TODO """
        self.logger.log(level=Level, msg=Message)

    def info_to_file(self, Message:str):
        """ TODO """
        level = 10
        self.log_to_file(Level=level, Message=Message)


    def ok_to_file(self, Message:str):
        """ TODO """
        level = 10
        header = "OK"
        #header = "OK"
        #self.log_to_file(Header=header, Message=Message, File=self.LogPath)
    
    def warning_to_file(self, Message:str):
        header = "WARNING"
        pass


    def error_to_warning(self, Message:str):
        header = "ERROR"
        pass


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
