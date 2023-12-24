idf_component_register(SRCS "servo_control.c" "tcp_server.c" "main.c"
                    INCLUDE_DIRS ""
                    REQUIRES protocol_examples_common nvs_flash usb mdns esp_ringbuf esp_timer esp_wifi driver)
