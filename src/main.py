import os
import requests
import sys
import curses

def print_help(command="cli"):
    help_texts = {
        "rm": """Usage: ember rm (COMMAND | VERSION)
Available options:
  -h, --help         Show this help text

Available commands:
  obc                Remove Obsidian
  cinder             Remove Cinder
  ember              Remove Ember""",
        "install": """Usage: ember install [COMMAND | OBC_VERSION] [--set]
Available options:
  --set         Set as active version after install
  -h, --help    Show this help text

Available commands:
  obc              Install Obsidian
  cinder           Install Cinder
  ember            Install Ember""",
        "cli": """Usage: ember [(-v|--verbose) | --no-verbose] [(-c|--cache) | --no-cache] COMMAND
Available options:
  -v, --verbose     Enable verbosity (default: disabled)
  -c, --cache       Cache downloads in ~/.ember/cache (default: disabled)
  -h, --help        Show this help text

Main commands:
  tui               Start the interactive Ember UI
  install           Install or update OBC/Cinder/Ember
  rm                Remove an OBC/Cinder/Ember version
  upgrade           Upgrade Ember
  compile           Compile a tool from source
  version           Shows version

Nuclear Commands:
  nuke

Report bugs at <https://github.com/obsidian-language/ember/issues>"""
    }
    print(help_texts.get(command, "Invalid command"))

def system_info():
    return os.uname().sysname, os.uname().machine

def download_file(url, output):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(output, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"Downloaded {output}")
    except requests.RequestException as e:
        print(f"Error downloading {url}: {e}")
        sys.exit(1)

def extract_tarball(tarball, output):
    os.makedirs(output, exist_ok=True)
    os.system(f"tar -xvf {tarball} -C {output}")

def install_tool(tool, version):
    sysname, machine = system_info()
    url = f"https://github.com/obsidian-language/{tool}/releases/download/{version}/{tool}-{sysname}-{machine}.tar.gz"
    tarball = f"{tool}.tar.gz"
    download_file(url, tarball)
    extraction_dir = os.path.join(os.getenv("HOME"), ".ember", tool)
    extract_tarball(tarball, extraction_dir)
    os.remove(tarball)
    
    original_exec = os.path.join(extraction_dir, f"{tool}-{sysname.lower()}-{machine}")
    new_exec = os.path.join(extraction_dir, f"{tool}-{sysname.lower()}-{machine}-{version}")
    if os.path.exists(original_exec):
        os.rename(original_exec, new_exec)
        print(f"Installed {tool} version {version}")
    else:
        print(f"Installation error: {tool} executable not found")

def remove_tool(tool, version):
    sysname, machine = system_info()
    tool_dir = os.path.join(os.getenv("HOME"), ".ember", tool)
    tool_exec = os.path.join(tool_dir, f"{tool}-{sysname.lower()}-{machine}-{version}")
    if os.path.exists(tool_exec):
        os.remove(tool_exec)
        print(f"Removed {tool} version {version}")
    else:
        print(f"Error: {tool} version {version} not found")

def fetch_github_releases(url):
    response = requests.get(url, headers={"Accept": "application/vnd.github.v3+json"})
    if response.status_code == 200:
        return response.json()
    return []

def parse_and_display_obc_info():
    tools = ["obsidian", "cinder", "ember"]
    versions = {}
    for tool in tools:
        url = f"https://api.github.com/repos/obsidian-language/{tool}/releases"
        releases = fetch_github_releases(url)
        if releases:
            latest = releases[0]
            versions[tool] = (latest.get("tag_name", "N/A"), ", ".join(asset.get("name", "") for asset in latest.get("assets", [])))
        else:
            versions[tool] = ("N/A", "N/A")
    return versions

def print_help_menu(stdscr, height, width):
    help_text = [
        "Press ↑ and ↓ to navigate the list of tools",
        "Press i to install the selected tool.",
        "Press u to uninstall a tool"
    ]
    
    help_height = len(help_text)
    help_width = max(len(line) for line in help_text) + 4
    start_y = (height - help_height) // 2
    start_x = (width - help_width) // 2
    
    stdscr.clear()
    stdscr.border()
    
    for i, line in enumerate(help_text):
        stdscr.addstr(start_y + i, start_x + 2, line)
    
    stdscr.refresh()
    stdscr.getch()

def draw_main_interface(stdscr, selected_index, versions):
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    stdscr.border()

    stdscr.addstr(1, 4, "Tool")
    stdscr.addstr(1, 15, "Version")

    tools = ["OBC", "Ember", "Cinder"]

    for i, tool in enumerate(tools):
        if i == selected_index:
            stdscr.attron(curses.A_REVERSE)
        stdscr.addstr(3 + i, 4, tool)
        stdscr.addstr(3 + i, 15, versions[i])
        stdscr.attroff(curses.A_REVERSE)

    stdscr.addstr(height - 2, 1, "q:Quit  i:Install  u:Uninstall  ↑:Up  ↓:Down  h:Help")

    stdscr.refresh()

def draw_ui(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)

    versions = parse_and_display_obc_info()

    obc_version, obc_tags = versions.get("obsidian", ("N/A", "N/A"))
    ember_version, ember_tags = versions.get("ember", ("N/A", "N/A"))
    cinder_version, cinder_tags = versions.get("cinder", ("N/A", "N/A"))

    selected_index = 0
    tools = ["obsidian", "ember", "cinder"]

    draw_main_interface(stdscr, selected_index, [obc_version, ember_version, cinder_version])

    while True:
        ch = stdscr.getch()

        if ch == ord('q'):
            break
        elif ch == ord('h'):
            print_help_menu(stdscr, *stdscr.getmaxyx())
        elif ch == curses.KEY_UP:
            selected_index = (selected_index - 1) % 3
        elif ch == curses.KEY_DOWN:
            selected_index = (selected_index + 1) % 3
        elif ch == ord('i'):
            tool = tools[selected_index]
            version = versions[tool][0]
            if version != "N/A":
                install_tool(tool, version)
        elif ch == ord('u'):
            tool = tools[selected_index]
            version = versions[tool][0]
            if version != "N/A":
                remove_tool(tool, version)

        draw_main_interface(stdscr, selected_index, [obc_version, ember_version, cinder_version])

def main():
    if len(sys.argv) < 2:
        print_help()
        sys.exit(1)
    
    command = sys.argv[1]
    if command == "install" and len(sys.argv) >= 4:
        install_tool(sys.argv[2], sys.argv[3])
    elif command == "rm" and len(sys.argv) >= 4:
        remove_tool(sys.argv[2], sys.argv[3])
    elif command in ["rm", "install", "cli"]:
        print_help(command)
    elif command == "tui":
        curses.wrapper(draw_ui)
    else:
        print("Unknown command. Use -h for help.")

if __name__ == "__main__":
    main()