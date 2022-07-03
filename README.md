# logger

[![Tests](https://github.com/henryriveraCS/logger/actions/workflows/run-tests.yaml/badge.svg)](https://github.com/henryriveraCS/logger/actions/workflows/run-tests.yaml)

An easy-to-use logger class built using python3's native <code>logger</code> library. It can intelligently handle pushing stdout messages between files/terminals based off configured options. Extremely useful for setting up a whole <code>logger.Logging()</code> instance without worrying about configuring format/file-handling for scripts/applications.

<h2>Features</h2>
<ul>
  <li>Has a built-in logging style: [DATE TIME] [LEVEL] [LOG NAME] [LOG COUNT] - [MESSAGE]</li>
  <li>supports python's built-in <code>with()</code> statement</li>
  <li>Can figure out whether to log a specific message to a file or log based off the Level configured such as:
      <ul>
        <li>Level 0/None - Log everything to the terminal.</li>
        <li>Level 1 - Log critical to file. Log warnings/ok/info to terminal.</li>
        <li>Level 2 - Log critical/error to file. Log warnings/info/ok to terminal.</li>
        <li>Level 3 - Log errors/warnings to file. Log INFO/OK  the terminal</li>
        <li>Level 4 - Log everything into file</li>
      </ul>
  </li>
  <li>Dynamically switch log levels and logging files with <code>set_log_file()</code> and <code>set_log_level()</code> respectively.</li>
  <li>Enable/Disable logging as needed.</li>
  
</ul>
<h2>Installation(Requires python >= 3.6)</h2>
<p><code>pip3 install logger-henryriveracs==0.3.0</code> OR copy <code>src/logger/logger.py</code> into your repository. </p>

<h2>Usage</h2>

```python
#python3
from logger.logger import Log
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
```


Results from running example.py under the <code>example/</code> folder
<h3>Terminal:</h3>

![Image of example.py logger results for the terminal](https://github.com/henryriveraCS/logger/blob/main/images/example.png)

<h3>File:</h3>

![Image of example.py logger results for the terminal](https://github.com/henryriveraCS/logger/blob/main/images/example2.png)
