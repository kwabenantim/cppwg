#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "wrapper_header_collection.hpp"

#include "AbstractMesh3_3.cppwg.hpp"

namespace py = pybind11;
typedef AbstractMesh<3,3 > AbstractMesh3_3;
PYBIND11_DECLARE_HOLDER_TYPE(T, std::shared_ptr<T>);

class AbstractMesh3_3_Overrides : public AbstractMesh3_3{
    public:
    using AbstractMesh3_3::AbstractMesh;
    void Scale(double const factor) override {
        PYBIND11_OVERRIDE_PURE(
            void,
            AbstractMesh3_3,
            Scale,
                    factor);
    }

};
void register_AbstractMesh3_3_class(py::module &m){
py::class_<AbstractMesh3_3 , AbstractMesh3_3_Overrides , std::shared_ptr<AbstractMesh3_3 >   >(m, "AbstractMesh3_3")
        .def(py::init< >())
        .def(
            "GetIndex",
            (unsigned int(AbstractMesh3_3::*)() const ) &AbstractMesh3_3::GetIndex,
            " "  )
        .def(
            "SetIndex",
            (void(AbstractMesh3_3::*)(unsigned int)) &AbstractMesh3_3::SetIndex,
            " " , py::arg("index") )
        .def(
            "AddVertex",
            (void(AbstractMesh3_3::*)(::Point<3>)) &AbstractMesh3_3::AddVertex,
            " " , py::arg("vertex") )
        .def(
            "Scale",
            (void(AbstractMesh3_3::*)(double const)) &AbstractMesh3_3::Scale,
            " " , py::arg("factor") )
    ;
}
