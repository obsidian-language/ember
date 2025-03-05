import curses
from installer import install_tool, remove_tool
from utils import fetch_github_releases

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

    tools = ["obsidian", "ember", "cinder"]
    versions = parse_and_display_obc_info()

    selected_index = 0

    draw_main_interface(stdscr, selected_index, [versions["obsidian"][0], versions["ember"][0], versions["cinder"][0]])

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

        draw_main_interface(stdscr, selected_index, [versions["obsidian"][0], versions["ember"][0], versions["cinder"][0]])

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
