#include "include/common.h"
#include "include/fetch.h"

size_t write_data(void *ptr, size_t size, size_t nmemb, FILE *stream) {
    return fwrite(ptr, size, nmemb, stream);
}

size_t write_callback(void *ptr, size_t size, size_t nmemb, void *userdata) {
    ResponseBuffer *response = (ResponseBuffer *)userdata;
    size_t total_size = size * nmemb;

    if (response->size + total_size >= BUFFER_SIZE - 1) {
        fprintf(stderr, "Buffer overflow potential, data too large\n");
        return 0;
    }

    memcpy(response->data + response->size, ptr, total_size);
    response->size += total_size;
    response->data[response->size] = '\0';
    return total_size;
}

void fetch_github_releases(const char *url, char *response_buffer) {
    CURL *curl;
    CURLcode res;

    ResponseBuffer response = { response_buffer, 0 };
    response_buffer[0] = '\0';

    curl_global_init(CURL_GLOBAL_DEFAULT);
    curl = curl_easy_init();

    if (curl) {
        curl_easy_setopt(curl, CURLOPT_URL, url);
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_callback);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &response);
        curl_easy_setopt(curl, CURLOPT_USERAGENT, "Mozilla/5.0");

        res = curl_easy_perform(curl);

        if (res != CURLE_OK) {
            fprintf(stderr, "curl_easy_perform() failed: %s\n", curl_easy_strerror(res));
        }

        curl_easy_cleanup(curl);
    }

    curl_global_cleanup();
}

void parse_and_display_obc_info(const char *response_buffer, char *version, char *tags) {
    const char *tag_start = strstr(response_buffer, "\"tag_name\":");
    const char *pre_start = strstr(response_buffer, "\"prerelease\":");

    if (tag_start) {
        tag_start += 12;
        while (*tag_start == ' ' || *tag_start == '\"') tag_start++;

        sscanf(tag_start, "%255[^\"]", version);
    } else {
        strcpy(version, "N/A");
    }

    if (pre_start) {
        int is_prerelease = 0;
        sscanf(pre_start, "\"prerelease\": %d", &is_prerelease);
        strcpy(tags, is_prerelease ? "beta" : "stable");
    } else {
        strcpy(tags, "N/A");
    }
}

