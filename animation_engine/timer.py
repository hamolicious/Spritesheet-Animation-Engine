import time


class Timer:
	def __init__(self, interval_seconds: float) -> None:
		self._interval_seconds = interval_seconds
		self._next_exec = None

		self.reset()

	def reset(self) -> None:
		self._next_exec = time.time() + self._interval_seconds

	def is_ready(self, one_shot:bool=False) -> bool:
		if time.time() > self._next_exec:
			if not one_shot:
				self.reset()
			return True
		return False
