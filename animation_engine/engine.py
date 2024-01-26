import pygame
from .animation import Animation
from .test_app import BaseApp
from .exceptions import NoSuchAnimationError


class AnimationEngine:
  def __init__(self, frames: list[pygame.Surface]) -> None:
    self._frames = frames
    self._animations: dict[str, Animation] = {}
    self._current_animation: Animation = None

  def register_animation(self, fps: int, name: str, indices: list[int], one_shot: bool = False, invert: bool = False) -> None:
    self._animations[name] = Animation(fps, self._frames, name, indices, one_shot, invert)

  def preview_animation(self, *names: str, scale: int = 5, background_color: list[int] = None) -> None:
    if len(names) == 0:
      names = self._animations.keys()

    class Preview(BaseApp):
      def setup(self_child) -> None:
        self_child.animations = [self._animations.get(name) for name in names]
        if self_child.animations is None:
          raise NoSuchAnimationError(names)

      def loop(self_child) -> None:
        if self_child.key_press[pygame.K_ESCAPE]:
          quit()

        self_child.screen.fill(
          background_color if background_color is not None else [50, 50, 60]
        )

        for animation_index, animation in enumerate(self_child.animations):
          if animation.is_finished():
            animation.reset()

          frame = animation.get_frame()

          frame = pygame.transform.scale(frame, [
            frame.get_size()[0] * scale,
            frame.get_size()[1] * scale,
          ])
          self_child.screen.blit(frame, (frame.get_size()[0] * animation_index, 0))

    app = Preview()
    app.size = [
      (self._frames[0].get_size()[0] * scale) * len(names),
      self._frames[0].get_size()[1] * scale,
    ]
    app.run()

  def play(self, anim_name: str) -> None:
    anim = self._animations.get(anim_name)
    if anim is None:
      raise NoSuchAnimationError(anim_name)

    self._current_animation = anim

  def update(self) -> pygame.Surface | None:
    return self._current_animation.get_frame()
