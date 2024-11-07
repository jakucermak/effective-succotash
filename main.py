import argparse
from enum import StrEnum
from typing import List, Dict
from compose.utils import Compose, ComposeSet
from package.utils import PackageComparator, PackageResult, PackageVersion
import ijson

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


def parse_json(file_path: str) -> Dict[str,PackageVersion]:
    result = {}
    with open(file_path, 'r') as f:
        for key, value in ijson.kvitems(f,"payload.rpms.Everything.{}".format(arch)):
            package = PackageVersion.from_string(key)
            result[package.name] = package

    return result

def main(arch, files: List[str]):
    out: List[str] = []
    older_build = parse_json(files[0])
    newer_build = parse_json(files[1])

    def compare_and_collect(package_dict_1, package_dict_2):
        for pkg_name in list(package_dict_1.keys()):
            comp = PackageComparator(
                new=package_dict_2.pop(pkg_name, None),
                old=package_dict_1.pop(pkg_name, None)
            ).out()
            if comp[1] != PackageResult.NOT_CHANGED:
                out.append(comp[0])

    compare_and_collect(older_build, newer_build)
    compare_and_collect(newer_build, older_build)

    return sorted(out)


def choose_composers(lst: List[Compose]) -> tuple[Compose,Compose]:
    print("Choose two different options from following list:")
    for index, item in enumerate(lst):
        print(f"{index + 1}. {item.build_name}")

    old = int(input("Choose number for old composer: ")) - 1

    new = int(input("Choose number for new composer: ")) - 1

    if old < 0 or old >= len(lst) or new < 0 or new >= len(lst):
        print("Invalid option, try again")
        return choose_composers(lst)
    elif old == new:
        print("Not able to choose same item twice, try again with different number.")
        return choose_composers(lst)

    return lst[old], lst[new]

parser = argparse.ArgumentParser(prog="RedHatAplicationTask", description="Diff versions of packages in two compose files for specific architecture.")
parser.add_argument('-a', "--architecture", required=True, help="Provide architecture for lookup.")
parser.add_argument('-f', "--files", help="Provide files that you want to compare and do not download", nargs=2)

if __name__ == "__main__":
    args = parser.parse_args()
    arch = parse_architecture(args.architecture)
    files: List[str] = []
    if not args.files:
        builds = ComposeSet.fetch()
        selection = choose_composers(builds.available_composes)
        files = builds.download([selection[0], selection[1]])
    else:
        files = args.files

    for pkg in main(arch,files): print(pkg)
