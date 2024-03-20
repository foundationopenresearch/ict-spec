"""Test SemVer Object."""

import pytest
from pydantic import ValidationError

from ict.semver import Version

G = [
    "1.2.3",
    "1.4.7-rc1",
    "4.1.5",
    "12.8.3",
    "10.2.0",
    "2.2.3-dev5",
    "0.3.4",
    "0.2.34-rc23",
]
B = ["02.2.3", "002.2.3", "1.2", "1.0", "1.03.2", "23.3.03", "d.2.4"]


@pytest.mark.parametrize("ver", G, ids=G)
def test_version(ver):
    """Test Version pydantic model."""
    Version(ver)


@pytest.mark.parametrize("ver", B, ids=B)
def test_bad_version1(ver):
    """Test ValidationError is raised for invalid versions."""
    with pytest.raises(ValidationError):
        Version(ver)


mj = ["2.4.3", "2.98.28", "2.1.2", "2.0.0", "2.4.0"]
mn = ["1.3.3", "7.3.4", "98.3.12", "23.3.0", "1.3.5"]
pt = ["12.2.7", "2.3.7", "1.7.7", "7.7.7", "7.29.7"]


@pytest.mark.parametrize("ver", mj, ids=mj)
def test_major(ver):
    """Test major version."""
    assert Version(ver).major == "2"


@pytest.mark.parametrize("ver", mn, ids=mn)
def test_minor(ver):
    """Test minor version."""
    assert Version(ver).minor == "3"


@pytest.mark.parametrize("ver", pt, ids=pt)
def test_patch(ver):
    """Test patch version."""
    assert Version(ver).patch == "7"


def test_gt1():
    """Test greater than operator."""
    assert Version("1.2.3") > Version("1.2.1")


def test_gt2():
    """Test greater than operator."""
    assert Version("5.7.3") > Version("5.6.3")


def test_st1():
    """Test less than operator."""
    assert Version("5.7.3") < Version("5.7.31")


def test_st2():
    """Test less than operator."""
    assert Version("1.0.2") < Version("2.0.2")


def test_eq1():
    """Test equality operator."""
    assert Version("1.3.3") == Version("1.3.3")


def test_eq2():
    """Test equality operator."""
    assert Version("5.4.3") == Version("5.4.3")


def test_eq3():
    """Test equality operator."""
    assert Version("1.3.3") != Version("1.3.8")
