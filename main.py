import argparse
from enum import StrEnum
from typing import List

class UnknownArchitetureError(Exception):
    """
    Error for unknown architecture.
    """
    def __init__(self, arch: str):
        super().__init__("Unknown architecture '{}'. Please use valid arch.".format(arch))

class Architecture(StrEnum):
    """
    Enumeration of available architectures
    """
    X86_64 = "x86_64"
    AARCH64 = "aarch64"
    PPC64LE = "ppc64le"
    S390X = "s390x"

def parse_architecture(arch: str) -> Architecture:
    """
    Parses a string representation of an architecture and returns the corresponding `Architecture` enum.

    Parameters
    ----------
    arch : str
    String identifier for the architecture, expected to match one of the defined architecture values.

    Returns
    -------
    Architecture
    The `Architecture` enum that matches the provided `arch` string.

    Raises
    ------
    UnknownArchitectureError
    If the `arch` string does not match any known architecture values.
    """
    match arch:
        case Architecture.X86_64.value:
            return Architecture.X86_64
        case Architecture.AARCH64.value:
            return Architecture.AARCH64
        case _:
            raise UnknownArchitetureError(arch)

def main(arch, files: List[str]):
    pass
parser = argparse.ArgumentParser(prog="RedHatAplicationTask", description="Diff versions of packages in two compose files for specific architecture.")
parser.add_argument('-a', "--architecture", required=True, help="Provide architecture for lookup.")
parser.add_argument('-f', "--files", nargs=2, help="Provide file paths for version compasion.")
if __name__ == "__main__":
    args = parser.parse_args()
    arch = parse_architecture(args.architecture)
    files = args.files
    main(arch, files)
