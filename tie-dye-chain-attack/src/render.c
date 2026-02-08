/*
 * render.c
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
#include <stdlib.h>
#include <time.h>
#include "config.h"
#include "render.h"

/**
 * Draw a filled circle at the given position
 *
 * This function draws a filled circle at the given position, using the
 * current drawing color. The circle's edge is smoothly faded out to
 * the transparent color.
 *
 * @param renderer The SDL renderer to draw with
 * @param cx The x coordinate of the circle's center
 * @param cy The y coordinate of the circle's center
 * @param radius The radius of the circle to draw
 */
void drawCircle(SDL_Renderer *renderer, int cx, int cy, int radius)
{
    Uint8 r, g, b, baseAlpha;
    SDL_GetRenderDrawColor(renderer, &r, &g, &b, &baseAlpha);

    // Loop over all pixels in a box around the circle
    for (int y = -radius - 1; y <= radius + 1; y++)
    {
        for (int x = -radius - 1; x <= radius + 1; x++)
        {
            float distance = sqrtf(x * x + y * y);

            // If the distance is within the circle's radius, draw the pixel
            if (distance <= radius + 1)
            {
                // Smooth edge falloff for "manual" anti-aliasing
                float alpha = 1.0f;
                if (distance > radius - 1)
                {
                    alpha = (radius + 1) - distance;
                    if (alpha < 0)
                        alpha = 0;
                    if (alpha > 1)
                        alpha = 1;
                }

                Uint8 finalAlpha = (Uint8)(baseAlpha * alpha);
                SDL_SetRenderDrawColor(renderer, r, g, b, finalAlpha);
                SDL_RenderDrawPoint(renderer, cx + x, cy + y);
            }
        }
    }
}

/**
 * Render the game state
 *
 * @param renderer The SDL renderer to draw with
 * @param gs The game state to render
 */
void renderGame(SDL_Renderer *renderer, GameState *gs)
{
    // Calculate background color with flash
    int baseR = BACKGROUND_COLOR_R, baseG = BACKGROUND_COLOR_G, baseB = BACKGROUND_COLOR_B;
    if (gs->flashTimer > 0)
    {
        float flashIntensity = (float)gs->flashTimer / (float)(FLASH_DURATION);
        int flashAmount = (int)(flashIntensity * 100);

        baseR += flashAmount;
        baseG += flashAmount;
        baseB += flashAmount;
    }

    // Clear the screen
    SDL_SetRenderDrawColor(renderer, baseR, baseG, baseB, 255);
    SDL_RenderClear(renderer);

    // Draw explosions
    for (int i = 0; i < MAX_BALLS_OR_EXPLOSIONS; i++)
    {
        if (gs->explosions[i].active)
        {
            // Fade explosion referencing remaining time
            Uint8 alpha;
            if (gs->explosions[i].timer > EXPLOSION_FADE_TIME)
            {
                alpha = 255;
            }
            else
            {
                alpha = (Uint8)((gs->explosions[i].timer * 255) / EXPLOSION_FADE_TIME);
            }
            // Use the explosion's stored color
            SDL_SetRenderDrawColor(renderer,
                                   gs->explosions[i].r,
                                   gs->explosions[i].g,
                                   gs->explosions[i].b,
                                   alpha);
            drawCircle(renderer, (int)gs->explosions[i].x, (int)gs->explosions[i].y, (int)gs->explosions[i].radius);
        }
    }

    // Draw balls
    for (int i = 0; i < gs->ballCount; i++)
    {
        Ball *ball = &gs->balls[i];
        if (ball->state == BALL_MOVING)
        {
            SDL_SetRenderDrawColor(renderer, ball->r, ball->g, ball->b, 255);
            drawCircle(renderer, (int)ball->x, (int)ball->y, BALL_RADIUS);
        }
    }

    SDL_RenderPresent(renderer);
}
