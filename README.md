# logger

[![Tests](https://github.com/henryriveraCS/logger/actions/workflows/run-tests.yaml/badge.svg)](https://github.com/henryriveraCS/logger/actions/workflows/run-tests.yaml)

An easy-to-use logger class that can intelligently handle pushing stdout messages between files/terminals based off configured options. Extremely useful for setting up a whole <code>logger.Logging()</code> instance without worrying about configuring format/file-handling for scripts/applications.

<h2>Features</h2>
<ul>
  <li>Has a basic built-in logging style: [DATE TIME] [LEVEL] [LOG NAME] [LOG COUNT] - [MESSAGE]</li>
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
</ul>
<h2>Installation</h2>
<ol>
  <li><p><code>git clone https://github.com/henryriveraCS/logger</code></p></li>
  <li>
    <p>
      Move <code>logger/logger.py</code> into your project directory
    </p>
  </li>
  <li>
    <p>
      Because we don't use any third party libraries the installation is done :^)
    </p>
  </li>
</ol>

<h2>Usage</h2>

```python
""" Example from example/example.py """
from logger import Log
#Prints everything to the terminal
app_log = Log(Name="My App")
#This app_log would print all WARNING/ERROR messages to a file log and print out INFO/OK to the termminal
#app_log = Log(Name="Other App", Level=2, FilePath="path/to/example.log") 
app_log.info("Starting script.")

someValue = True
if someValue:
  app_log.ok("Value passed")
else:
    app_log.error("Value failed")
app_log.info("Script is done.")
```


<h3>Output</h3>

![Image of example.py logger results for the terminal](https://github.com/henryriveraCS/logger/blob/main/images/terminal_output.png)
