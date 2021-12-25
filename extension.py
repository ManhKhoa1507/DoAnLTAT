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
    name = "g03",
    display_name = "G03 Static Application Secure Testing",
    version = "0.0.1",
    config = [c]
    )

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

def dependency_check(dir):
    if (os.path.exists(dir) == True):
        subprocess.run([os.getcwd() + "/cheque/cheque", "-cheque-scan", dir, "-export-sbom"])
        vscode.window.show_info_message("A CycloneDX SBOM file has been exported")
        
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
def menu():
    selection = vscode.window.show_quick_pick(
        [
            vscode.window.QuickPickItem(label = "G03 Static Code Analysis", detail = "Perform static code analysis on source code."),
            vscode.window.QuickPickItem(label = "G03 Dependency Check", detail = "Perform dependency check on a project"),
            vscode.window.QuickPickItem(label = "Both", detail = "Perform both Static code analysis and Dependency check")
        ]
    )
    if not selection:
        return

    elif selection.label == "G03 Static Code Analysis":
        # Get file to scan
        location = vscode.window.show_input_box()

        # vscode.window.show_info_message("Source code location: ", location)
        static_code_analyst(location)

    elif selection.label == "G03 Dependency Check":
        # Choose workspace folder to perform dependency check on
        dir = vscode.window.show_workspace_folder_pick()
        dir_path = dir["uri"]["path"]

        # Perform dependency check
        dependency_check(dir_path)
    
    elif selection.label == "Both":
        # SAST
        location = vscode.window.show_input_box()
        static_code_analyst(location)

        # Dependency check
        dir = vscode.window.show_workspace_folder_pick()
        dir_path = dir["uri"]["path"]
        dependency_check(dir_path)

# Build extension and theme
vscode.build_theme(theme)
vscode.build(ext)
