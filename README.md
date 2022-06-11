# logger

[![logger.py Build Tests](https://github.com/henryriveraCS/private-github-actions/actions/workflows/run-tests.yaml/badge.svg?branch=master&event=push)](https://github.com/henryriveraCS/private-github-actions/actions/workflows/run-tests.yaml)

An easy-to-deploy file/terminal logger class for python3 using Python's native <code>logger</code> library. Useful for when setting up a whole <code>logger.Logging()</code> instance is too much work for scripts/applications.

<h2>Features</h2>
<ul>
  <li>Has a basic built-in logging style: [DATETIME] [LEVEL] [LOG NAME] [LOG COUNT] - [MESSAGE]</li>
  <li>supports python's built-in <code>with()</code> statement</li>
  <li>Can figure out whether to log a specific message to a file or log based off the Level configured such as:
      <ul>
        <li>Level 0/None - Log everything to the terminal.</li>
        <li>Level 1 - Log errors to a file. Log warnings and info to terminal.</li>
        <li>Level 2 - Log errors/warnings to a file. Log INFO/OK to the terminal</li>
        <li>Level 3 - Log everything into a file</li>
      </ul>
  </li>
</ul>
<h2>Installation</h2>
<ol>
  <li><p><code>git clone https://github.com/henryriveraCS/logger</code></p></li>
  <li>
    <p>
      Move <code>logger.py</code> into your project directory
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
