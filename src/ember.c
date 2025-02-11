#include "include/common.h"
#include "include/cli.h"
#include "include/fetch.h"
#include "include/ui.h"

#define VERSION "0.0.1"

int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s <command>\n", argv[0]);
        return 1;
    }

    if (strcmp(argv[1], "-h") == 0 || strcmp(argv[1], "--help") == 0) {
        print_cli_help();
        return 0;
    } else if (strcmp(argv[1], "-v") == 0 || strcmp(argv[1], "--verbose") == 0) {
        return 1;
    } else if (strcmp(argv[1], "-c") == 0 || strcmp(argv[1], "--cache") == 0) {
        return 1;
    } else if (strcmp(argv[1], "tui") == 0) {
        draw_ui();
    } else if (strcmp(argv[1], "install") == 0) {
        if (argc == 2 || (argc > 2 && (strcmp(argv[2], "-h") == 0 || strcmp(argv[2], "--help") == 0))) {
            print_install_help();
        } else {
            install(argc, argv);
        }
    } else if (strcmp(argv[1], "rm") == 0) {
        if (argc == 2 || (argc > 2 && (strcmp(argv[2], "-h") == 0 || strcmp(argv[2], "--help") == 0))) {
            print_rm_help();
        } else {
            _remove(argc, argv);
        }
    } else if (strcmp(argv[1], "upgrade") == 0) {
        // Add upgrading...
    } else if (strcmp(argv[1], "compile") == 0) {
        // Add compiling...
    } else if (strcmp(argv[1], "nuke") == 0) {
        system("rm -rf ~/.ember");
    } else if (strcmp(argv[1], "version") == 0) {
        printf("The Ember Obsidian Installer, version %s\n", VERSION);
    } else {
        fprintf(stderr, "Invaild argment: `%s'\n", argv[1]);
        print_cli_help();
        return 1;
    }

    return 0;
}
