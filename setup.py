import os
import time
from pathlib import Path
from distutils.core import setup


from setuptools import find_packages

_version = "0.1.%sdev" % int(time.time())
_packages = find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"])


def _list_assets():
    return [str(x) for x in Path("./assets").rglob("*")]


_reqs_dir = os.path.join(os.path.dirname(__file__), "requirements")


def _strip_comments(line):
    return line.split("#", 1)[0].strip()


def _get_reqs(req):
    with open(os.path.join(_reqs_dir, req)) as f:
        requires = f.readlines()
        requires = map(_strip_comments, requires)
        requires = filter(lambda x: x.strip() != "", requires)
        return list(requires)


_install_requires = _get_reqs("requirements.txt")

_data_files = [("", _list_assets() + ["requirements/%s" % reqs_file for reqs_file in os.listdir(_reqs_dir)])]


with open("/tmp/lala", "w") as f:
    f.write(str(_data_files))

setup(
    name="pyrats",
    version=_version,
    packages=_packages,
    data_files=_data_files,
    install_requires=_install_requires,
    entry_points={"console_scripts": ["pyrats = pyrats.run:main",]},
)
