import pygame


class Pane:
	def __init__(self, frame: pygame.Surface, pos: list[int], direction: tuple[int]) -> None:
		self.frame: pygame.Surface = frame
		self.pos: list[int] = pos
		self.direction: tuple[int] = direction

	def move(self, speed: float) -> None:
		self.pos = [
			self.pos[0] + (speed * self.direction[0]),
			self.pos[1] + (speed * self.direction[1]),
		]

