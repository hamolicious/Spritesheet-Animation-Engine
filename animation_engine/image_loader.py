import pygame
import os


class BaseImageLoader:
    _valid_file_ext = ['PNG', 'JPG', 'JPEG', 'GIF']

    @classmethod
    def _check_path_valid(cls, path: str) -> bool:
        raise NotImplementedError()

    @classmethod
    def load(cls) -> list[pygame.Surface]:
        raise NotImplementedError()


# TODO: finish implementing and verifying this works
# TODO: add testing
class FramesLoader(BaseImageLoader):
    @classmethod
    def _check_path_valid(cls, path: str) -> bool:
        if not os.path.exists(path):
            return False

        files = os.listdir(path)
        for f in files:
            if f.split('.')[-1].upper() not in cls._valid_file_ext:
                return False

        return True


class SpriteSheetLoader(BaseImageLoader):
    @classmethod
    def _check_path_valid(cls, path: str) -> bool:
        if not os.path.exists(path):
            return False

        ext = path.split('.')[-1].upper()
        if ext not in cls._valid_file_ext:
            return False

        return True

    @classmethod
    def load(cls, path: str, sprites_count: tuple[int], row: int = None) -> list[pygame.Surface]:
        if not cls._check_path_valid(path):
            raise FileExistsError('Spritesheet path is not valid')

        image = pygame.image.load(path)

        images = []
        sprite_size = [
            int(image.get_size()[0] / sprites_count[0]),
            int(image.get_size()[1] / sprites_count[1]),
        ]

        for i in range(sprites_count[1]):
            if row is not None and row != i:
                continue

            for j in range(sprites_count[0]):
                rect = pygame.Rect(
                    (j * sprite_size[0], i * sprite_size[1]),
                    sprite_size
                )

                sprite_surface = pygame.Surface(
                    sprite_size, pygame.SRCALPHA, 32)
                sprite_surface.blit(image, (-rect.x, -rect.y))
                images.append(sprite_surface.copy())

        return images
