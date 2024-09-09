![build](https://github.com/Chaste/cppwg/actions/workflows/build-and-test.yml/badge.svg)

# cppwg

Automatically generate PyBind11 Python wrapper code for C++ projects.

## Installation
Clone the repository and install cppwg:

```bash
git clone https://github.com/Chaste/cppwg.git
cd cppwg
pip install .
```

## Usage

This project generates PyBind11 wrapper code, saving lots of boilerplate in
bigger projects. Please see the [PyBind11 documentation](https://pybind11.readthedocs.io/en/stable/)
for help on the generated wrapper code. 

### First Example

The `examples/shapes/` directory is a full example project, demonstrating how to
generate a Python package `pyshapes` from C++ source code. It is recommended
that you use it as a template project when getting started.

As a small example, we can start with a free function in
`examples/shapes/src/math_funcs/SimpleMathFunctions.hpp`:

```c++
#ifndef _SIMPLEMATHFUNCTIONS_HPP
#define _SIMPLEMATHFUNCTIONS_HPP

/**
 * Add the two input numbers and return the result
 * @param i the first number
 * @param j the second number
 * @return the sum of the numbers
 */
int add(int i, int j)
{
    return i + j;
}

#endif  // _SIMPLEMATHFUNCTIONS_HPP
```

Add a package description to `examples/shapes/wrapper/package_info.yaml`:

```yaml
name: pyshapes
modules:
- name: math_funcs
  free_functions: CPPWG_ALL
```

Generate the wrappers with:

```bash
cd examples/shapes
cppwg src/ \
  --wrapper_root wrapper/ \
  --package_info wrapper/package_info.yaml \
  --includes src/math_funcs/
```

The following PyBind11 wrapper code will be output to
`examples/shapes/wrapper/math_funcs/math_funcs.main.cpp`:

```c++
#include <pybind11/pybind11.h>
#include "wrapper_header_collection.hpp"

namespace py = pybind11;

PYBIND11_MODULE(_pyshapes_math_funcs, m)
{
    m.def("add", &add, "");
}
```

The wrapper code can be built into a Python module and used as follows:

```python
from pyshapes import math_funcs
a = 4
b = 5
c = math_funcs.add(4, 5)
print c
>>> 9
```

### Full Example

To generate Pybind11 wrappers for all the C++ code in `examples/shapes`:

```bash
cd examples/shapes
cppwg src/ \
  --wrapper_root wrapper/ \
  --package_info wrapper/package_info.yaml \
  --includes src/geometry/ src/math_funcs/ src/mesh/ src/primitives extern/meshgen
```

To build the example `pyshapes` package:

```bash
mkdir build
cd build
cmake ..
make
```

## Starting a New Project
* Make a wrapper directory in your source tree e.g. `mkdir wrappers`
* Copy the template in `examples/shapes/wrapper/generate.py` to the wrapper directory and fill it in as appropriate.
* Copy the template in `examples/shapes/wrapper/package_info.yaml` to the wrapper directory and fill it in as appropriate.
* Run `cppwg` with appropriate arguments to generate the PyBind11 wrapper code in the wrapper directory.
* Follow the [PyBind11 guide](https://pybind11.readthedocs.io/en/stable/compiling.html) for building with CMake, using `examples/shapes/CMakeLists.txt` as an initial guide.
