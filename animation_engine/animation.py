from typing import Generator, Callable
import pygame
from .timer import Timer


class Animation:
    def __init__(self, fps: int, frames: list[pygame.Surface], name: str, indices: list[int], one_shot:bool=False) -> None:
        self._name = name
        self._one_shot = one_shot
        self._frames = tuple([frames[i] for i in indices])
        self._played = False

        self._fps = fps
        self._frame_timer = Timer(1 / fps)
        self._frame_index = 0
        self._last_frame = self._frames[0]

    def is_one_shot(self) -> bool:
        return self._one_shot

    def is_finished(self) -> bool:
        return self._played

    def reset(self) -> None:
        self._played = False
        self._frame_index = 0

    def get_frame(self) -> pygame.Surface:
        if self._played:
            return self._last_frame

        if self._frame_timer.is_ready():
            self._frame_index += 1

        if self._frame_index == len(self._frames):
            self._frame_index = 0
            self._played = True
            return self._last_frame

        self._last_frame = self._frames[self._frame_index]
        return self._last_frame
