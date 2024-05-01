#include <pybind11/pybind11.h>
#include "wrapper_header_collection.hpp"
#include "AbstractMesh2_2.cppwg.hpp"
#include "AbstractMesh3_3.cppwg.hpp"
#include "ConcreteMesh2.cppwg.hpp"
#include "ConcreteMesh3.cppwg.hpp"

namespace py = pybind11;

PYBIND11_MODULE(_pyshapes_mesh, m)
{
    register_AbstractMesh2_2_class(m);
    register_AbstractMesh3_3_class(m);
    register_ConcreteMesh2_class(m);
    register_ConcreteMesh3_class(m);
}
