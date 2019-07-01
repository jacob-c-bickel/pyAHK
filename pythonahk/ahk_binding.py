import collections
import os
import re
import subprocess
import tempfile
import time
import uuid


Hotkey = collections.namedtuple(
    'Hotkey',
    'ahk_snippet callback args',
    defaults=("", None, [])
)

SCRIPT_HEADER = """stdout(message, ending:="`n", flush:=True) {
    static stdout := FileOpen("*", "w `n")
    stdout.write(message . ending)
    if (flush) {
        stdout.Read(0)
    }
}

"""


class AhkBinding:
    def __init__(self, termination_trigger=None):
        self.ahk_path = self._get_ahk_path()
        self.script_filename = None

        self.templates = []
        self.hotkeys = {}

        if termination_trigger is not None:
            self.add_hotkey(termination_trigger, ahk_snippet="ExitApp")


    def _get_ahk_path(self):
        """
        Gets the path for AHK from Windows registry.
        Returns False if no installation is detected.
        """
        import winreg, shlex
        try:
            file_class = winreg.QueryValue(winreg.HKEY_CLASSES_ROOT, ".ahk")
            key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT,
                    f'{file_class}\\shell\\open\\command')
            command = winreg.QueryValueEx(key, '')[0]
            return shlex.split(command)[0]
        except FileNotFoundError:
            return False


    def _generate_ahk_script(self):
        """
        Generates the temporary script file and returns its name.
        """
        # Add IPC message passing function.
        script = SCRIPT_HEADER

        # Add templates.
        for template in self.templates:
            script += f"{template}\n"

        # Add hotkeys.
        for trigger, hotkey in self.hotkeys.items():
            script += f"{trigger}::\n"
            script += f"{hotkey.ahk_snippet}\n"
            script += f"stdout(\"{trigger}\")\n"
            script += "return\n\n"

        # Write the script to file.
        f = tempfile.NamedTemporaryFile(suffix=".ahk", delete=False)
        f.write(str.encode(script))
        script_name = f.name
        f.close()
        return f.name


    def add_hotkey(self, trigger, ahk_snippet="", callback=None, args=[]):
        """
        Registers a hotkey to execute an AHK code snippet or a python callback.
        """
        # Triggers must be unique.
        if trigger in self.hotkeys:
            return False
        
        self.hotkeys[trigger] = Hotkey(ahk_snippet=ahk_snippet,
                callback=callback, args=args)


    def add_template(self, template_filename, params={}):
        # Load the script template.
        script = ''.join(open(template_filename, "r").readlines())

        # Interpolate params.
        # TODO: use regex to allow for spaces.
        for param in params:
            script = script.replace("{{" + param + "}}", str(params[param]))

        self.templates.append(script)


    def execute(self, blocking=True):
        """
        Generate and execute the AHK script in a subprocess.
        If 'blocking' is True, listen for stdout and execute callbacks.
        Note: If 'blocking' is False, the script may only be used for AHK code
        snippets.
        """
        # Create the script.
        script_name = self._generate_ahk_script()

        # Run the script in a subprocess.
        with subprocess.Popen([self.ahk_path, script_name], bufsize=1,
                stdout=subprocess.PIPE, universal_newlines=True) as p:
            # If set the
            if blocking:
                for line in p.stdout:
                    line = line.rstrip("\n")
                    if line in self.hotkeys:
                        hotkey = self.hotkeys[line]
                        if callable(hotkey.callback):
                            hotkey.callback(*hotkey.args)

        # Delete the script.
        os.remove(script_name)