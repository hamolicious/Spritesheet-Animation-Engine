import pygame
from animation_engine import AnimationEngine, SpriteSheetLoader


class App:
    def __init__(self) -> None:
        self.size = (1000, 700)
        self.fps = 0

        self.clock = pygame.time.Clock()
        self.delta_time = 0

        self.screen: pygame.Surface
        self.mouse_pos: list[int]
        self.mouse_rel: list[int]
        self.mouse_press: list[int]
        self.key_press: list[int]

    def init_pygame(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        self.screen.fill([255, 255, 255])
        pygame.display.set_icon(self.screen)

    def check_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

    def update_io(self) -> None:
        self.mouse_pos = pygame.mouse.get_pos()
        self.mouse_rel = pygame.mouse.get_rel()
        self.mouse_press = pygame.mouse.get_pressed()
        self.key_press = pygame.key.get_pressed()

    def update_display(self) -> None:
        pygame.display.update()
        self.delta_time = self.clock.tick(self.fps)
        pygame.display.set_caption(
            f'Framerate: {int(self.clock.get_fps())}')

    def run(self):
        self.init_pygame()
        self.setup()

        while True:
            self.check_events()
            self.update_io()
            self.loop()
            self.update_display()

    def setup(self) -> None:
        frames = SpriteSheetLoader.load('assets/characters.png', [23, 4], row=1)
        animation_engine = AnimationEngine(frames)
        animation_engine.register_animation(15, 'walk-left', range(0, 4))
        animation_engine.register_animation(3, 'jump', [6, 7, 8, 7, 6], one_shot=True)
        animation_engine.register_animation(3, 'hit', [0, 9, 10, 9], one_shot=True)
        animation_engine.register_animation(3, 'punch', [11, 12, 13], one_shot=True)

        animation_engine.preview_animation()

    def loop(self) -> None:
        self.screen.fill('black')

        width = self.surface[0].get_size()[0]
        for i, img in enumerate(self.surface):
            self.screen.blit(img, (i * width, 0))

        if self.key_press[pygame.K_ESCAPE]:
            pygame.quit()
            quit(0)


if __name__ == '__main__':
    app = App()
    app.run()
