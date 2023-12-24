#include "servo_control.h"
#include <stdio.h>
#include <time.h>
#include <string.h>
#include <math.h>
#include <sdkconfig.h>
#include <driver/gpio.h>
#include <driver/ledc.h>
#include <freertos/FreeRTOS.h>
#include <freertos/task.h>

int pinServo1 = 8;
int pinServo2 = 3;

void servoDeg(int pinServo, float ms, ledc_channel_t channel) {
  ledc_timer_config_t ledc_timer = {
        .speed_mode       = LEDC_LOW_SPEED_MODE,
        .timer_num        = LEDC_TIMER_0,
        .duty_resolution  = LEDC_TIMER_13_BIT,
        .freq_hz          = 50,  
        .clk_cfg          = LEDC_AUTO_CLK
  };
  ledc_timer_config(&ledc_timer);
  ledc_channel_config_t ledc_channel = {
        .speed_mode     = LEDC_LOW_SPEED_MODE,
        .channel        = channel,
        .timer_sel      = LEDC_TIMER_0,
        .intr_type      = LEDC_INTR_DISABLE,
        .gpio_num       = pinServo,
        .duty           = 0,
        .hpoint         = 0
  };
  ledc_channel_config(&ledc_channel);  
  int duty = (int)(100.0*(ms/20.0)*81.91);
  printf("%fms, duty = %f%% -> %d\n",ms, 100.0*(ms/20.0), duty);
  ledc_set_duty(LEDC_LOW_SPEED_MODE, channel, duty);
  ledc_update_duty(LEDC_LOW_SPEED_MODE, channel);
  vTaskDelay( 50/portTICK_PERIOD_MS );
  ledc_stop(LEDC_LOW_SPEED_MODE, channel, 0);
}