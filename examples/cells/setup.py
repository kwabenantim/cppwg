from skbuild import setup

setup(
    name="pycells",
    version="0.0.1",
    description="pycells",
    author="kna",
    license="BSD-3-Clause",
    packages=["pycells"],
    package_dir={"": "src/py"},
    cmake_install_dir="src/py/pycells",
    python_requires=">=3.8",
)
