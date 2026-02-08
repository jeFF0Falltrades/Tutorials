/*
 * explosion.c
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
#include <stdint.h>
#include "config.h"
#include "explosion.h"

/**
 * Lighten a given color by a specified amount
 *
 * @param color The color to lighten
 * @param amount The amount to lighten the color by
 * @return The lightened color
 */
static uint8_t lighten(uint8_t color, int amount)
{
    int result = color + amount;
    // Cap the result at 255 to prevent overflow
    return (result > 255) ? 255 : result;
}

/**
 * Create a new explosion at the given position
 *
 * @param gs The game state to modify
 * @param x The x position of the explosion
 * @param y The y position of the explosion
 */
void createExplosion(GameState *gs, float x, float y, uint8_t r, uint8_t g, uint8_t b)
{
    // Find the first inactive explosion
    for (int i = 0; i < MAX_BALLS_OR_EXPLOSIONS; i++)
    {
        if (!gs->explosions[i].active)
        {
            gs->explosions[i].x = x;
            gs->explosions[i].y = y;
            gs->explosions[i].radius = 0;
            gs->explosions[i].maxRadius = EXPLOSION_MAX_RADIUS;
            gs->explosions[i].active = true;
            gs->explosions[i].timer = EXPLOSION_DURATION;
            gs->explosions[i].r = lighten(r, 50);
            gs->explosions[i].g = lighten(g, 50);
            gs->explosions[i].b = lighten(b, 50);
            break;
        }
    }
}

/**
 * Check if the given ball is colliding with the given explosion
 *
 * @param ball The ball to check for collision
 * @param exp The explosion to check for collision
 * @return true if the ball is colliding with the explosion, false otherwise
 */
bool checkCollision(Ball *ball, Explosion *exp)
{
    float dx = ball->x - exp->x;
    float dy = ball->y - exp->y;
    float distance = sqrt(dx * dx + dy * dy);
    return distance < (BALL_RADIUS + exp->radius);
}

/**
 * Check if there are any active explosions in the game state
 *
 * @param gs The game state to check
 * @return true if there are any active explosions, false otherwise
 */
bool explosionsActive(GameState *gs)
{
    for (int i = 0; i < MAX_BALLS_OR_EXPLOSIONS; i++)
    {
        if (gs->explosions[i].active)
        {
            return true;
        }
    }
    return false;
}
