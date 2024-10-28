cmake_minimum_required(VERSION 3.16...3.22)
project(cells LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find Python
find_package(Python3 REQUIRED COMPONENTS Interpreter Development)

# Find VTK
find_package(VTK 7.1
    REQUIRED
    COMPONENTS
        vtkCommonCore
        vtkCommonDataModel
        vtkFiltersCore
        vtkFiltersGeneral
        vtkFiltersGeneric
        vtkFiltersGeometry
        vtkFiltersModeling
        vtkFiltersProgrammable
        vtkFiltersSources
        vtkFiltersVerdict
        vtkInteractionStyle
        vtkIOCore
        vtkIOGeometry
        vtkIOImage
        vtkIOLegacy
        vtkIOMovie
        vtkIOParallelXML
        vtkIOXML
        vtkRenderingAnnotation
        vtkRenderingCore
        vtkRenderingFreeType
        vtkRenderingOpenGL2
        vtkWrappingPythonCore
)

# Fetch pybind11
include(FetchContent)
FetchContent_Declare(
    pybind11
    GIT_REPOSITORY https://github.com/pybind/pybind11
    GIT_TAG v2.13.5
    GIT_SHALLOW 1
)
FetchContent_MakeAvailable(pybind11)

# Add external library
add_subdirectory(extern/meshgen meshgen_build)

# Add a shared library for the main C++ source
file(GLOB_RECURSE CELLS_SOURCES
    ${CMAKE_CURRENT_SOURCE_DIR}/src/cpp/*.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/src/cpp/*.hpp
)
add_library(cells SHARED ${CELLS_SOURCES})
target_include_directories(
    cells
    PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}/src/cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/src/cpp/mesh
)
target_link_libraries(cells PUBLIC meshgen::meshgen)

# Set up Pybind11 module
file(GLOB PYCELLS_SOURCES 
    ${CMAKE_CURRENT_SOURCE_DIR}/dynamic/wrappers/lib/*.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/dynamic/wrappers/lib/*.hpp
)
pybind11_add_module(_pycells_lib MODULE ${PYCELLS_SOURCES})
target_link_libraries(
    _pycells_lib
    PRIVATE
    cells
)
target_include_directories(
    _pycells_lib
    PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/wrappers/lib
)

# Add install target for scikit-build
install(TARGETS cells DESTINATION .)
