import time


class Timer:
  def __init__(self, interval_seconds: float) -> None:
    self._interval_seconds = interval_seconds
    self._next_exec = None

    self.reset()

  def reset(self) -> None:
    self._next_exec = time.time() + self._interval_seconds

  def is_ready(self) -> bool:
    if time.time() > self._next_exec:
      return True
    return False
