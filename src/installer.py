import os
from downloader import download_file
from utils import system_info

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
