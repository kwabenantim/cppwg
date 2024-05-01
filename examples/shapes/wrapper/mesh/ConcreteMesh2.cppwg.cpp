#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "wrapper_header_collection.hpp"

#include "ConcreteMesh2.cppwg.hpp"

namespace py = pybind11;
typedef ConcreteMesh<2 > ConcreteMesh2;
PYBIND11_DECLARE_HOLDER_TYPE(T, std::shared_ptr<T>);

class ConcreteMesh2_Overrides : public ConcreteMesh2{
    public:
    using ConcreteMesh2::ConcreteMesh;
    void Scale(double const factor) override {
        PYBIND11_OVERRIDE(
            void,
            ConcreteMesh2,
            Scale,
                    factor);
    }

};
void register_ConcreteMesh2_class(py::module &m){
py::class_<ConcreteMesh2 , ConcreteMesh2_Overrides , std::shared_ptr<ConcreteMesh2 >  , AbstractMesh<2>  >(m, "ConcreteMesh2")
        .def(py::init< >())
        .def(
            "Scale",
            (void(ConcreteMesh2::*)(double const)) &ConcreteMesh2::Scale,
            " " , py::arg("factor") )
    ;
}
