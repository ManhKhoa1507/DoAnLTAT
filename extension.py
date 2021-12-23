import vscode
import joern
import os
import subprocess
from vscode.config import Config

# Build config
c = Config(name="setting", description="Plugin Settings",
           input_type=str, default="./")

# Build extension
ext = vscode.Extension(
    name="messages", display_name="Messages", version="0.0.1", config=[c])

# Build theme
theme = vscode.ColorTheme(
    name="scan_theme", display_name="Scan theme", version="0.0.1")
# theme.set_colors(
# background='#282C34',
# foreground='#1D2026',
# accent_colors=['#45C2A8', '#6EC262', '#F2B85D', '#EB5BF2']
# )


def get_warning(result):
    # Delete all the warning except the result
    warning_list = []
    split_string = result.split("\n")

    for element in split_string:
        if (element.find("Result: ") >= 0):
            warning_list.append(element)

    return warning_list


def display_warning(warning_list):
    # Display the warning message form warning list
    warning_string = ""
    for element in warning_list:
        warning_string += element + "\n"
    vscode.window.show_warn_message(warning_string)
    return


def static_code_analyst(location):

    # Static code analyst using joern
    if(os.path.exists(location) == True):
        joern_result = os.popen(
            "joern-scan " + location + " --overwrite").read()
        warning_list = get_warning(joern_result)
        display_warning(warning_list)

    else:
        vscode.window.show_error_message("File not found")
    return

# Noti the extension


@ext.event
def on_activate():
    return f"The extension {ext.name} has started"

# Config settings
# Keybind ALT+S


@ext.command(keybind="ALT+S")
def message_say_config():
    vscode.window.show_info_message(ext.get_config('settings') or c.default)

# Choose mode to run
# Keybind ALT+5


@ext.command(keybind="ALT+5")
def show_choices():
    # This works the same with warning and error
    choice = vscode.window.show_info_message(
        "Which scan?", "SAST", "Dependency-Check", "Both")

    # if not choice anything
    if not choice:
        return

    # if run SAST
    elif choice == "SAST":

        # Get file to scan
        location = vscode.window.show_input_box()

        # vscode.window.show_info_message("Source code location: ", location)
        static_code_analyst(location)

    # if run Dependency-check
    elif choice == "Dependency-check":
        vscode.window.show_info_message("Dependency-Check using Safety")

    # if run both
    elif choice == "Both":
        vscode.window.show_info_message("Safety & Joern")


# Build extension and theme
vscode.build_theme(theme)
vscode.build(ext)
