// This file is automatically generated by cppwg.
// Do not modify this file directly.

#include <pybind11/pybind11.h>
#include "wrapper_header_collection.cppwg.hpp"
#include "AbstractMesh_2_2.cppwg.hpp"
#include "AbstractMesh_3_3.cppwg.hpp"
#include "ConcreteMesh_2.cppwg.hpp"
#include "ConcreteMesh_3.cppwg.hpp"

namespace py = pybind11;

PYBIND11_MODULE(_pyshapes_mesh, m)
{
    register_AbstractMesh_2_2_class(m);
    register_AbstractMesh_3_3_class(m);
    register_ConcreteMesh_2_class(m);
    register_ConcreteMesh_3_class(m);
}