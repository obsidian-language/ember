import pytest
from utils import system_info

def test_system_info():
    sysname, machine = system_info()
    assert isinstance(sysname, str)
    assert isinstance(machine, str)
