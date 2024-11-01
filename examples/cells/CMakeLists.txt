cmake_minimum_required(VERSION 3.16...3.22)
project(pycells LANGUAGES C CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} ${CMAKE_CURRENT_SOURCE_DIR}/cmake)

# Find Python
find_package(Python3 REQUIRED COMPONENTS Interpreter Development)

# Find VTK
find_package(VTK REQUIRED COMPONENTS
    vtkCommonCore
    vtkRenderingCore
    vtkRenderingOpenGL2
    vtkWrappingPythonCore
)

# Find PETSc
find_package(PETSc REQUIRED)

# Find PETSc4py
find_package(PETSc4py REQUIRED)

# Find MPI
find_package(MPI REQUIRED COMPONENTS CXX)

# Fetch pybind11
include(FetchContent)
FetchContent_Declare(
  pybind11
  URL https://github.com/pybind/pybind11/archive/refs/tags/v2.10.4.tar.gz
  URL_HASH SHA256=832e2f309c57da9c1e6d4542dedd34b24e4192ecb4d62f6f4866a737454c9970
)
FetchContent_MakeAvailable(pybind11)

# Add a shared library target for the main C++ source
file(GLOB_RECURSE MAIN_SOURCES
    ${CMAKE_CURRENT_SOURCE_DIR}/src/cpp/*.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/src/cpp/*.hpp
)
add_library(cells SHARED ${MAIN_SOURCES})
target_link_libraries(cells PUBLIC
    ${VTK_LIBRARIES}
    ${PETSC_LIBRARIES}
    ${MPI_C_LIBRARIES}
    ${MPI_CXX_LIBRARIES}
)
target_include_directories(cells PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}/src/cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/src/cpp/cell
    ${CMAKE_CURRENT_SOURCE_DIR}/src/cpp/mesh
    ${CMAKE_CURRENT_SOURCE_DIR}/src/cpp/utils
    ${CMAKE_CURRENT_SOURCE_DIR}/src/cpp/visualization
    ${VTK_INCLUDE_DIRS}
    ${PETSC_INCLUDES}
    ${MPI_C_INCLUDE_PATH}
    ${MPI_CXX_INCLUDE_PATH}
)

# Set up the pycells module with pybind11
file(GLOB WRAPPER_SOURCES
    ${CMAKE_CURRENT_SOURCE_DIR}/dynamic/wrappers/all/*.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/dynamic/wrappers/all/*.hpp
)
pybind11_add_module(_pycells_all MODULE ${WRAPPER_SOURCES})
target_link_libraries(_pycells_all PRIVATE cells)
target_include_directories(_pycells_all PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/dynamic/wrappers/all
    ${CMAKE_CURRENT_SOURCE_DIR}/dynamic/thirdparty/dolfinx
    ${CMAKE_CURRENT_SOURCE_DIR}/dynamic/thirdparty/smtk
    ${PETSC4PY_INCLUDES}
)

# Add install targets for scikit-build
if(SKBUILD)
    set_target_properties(_pycells_all PROPERTIES
        SKIP_BUILD_RPATH FALSE
        BUILD_WITH_INSTALL_RPATH FALSE
        INSTALL_RPATH_USE_LINK_PATH TRUE
        INSTALL_RPATH $ORIGIN
    )
    install(TARGETS cells LIBRARY DESTINATION .)
    install(TARGETS _pycells_all LIBRARY DESTINATION .)
endif()
