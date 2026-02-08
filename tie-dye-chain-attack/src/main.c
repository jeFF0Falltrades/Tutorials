/*
 * main.c
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
#include <time.h>
#include "game.h"
#include "explosion.h"
#include "render.h"

int main(int argc, char *argv[])
{
    srand(time(NULL));

    // Initialize SDL
    if (SDL_Init(SDL_INIT_VIDEO) < 0)
    {
        printf("SDL init failed: %s\n", SDL_GetError());
        return 1;
    }

    // Create the window
    SDL_Window *window = SDL_CreateWindow("Tie-Dye Chain Attack",
                                          SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED,
                                          SCREEN_WIDTH, SCREEN_HEIGHT, SDL_WINDOW_SHOWN);

    if (!window)
    {
        printf("Window creation failed: %s\n", SDL_GetError());
        SDL_Quit();
        return 1;
    }

    // Create the renderer
    SDL_Renderer *renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);

    if (!renderer)
    {
        printf("Renderer creation failed: %s\n", SDL_GetError());
        SDL_DestroyWindow(window);
        SDL_Quit();
        return 1;
    }

    // Enable alpha blending for transparency
    SDL_SetRenderDrawBlendMode(renderer, SDL_BLENDMODE_BLEND);

    // Initialize game state
    GameState gs;
    initLevel(&gs, 1);

    // Main game loop
    bool running = true;
    bool levelComplete = false;
    bool levelFailed = false;

    SDL_Event e;
    while (running)
    {
        while (SDL_PollEvent(&e))
        {
            if (e.type == SDL_QUIT)
            {
                running = false;
            }
            else if (e.type == SDL_MOUSEBUTTONDOWN && !gs.clicked && !levelComplete && !levelFailed)
            {
                int mx, my;
                SDL_GetMouseState(&mx, &my);
                createExplosion(&gs, mx, my, 255, 255, 255);
                gs.clicked = true;
            }
            else if (e.type == SDL_KEYDOWN && (levelComplete || levelFailed))
            {
                if (e.key.keysym.sym == SDLK_SPACE)
                {
                    if (levelComplete)
                    {
                        initLevel(&gs, gs.level + 1);
                    }
                    else
                    {
                        initLevel(&gs, gs.level);
                    }
                    levelComplete = false;
                    levelFailed = false;
                }
            }
        }

        if (!levelComplete && !levelFailed)
        {
            updateGame(&gs);

            // Check win condition - but only after explosions finish
            if (gs.ballsDestroyed >= gs.targetBalls)
            {
                // Trigger flash on win
                if (!gs.flashTriggered)
                {
                    gs.flashTimer = FLASH_DURATION;
                    gs.flashTriggered = true;
                }

                // Only complete level when explosions are done
                if (!explosionsActive(&gs))
                {
                    levelComplete = true;
                    printf("Level %d Complete! Achieved %d/%d. Press SPACE for next level.\n",
                           gs.level, gs.ballsDestroyed, gs.ballCount);
                }
            }

            // Decay flash timer
            if (gs.flashTimer > 0)
            {
                gs.flashTimer--;
            }

            // Check fail condition (no more active explosions and clicked)
            if (gs.clicked)
            {
                if (!explosionsActive(&gs) && gs.ballsDestroyed < gs.targetBalls)
                {
                    levelFailed = true;
                    printf("Level Failed. %d/%d achieved. Press SPACE to retry.\n",
                           gs.ballsDestroyed, gs.targetBalls);
                }
            }
        }

        renderGame(renderer, &gs);
        SDL_Delay(16); // ~60 FPS
    }

    // Clean up
    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    SDL_Quit();

    return 0;
}
