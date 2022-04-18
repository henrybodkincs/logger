# logger
Light and easy to use python logger with sys.stdout and file support(coming).

<p>This logger is based off Python's own <code>logger</code> library and supports some basic input/output formatting and printing for quickly testing whether other things(your code) work as intended or not.</p>

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
my_log.log_info("Hello world!")

x = 20
if x > 21:
  my_log.log_ok("X is greater than 21")
else:
  my_log.log_error("The math is wrong")

my_log.log_warning("Done.")
```

Running <code>example.py</code>(shown above) displays the following:
![Image of example.py logger results](https://github.com/henryriveraCS/logger/blob/main/log_img.png)
