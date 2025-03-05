import sys
from utils import print_help
from installer import install_tool, remove_tool
from ui import draw_ui
import curses

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