import os
import sys
import re
import click
import snakypy
import tomlkit
from eqversion import __version__


class EQVersion:
    def __init__(self, root):
        self.root = root
        self.pyproject = os.path.join(self.root, "pyproject.toml")

    def version_name_pyproject(self):
        if not os.path.isfile(self.pyproject):
            print(">>> Directory not supported by EQVersion. Aborted.")
            sys.exit(1)
        try:
            r_file = snakypy.file.read(self.pyproject)
            parsed = tomlkit.parse(r_file)["tool"]["poetry"]
            return parsed["version"], parsed["name"].replace("-", "_")
        except Exception:
            raise Exception(
                ">>> An error occurred while reading the version of pyproject.toml"
            )

    def read_init(self, package):
        init_file = os.path.join(self.root, package, "__init__.py")
        if os.path.isdir(os.path.join(self.root, package)) and os.path.isfile(
            init_file
        ):
            file_content = snakypy.file.read(init_file)
            m = re.search(r"__version__ = .*", file_content)
            if m is not None:
                line_version = m.group(0)
                lst = line_version.split("=")
                version = [s.replace('"', "").replace("'", "").strip() for s in lst][1]
                return version, line_version, file_content
            return
        return

    def match(self, package):
        init_file = os.path.join(self.root, package, "__init__.py")
        if not self.read_init(package) or not self.version_name_pyproject():
            print(">>> Directory not supported by EQVersion. Aborted.")
            sys.exit(1)
        else:
            line_version = self.read_init(package)[1]
            new_line_version = f'__version__ = "{self.version_name_pyproject()[0]}"'
            new_init_file = re.sub(
                rf"{line_version}",
                new_line_version,
                self.read_init(package)[2],
                flags=re.M,
            )
            if self.read_init(package)[0] != self.version_name_pyproject()[0]:
                print(
                    f"File: {package}/__init__.py: "
                    f"{self.read_init(package)[0]} >> "
                    f"{self.version_name_pyproject()[0]}"
                )
                snakypy.file.create(new_init_file, init_file, force=True)
            else:
                print(">>> All the same!")
            return True
        return


def print_version(ctx, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(f"Version {__version__}")
    ctx.exit()


@click.command()
@click.option("--package", help="Receives the name of the main package.")
@click.option(
    "--version",
    is_flag=True,
    callback=print_version,
    expose_value=False,
    is_eager=True,
    help="Show the current version.",
)
def main(package):
    """EQversion maintains the same versions of pyproject.toml and
    __init__.py (from the main package) of projects using Poetry."""
    root = os.getcwd()
    eqversion = EQVersion(root)
    if package is not None:
        eqversion.match(package)
    else:
        eqversion.match(eqversion.version_name_pyproject()[1])
