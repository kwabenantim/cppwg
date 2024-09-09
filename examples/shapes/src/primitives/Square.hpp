#ifndef _SQUARE_HPP
#define _SQUARE_HPP

#include "Rectangle.hpp"

/**
 * A Square
 */
class Square : public Rectangle
{

public:
    /**
     * Default Constructor
     */
    Square(double width = 2.0);

    /**
     * Destructor
     */
    ~Square();
};

#endif // _SQUARE_HPP
