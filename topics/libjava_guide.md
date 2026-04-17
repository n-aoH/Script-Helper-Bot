## How to use lib_java v2?
-# for minescript 4.0 only, for 5.0+ please look at `+t java_guide`

[Download lib_java v2](https://minescript.net/sdm_downloads/lib_java-v2)

On its own, this library only allows you to use `intermediary` mappings which get confusing, really fast. However, Minescript adds in a way, to map your own names to intermediary mappings

The format is: `"customname":"intermediary_equivalent"`

```py
# For Java Classes
java_class_map.update({
    "net.minecraft.client.Minecraft": "net.minecraft.class_310",
})

# For methods / fields / subclasses
java_member_map.update({
    "getInstance": "method_1551",
    "getFps": "method_47599",
})
```

For a list of all `intermediary` names, visit [mappings.dev](https://mappings.dev/index.html)

After this, the way you access java is the exact same way as you would with modern versions (see: `+t java_guide`)
Note:
- Technically, you can name the methods and classes anything you want
-# Pyjinn does not exist in 4.0