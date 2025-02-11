#include "include/common.h"
#include "include/cli.h"
#include "include/fetch.h"
#include <stdio.h>

void print_rm_help() {
    puts("Usage: ember rm (COMMAND | VERSION)\n\n"
         "Available options:\n"
         "  -h, --help         Shows this help text\n\n"
         "Available commands:\n"
         "  obc               Install OBC\n"
         "  cinder            Install Cinder\n"
         "  ember             Install Ember");
}

void print_install_help() {
    puts("Usage: ember install [COMMAND | OBC_VERSION] [--set ]\n\n"
         "Available options:\n"
         "  --set             Set as active version after install\n"
         "  -h, --help        Shows this help text\n\n"
         "Available commands:\n"
         "  obc               Install OBC\n"
         "  cinder            Install Cinder\n"
         "  ember             Install Ember");
}

void print_cli_help() {
    puts("Usage: ember [(-v|--verbose) | --no-verbose] [(-c|--cache) | --no-cache] COMMAND\n\n"
         "Available options:\n"
         "  -v, --verbose     Enable verbosity (default: disabled)\n"
         "  -c, --cache       Cache downloads in ~/.ember/cache (default: disabled)\n"
         "  -h, --help        Show this help text\n\n"
         "Main commands:\n"
         "  tui               Start the interactive Ember UI\n"
         "  install           Install or update OBC/Cinder/Ember\n"
         "  rm                Remove an OBC/Cinder/Ember version\n"
         "  upgrade           Upgrade Ember\n"
         "  compile           Compile a tool from source\n"
         "  version           Shows version\n\n"
         "Nuclear Commands:\n"
         "  nuke              Completely remove Ember from your system\n\n"
         "Report bugs at <https://github.com/obsidian-language/ember/issues>");
}

void system_info(char *os_name, char *arch) {
    struct utsname sysinfo;
    uname(&sysinfo);
    
    strcpy(os_name, sysinfo.sysname);
    strcpy(arch, sysinfo.machine);
    
    for (int i = 0; os_name[i]; i++) {
        os_name[i] = tolower((unsigned char)os_name[i]);
    }
}

int download_file(const char *url, const char *output_file) {
    CURL *curl = curl_easy_init();
    if (!curl) {
        fprintf(stderr, "Failed to initialize cURL\n");
        return -1;
    }

    FILE *fp = fopen(output_file, "wb");
    if (!fp) {
        fprintf(stderr, "Failed to open file for writing: %s\n", output_file);
        curl_easy_cleanup(curl);
        return -1;
    }

    curl_easy_setopt(curl, CURLOPT_URL, url);
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_data);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, fp);
    curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, 1L);

    CURLcode res = curl_easy_perform(curl);
    fclose(fp);
    curl_easy_cleanup(curl);

    if (res != CURLE_OK) {
        fprintf(stderr, "Download failed: %s\n", curl_easy_strerror(res));
        return -1;
    }
    return 0;
}

int extract_tar(const char *tar_file, const char *tool, const char *os_name, const char *arch, const char *version) {
    char command[512];
    snprintf(command, sizeof(command), "tar -xzf %s && mv %s-%s-%s %s-%s-%s-%s", tar_file, tool, os_name, arch, tool, os_name, arch, version);
    return system(command);
}

void install_tool(const char *tool, const char *version) {
    char os_name[64], arch[64], url[256], tar_file[128], install_dir[128], extract_dir[128];
    system_info(os_name, arch);

    snprintf(url, sizeof(url), "https://github.com/obsidian-language/%s/releases/download/%s/%s-%s-%s.tar.gz",
             tool, version, tool, os_name, arch);
    snprintf(tar_file, sizeof(tar_file), "%s.tar.gz", tool);
    snprintf(install_dir, sizeof(install_dir), "%s/.ember/%s", getenv("HOME"), tool);
    snprintf(extract_dir, sizeof(extract_dir), "%s/%s-%s-%s-%s", install_dir, tool, os_name, arch, version);

    char mkdir_cmd[256];
    snprintf(mkdir_cmd, sizeof(mkdir_cmd), "mkdir -p %s", install_dir);
    system(mkdir_cmd);

    if (download_file(url, tar_file) != 0) {
        fprintf(stderr, "Failed to download %s\n", tool);
        return;
    }

    char command[512];
    snprintf(command, sizeof(command), "tar -xzf %s -C %s", tar_file, install_dir);

    if (system(command) != 0) {
        fprintf(stderr, "Failed to extract %s\n", tar_file);
        remove(tar_file);
        return;
    }

    snprintf(command, sizeof(command), "mv %s/%s-%s-%s %s", install_dir, tool, os_name, arch, extract_dir);
    if (system(command) != 0) {
        fprintf(stderr, "Failed to move extracted files\n");
        remove(tar_file);
        return;
    }

    if (remove(tar_file) != 0) {
        fprintf(stderr, "Warning: Failed to remove %s\n", tar_file);
    }

    snprintf(command, sizeof(command), "sudo ln -s ~/.ember/%s/%s-%s-%s-%s /usr/local/bin/%s", tool, tool, os_name, arch, version, tool);
    system(command);

    printf("%s installed successfully in %s\n", tool, extract_dir);
}

void remove_tool(const char *tool, const char *version) {
    char os_name[64], arch[64], install_dir[128], extract_dir[128];
    system_info(os_name, arch);

    snprintf(install_dir, sizeof(install_dir), "%s/.ember/%s", getenv("HOME"), tool);
    snprintf(extract_dir, sizeof(extract_dir), "%s/%s-%s-%s-%s", install_dir, tool, os_name, arch, version);

    char command[512];
    snprintf(command, sizeof(command), "sudo unlink /usr/local/bin/%s && sudo rm -rf /usr/local/bin/%s", tool, tool);
    system(command);

    snprintf(command, sizeof(command), "rm -rf ~/.ember/%s/%s-%s-%s-%s ", tool, tool, os_name, arch, version);
    system(command);

    printf("%s uninstalled successfully", tool);

}

void install(int argc, char *argv[]) {
    if (argc < 4) {
        return;
    }

    install_tool(argv[2], argv[3]);
}

void _remove(int argc, char *argv[]) {
    if (argc < 4) {
        return;
    } 

    remove_tool(argv[2], argv[3]);
}
