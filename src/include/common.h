#ifndef COMMON_H
#define COMMON_H

#include <ncurses.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <curl/curl.h>

#define BUFFER_SIZE 2048
#define MAX_VERSION 5
#define VERSION "0.0.1"

typedef struct {
    char *data;
    size_t size;
} ResponseBuffer;

#endif
