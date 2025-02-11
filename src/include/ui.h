#ifndef UI_H
#define UI_H

void print_help_menu(unsigned short height, unsigned short width);
void draw_border(int height, int width, const char *title);
void draw_main_interface(unsigned short height, int selected_index, const char *version, const char *tags);
int draw_ui();

#endif
