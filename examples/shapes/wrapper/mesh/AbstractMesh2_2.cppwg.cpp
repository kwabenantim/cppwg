#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "wrapper_header_collection.hpp"

#include "AbstractMesh2_2.cppwg.hpp"

namespace py = pybind11;
typedef AbstractMesh<2,2 > AbstractMesh2_2;
PYBIND11_DECLARE_HOLDER_TYPE(T, std::shared_ptr<T>);

class AbstractMesh2_2_Overrides : public AbstractMesh2_2{
    public:
    using AbstractMesh2_2::AbstractMesh;
    void Scale(double const factor) override {
        PYBIND11_OVERRIDE_PURE(
            void,
            AbstractMesh2_2,
            Scale,
                    factor);
    }

};
void register_AbstractMesh2_2_class(py::module &m){
py::class_<AbstractMesh2_2 , AbstractMesh2_2_Overrides , std::shared_ptr<AbstractMesh2_2 >   >(m, "AbstractMesh2_2")
        .def(py::init< >())
        .def(
            "GetIndex",
            (unsigned int(AbstractMesh2_2::*)() const ) &AbstractMesh2_2::GetIndex,
            " "  )
        .def(
            "SetIndex",
            (void(AbstractMesh2_2::*)(unsigned int)) &AbstractMesh2_2::SetIndex,
            " " , py::arg("index") )
        .def(
            "AddVertex",
            (void(AbstractMesh2_2::*)(::Point<2>)) &AbstractMesh2_2::AddVertex,
            " " , py::arg("vertex") )
        .def(
            "Scale",
            (void(AbstractMesh2_2::*)(double const)) &AbstractMesh2_2::Scale,
            " " , py::arg("factor") )
    ;
}
