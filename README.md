# logger
Preconfigured lightweight logger for python3 using Python's native <code>logger</code> library with standard terminal output and file output(coming soon TM). Useful for when setting up a whole <code>logger.Logging()</code> instance is too much work.

<h2>Installation and Usage:</h2>
<ul>
  <li><p><code>git clone https://github.com/henryriveraCS/logger</code></p></li>
  <li>
    <p>
      Move <code>logger.py</code> into your project directory
    </p>
  </li>
  <li>
    <p>
      Intallation is done :^)
    </p>
  </li>
</ul>

```python

from logger import Log

my_log = Log(Name="My App")
my_log.ok("Hello world!")

x = 20
if x > 21:
    my_log.ok("X is greater than 21")
else:
    my_log.error("The math is wrong")
my_log.warning("Done.")
```

Running <code>example.py</code>(shown above) displays the following:
Terminal output:

![Image of example.py logger results for the terminal](https://github.com/henryriveraCS/logger/blob/main/terminal_output.png)
File output:

![Image of example.py logger results for the file](https://github.com/henryriveraCS/logger/blob/main/file_output.png)
