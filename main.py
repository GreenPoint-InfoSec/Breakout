from paddle import Paddle
from ball import Ball
from brick import Brick
import pygame

pygame.init()

def main():
    # Define colors
    WHITE = (255,255,255)
    DARKBLUE = (0,50,150)
    LIGHTBLUE = (0,180,240)
    RED = (255,0,0)
    ORANGE = (255,100,0)
    YELLOW = (255,255,0)

    # Define starting score and lives
    score = 0
    lives = 3
    
    # Open a new window0
    size = (800, 600)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Breakout")
    
    # The loop will carry on until the user exits the game
    carryOn = True

    # This will be a list that will contain all the sprites we intend to use in our game.
    all_sprites_list = pygame.sprite.Group()
    
    # Create the Paddle
    paddle = Paddle(LIGHTBLUE, 100, 10)
    paddle.rect.x = 350
    paddle.rect.y = 560

    # Create the Ball
    ball = Ball(WHITE, 10, 10)
    ball.rect.x = 345
    ball.rect.y = 195

    # Bricks
    all_bricks = pygame.sprite.Group()
    for i in range(7):
        brick = Brick(RED,80,30)
        brick.rect.x = 60 + i* 100
        brick.rect.y = 60
        all_sprites_list.add(brick)
        all_bricks.add(brick)
    for i in range(7):
        brick = Brick(ORANGE,80,30)
        brick.rect.x = 60 + i* 100
        brick.rect.y = 100
        all_sprites_list.add(brick)
        all_bricks.add(brick)
    for i in range(7):
        brick = Brick(YELLOW,80,30)
        brick.rect.x = 60 + i* 100
        brick.rect.y = 140
        all_sprites_list.add(brick)
        all_bricks.add(brick)
    
    # Add the paddle to the list of sprites
    all_sprites_list.add(paddle)
    all_sprites_list.add(ball)

    # The clock will be used to control how fast the screen updates
    clock = pygame.time.Clock()

    # -------- Main Program Loop -----------
    while carryOn:
        # --- Main event loop
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                carryOn = False
            elif event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_x]:
                    carryOn = False

        # Move the paddle when arrow keys pressed
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            paddle.moveLeft(5)
        if keys[pygame.K_RIGHT]:
            paddle.moveRight(5)

        # --- Game logic should go here
        all_sprites_list.update()

        #Check if the ball is bouncing against any of the 4 walls:
        if ball.rect.x >= 790:
            ball.velocity[0] = -ball.velocity[0]
        if ball.rect.x <= 0:
            ball.velocity[0] = -ball.velocity[0]
        if ball.rect.y > 590:
            ball.velocity[1] = -ball.velocity[1]
            lives -= 1
            if lives == 0:
                # Game Over
                font = pygame.font.Font(None, 74)
                text = font.render("Game Over", 1, WHITE)
                screen.blit(text, (250, 300))
                pygame.display.flip()
                pygame.time.wait(3000)

                carryOn = False
        if ball.rect.y < 40:
            ball.velocity[1] = -ball.velocity[1]

        # Detect collisons between the ball and the paddles
        if pygame.sprite.collide_mask(ball, paddle):
            ball.rect.x -= ball.velocity[0]
            ball.rect.y -= ball.velocity[1]
            ball.bounce()

        # Detect collisons between ball and brick
        brick_collison_list = pygame.sprite.spritecollide(ball, all_bricks, False)
        for brick in brick_collison_list:
            ball.bounce()
            score += 1
            brick.kill()
            if len(all_bricks) == 0:
                font = pygame.font.Font(None, 74)
                text = font.render("LEVEL COMPLETE", 1, WHITE)
                screen.blit(text, (200, 300))
                pygame.display.flip()
                pygame.time.wait(3000)

                carryOn = False

        # --- Drawing code should go here
        # First, clear the screen to dark blue. 
        screen.fill(DARKBLUE)
        pygame.draw.line(screen, WHITE, [0, 35], [800, 35], 2)

        # Display the score and the number of lives at the top of the screen
        font = pygame.font.Font(None, 30)
        text = font.render("Score: " + str(score), 1, WHITE)
        screen.blit(text, (20,10))
        text = font.render("Lives: " + str(lives), 1, WHITE)
        screen.blit(text, (700,10))

        # Now let's draw all the sprites in one go. (For now we only have 2 sprites!)
        all_sprites_list.draw(screen)

        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
        
        # --- Limit to 60 frames per second
        clock.tick(60)

    #Once we have exited the main program loop we can stop the game engine:
    pygame.quit()

if __name__ == "__main__":
    main()