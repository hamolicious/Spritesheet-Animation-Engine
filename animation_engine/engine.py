import pygame
from .animation import Animation
from .test_app import BaseApp
from .exceptions import NoSuchAnimationError


class AnimationEngine:
  def __init__(self, frames: list[pygame.Surface]) -> None:
    self._frames = frames
    self._animations: dict[str, Animation] = {}
    self._current_animation: Animation = None

  def register_animation(self, fps: int, name: str, indices: list[int], one_shot: bool = False) -> None:
    self._animations[name] = Animation(fps, self._frames, name, indices, one_shot)

  def preview_animation(self, name: str, scale: int = 5, background_color: list[int] = None) -> None:
    class Preview(BaseApp):
      def setup(self_child) -> None:
        self_child.anim = self._animations.get(name)
        if self_child.anim is None:
          raise NoSuchAnimationError(name)

      def loop(self_child) -> None:
        if self_child.key_press[pygame.K_ESCAPE]:
          quit()

        self_child.screen.fill(
          background_color if background_color is not None else [31, 31, 40]
        )

        frame = self_child.anim.get_frame()

        if self_child.anim.is_finished() and not self_child.anim.is_one_shot():
          print('reset')
          self_child.anim.reset()

        if self_child.anim.is_one_shot() and self_child.anim.is_finished() and self_child.key_press[pygame.K_SPACE]:
          self_child.anim.reset()

        frame = pygame.transform.scale(frame, [
          frame.get_size()[0] * scale,
          frame.get_size()[1] * scale,
        ])
        self_child.screen.blit(frame, (0, 0))

    app = Preview()
    app.size = [
      self._frames[0].get_size()[0] * scale,
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
