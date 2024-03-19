# cppwg

Automatically generate PyBind11 code for C++ projects.

## Example

`cppwg/shapes/` is a full example project, demonstrating how to generate a Python package `pyshapes` from 
C++ source code. It is recommended that you use it as a template project when getting started.

As a small example, we can start with a free function in `cppwg/shapes/src/math_funcs/SimpleMathFunctions.hpp`:
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

add a package description to `cppwg/shapes/wrapper/package_info.yaml`:

```yaml
name: pyshapes
modules:
- name: math_funcs
  free_functions: cppwg_ALL
```

and do `python cppwg/shapes/wrapper/generate.py` (with some suitable arguments).

The generator will make the following PyBind11 wrapper code in `cppwg/shapes/wrapper/math_funcs/math_funcs.main.cpp`:
```c++
#include <pybind11/pybind11.h>
#include "wrapper_header_collection.hpp"

namespace py = pybind11;

PYBIND11_MODULE(_pyshapes_math_funcs, m)
{
    m.def("add", &add, "");
}
```

which can be built into a Python module and (with some import tidying) used as follows:
```python
from pyshapes import math_funcs
a = 4
b = 5
c = math_funcs.add(4, 5)
print c
>>> 9
```

## Usage
It is recommended that you [learn how to use PyBind11 first](https://pybind11.readthedocs.io/en/stable/). This project 
generates PyBind11 wrapper code, saving lots of boilerplate in bigger projects.

### Dependencies
Developed and tested with Python 3.8 - 3.12 on Ubuntu 22.04.

* [CastXML](https://github.com/CastXML/CastXML)
* [pygccxml](https://github.com/CastXML/pygccxml)
* [pyyaml](https://github.com/yaml/pyyaml)

You can install the dependencies with `pip install pyyaml pygccxml castxml`

### Test the Installation
To generate the full `pyshapes` wrapper do:

```bash
git clone https://github.com/Chaste/cppwg.git
python cppwg/shapes/wrapper/generate.py \
  --source_root cppwg/shapes/src/ \
  --wrapper_root cppwg/shapes/wrapper/ \
  --castxml_binary path/to/bin/castxml \
  --package_info cppwg/shapes/wrapper/package_info.yaml \
  --includes cppwg/shapes/src/
```

then to build the example package do:

```bash
mkdir cppwg/shapes/build
cd cppwg/shapes/build
cmake ..
make
```

To test the resulting package do:

```bash
python test_functions.py 
python test_classes.py 
```

### Starting a New Project
* Make a wrapper directory in your source tree e.g. `mkdir wrappers`
* Copy the template in `cppwg/shapes/wrapper/generate.py` to the wrapper directory and fill it in.
* Copy the template in `cppwg/shapes/wrapper/package_info.yaml` to the wrapper directory and fill it in.
* Do `python wrappers/generate.py` to generate the PyBind11 wrapper code in the wrapper directory.
* Follow the [PyBind11 guide](https://pybind11.readthedocs.io/en/stable/compiling.html) for building with CMake, using `cppwg/shapes/CMakeLists.txt` as an initial guide.
