## How to use Java in minescript?
-# for minescript v4.0, please look at `+t libjava_guide`

The way you access Java, in both Python and Pyjinn, is very similar

For Python you have to use the built-in Java library
```py
import java

from java import *
```
If you don't have syntax highlighting set up, you can use this import instead (assuming the file is placed in the `.../minescript/` folder)
```py
from system.lib import java

from system.lib.java import *
```
Note: this is only a visual change, it does not affect your code

For Pyjinn, you don't have to import anything, it's automatically imported.

## How can I use Java in my script?

For Python, it depends on how you imported the Java library
```py
class = java.JavaClass("class.full.path") # for "import java"

class = JavaClass("class.full.path") # for "from java import *"
```
For Pyjinn, it's always
```py
class = JavaClass("class.full.path")
```

After this, you can call any* Java member, just like you would with a Python class
```py
# Example
from system.lib.java import JavaClass

Minecraft = JavaClass("net.minecraft.client.Minecraft")

mc = Minecraft.getInstance()
```
Notes:
- In Python, Java access is very slow (~0.1 sec / Java access), for ways to speed up this, type `+t fastjava`
- For a list of all classes, and their methods (functions), visit [mappings.dev](https://mappings.dev/index.html)
- Minescript uses the official `Mojang` mappings
- Make sure you have mappings installed! (`\install_mappings`)

*This includes:
- The Java standard library (JSL)
- Any and all classes, methods (only the ones that are runnable at runtime) and fields of minecraft, and every currently loaded mod

Naming conventions:
-# There isn't really a set of rules, you can name anything whatever you want, however, following these naming conventions will make your code more readable for everyone (including you)
`class = JavaClass("class.full.path")` 
- "`class`" should be named what minecraft calls it internally (so, for example, "`net.minecraft.client.Minecraft`"-s variable name would become "`Minecraft`")
`class.method()`
- It's a free for all, but specifically for `Minecraft.getInstance()` its variable is called `mc` in 99% of cases
`class.field`
- It should be called what its value is (example: `Player = mc.player` or `Screen = mc.screen`)
