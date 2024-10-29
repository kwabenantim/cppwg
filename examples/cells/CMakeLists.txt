cmake_minimum_required(VERSION 3.16...3.22)
project(pycells LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find pybind11
find_package(pybind11 CONFIG REQUIRED)

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

# Add external library
add_subdirectory(extern/meshgen meshgen_build)

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
    PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/wrappers/lib
    ${CMAKE_CURRENT_SOURCE_DIR}/src/cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/src/cpp/mesh
    ${CMAKE_CURRENT_SOURCE_DIR}/src/cpp/visualization
    ${VTK_INCLUDE_DIRS}
)

target_link_libraries(_pycells_lib PUBLIC meshgen::meshgen ${VTK_LIBRARIES})

install(TARGETS _pycells_lib LIBRARY DESTINATION pycells)
