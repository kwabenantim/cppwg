// This file is auto-generated by cppwg; manual changes will be overwritten.

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "PybindVTKTypeCaster.h"
#include <memory>
#include "Scene.hpp"

#include "Scene_3.cppwg.hpp"

namespace py = pybind11;
typedef Scene<3> Scene_3;
PYBIND11_DECLARE_HOLDER_TYPE(T, std::shared_ptr<T>);

void register_Scene_3_class(py::module &m)
{
    py::class_<Scene_3, std::shared_ptr<Scene_3>>(m, "Scene_3")
        .def(py::init<>())
        .def("GetRenderer",
            (::vtkSmartPointer<vtkRenderer>(Scene_3::*)()) &Scene_3::GetRenderer,
            " ")
    ;
}
