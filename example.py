from logger import Log

my_log = Log(Name="My App")
my_log.ok("Hello world!")

x = 20
if x > 21:
    my_log.ok("X is greater than 21")
else:
    my_log.error("The math is wrong")
my_log.warning("Done.")
