"""Tests for EchoLM."""

import subprocess
import sys

import pytest

from echolm import EchoLM


class TestEchoLM:
    def setup_method(self):
        self.model = EchoLM()

    def test_returns_exact_input(self):
        prompt = "Hello, world!"
        assert self.model.generate(prompt) == prompt

    def test_empty_string(self):
        assert self.model.generate("") == ""

    def test_whitespace_preserved(self):
        prompt = "  spaces   and\ttabs\n"
        assert self.model.generate(prompt) == prompt

    def test_multiline(self):
        prompt = "line one\nline two\nline three"
        assert self.model.generate(prompt) == prompt

    def test_unicode(self):
        prompt = "日本語テスト 🎉"
        assert self.model.generate(prompt) == prompt

    def test_no_hallucination(self):
        prompt = "the sky is green"
        assert self.model.generate(prompt) == "the sky is green"

    def test_numbers(self):
        prompt = "42 3.14 -7"
        assert self.model.generate(prompt) == prompt

    def test_special_characters(self):
        prompt = "!@#$%^&*()_+-=[]{}|;':\",./<>?"
        assert self.model.generate(prompt) == prompt

    @pytest.mark.parametrize("prompt", [
        "short",
        "a slightly longer prompt for the model",
        "x" * 10000,
    ])
    def test_various_lengths(self, prompt):
        assert self.model.generate(prompt) == prompt


class TestCLI:
    def _run(self, *args):
        return subprocess.run(
            [sys.executable, "-m", "echolm.cli", *args],
            capture_output=True,
            text=True,
        )

    def test_cli_echoes_single_arg(self):
        result = self._run("hello")
        assert result.returncode == 0
        assert result.stdout.strip() == "hello"

    def test_cli_echoes_multiple_args(self):
        result = self._run("hello", "world")
        assert result.returncode == 0
        assert result.stdout.strip() == "hello world"

    def test_cli_no_args_exits_nonzero(self):
        result = self._run()
        assert result.returncode != 0
