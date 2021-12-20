import vscode
import joern

ext = vscode.Extension(
    name="messages", display_name="Messages", version="0.0.1")


def static_code_analyst():
    vscode.window.show_info_message("Connect to DB")
    j = joern.JoernSteps()
    j.setGraphDbURL('http://localhost:7474/db/data')
    j.connectToDatabase()
    res = j.runGremlinQuery('getFunctionsByName("main")')
    for r in res : print(r)
    return


@ext.event
def on_activate():
    return f"The extension {ext.name} has started"


@ext.command()
def show_choices():
    # This works the same with warning and error
    choice = vscode.window.show_info_message(
        "Are you happy using this?", "SAST", "Dependency-Check", "Both")

    if not choice:
        return
    elif choice == "SAST":
        vscode.window.show_info_message("Static code Analyst using Joern")
        static_code_analyst()

    elif choice == "Dependency-check":
        vscode.window.show_info_message("Dependency-Check using Safety")

    elif choice == "Both":
        vscode.window.show_info_message("Safety & Joern")


vscode.build(ext)
