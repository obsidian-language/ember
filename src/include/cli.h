#ifndef CLI_H
#define CLI_H

#include <sys/utsname.h>
#include <ctype.h>
#include <sys/stat.h>

void print_rm_help();
void print_install_help();
void print_cli_help();
void install(int argc, char *argv[]);
void _remove(int argc, char *argv[]);
void system_info(char *system, char *arch);
int download_file(const char *url, const char *output_file);
int extract_tar(const char *tar_file, const char *tool, const char *system, const char *arch, const char *version);
void install_tool(const char *tool, const char *version);
void remove_tool(const char *tool, const char *version);

#endif
