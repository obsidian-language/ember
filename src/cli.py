import sys
from utils import print_help
from installer import install_tool, remove_tool
from ui import draw_ui
import pkg_resources
import curses

def get_version():
    return pkg_resources.get_distribution('ember').version

def main():
    if len(sys.argv) < 2 or sys.argv[1] in ["-h", "--help"]:
        print_help()
        sys.exit(0)
    
    command = sys.argv[1]
    
    if command == "install":
        if len(sys.argv) != 4 or sys.argv[2] in ["-h", "--help"]:
            print_help(command)
            sys.exit(1)
        install_tool(sys.argv[2], sys.argv[3])
    
    elif command == "rm":
        if len(sys.argv) != 4 or sys.argv[2] in ["-h", "--help"]:
            print_help(command)
            sys.exit(1)
        remove_tool(sys.argv[2], sys.argv[3])
    
    elif command in ["tui", "version"]:
        if command == "tui":
            curses.wrapper(draw_ui)
        elif command == "version":
            version = get_version()
            print(f"ember version {version}")
        else:
            print_help(command)
    
    else:
        print("Unknown command. Use -h or --help for help.")

if __name__ == "__main__":
    main()