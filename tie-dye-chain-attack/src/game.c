/*
 * game.c
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
#include <stdio.h>
#include "ball.h"
#include "config.h"
#include "explosion.h"
#include "game.h"

/**
 * Initialize a new level with the given number
 * @param gs The game state to modify
 * @param level The level number to initialize
 */
void initLevel(GameState *gs, int level)
{
    gs->level = level;
    gs->ballCount = 10 + (level * 2); // Add more balls each level
    if (gs->ballCount > MAX_BALLS_OR_EXPLOSIONS)
        gs->ballCount = MAX_BALLS_OR_EXPLOSIONS;

    gs->targetBalls = 5 + level; // Increase min explosions for victory
    if (gs->targetBalls > gs->ballCount)
        gs->targetBalls = gs->ballCount;

    gs->ballsDestroyed = 0;
    gs->clicked = false;
    gs->flashTimer = 0;
    gs->flashTriggered = false;

    // Initialize balls
    for (int i = 0; i < gs->ballCount; i++)
    {
        initBall(&gs->balls[i]);
    }

    // Reset explosion states
    for (int i = 0; i < MAX_BALLS_OR_EXPLOSIONS; i++)
    {
        gs->explosions[i].active = false;
    }
    printf("Level %d Goal: %d.\n", gs->level, gs->targetBalls);
}

/**
 * Check if a ball has collided with a boundary (wall or ceiling).
 * If so, reverse the ball's velocity and correct its position to prevent
 * it from getting stuck.
 * @param ball The Ball object to check
 */
void checkForBoundary(Ball *ball)
{
    // Check if the ball has collided with the left/right wall
    if (ball->x < BALL_RADIUS || ball->x > SCREEN_WIDTH - BALL_RADIUS)
    {
        ball->vx = -ball->vx;
        ball->x = (ball->x < BALL_RADIUS) ? BALL_RADIUS : SCREEN_WIDTH - BALL_RADIUS;
    }
    // Check if the ball has collided with the top/bottom ceiling
    if (ball->y < BALL_RADIUS || ball->y > SCREEN_HEIGHT - BALL_RADIUS)
    {
        ball->vy = -ball->vy;
        ball->y = (ball->y < BALL_RADIUS) ? BALL_RADIUS : SCREEN_HEIGHT - BALL_RADIUS;
    }
}

/**
 * Check if the given ball has collided with any active explosions
 * @param gs The game state to modify
 * @param ball The Ball object to check
 */
void checkForExplosion(GameState *gs, Ball *ball)
{
    // Check if the ball has collided with any active explosions
    for (int j = 0; j < MAX_BALLS_OR_EXPLOSIONS; j++)
    {
        if (gs->explosions[j].active && checkCollision(ball, &gs->explosions[j]))
        {
            ball->state = BALL_EXPLODING;
            createExplosion(gs, ball->x, ball->y, ball->r, ball->g, ball->b);
            gs->ballsDestroyed++;
            break;
        }
    }
}

/**
 * Update the balls in the game state
 * @param gs The game state to update
 */
void updateBalls(GameState *gs)
{
    for (int i = 0; i < gs->ballCount; i++)
    {
        Ball *ball = &gs->balls[i];

        if (ball->state == BALL_MOVING)
        {
            // Move ball to next position
            ball->x += ball->vx;
            ball->y += ball->vy;

            // Bounce off boundaries
            checkForBoundary(ball);

            // Check collision with explosions
            checkForExplosion(gs, ball);
        }
        else if (ball->state == BALL_EXPLODING)
        {
            ball->explosionTimer++;
            if (ball->explosionTimer > EXPLOSION_DURATION)
            {
                ball->state = BALL_DEAD;
            }
        }
    }
}

/**
 * Update the explosions in the game state
 * @param gs The game state to update
 */
void updateExplosions(GameState *gs)
{
    for (int i = 0; i < MAX_BALLS_OR_EXPLOSIONS; i++)
    {
        if (gs->explosions[i].active)
        {
            gs->explosions[i].timer--;

            // Only expand during the growth phase
            int elapsed = EXPLOSION_DURATION - gs->explosions[i].timer;
            if (elapsed < EXPLOSION_GROWTH_TIME && gs->explosions[i].radius < gs->explosions[i].maxRadius)
            {
                gs->explosions[i].radius += EXPLOSION_GROWTH_RATE;
            }

            // Deactivate when timer runs out
            if (gs->explosions[i].timer <= 0)
            {
                gs->explosions[i].active = false;
            }
        }
    }
}

/**
 * Update the game state
 * @param gs The game state to update
 */
void updateGame(GameState *gs)
{
    updateBalls(gs);
    updateExplosions(gs);
}
