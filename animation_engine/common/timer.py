import time


class Timer:
  def __init__(self, interval_seconds: float) -> None:
    self._interval_seconds = interval_seconds
    self._last_exec = 0

  def is_ready(self) -> bool:
    if time.time() - self._last_exec >= self._interval_seconds:
      self._last_exec = time.time()
      return True

    return False
