#ifndef _RECTANGLE_HPP
#define _RECTANGLE_HPP

#include "Shape.hpp"

/**
 * A Rectangle
 */
class Rectangle : public Shape<2>
{

public:

    /**
     * Default Constructor
     */
    Rectangle(double width = 2.0, double height = 1.0);

    /**
     * Destructor
     */
    ~Rectangle();

};

#endif  // _RECTANGLE_HPP
