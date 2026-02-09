import pygame
import sys
from logger import log_state, log_event
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot


def main():
    pygame.init()
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Shot.containers = (shots, drawable, updatable)

    asteroidfield = AsteroidField()
    player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

    while True:
        log_state()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
        screen.fill("black")
        updatable.update(dt)

        for item in drawable:
            item.draw(screen)

        for ast in asteroids:
            if ast.collides_with(player):
                log_event("player_hit")
                font = pygame.font.Font(None, 74)  # None = default font, 74 = size
                text_surface = font.render("Game Over!", True, "white")  # True = anti-aliasing, "white" = color
                screen.blit(text_surface, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))  # blit means "draw this surface onto the screen"
                pygame.display.flip()
                pygame.time.wait(3000)
                sys.exit()
                
            
        for ast in asteroids:
            for shot in shots:
                if shot.collides_with(ast):
                    log_event("asteroid_shot")
                    shot.kill()
                    ast.split()
                

        pygame.display.flip()
        dt = clock.tick(60)/1000
        

if __name__ == "__main__":
    main()
