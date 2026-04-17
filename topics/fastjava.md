## How to speed up access to Java in Python?

There are a few options, depending on the use case:

**In the case you do** ***NOT*** **want to extract data, but rather just execute a function (like sending a packet)**

Quick way:
```py
from system.lib.minescript import execute

def exec_pyj(code:str)
    if not code.startswith("\n"): code = "\n" + code
    if not code.endswith("\n"): code += "\n"
    execute(f"\eval {code.replace("\n","' '")[2:-2]}")
```
Calling this function will execute a piece of Pyjinn code.
Pros:
- Decent speed (0.01 - 0.05 sec)
- Easy integration

Cons:
- 5.0+ only
- You cannot use `'` in your code (only `"`)
- No return value

File writing way:
```py
from system.lib.minescript import execute
from pathlib import Path

execpath = Path(__file__).resolve().parent / "execpyj.pyj"

def exec_pyj(code):
    with open(execpath,"w") as f:
        f.write(code)
        f.flush()
    execute("\execpyj")
```
Calling this function will create a file and run it
Pros:
- Any character is allowed
- Decent speed (same as the former)

Cons:
- Harder to integrate (may need to adjust path, and / or the execute command)
- 5.0+ only
- No return value