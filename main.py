from importlib import metadata
import subprocess
import sys

ORANGE = "\033[38;2;255;165;0m"
RED = "\033[38;2;255;0;0m"
END = "\033[0m"


def colored_print(text, color=ORANGE):
    print(color + text + END)


def is_package_installed(package_name):
    try:
        metadata.version(package_name)
        return True
    except metadata.PackageNotFoundError:
        return False


def install_packages():
    required_packages = ["selenium", "flet", "webdriver-manager"]
    for package in required_packages:
        if not is_package_installed(package):
            colored_print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            colored_print(f"{package} successfully installed.")


def post_to_pastebin(content, title):
    from src.pastebin_poster import PastebinPoster

    poster = PastebinPoster()
    return poster.post_to_pastebin(content, title)


def main():
    interface_type = input(
        "@admin ➜ /pastecreater $~ Choose an interface (CLI/GUI): "
    ).strip().lower()

    if interface_type == "cli":
        content = input("@admin ➜ /pastecreater $~ Write the content of the paste  : ")
        title = input("@admin ➜ /pastecreater $~ Write the title of the paste: ")
        url = post_to_pastebin(content, title)
        colored_print(f"The paste is published: {url}")
    elif interface_type == "gui":
        import flet
        from gui import main as gui_main

        flet.app(target=gui_main)
    else:
        colored_print("Incorrect interface selection.", RED)
        sys.exit(1)


if __name__ == "__main__":
    install_packages()
    main()