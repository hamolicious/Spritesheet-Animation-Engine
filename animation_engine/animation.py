from typing import Generator, Callable
import pygame
from .timer import Timer


class Animation:
	def __init__(self, fps: int, frames: list[pygame.Surface], name: str, indices: list[int], one_shot:bool=False) -> None:
		self._name = name
		self._one_shot = one_shot
		self._frames = [frames[i] for i in indices]
		self.get_frame: Callable[[None], pygame.Surface | None] = self._one_shot_get_frame if self._one_shot else self._get_repeating_frame
		self._played = False

		if self._one_shot:
			self._frames = self._list_to_generator(frames)

		self._fps = fps
		self._frame_timer = Timer(1 / fps)
		self._frame_index = 0

	def finished(self) -> bool:
		return self._played

	def reset(self) -> None:
		self._played = False

	def _list_to_generator(self, frames: [list[pygame.Surface]]) -> Generator:
		for frame in frames:
			yield frame

	def _one_shot_get_frame(self) -> pygame.Surface | None:
		if self._played:
			return None

		try:
			frame = next(self._frames)
			return frame
		except StopIteration:
			self._played = True
			return None

	def _get_repeating_frame(self) -> pygame.Surface:
		if self._frame_timer.is_ready(one_shot=self._one_shot):
			self._frame_index += 1
			if self._frame_index == len(self._frames):
				self._frame_index = 0
		return self._frames[self._frame_index]

