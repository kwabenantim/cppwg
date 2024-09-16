#include <cassert>
#include <memory>

#include "Point.hpp"
#include "Triangle.hpp"

Triangle::Triangle(const std::vector<std::shared_ptr<Point<2> > > points) : Shape<2>()
{
    assert(points.size() == 3);

    for (unsigned i = 0; i < points.size(); ++i)
    {
        this->mVertices.push_back(points[i]);
    }
}

Triangle::~Triangle()
{
}
