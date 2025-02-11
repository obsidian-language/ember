#ifndef FETCH_H
#define FETCH_H

#include <stddef.h>
#include <stdio.h>

void fetch_github_releases(const char *url, char *response_buffer);
void parse_and_display_obc_info(const char *response_buffer, char *version, char *tags);
size_t write_data(void *ptr, size_t size, size_t nmemb, FILE *stream);
size_t write_callback(void *ptr, size_t size, size_t nmemb, void *userdata);

#endif
