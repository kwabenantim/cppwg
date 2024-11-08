#ifndef _ABSTRACT_MESH_HPP
#define _ABSTRACT_MESH_HPP

#include "Node.hpp"

/**
 * A mesh in SPACE_DIM space with ELEMENT_DIM dimensional elements
 */
template <unsigned ELEMENT_DIM, unsigned SPACE_DIM = ELEMENT_DIM>
class AbstractMesh
{
private:
    /**
     * AbstractMesh index
     */
    unsigned mIndex;

public:
    /**
     * Default Constructor
     */
    AbstractMesh();

    /**
     * Destructor
     */
    ~AbstractMesh();

    /**
     * Return the index
     */
    unsigned GetIndex() const;

    /**
     * Set the index
     */
    void SetIndex(unsigned index);

    /**
     * Add a node to the mesh
     */
    void AddNode(Node<SPACE_DIM> node);

    /**
     * Scale the mesh by a factor
     */
    virtual void Scale(const double factor) = 0;
};

#endif // _ABSTRACT_MESH_HPP
