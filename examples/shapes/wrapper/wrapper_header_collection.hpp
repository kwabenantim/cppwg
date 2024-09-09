// This file is automatically generated by cppwg.
// Do not modify this file directly.

#ifndef pyshapes_HEADERS_HPP_
#define pyshapes_HEADERS_HPP_

// Includes
#include "ConcreteMesh.hpp"
#include "AbstractMesh.hpp"
#include "SimpleMathFunctions.hpp"
#include "Square.hpp"
#include "Shape.hpp"
#include "Cuboid.hpp"
#include "Rectangle.hpp"
#include "Point.hpp"

// Instantiate Template Classes
template class Point<2>;
template class Point<3>;
template class Shape<2>;
template class Shape<3>;
template class AbstractMesh<2,2>;
template class AbstractMesh<3,3>;
template class ConcreteMesh<2>;
template class ConcreteMesh<3>;

// Typedefs for nicer naming
namespace cppwg
{
typedef Point<2> Point2;
typedef Point<3> Point3;
typedef Shape<2> Shape2;
typedef Shape<3> Shape3;
typedef AbstractMesh<2,2> AbstractMesh2_2;
typedef AbstractMesh<3,3> AbstractMesh3_3;
typedef ConcreteMesh<2> ConcreteMesh2;
typedef ConcreteMesh<3> ConcreteMesh3;
} // namespace cppwg

#endif // pyshapes_HEADERS_HPP_
