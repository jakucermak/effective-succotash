from enum import Enum

class PackageVersion():

    def __init__(self, name, version_string, major, minor,patch, rev):
        self.version_string = version_string
        self.name = name
        self.major = major
        self.minor = minor
        self.rev = rev
        self.patch = patch

    @classmethod
    def from_string(cls, version_string: str):

        parts = version_string.rsplit("-", 2)
        version_part = parts[1]
        rev = int(parts[2].split(".")[0])
        name = parts[0]

        prefix, version = version_part.split(":")
        version_nums = list(map(int,version.split(".")))
        major = version_nums[0]
        minor = version_nums[1] if len(version_nums) > 1 else None
        patch = version_nums[2] if len(version_nums) > 2 else None

        return cls(name=name, major=major, minor=minor, patch=patch, version_string="-".join(parts[1:]), rev=rev)

    def __eq__(self, value) -> bool:
        if self.major == value.major:
            if self.minor == value.minor:
                if self.patch == value.patch:
                    if self.rev == value.rev:
                        return True

        return False

    def __lt__(self, value) -> bool:

      self_minor = self.minor if self.minor is not None else 0
      self_patch = self.patch if self.patch is not None else 0
      value_minor = value.minor if value.minor is not None else 0
      value_patch = value.patch if value.patch is not None else 0

      if self.major < value.major:
          return True
      elif self.major == value.major:
          if self_minor < value_minor:
              return True
          elif self_minor == value_minor:
              if self_patch < value_patch:
                  return True
              elif self_patch == value_patch:
                  if self.rev < value.rev:
                      return True
      return False

class PackageResult(Enum):
    ADDED = 0
    REMOVED = 1
    CHANGED = 2


class CouldNotCompareError(Exception):
    def __init__(self, o_pkg, n_pkg):
        super().__init__("Cound not compare {} and {}.".format(o_pkg.name, n_pkg.name))

class PackageComparator:
    def __init__(self, old: PackageVersion | None = None, new: PackageVersion | None = None):
        self.o_pkg = old
        self.n_pkg = new

    @classmethod
    def compare(cls, o_pkg: PackageVersion | None, n_pkg: PackageVersion | None ) -> PackageResult:

        if o_pkg is None and n_pkg is not None:
            return PackageResult.ADDED
        if o_pkg is not None and n_pkg is None:
            return PackageResult.REMOVED
        if o_pkg != n_pkg:
            return PackageResult.CHANGED

        raise CouldNotCompareError(o_pkg,n_pkg)

    def out(self) -> str:

        result = PackageComparator.compare(self.o_pkg,self.n_pkg)

        match result:
            case PackageResult.ADDED:
                if self.n_pkg:
                    return "{} {} ({})".format(self.n_pkg.name, result.name, self.n_pkg.version_string)
            case PackageResult.REMOVED:
                if self.o_pkg:
                    return "{} {} ({})".format(self.o_pkg.name, result.name, self.o_pkg.version_string)
            case PackageResult.CHANGED:
                if self.o_pkg and self.n_pkg:
                    return "{} {} ({} -> {})".format(self.n_pkg.name, result.name, self.o_pkg.version_string, self.n_pkg.version_string)

        raise Exception("Could not process output.")
