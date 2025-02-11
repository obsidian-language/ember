#include "include/common.h"
#include "include/fetch.h"
#include "include/ui.h"

void print_help_menu(unsigned short height, unsigned short width) {
    const char *title = " Key Actions ";
    const char *help_text[] = {
        "Press ^ and v to navigate the list of tools",
        "Press i to install the selected tool.",
        "Press u to uninstall a tool"
    };

    unsigned short help_height = sizeof(help_text) / sizeof(help_text[0]);
    unsigned short help_width = 0;

    for (int i = 0; i < help_height; i++) {
        if (strlen(help_text[i]) > help_width) {
            help_width = strlen(help_text[i]);
        }
    }

    help_width += 4;
    unsigned short start_y = (height - help_height) / 2;
    unsigned short start_x = (width - help_width) / 2;

    for (int y = start_y - 1; y <= start_y + help_height; y++) {
        mvaddch(y, start_x - 1, ACS_VLINE);
        mvaddch(y, start_x + help_width, ACS_VLINE);
    }

    unsigned short title_pos = start_x + (help_width - strlen(title)) / 2;
    for (int x = start_x - 1; x <= start_x + help_width; x++) {
        if (x >= title_pos && x < title_pos + (unsigned short)strlen(title)) {
            mvaddch(start_y - 1, x, title[x - title_pos]);
        } else {
            mvaddch(start_y - 1, x, ACS_HLINE);
        }
    }

    for (int x = start_x - 1; x <= start_x + help_width; x++) {
        mvaddch(start_y + help_height, x, ACS_HLINE);
    }

    mvaddch(start_y - 1, start_x - 1, ACS_ULCORNER);
    mvaddch(start_y - 1, start_x + help_width, ACS_URCORNER);
    mvaddch(start_y + help_height, start_x - 1, ACS_LLCORNER);
    mvaddch(start_y + help_height, start_x + help_width, ACS_LRCORNER);

    for (int i = 0; i < help_height; i++) {
        mvprintw(start_y + i, start_x + 2, "%s", help_text[i]);
    }

    refresh();
}

void draw_border(int height, int width, const char *title) {
    int title_pos = (width - (int)strlen(title)) / 2;

    for (int i = 0; i < width; i++) {
        if (i >= title_pos && i < title_pos + (int)strlen(title)) {
            mvaddch(0, i, title[i - title_pos]);
        } else {
            mvaddch(0, i, ACS_HLINE);
        }
    }

    for (int i = 0; i < width; i++) {
        mvaddch(height - 1, i, ACS_HLINE);
    }

    for (int i = 1; i < height - 1; i++) {
        mvaddch(i, 0, ACS_VLINE);
        mvaddch(i, width - 1, ACS_VLINE);
    }

    mvaddch(0, 0, ACS_ULCORNER);
    mvaddch(0, width - 1, ACS_URCORNER);
    mvaddch(height - 1, 0, ACS_LLCORNER);
    mvaddch(height - 1, width - 1, ACS_LRCORNER);
}

void draw_main_interface(unsigned short height, int selected_index, const char *version, const char *tags) {
    draw_border(22, 79, "Ember");

    mvprintw(1, 4, "Tool");
    mvprintw(1, 10, "Version");
    mvprintw(1, 30, "Tags");
    mvprintw(1, 60, "Notes");

    for (int i = 1; i < 78; i++) {
        mvaddch(2, i, ACS_HLINE);
        mvaddch(3, i, ACS_HLINE);
    }
    
    char *tools[] = { "OBC", "Ember", "Cinder" };
    int num_tools = sizeof(tools) / sizeof(tools[0]);

    for (int i = 0; i < num_tools; i++) {
        if (i == selected_index) {
            attron(A_REVERSE);
        }
        mvprintw(4 + i, 4, "%s", tools[i]);
        mvprintw(4 + i, 10, "%s", i == 0 ? version : "N/A");
        mvprintw(4 + i, 30, "%s", i == 0 ? tags : "N/A");
        attroff(A_REVERSE);
    }

    mvprintw(height - 2, 0, "q:Quit");
    mvprintw(height - 2, 7, "i:Install");
    mvprintw(height - 2, 17, "u:Uninstall");
    mvaddch(height - 2, 29, ACS_UARROW);
    mvprintw(height - 2, 30, ":Up");
    mvaddch(height - 2, 34, ACS_DARROW);
    mvprintw(height - 2, 35, ":Down");
    mvprintw(height - 2, 41, "h:help");

    refresh();
}

int draw_ui() {
    int ch;
    unsigned short height, width;
    int help_menu_open = 0;
    int selected_index = 0;

    char response_buffer[BUFFER_SIZE] = "";
    char version[256] = "";
    char tags[256] = "";

    fetch_github_releases("https://api.github.com/repos/obsidian-language/obsidian/releases", response_buffer);
    parse_and_display_obc_info(response_buffer, version, tags);

    initscr();
    cbreak();
    noecho();
    curs_set(0);
    keypad(stdscr, TRUE);

    getmaxyx(stdscr, height, width);

    draw_main_interface(height, selected_index, version, tags);

    while (1) {
        ch = getch();

        switch (ch) {
            case 'q':
                if (help_menu_open) {
                    help_menu_open = 0;
                    clear();
                    draw_main_interface(height, selected_index, version, tags);
                } else {
                    endwin();
                    return 0;
                }
                break;
            case 'h':
                if (!help_menu_open) {
                    print_help_menu(height, width);
                    help_menu_open = 1;
                }
                break;
            case KEY_UP:
                selected_index = (selected_index - 1 + 3) % 3;
                draw_main_interface(height, selected_index, version, tags);
                break;
            case KEY_DOWN:
                selected_index = (selected_index + 1) % 3;
                draw_main_interface(height, selected_index, version, tags);
                break;
        }
    }

    endwin();
}
