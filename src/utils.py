import os
import requests

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

def fetch_github_releases(url):
    response = requests.get(url, headers={"Accept": "application/vnd.github.v3+json"})
    if response.status_code == 200:
        return response.json()
    return []
