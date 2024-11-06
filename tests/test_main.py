import pytest
from main import Architecture, parse_architecture, UnknownArchitetureError

class TestArchitecture():
    def test_valid_arch(self):
        input_string = "x86_64"
        expectedArch = Architecture.X86_64
        result = parse_architecture(input_string)

        assert expectedArch == result

    def test_non_valid_arch(self):
        input_str = "arch64"
        with pytest.raises(UnknownArchitetureError):
            result = parse_architecture(input_str)
