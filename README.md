# Python AHK Hotkeys and Interpolation
Python bindings for AHK with support to register hotkeys and interpolate scripts.

There are two main features:

1. Register hotkeys either execute callbacks or AHK code snippets.
```
from pythonahk import AhkBinding
ahk = AhkBinding(termination_trigger="!Esc")

# A hotkey that executes a python callback.
ahk.add_hotkey(
    trigger="!p",
    callback=print,
    args=["Nice hotkey, bud."]
)

# A hotkey the executes an AHK code snippet.
ahk.add_hotkey(
    trigger="^j",
    ahk_snippet="MsgBox, Hey thanks, I sure think it's neat."
)

ahk.execute()
```

2. Interpolate existing AHK scripts. In the AHK script, use `{{param}}` as value placeholders.
```
from pythonahk import AhkBinding
ahk = AhkBinding(termination_trigger="!Esc")

ahk.add_template("my_form.ahk", params={
    "field1": "Name",
    "field2": "Favorite Color",
    "field2_default": "Blue",
    "field3": "Hobby",
    "field3_options": "Coding|Running|Snoozing|Writing"
})

ahk.add_hotkey(
    trigger="!f",
    ahk_snippet="display_form()"
)

ahk.execute()
```

<hr>

<h2>class pythonahk.AhkBinding</h2>

* AhkBinding.add_hotkey(trigger, ahk_snippet="", callback=None, args=[])
* AhkBinding.add_template(script_filename, params={})
* AhkBinding.execute()