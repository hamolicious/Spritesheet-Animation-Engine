import pygame
from typing import Iterable, Any, Generator
from ..test_app import BaseApp
from ..common.exceptions import NoSuchLocationError
from .. import sliding_background
from ..common.pane import Pane
from ..common.scroll_vector import ScrollVector
from .paneset import PaneSet


class AnimationEngine:
  def __init__(self) -> None:
    self._current_slides: tuple[sliding_background.AnimationEngine] = None
    self._locations: dict[str, tuple[sliding_background.AnimationEngine]] = {}
    self._horizon_distance = 10000
    self._spacing = 3000

  def register_location(self, name: str, images: list[pygame.Surface], scroll_vector: ScrollVector = ScrollVector.LEFT) -> None:
    self._locations[name] = []

    for index, image in enumerate(images):
      engine = sliding_background.AnimationEngine()
      engine.register_location(f'{name}-{index}', image, scroll_vector=scroll_vector)
      engine.select_location(f'{name}-{index}')
      self._locations[name].append(engine)

    self._locations[name] = tuple(self._locations.get(name))

  def preview_animation(self, name: str, scale: int = 5, background_color: list[int] = None) -> None:
    if len(name) == 0:
      name = self._animations.keys()

    class Preview(BaseApp):
      def setup(self_child) -> None:
        self_child.parallax_engine = AnimationEngine()
        self_child.parallax_engine._locations = self._locations
        self_child.parallax_engine.select_location(name)

      def loop(self_child) -> None:
        if self_child.key_press[pygame.K_ESCAPE]:
          quit()

        self_child.screen.fill(
            background_color if background_color is not None else [50, 50, 60]
        )

        frame = self_child.parallax_engine.update(0.01 * self_child.delta_time)

        frame = pygame.transform.scale(frame, [
            frame.get_size()[0] * scale,
            frame.get_size()[1] * scale,
        ])
        self_child.screen.blit(frame, (0, 0))

    app = Preview()
    app.size = (
        self._locations.get(name)[0]._current_slides[0].frame.get_size()[0] * scale,
        self._locations.get(name)[0]._current_slides[0].frame.get_size()[1] * scale,
    )
    app.run()

  def _calculate_parallax_speed(self, foreground_speed: float, layer_index: int) -> float:
      return ((self._horizon_distance - layer_index * self._spacing) * foreground_speed) / self._horizon_distance

  def select_location(self, location_name: str) -> None:
    loc = self._locations.get(location_name)
    if loc is None:
      raise NoSuchLocationError(location_name)

    self._current_slides = loc
    self._surface = pygame.Surface(pygame.display.get_window_size(), pygame.SRCALPHA, 32)

  def update(self, speed: int) -> pygame.Surface | None:
    for index, engine in enumerate(self._current_slides):
      parallax_speed = self._calculate_parallax_speed(speed, -index)
      layer = engine.update(parallax_speed)

      self._surface.blit(layer, (0, (self._surface.get_height() / 3) - layer.get_height())) # temp

    return self._surface
