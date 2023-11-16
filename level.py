import pygame as pg

from tiles import Tile
from settings import tile_size, screen_width
from player import Player

class Level:
    def __init__(self, level_data, surface):
        self.display_surface = surface
        self.canJump = False
               
        self.setup_level(level_data)
        self.world_shift = 0
        self.current_x = 0
        #Parallax
        self.canParallax = True
        self.scroll = 0
        self.bg_images = []
        for i in range(1, 6):
            self.bg_image = pg.image.load(f"Images/Parallax/plx-{i}.png").convert_alpha()
            self.w = self.bg_image.get_width()
            self.h = self.bg_image.get_height()
            self.bg_image = pg.transform.scale(self.bg_image, (self.w * 1.7, self.h* 1.7))
            self.bg_images.append(self.bg_image)
        self.bg_width = self.bg_images[0].get_width()
        

    def getCanJump(self):
        return self.canJump
    
    def setup_level(self, layout):
        self.tiles = pg.sprite.Group()
        self.player = pg.sprite.GroupSingle()
        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                x = tile_size * col_index
                y = tile_size * row_index
                if cell == 'X':
                    tile = Tile((x, y), tile_size)
                    self.tiles.add(tile)
                if cell == 'P':
                    player_sprite = Player((x, y), self)
                    self.player.add(player_sprite)

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < screen_width/4 and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        elif player_x > screen_width - (screen_width/4) and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        for sprite in self.tiles.sprites():
            if(sprite.rect.colliderect(player.rect)):
                if(player.direction.x < 0):
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif(player.direction.x > 0):
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right
        if(player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0)):
            player.on_left = False
        if player.on_right and (player.rect.left > self.current_x or player.direction.x <= 0):
            player.on_right = False
    
    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()

        for sprite in self.tiles.sprites():
            if(sprite.rect.colliderect(player.rect)):
                if(player.direction.y > 0):
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif(player.direction.y < 0):
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = False
        if player.on_ground and player.direction.y<0 or player.direction.y > 1:
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0:
            player.on_ceiling = False
    
    def parallax(self):
        for x in range(5):
            speed = 0.5
            for i in self.bg_images:
                self.display_surface.blit(i, ((x * self.bg_width) - self.scroll * speed, 0))
                speed += 0.2
        
        keys = pg.key.get_pressed()

        if(keys[pg.K_d]):
            self.scroll += 5
        elif(keys[pg.K_a]):
            self.scroll -= 5

    def run(self):
        #level
        self.parallax()
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        self.scroll_x()

        #Player
        self.player.update()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.player.draw(self.display_surface)
        