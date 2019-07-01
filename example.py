import pythonahk

# An example callback.
def foo(x):
    print(f"I have {x} peppermints.")

if __name__ == "__main__":
    # Create the AHK binding object. Alt+Escape will terminate the script.
    ahk = pythonahk.AhkBinding(termination_trigger="!Esc")

    # Add a template.
    ahk.add_template("example_template.ahk", params={
        "first_field": "Favorite Color",
        "default_value": "Blue",
        "second_field": "Region",
        "values": 'Bandle City|Bilgewater|Demacia|Freljord|Ionia|Ixtal|Noxus|'
                  'Piltover|Shadow Isles|Shurima|Targon|Zaun'
    })

    # Add a hotkey that executes an AHK code snippet.
    ahk.add_hotkey(
        "^i",
        ahk_snippet="get_information()"
    )

    # Add a hotkey the execute both an AHK code snippet and a python callback.
    ahk.add_hotkey(
        "!j",
        ahk_snippet="MsgBox, Hello!",
        callback=foo,
        args=[100]
    )

    # Generate and execute the script.
    ahk.execute()