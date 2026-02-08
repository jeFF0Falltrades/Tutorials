/*
 * ball.c
 *
 * Author: jeFF0Falltrades
 * From the video "Will AI Reverse Engineer my Game?": https://youtu.be/WBTyE1eac_s
 *
 * MIT License
 *
 * Copyright 2026 Jeff Archer
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the “Software”), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */
#include <math.h>
#include <stdlib.h>
#include "ball.h"
#include "config.h"

// Define M_PI, as it can be a nonstandard extension
#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

/**
 * Initialize a Ball object with a random position and velocity.
 *
 * @param ball the Ball object to initialize
 */
void initBall(Ball *ball)
{
    // Set ball position
    ball->x = rand() % SCREEN_WIDTH;
    ball->y = rand() % SCREEN_HEIGHT;

    // Calculate the ball's velocity based on a random angle
    float angle = (rand() % 360) * M_PI / 180.0f;
    ball->vx = cos(angle) * BALL_SPEED;
    ball->vy = sin(angle) * BALL_SPEED;

    ball->state = BALL_MOVING;
    ball->explosionTimer = 0;

    // Assign a random color to the ball
    ball->r = rand() % 256;
    ball->g = rand() % 256;
    ball->b = rand() % 256;
}
