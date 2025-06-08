import pytest
from game.engine import generate_crash_point


def test_generate_crash_point_deterministic():
    result = generate_crash_point('server', 'client')
    assert result == 1.72
    assert result >= 1.01
