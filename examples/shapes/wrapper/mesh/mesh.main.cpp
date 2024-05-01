#include <pybind11/pybind11.h>
#include "wrapper_header_collection.hpp"
#include "Mesh2_2.cppwg.hpp"
#include "Mesh3_3.cppwg.hpp"

namespace py = pybind11;

PYBIND11_MODULE(_pyshapes_mesh, m)
{
    register_Mesh2_2_class(m);
    register_Mesh3_3_class(m);
}
