from logger import Log

def basic_example():
    app_log = Log(Name="My App")

    app_log.ok("Starting script.")

    someValue = True
    if someValue:
        app_log.ok("Value passed")
    else:
        app_log.error("Value failed")
    app_log.info("Script is done.")


def with_example():
    with Log(Name="Admin Log", Level=3, FilePath="example.log") as admin_log:
        admin_log.info("This will be stored to the example.log file")



basic_example()
with_example()
