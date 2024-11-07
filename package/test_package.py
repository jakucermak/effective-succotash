import pytest
from package.utils import PackageResult, PackageVersion, PackageComparator

def test_package_name():
    input_string = "CardManager-0:3-31.fc41.src"
    package_version = PackageVersion.from_string(input_string)

    exp_name = "CardManager"
    act_name = package_version.name

    assert exp_name == act_name

def test_package_name_xorg():
    input_string = "xorg-x11-server-0:21.1.13-5.fc41.src"
    package_version = PackageVersion.from_string(input_string)

    exp_name = "xorg-x11-server"
    act_name = package_version.name

    assert exp_name == act_name

def test_package_ver_simple():
    input_string = "CardManager-0:3-31.fc41.src"
    package_version = PackageVersion.from_string(input_string)

    exp_maj = '3'
    exp_minor = None
    exp_rev = '31'
    exp_ver_str = "0:3-31.fc41.src"

    assert exp_maj == package_version.major
    assert exp_minor == package_version.minor
    assert exp_rev == package_version.rev
    assert exp_ver_str == package_version.version_string

def test_package_ver_xorg():
    input_string = "xorg-x11-server-0:21.1.13-5.fc41.src"
    package_version = PackageVersion.from_string(input_string)

    exp_maj = '21'
    exp_minor = '1'
    exp_patch = '13'
    exp_rev = '5'
    exp_ver_str = "0:21.1.13-5.fc41.src"

    assert exp_maj == package_version.major
    assert exp_minor == package_version.minor
    assert exp_rev == package_version.rev
    assert exp_ver_str == package_version.version_string

def test_eq_comparsion():
    input_string = "xorg-x11-server-0:21.1.13-5.fc41.src"
    package_version = PackageVersion.from_string(input_string)

    assert package_version == package_version

def test_non_eq_comparsion():

    input_string = "xorg-x11-server-0:21.1.13-4.fc41.src"
    package_version = PackageVersion.from_string(input_string)

    input_string_2 = "xorg-x11-server-0:21.1.13-5.fc41.src"
    package_2_version = PackageVersion.from_string(input_string_2)

    assert package_version != package_2_version

def test_newer_comparsion():
    # TODO: Rename variables
    input_string = "xorg-x11-server-0:21.2.13-5.fc41.src"
    package_version = PackageVersion.from_string(input_string)

    input_string_l = "xorg-x11-server-0:21.1.13-6.fc41.src"
    package_l_version = PackageVersion.from_string(input_string_l)

    assert package_l_version < package_version

def test_newer_with_less_subversions():
    h_input_string = "CardManager-0:3-31.fc41.src"
    h_package_version = PackageVersion.from_string(h_input_string)

    l_input_string = "CardManager-0:3-30.fc41.src"
    l_package_version = PackageVersion.from_string(l_input_string)

    assert l_package_version < h_package_version

def test_compare_package():
    older_build = [
        PackageVersion.from_string("CardManager-0:3-30.fc41.src"),
        PackageVersion.from_string("xorg-x11-server-0:21.1.13-6.fc41.src"),
        PackageVersion.from_string("0xFFFF-0:0.10-8.fc41.src") # Removed
    ]

    newer_build = [
        PackageVersion.from_string("CardManager-0:3-31.fc41.src"), # Changed
        PackageVersion.from_string("xorg-x11-server-0:21.2.13-5.fc41.src"), # Changed
        PackageVersion.from_string("0ad-0:0.0.26-22.fc41.src") # Added
    ]

    assert PackageComparator.compare(older_build[0],newer_build[0]) == PackageResult.CHANGED
    assert PackageComparator.compare(older_build[1],newer_build[1]) == PackageResult.CHANGED
    assert PackageComparator.compare(older_build[2], None) == PackageResult.REMOVED
    assert PackageComparator.compare(None, newer_build[2]) == PackageResult.ADDED

def test_out():
    older_build = [
        PackageVersion.from_string("CardManager-0:3-30.fc41.src"),
        PackageVersion.from_string("xorg-x11-server-0:21.1.13-6.fc41.src"),
        PackageVersion.from_string("0xFFFF-0:0.10-8.fc41.src") # Removed
    ]

    newer_build = [
        PackageVersion.from_string("CardManager-0:3-30.fc41.src"), # NOT-Changed
        PackageVersion.from_string("xorg-x11-server-0:21.2.13-5.fc41.src"), # Changed
        PackageVersion.from_string("0ad-0:0.0.26-22.fc41.src") # Added
    ]

    pkg_added = PackageComparator(new=newer_build[2]).out()[0]
    pkg_removed = PackageComparator(old=older_build[2]).out()[0]
    pkg_changed = PackageComparator(old=older_build[1], new=newer_build[1]).out()[0]
    pkg_n_changed = PackageComparator(old=older_build[0], new=newer_build[0]).out()[0]

    assert "0ad ADDED (0:0.0.26-22.fc41.src)" == pkg_added
    assert "0xFFFF REMOVED (0:0.10-8.fc41.src)" == pkg_removed
    assert "xorg-x11-server CHANGED (0:21.1.13-6.fc41.src -> 0:21.2.13-5.fc41.src)" == pkg_changed
    assert "CardManager NOT_CHANGED (0:3-30.fc41.src)" == pkg_n_changed
