cmake_minimum_required(VERSION 3.16...3.22)
project(pycells LANGUAGES C CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} ${CMAKE_SOURCE_DIR}/cmake)

# Find Python
find_package(Python3 REQUIRED COMPONENTS Interpreter Development)

# Find Boost
find_package (Boost REQUIRED)

# Find VTK
foreach(_core_module vtkCommonCore CommonCore)
    find_package(VTK COMPONENTS ${_core_module} QUIET)
    if(VTK_FOUND)
        break()
    endif()
endforeach()

if(VTK_VERSION VERSION_LESS 9.0.0)
    find_package(VTK REQUIRED COMPONENTS vtkCommonCore vtkRenderingCore vtkRenderingOpenGL2 vtkWrappingPythonCore)
else()
    find_package(VTK REQUIRED COMPONENTS CommonCore RenderingCore RenderingOpenGL2 WrappingPythonCore)
endif()

message(STATUS "VTK version: ${VTK_VERSION}")

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
    GIT_REPOSITORY https://github.com/pybind/pybind11
    GIT_TAG v2.13.6
    GIT_SHALLOW 1
)
FetchContent_MakeAvailable(pybind11)

# Add a shared library target for the main C++ source
file(GLOB_RECURSE MAIN_SOURCES
    ${CMAKE_SOURCE_DIR}/src/cpp/*.cpp
    ${CMAKE_SOURCE_DIR}/src/cpp/*.hpp
)
add_library(cells SHARED ${MAIN_SOURCES})
target_link_libraries(cells PUBLIC
    ${Boost_LIBRARIES}
    ${VTK_LIBRARIES}
    ${PETSC_LIBRARIES}
    ${MPI_C_LIBRARIES}
    ${MPI_CXX_LIBRARIES}
)
target_include_directories(cells PUBLIC
    ${CMAKE_SOURCE_DIR}/src/cpp
    ${CMAKE_SOURCE_DIR}/src/cpp/cell
    ${CMAKE_SOURCE_DIR}/src/cpp/mesh
    ${CMAKE_SOURCE_DIR}/src/cpp/utils
    ${CMAKE_SOURCE_DIR}/src/cpp/visualization
    ${Boost_INCLUDE_DIR}
    ${VTK_INCLUDE_DIRS}
    ${PETSC_INCLUDES}
    ${MPI_C_INCLUDE_PATH}
    ${MPI_CXX_INCLUDE_PATH}
)

# Set up the pycells module with pybind11
file(GLOB WRAPPER_SOURCES
    ${CMAKE_SOURCE_DIR}/dynamic/wrappers/all/*.cpp
    ${CMAKE_SOURCE_DIR}/dynamic/wrappers/all/*.hpp
)
pybind11_add_module(_pycells_all MODULE ${WRAPPER_SOURCES})
target_link_libraries(_pycells_all PRIVATE cells)
target_include_directories(_pycells_all PRIVATE
    ${CMAKE_SOURCE_DIR}/dynamic/wrappers/all
    ${CMAKE_SOURCE_DIR}/dynamic/typecasters/
    ${CMAKE_SOURCE_DIR}/dynamic/typecasters/thirdparty/dolfinx
    ${CMAKE_SOURCE_DIR}/dynamic/typecasters/thirdparty/smtk
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

# Target for re-generating wrappers
find_program(CPPWG cppwg REQUIRED)
add_custom_target(pycells_wrappers
    COMMAND ${CPPWG} ${CMAKE_SOURCE_DIR}/src/cpp
            -w ${CMAKE_SOURCE_DIR}/dynamic/wrappers
            -p ${CMAKE_SOURCE_DIR}/dynamic/config.yaml
            -i "$<JOIN:$<TARGET_PROPERTY:_pycells_all,INCLUDE_DIRECTORIES>,;>"
            -l ${CMAKE_BINARY_DIR}/cppwg.log
            --std c++17
    COMMAND_EXPAND_LISTS
)
