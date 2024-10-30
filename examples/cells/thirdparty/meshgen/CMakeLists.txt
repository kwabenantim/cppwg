cmake_minimum_required(VERSION 3.8)
project(meshgen)

add_library(meshgen MeshGen.cpp MeshGen.hpp)
target_include_directories(meshgen PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})
add_library(meshgen::meshgen ALIAS meshgen)
