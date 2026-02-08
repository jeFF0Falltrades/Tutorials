/*
 * config.h
 *
 * Defines customizable constants used throughout the game
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
#define BACKGROUND_COLOR_R 10
#define BACKGROUND_COLOR_G 10
#define BACKGROUND_COLOR_B 30
#define BALL_RADIUS 8
#define BALL_SPEED 2.0f
#define EXPLOSION_FADE_TIME 120
#define EXPLOSION_GROWTH_RATE 2.0f // lower value == smoother expansion
#define EXPLOSION_GROWTH_TIME 50   //  higher value == smoother transitions
#define EXPLOSION_MAX_RADIUS (EXPLOSION_GROWTH_RATE * EXPLOSION_GROWTH_TIME)
#define EXPLOSION_DURATION (EXPLOSION_GROWTH_TIME + EXPLOSION_FADE_TIME)
#define FLASH_DURATION 90
#define MAX_BALLS_OR_EXPLOSIONS 50
#define SCREEN_HEIGHT 600
#define SCREEN_WIDTH 800
