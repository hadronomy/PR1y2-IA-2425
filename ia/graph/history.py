"""History class for the algorithms."""

from copy import deepcopy


class AlgorithmHistory:
    """Algorithm history class."""

    def __init__(self):
        """Initialize the history."""
        self.history = []

    def add_step(self, **kargs) -> None:
        """Add a step to the history."""
        self.history.append(deepcopy(kargs))

    def get_history(self) -> list[dict]:
        """Get the history."""
        return self.history

    def __str__(self) -> str:
        """Return the history as a string."""
        return str(self.history)

    def __iter__(self):
        """Iterate over the history."""
        return iter(self.history)
