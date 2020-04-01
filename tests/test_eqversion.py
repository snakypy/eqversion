import pytest
import tomlkit
import snakypy
import subprocess
from os.path import join
from eqversion.eqversion import EQVersion


@pytest.fixture
def base(tmpdir):
    root = tmpdir.mkdir("base")
    project_name = "project"
    subprocess.call(f"poetry new {join(root, project_name)} -q", shell=True)
    return {"root": join(root, project_name), "package": project_name}


def class_eqversion(base):
    inst = EQVersion(base["root"])
    return inst


def test_eqversion(base):
    assert class_eqversion(base).version_name_pyproject()[0] == "0.1.0"
    assert class_eqversion(base).read_init(base["package"])[0] == "0.1.0"
    file_r = snakypy.file.read(class_eqversion(base).pyproject)
    toml_parsed = tomlkit.parse(file_r)
    toml_parsed["tool"]["poetry"]["version"] = "0.1.1"
    dumps = tomlkit.dumps(toml_parsed)
    snakypy.file.create(dumps, class_eqversion(base).pyproject, force=True)
    assert class_eqversion(base).version_name_pyproject()[0] == "0.1.1"
    class_eqversion(base).match(base["package"])
    assert class_eqversion(base).read_init(base["package"])[0] == "0.1.1"
