#!/usr/bin/env python

import os
import sys
from unittest.mock import patch


# Добавление пути к модулю main
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Проверяем, установлен ли pytest
try:
    import pytest
except ImportError:
    print("pytest не установлен. Установите его с помощью команды: pip install pytest")
    sys.exit(1)

from main import parse_arguments


def test_parse_arguments_with_extensions():
    with patch(
        "sys.argv", ["main.py", "--pattern", "newfile", "--extension", ".txt", ".csv"]
    ):
        args = parse_arguments()
        assert args.pattern == "newfile"
        assert args.ext == [".txt", ".csv"]


def test_parse_arguments_without_extensions():
    with patch("sys.argv", ["main.py", "--pattern", "newfile"]):
        args = parse_arguments()
        assert args.pattern == "newfile"
        assert args.ext is None


def test_parse_arguments_missing_pattern():
    with patch("sys.argv", ["main.py"]):
        with pytest.raises(SystemExit):
            parse_arguments()


def test_parse_arguments_help():
    with patch("sys.argv", ["main.py", "--help"]):
        with pytest.raises(SystemExit):
            parse_arguments()
