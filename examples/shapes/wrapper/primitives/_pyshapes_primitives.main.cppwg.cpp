// This file is automatically generated by cppwg.
// Do not modify this file directly.

#include <pybind11/pybind11.h>
#include "wrapper_header_collection.cppwg.hpp"
#include "Shape_2.cppwg.hpp"
#include "Shape_3.cppwg.hpp"
#include "Rectangle.cppwg.hpp"
#include "Cuboid.cppwg.hpp"

namespace py = pybind11;

PYBIND11_MODULE(_pyshapes_primitives, m)
{
    register_Shape_2_class(m);
    register_Shape_3_class(m);
    register_Rectangle_class(m);
    register_Cuboid_class(m);
}
