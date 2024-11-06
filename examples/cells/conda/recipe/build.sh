#!/bin/bash -ex

export CMAKE_PREFIX_PATH="$PREFIX;$CMAKE_PREFIX_PATH"
export PETSC_DIR="$PREFIX"
export PETSC_ARCH=
export VTK_DIR="$PREFIX"

$PYTHON -m pip install -v --no-build-isolation .
