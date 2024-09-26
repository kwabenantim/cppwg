// This file is automatically generated by cppwg.
// Do not modify this file directly.

#ifndef pyshapes_HEADERS_HPP_
#define pyshapes_HEADERS_HPP_

// Includes
#include "ConcreteMesh.hpp"
#include "MeshFactory.hpp"
#include "AbstractMesh.hpp"
#include "SimpleMathFunctions.hpp"
#include "Square.hpp"
#include "Shape.hpp"
#include "Cuboid.hpp"
#include "Triangle.hpp"
#include "Rectangle.hpp"
#include "Point.hpp"

// Instantiate Template Classes
template class Point<2>;
template class Point<3>;
template class Shape<2>;
template class Shape<3>;
template class ConcreteMesh<2>;
template class ConcreteMesh<3>;
template class AbstractMesh<2, 2>;
template class AbstractMesh<3, 3>;

// Typedefs for nicer naming
namespace cppwg
{
    typedef Point<2> Point_2;
    typedef Point<3> Point_3;
    typedef Shape<2> Shape_2;
    typedef Shape<3> Shape_3;
    typedef ConcreteMesh<2> ConcreteMesh_2;
    typedef ConcreteMesh<3> ConcreteMesh_3;
    typedef AbstractMesh<2, 2> AbstractMesh_2_2;
    typedef AbstractMesh<3, 3> AbstractMesh_3_3;
} // namespace cppwg

#endif // pyshapes_HEADERS_HPP_