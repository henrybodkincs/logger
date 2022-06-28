from logger import Log
items = ["item1", "item2", "item3", "item4", "item5"]

my_logger = Log(Name="My Logger")

my_logger.info(items[0])
my_logger.ok(items[1])
my_logger.warning(items[2])
my_logger.error(items[3])
my_logger.critical(items[4])


# pointing logger to example.log with log level set to 2
my_logger.set_log_file("example.log")
my_logger.set_log_level(2)
my_logger.ok("Test OK")
my_logger.error("Test Error")
