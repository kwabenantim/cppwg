#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "wrapper_header_collection.hpp"

#include "ConcreteMesh3.cppwg.hpp"

namespace py = pybind11;
typedef ConcreteMesh<3 > ConcreteMesh3;
PYBIND11_DECLARE_HOLDER_TYPE(T, std::shared_ptr<T>);

class ConcreteMesh3_Overrides : public ConcreteMesh3{
    public:
    using ConcreteMesh3::ConcreteMesh;
    void Scale(double const factor) override {
        PYBIND11_OVERRIDE(
            void,
            ConcreteMesh3,
            Scale,
                    factor);
    }

};
void register_ConcreteMesh3_class(py::module &m){
py::class_<ConcreteMesh3 , ConcreteMesh3_Overrides , std::shared_ptr<ConcreteMesh3 >  , AbstractMesh<3>  >(m, "ConcreteMesh3")
        .def(py::init< >())
        .def(
            "Scale",
            (void(ConcreteMesh3::*)(double const)) &ConcreteMesh3::Scale,
            " " , py::arg("factor") )
    ;
}