import pygame
import sys

class Slider:
    def __init__(self, x, y, width, height, text, audio_list, font_size = 50):
        self.screen = pygame.display.get_surface()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.audio_list = audio_list
        self.clicked = False
        self.click = False
        self.volume = 0.5
        self.text = text
        self.font_size = font_size

        self.surf = pygame.Surface((self.width, self.height))
        self.surf.fill((0,0,0))
        self.rect = self.surf.get_rect(topleft = (self.x, self.y))

        self.slider_surf = pygame.Surface((10,self.height + 4))
        self.slider_surf.fill((30,30,30))
        self.slider_rect = self.slider_surf.get_rect(center = self.rect.center)

        self.left_of_slider_surf = pygame.Surface((self.slider_rect.centerx - self.rect.left - 3, self.height - 3))
        self.left_of_slider_surf.fill((100,255,100))
        self.left_of_slider_rect = self.left_of_slider_surf.get_rect(topleft = (self.x + 2, self.y + 2))


        self.font = pygame.font.Font(None, font_size)
        self.volume_surf = self.font.render(str(self.volume), True, (255,255,255))
        self.volume_rect = self.volume_surf.get_rect(topleft = (self.x + self.width + 10, self.y))

        self.text_surf = self.font.render(text, True, (255,255,255))
        self.text_rect = self.text_surf.get_rect(topright = self.rect.topleft - pygame.Vector2(10,0))


    def draw(self):
        self.screen.blit(self.surf, self.rect)
        pygame.draw.rect(self.screen, (255,255,255), self.rect, 2)

        self.screen.blit(self.left_of_slider_surf, self.left_of_slider_rect)

        self.screen.blit(self.slider_surf, self.slider_rect)
        pygame.draw.rect(self.screen, (255,255,255), self.slider_rect, 2)

        self.screen.blit(self.volume_surf, self.volume_rect)
        self.screen.blit(self.text_surf, self.text_rect)

    def adjust_slider(self):
        if not self.click or self.clicked:
            if pygame.mouse.get_pressed()[0]:
                mouse_pos = pygame.mouse.get_pos()
                self.click = True
                if self.slider_rect.collidepoint(mouse_pos) or self.clicked:
                    self.clicked = True
                    self.slider_rect.centerx = mouse_pos[0]

                    if self.slider_rect.left <= self.rect.left:
                        self.slider_rect.left = self.rect.left
                    elif self.slider_rect.right >= self.rect.right:
                        self.slider_rect.right = self.rect.right

                    self.left_of_slider_surf = pygame.Surface((self.slider_rect.centerx - self.rect.left, self.height - 3))
                    self.left_of_slider_surf.fill((100,255,100))
                    self.left_of_slider_rect = self.left_of_slider_surf.get_rect(topleft = (self.x + 2, self.y + 2))

                    self.volume = round((self.slider_rect.left - self.x) / (self.width - self.slider_rect.width), 2)
                    self.volume_surf = self.font.render(str(self.volume), True, (255,255,255))
                    self.adjust_volume()
            else:
                self.clicked = False
        else:
            if not pygame.mouse.get_pressed()[0]:
                self.click = False

    def adjust_volume(self):
        for audio in self.audio_list:
            audio.set_volume(self.volume)


    def update(self):
        self.adjust_slider()

if __name__ == "__main__":
    pygame.init()
    screen_width, screen_height = 600,600
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()

    bg_music1 = pygame.mixer.Sound('background.mp3')
    bg_music1.set_volume(0.5)
    bg_music1.play(loops = -1)

    bg_music2 = pygame.mixer.Sound('music.wav')
    bg_music2.set_volume(0.5)
    bg_music2.play(loops = -1)

    # Slider
    slider_list = []
    slider1 = Slider(200, 200, 300, 30, "music1",[bg_music1])
    slider2 = Slider(200, 250, 300, 30, "music2", [bg_music2])
    slider_list.append(slider1)
    slider_list.append(slider2)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((30,30,30))
        for slider in slider_list:
            slider.update()
            slider.draw()

        pygame.display.update()
        clock.tick(60)
