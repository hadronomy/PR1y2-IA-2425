class AlgorithmHistory:
    """
    Algorithm history class
    """

    def __init__(self):
        self.history = []

    def add_step(self, step: dict) -> None:
        """
        Add a step to the history
        """
        self.history.append(step)

    def get_history(self) -> list[dict]:
        """
        Get the history
        """
        return self.history

    def __str__(self) -> str:
        return str(self.history)

    def __iter__(self):
        return iter(self.history)
