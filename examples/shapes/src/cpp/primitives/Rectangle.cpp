#include <cassert>
#include <memory>

#include "Point.hpp"
#include "Rectangle.hpp"

Rectangle::Rectangle(double width, double height) : Shape<2>()
{
    this->mVertices.push_back(std::make_shared<Point<2> >(0.0, 0.0));
    this->mVertices.push_back(std::make_shared<Point<2> >(width, 0.0));
    this->mVertices.push_back(std::make_shared<Point<2> >(width, height));
    this->mVertices.push_back(std::make_shared<Point<2> >(0.0, height));
}

Rectangle::Rectangle(const std::vector<std::shared_ptr<Point<2> > > points) : Shape<2>()
{
    assert(points.size() == 4);

    for (unsigned i = 0; i < points.size(); ++i)
    {
        this->mVertices.push_back(points[i]);
    }
}

Rectangle::~Rectangle()
{
}
