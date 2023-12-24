#ifndef SERVO_CONTROL_H
#define SERVO_CONTROL_H

#include "driver/ledc.h"

extern void servoDeg(int pinServo, float ms, ledc_channel_t channel);
extern int pinServo1;
extern int pinServo2;

#endif // SERVO_CONTROL_H
