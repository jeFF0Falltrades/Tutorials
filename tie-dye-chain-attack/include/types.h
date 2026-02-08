/*
 * types.h
 *
 * This file contains the types/structs used in the game, unified in one place
 * to avoid circular dependencies in a simple way
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
#ifndef TYPES_H
#define TYPES_H
#include <stdbool.h>
#include <stdint.h>
#include "config.h"

typedef enum
{
    BALL_MOVING,
    BALL_EXPLODING,
    BALL_DEAD
} BallState;

typedef struct
{
    float x, y;
    float vx, vy;
    BallState state;
    int explosionTimer;
    uint8_t r, g, b;
} Ball;

typedef struct
{
    float x, y;
    float radius;
    float maxRadius;
    bool active;
    int timer;
    uint8_t r, g, b;
} Explosion;

typedef struct
{
    Ball balls[MAX_BALLS_OR_EXPLOSIONS];
    Explosion explosions[MAX_BALLS_OR_EXPLOSIONS];
    int ballCount;
    int ballsDestroyed;
    int targetBalls;
    bool clicked;
    int level;
    int flashTimer;
    bool flashTriggered;
} GameState;

#endif
