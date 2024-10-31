#ifndef PYBINDPETSCTYPECASTER_HPP_
#define PYBINDPETSCTYPECASTER_HPP_

#include <petsc/private/matimpl.h>
#include <petsc/private/vecimpl.h>

#include <pybind11/pybind11.h>

PYBIND11_MAKE_OPAQUE(Mat);
PYBIND11_MAKE_OPAQUE(Vec);

#endif // PYBINDPETSCTYPECASTER_HPP_
