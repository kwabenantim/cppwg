cmake_minimum_required(VERSION 3.16...3.22)
project(pycells LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} ${CMAKE_CURRENT_SOURCE_DIR}/cmake)

# Find Python
find_package(Python3 REQUIRED COMPONENTS Interpreter Development)

# Find pybind11
find_package(pybind11 CONFIG REQUIRED)

# Find VTK
find_package(VTK REQUIRED COMPONENTS
    vtkCommonCore
    vtkRenderingCore
    vtkRenderingOpenGL2
    vtkWrappingPythonCore
)

# Find PETSc
find_package(PETSc REQUIRED)

# Find MPI
find_package(MPI REQUIRED COMPONENTS CXX)

# Set up pycells module
file(GLOB SOURCES
    ${CMAKE_CURRENT_SOURCE_DIR}/src/cpp/**/*.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/src/cpp/**/*.hpp
    ${CMAKE_CURRENT_SOURCE_DIR}/dynamic/wrappers/**/*.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/dynamic/wrappers/**/*.hpp
)

pybind11_add_module(_pycells_lib ${SOURCES})

target_include_directories(
    _pycells_lib
    PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}/wrappers/lib
    ${CMAKE_CURRENT_SOURCE_DIR}/src/cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/src/cpp/cell
    ${CMAKE_CURRENT_SOURCE_DIR}/src/cpp/mesh
    ${CMAKE_CURRENT_SOURCE_DIR}/src/cpp/utils
    ${CMAKE_CURRENT_SOURCE_DIR}/src/cpp/visualization
    ${CMAKE_CURRENT_SOURCE_DIR}/thirdparty/smtk
    ${VTK_INCLUDE_DIRS}
    ${PETSC_INCLUDES}
    ${MPI_C_INCLUDE_PATH}
    ${MPI_CXX_INCLUDE_PATH}
)

target_link_libraries(
    _pycells_lib
    PUBLIC
    ${VTK_LIBRARIES}
    ${PETSC_LIBRARIES}
    ${MPI_C_LIBRARIES}
    ${MPI_CXX_LIBRARIES}
)

install(TARGETS _pycells_lib LIBRARY DESTINATION pycells)
