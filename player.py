import pygame as pg

from support import import_folder

class Player(pg.sprite.Sprite):
    def __init__(self, pos, level):
        super().__init__()
        self.level = level
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.06
        # print(self.animations)
        self.image = self.animations['idle'][self.frame_index]
        self.DEFAULT_IMAGE_SIZE = (1000, 1000)
        
        self.rect = self.image.get_rect(topleft = pos)

        #Player Movement
        self.gravity = 1.4
        self.direction = pg.math.Vector2(0, 0)
        self.speed = 2
        self.jump_speed = -20
        #player status
        self.status = 'idle'
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False
    
    def import_character_assets(self):
        character_path = 'Images/Player/PNG/'
        self.animations = {'idle':[], 'run':[], 'jump':[], 'fall':[]}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)
        print(self.animations)    

    def animate(self):
        animation = self.animations[self.status]

        #loop over frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        image = animation[int(self.frame_index)]
        if(self.facing_right):
            self.image = image
        else:
            flipped_image = pg.transform.flip(image, True, False)
            self.image = flipped_image
        
        #set the rect
        if self.on_ground and self.on_right:
            self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
        elif self.on_ground and self.on_left:
            self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
        elif self.on_ground:
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
        elif self.on_ceiling and self.on_right:
            self.rect = self.image.get_rect(topright = self.rect.topright)
        elif self.on_ceiling and self.on_left:
            self.rect = self.image.get_rect(topleft = self.rect.topleft)
        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop = self.rect.midtop)
            
    def get_input(self):
        #Take the input
        keys = pg.key.get_pressed()

        if(keys[pg.K_d]):
            self.direction.x = 1
            self.facing_right = True
        elif(keys[pg.K_a]):
            self.direction.x = -1
            self.facing_right = False
        else:
            self.direction.x = 0

        if(keys[pg.K_SPACE] and self.direction.y == 0 and self.status != 'jump'):
            self.jump()
    
    def get_status(self):
        if self.direction.y <0:
            self.status = 'jump'
        elif self.direction.y > 1.6:
            self.status = 'fall'
        else:
            if self.direction.x != 0:
                self.status = 'run'
            else:
                self.status = 'idle'
    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed

    def update(self):
        #Move the player
        self.get_input()
        self.get_status()
        self.animate()
        self.rect.x += self.direction.x*self.speed