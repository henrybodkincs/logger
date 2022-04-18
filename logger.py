from datetime import datetime
from os import path

class Colors:
    """ Class to be used for setting logging colors. """
    #colors
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

class Log(object):
    """ Logging class for managing the formatting, storage and output of logs.

    Logging Types:
        [ERROR] = raised for issues that return application-breaking responses that occured while handling some request
        [WARNING] = raised for unexpected actions or processing some request
        [INFO] = raised for notifying the admins of something
        [OK] = raised when a process executed as expected (good for tests!)

    Logging Levels:
        Level 0(Not recommended):
            Logs prints all messages to Terminal.
        Level 1(recommended):
            Logs Errors to Files. prints Warnings/Info/OK to Terminal.
        Level 2(recommended):
            Logs Errors and Warnings to Files. - prints Info/OK to Terminal.
        Level 3(Not recommended):
            Logs everything to Files. Can become cumbersome if lots of logging is done.
    """
    def __enter__(self):
        self.log_ok("Entering logger.")
        return self

    def __exit__(self):
        self.log_ok("Closing logger.")

    def __init__(self, Name:str, Level:int=None, LogPath:str=None):
        #Enable/Disable the logger
        self.enabled = True

        #name of the logger
        self.name = Name
        #Current count of the logger instance
        self.log_count = 0
        #flags set to save specific logging-types to a file.
        self.save_ok = False
        self.save_info = False
        self.save_warning = False
        self.save_error = False
        if Level is None or (Level >= 0 and Level <= 3):
            if Level is None:
                self.level = 0
            else:
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
            self.log_ok_to_terminal(Message=f"Log level set to: {self.level}")
        else:
            self.level = 0
            self.log_error_to_terminal(Message=f"Log level out of bounds: {self.level}")

        if LogPath is not None:
            if path.isfile(LogPath):
                self.log_path = LogPath
                self.log_ok_to_terminal(Message=f"Log file set to: {self.LogPath}")
            else:
                self.log_warning_to_terminal(Message=f"Log path was not specified/found. Log file will not be set for {self.name}")


            self.log_ok_to_terminal(Message=f"Sucessfuly started logging instance for: {self.name}")

    def get_current_time(self):
        return datetime.now().time()

    def log_to_terminal(self, Message:str, Header:str=None, Color:str=None, Style:str=None):
        current_time = self.get_current_time()
        if Header is None:
            Header = "LOG"
        if Color is None and Style is None:
            #E.G: [LOG] 146: 07:43:37:4562 - User John authenticated via SSH.
            print(f"[{Header}] [{self.name} - {self.log_count}]: {current_time} - {Message}")
        else:
        #pass formatting appropiately:
            if Color is not None and Style is not None:
                #color and style
                print(f"[{Color}{Style}{Header}{Colors.ENDC}] [{self.name} - {self.log_count}] [{current_time}] - {Message}")
            elif Color is not None and Style is None:
                #only color
                print(f"[{Color}{Header}{Colors.ENDC}] [{self.name} - {self.log_count}] [{current_time}] - {Message}")
            else:
                #only style
                print(f"[{Style}{Header}{Colors.ENDC}] [{self.name} - {self.log_count}] [{current_time}] - {Message}")

        self.log_count += 1

    def log_to_file(self, Header:str, Message:str, FilePath:str):
        """ TODO """
        pass

    def log_ok_to_file(self, Message:str):
        """ TODO """
        #header = "OK"
        #self.log_to_file(Header=header, Message=Message, File=self.LogPath)

    def log_warning_to_terminal(self, Message:str):
        header = "WARNING"
        color = Colors.WARNING
        style = Styles.BOLD
        self.log_to_terminal(Message=Message, Header=header, Color=color, Style=style)

    def log_error_to_terminal(self, Message:str):
        header = "ERROR"
        color = Colors.ERROR
        style = Styles.BOLD
        self.log_to_terminal(Message=Message, Header=header, Color=color, Style=style)

    def log_ok_to_terminal(self, Message:str):
        header = "OK"
        color = Colors.OKBLUE
        style = Styles.BOLD
        self.log_to_terminal(Message=Message, Header=header, Color=color, Style=style)

    def log_info_to_terminal(self, Message:str):
        header = "INFO"
        color = Colors.OKCYAN
        style = Styles.BOLD
        self.log_to_terminal(Message=Message, Header=header, Color=color, Style=style)

    def log_ok(self, Message:str):
        """ Logs [OK] messages to either the terminal or file depending on self.level """
        if not self.enabled:
            return
        if self.save_ok:
            self.log_ok_to_file(Message)
        else:
            self.log_ok_to_terminal(Message)


    def log_error(self, Message:str):
        """ Logs [ERROR] messages to either the terminal or file depending on self.level """
        if not self.enabled:
            return
        if self.save_error:
            self.log_error_to_file(Message)
        else:
            self.log_error_to_terminal(Message)

    def log_info(self, Message:str):
        """ Logs [INFO] messages to either the terminal or file depending on self.level """
        if not self.enabled:
            return
        if self.save_info:
            self.log_info_to_file(Message)
        else:
            self.log_info_to_terminal(Message)


    def log_warning(self, Message:str):
        """ Logs [WARNING] messages to either the terminal or file depending on self.level """
        if not self.enabled:
            return
        if self.save_warning:
            self.log_warning_to_file(Message)
        else:
            self.log_warning_to_terminal(Message)
