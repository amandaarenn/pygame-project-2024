import random 
import pygame as pg

# --CONSTANTS--
# COLOURS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
EMERALD = (21, 219, 147)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)

WIDTH = 1280  # Pixels
HEIGHT = 720
SCREEN_SIZE = (WIDTH, HEIGHT)

NUM_SNOWBALLS = 4
NUM_ENEMIES = 35


class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()

        #  load img
        SNOWMAN_IMAGE = pg.image.load("./Images/snowman.webp")
            # scale img
        SNOWMAN_IMAGE = pg.transform.scale(
            SNOWMAN_IMAGE, (SNOWMAN_IMAGE.get_width() // 4, SNOWMAN_IMAGE.get_height() // 4))    
    
        self.image = SNOWMAN_IMAGE

        self.rect = self.image.get_rect()

        self.lives_remaining = 9

    def update(self):
        self.rect.centerx = pg.mouse.get_pos()[0]
        self.rect.centery = pg.mouse.get_pos()[1]
        if self.rect.right < WIDTH - 2:
            self.rect.right = WIDTH - 2

class Bullet(pg.sprite.Sprite):
    def __init__(self, player_loc: list):
        """
        Params:
            player_loc: x,y coords of centerx and top
        """
        super().__init__()

        # Shooting Snowballs
        self.image = pg.image.load("./Images/snowball.png") 

        self.image = pg.transform.scale(
            self.image, (self.image.get_width() // 5, self.image.get_height() // 5))   
    
        self.rect = self.image.get_rect()

        # Spawn at the Player
        self.rect.centerx = player_loc[0]
        self.rect.top = player_loc[1]

        self.vel_x = -3  # move up

    def update(self):
        self.rect.x += self.vel_x

        # Kill the bullet if it leaves the screen
        if self.rect.right < 0:
            self.kill()

class Goat(pg.sprite.Sprite):
    def __init__(self, centerx: int, centery: int):
        """
        Params:
            centerx: center x spawn of the enemy
            centery: center y spawn of the enemy
        """
        super().__init__()

         #  load img
        ENEMY_IMAGE = pg.image.load("./Images/goat.png")
            # scale img
        ENEMY_IMAGE = pg.transform.scale(
            ENEMY_IMAGE, (ENEMY_IMAGE.get_width() // 10, ENEMY_IMAGE.get_height() // 10))    

        self.image = ENEMY_IMAGE

        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = centerx, centery

        self.vel_x = 2
        self.vel_y = 2

    def update(self):
        # Movement
        self.rect.y += self.vel_y

        # Bounce in the y-axis
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.vel_y *= -1
        if self.rect.top < 0:
            self.rect.top = 0
            self.vel_y *= -1

def start():

    pg.init()
    pg.mouse.set_visible(False)

    # --Game State Variables--
    screen = pg.display.set_mode(SCREEN_SIZE)
    done = False
    clock = pg.time.Clock()

    bg = pg.image.load("./Images/snowbg.png")
    bg = pg.transform.scale(bg, SCREEN_SIZE)

    score = 0 

    font = pg.font.SysFont("Apple Chancery", 24)

    # All sprites go in this sprite Group
    all_sprites = pg.sprite.Group()

    # Goat sprites
    enemy_sprites = pg.sprite.Group()

    # Sprite list for bullets
    bullet_sprites = pg.sprite.Group()

    #Create a player and store it in a variable
    player = Player ()
    all_sprites.add(player)

    for x in range(NUM_ENEMIES):
        random_x = random.randint(10, 900)
        random_y = random.randint(10, 500)
        enemy = Goat(random_x, random_y)
        all_sprites.add(enemy)
        enemy_sprites.add (enemy)
      

    pg.display.set_caption("Snowball Shooter")

    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            if event.type == pg.MOUSEBUTTONDOWN:
                bullet = Bullet((player.rect.centerx, player.rect.top))
                all_sprites.add(bullet)
                bullet_sprites.add(bullet)


        all_sprites.update()

        # Collision between bullets and enemies
        for bullet in bullet_sprites:
            enemies_hit = pg.sprite.spritecollide(bullet, enemy_sprites, False)
                
            for enemy in enemies_hit:
                enemy.kill()
                bullet.kill()
                score += 1000       

        if len(enemy_sprites) <= 0:
            for _ in range(NUM_ENEMIES):
                random_x = random.randint(10, 900)
                random_y = random.randint(10, 500)
                enemy = Goat(random_x, random_y)
                all_sprites.add(enemy)
                enemy_sprites.add(enemy)    
        # --- Draw items
        screen.blit(bg, (0, 0))

        all_sprites.draw(screen)
        enemy_sprites.draw(screen)

         # TODO: detect collisions with enemies
        enemies_collided = pg.sprite.spritecollide(
            player, 
            enemy_sprites, 
            False
        )

        # Create an image that has the score in it
        score_image = font.render(f"Score: {score}", True, WHITE)
        
        # Draw/blit the image on the screen
        screen.blit(score_image, (5,5))

        # Update the screen with anything new
        pg.display.flip()


        # --- Tick the Clock
        clock.tick(10000000000000)  # 60 fps

    pg.quit()


def main():
    start()


if __name__ == "__main__":
    main()