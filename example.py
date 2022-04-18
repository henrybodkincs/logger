from logger import Log

my_log = Log(Name="My App")
my_log.log_ok("Hello world!")

x = 20
if x > 21:
    my_log.log_ok("X is greater than 21")
else:
    my_log.log_error("The math is wrong")
my_log.log_warning("Done.")
