import pygame
from ..test_app import BaseApp
from ..common.exceptions import NoSuchLocationError
from ..common.scroll_vector import ScrollVector
from ..common.pane import Pane


class AnimationEngine:
  def __init__(self) -> None:
    self._current_slides: tuple[Pane] = None
    self._locations: dict[str, tuple[Pane]] = {}

  def register_location(self, name: str, image: pygame.Surface, scroll_vector: ScrollVector = ScrollVector.LEFT) -> None:
    image_size = image.get_size()

    offset = (
      image_size[0] * -scroll_vector[0],
      image_size[1] * -scroll_vector[1],
    )

    self._locations[name] = (
      Pane(image, (0, 0), scroll_vector),
      Pane(image, offset, scroll_vector),
    )

  def preview_animation(self, name: str, scale: int = 5) -> None:
    class Preview(BaseApp):
      def setup(self_child) -> None:
        self_child.bg = AnimationEngine()
        frame = pygame.transform.scale(
          self._locations.get(name)[0].frame,
          (
            self._locations.get(name)[0].frame.get_size()[0] * scale,
            self._locations.get(name)[0].frame.get_size()[1] * scale,
          )
        )
        self_child.bg.register_location(name, frame, ScrollVector.LEFT)
        self_child.bg.select_location(name)

      def loop(self_child) -> None:
        if self_child.key_press[pygame.K_ESCAPE]:
          quit()

        self_child.screen.fill('black')
        bg = self_child.bg.update(0.5 * self_child.delta_time)
        self_child.screen.blit(bg, (0, 0))

    app = Preview()
    app.size = (
        self._locations.get(name)[0].frame.get_size()[0] * scale,
        self._locations.get(name)[0].frame.get_size()[1] * scale,
    )
    app.run()

  def select_location(self, location_name: str) -> None:
    loc = self._locations.get(location_name)
    if loc is None:
      raise NoSuchLocationError(location_name)

    self._current_slides = loc
    self._screen_size = loc[0].frame.get_size()
    self._surface = pygame.Surface(self._screen_size, pygame.SRCALPHA, 32)

  def update(self, speed: float) -> pygame.Surface | None:
    self._surface.fill((0, 0, 0, 0))

    for pane in self._current_slides:
      pane.move(speed)

      if (pane.pos[0] <= -pane.frame.get_size()[0] and pane.direction[0] == -1):
        pane.pos[0] += pane.frame.get_size()[0] * 2

      if (pane.pos[0] >= pane.frame.get_size()[0] and pane.direction[0] == 1):
        pane.pos[0] -= pane.frame.get_size()[0] * 2

      if (pane.pos[1] <= -pane.frame.get_size()[1] and pane.direction[1] == -1):
        pane.pos[1] += pane.frame.get_size()[1] * 2

      if (pane.pos[1] >= pane.frame.get_size()[1] and pane.direction[1] == 1):
        pane.pos[1] -= pane.frame.get_size()[1] * 2

      self._surface.blit(pane.frame, (
        int(pane.pos[0]),
        int(pane.pos[1]),
      ))

    return self._surface
