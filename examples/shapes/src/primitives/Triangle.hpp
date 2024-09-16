#ifndef _TRIANGLE_HPP
#define _TRIANGLE_HPP

#include "Point.hpp"
#include "Shape.hpp"

/**
 * A Triangle
 */
class Triangle : public Shape<2>
{

public:
    /**
     * Default Constructor
     */
    Triangle(const std::vector<std::shared_ptr<Point<2> > > points);

    /**
     * Destructor
     */
    ~Triangle();
};

#endif // _TRIANGLE_HPP
