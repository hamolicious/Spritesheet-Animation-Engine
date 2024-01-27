import pygame
from ..common.pane import Pane


class PaneSet:
    def __init__(self, *layers: Pane) -> None:
        self._layers = layers

    def move(self, speed: float) -> None:
        for i, layer in enumerate(self._layers):
            layer.move(
                speed
            )
