#ifndef _NODE_HPP_
#define _NODE_HPP_

#include <array>
#include <vector>

/**
 * A node in a mesh
 */
template <unsigned SPACE_DIM>
class Node
{
private:
    /**
     * Node index
     */
    unsigned mIndex;

    /**
     * Node location
     */
    std::array<double, SPACE_DIM> mLocation;

public:
    /**
     * Default Constructor
     */
    Node();

    /**
     * Constructor with coordinates
     */
    Node(std::vector<double> coords);

    /**
     * Destructor
     */
    ~Node();

    /**
     * Return the index
     */
    unsigned GetIndex() const;
};

#endif //_NODE_HPP_
