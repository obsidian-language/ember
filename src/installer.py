import os
import sys
import shutil
import subprocess
from downloader import download_file
from utils import system_info

def extract_tarball(tarball, output):
    os.makedirs(output, exist_ok=True)
    subprocess.run(['tar', '-xvf', tarball, '-C', output], check=True)

def install_tool(tool, version):
    sysname, machine = system_info()
    url = f"https://github.com/obsidian-language/{tool}/releases/download/{version}/{tool}-{sysname}-{machine}.tar.gz"
    tarball = f"{tool}.tar.gz"
    download_file(url, tarball)
    extraction_dir = os.path.join(os.getenv("USERPROFILE"), ".ember", tool) if os.name == 'nt' else os.path.join(os.getenv("HOME"), ".ember", tool)
    extract_tarball(tarball, extraction_dir)
    os.remove(tarball)

    original_exec = os.path.join(extraction_dir, f"{tool}-{sysname.lower()}-{machine}")
    new_exec = os.path.join(extraction_dir, f"{tool}-{sysname.lower()}-{machine}-{version}")
    if os.path.exists(original_exec):
        os.rename(original_exec, new_exec)
        print(f"Installed {tool} version {version}")

        if os.name == 'nt':
            local_bin = os.path.join(os.getenv("USERPROFILE"), "AppData", "Local", "Programs", tool)
        else:
            local_bin = os.path.join(os.getenv("HOME"), ".local", "bin")
        
        os.makedirs(local_bin, exist_ok=True)
        exec_copy_path = os.path.join(local_bin, f"{tool}.exe" if os.name == 'nt' else tool)

        if not os.path.exists(exec_copy_path):
            shutil.copy(new_exec, exec_copy_path)
            print(f"Copied {tool} executable to {local_bin}")
        else:
            print(f"{tool} executable already exists in {local_bin}")

    else:
        print(f"Installation error: {tool} executable not found")

def remove_tool(tool, version):
    sysname, machine = system_info()
    tool_dir = os.path.join(os.getenv("USERPROFILE"), ".ember", tool) if os.name == 'nt' else os.path.join(os.getenv("HOME"), ".ember", tool)
    tool_exec = os.path.join(tool_dir, f"{tool}-{sysname.lower()}-{machine}-{version}.exe" if os.name == 'nt' else f"{tool}-{sysname.lower()}-{machine}-{version}")
    if os.path.exists(tool_exec):
        os.remove(tool_exec)
        print(f"Removed {tool} version {version}")

        local_bin = os.path.join(os.getenv("USERPROFILE"), "AppData", "Local", "Programs", tool) if os.name == 'nt' else os.path.join(os.getenv("HOME"), ".local", "bin")
        exec_copy_path = os.path.join(local_bin, f"{tool}.exe" if os.name == 'nt' else tool)
        if os.path.exists(exec_copy_path):
            os.remove(exec_copy_path)
            print(f"Removed {tool} executable from {local_bin}")
    else:
        print(f"Error: {tool} version {version} not found")
