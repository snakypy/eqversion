import os
import re
import argparse
import snakypy
import tomlkit


class EQVersion:
    def __init__(self, root, package, tool):
        self.root = root
        self.package = package
        self.tool = tool
        self.init_file = os.path.join(self.root, self.package, "__init__.py")
        self.pyproject = os.path.join(self.root, "pyproject.toml")

    def version_pyproject(self):
        if os.path.isfile(self.pyproject):
            r_file = snakypy.file.read(self.pyproject)
            parsed = tomlkit.parse(r_file)["tool"][self.tool]
            return parsed["version"]
        return

    def read_init(self):
        if os.path.isdir(os.path.join(self.root, self.package)) and os.path.isfile(
            self.init_file
        ):
            file_content = snakypy.file.read(self.init_file)
            m = re.search(r"__version__ = .*", file_content)
            if m is not None:
                line_version = m.group(0)
                lst = line_version.split("=")
                version = [s.replace('"', "").replace("'", "").strip() for s in lst][1]
                return version, line_version, file_content
            return
        return

    def match(self):
        if self.read_init() and self.version_pyproject():
            line_version = self.read_init()[1]
            new_line_version = f'__version__ = "{self.version_pyproject()}"'
            new_init_file = re.sub(
                rf"{line_version}", new_line_version, self.read_init()[2], flags=re.M
            )
            if self.read_init()[0] != self.version_pyproject():
                print(
                    f"File: {self.package}/__init__.py: "
                    f"{self.read_init()[0]} >> {self.version_pyproject()}"
                )
                snakypy.file.create(new_init_file, self.init_file, force=True)
            else:
                print("All the same!")
            return True
        return


def options():
    parser = argparse.ArgumentParser(
        description="EQversion keeps the versions of pyproject.toml and __init__.py\
                     the same."
    )
    parser.add_argument(
        "package", metavar="PACKAGE", type=str, help="Name of the main package."
    )
    args = parser.parse_args()
    return args


def main():
    EQVersion(os.getcwd(), options().package, "poetry").match()
