"""Core EchoLM model: f(x) = x."""


class EchoLM:
    """A language model that returns exactly what you give it.

    It does not reason.
    It does not summarize.
    It does not refuse.
    It does not autocomplete.
    It simply returns exactly what you give it.

    f(x) = x
    """

    def generate(self, prompt: str) -> str:
        """Return *prompt* unchanged.

        Parameters
        ----------
        prompt:
            The input text.

        Returns
        -------
        str
            Exactly *prompt*, unmodified.
        """
        return prompt
