#pragma once

#include "esp_err.h"

#ifdef __cplusplus
extern "C" {
#endif

void receive_from_client(int *center_x, int *center_y, float *degree_x, float *degree_y);

esp_err_t tcp_server_wait_for_connection(void);

esp_err_t tcp_server_send(uint8_t *payload, size_t size);

void tcp_server_close_when_done(void);

#ifdef __cplusplus
}
#endif
