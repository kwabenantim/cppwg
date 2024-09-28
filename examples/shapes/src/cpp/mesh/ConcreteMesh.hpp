#ifndef _CONCRETE_MESH_HPP
#define _CONCRETE_MESH_HPP

#include "AbstractMesh.hpp"

/**
 * A concrete mesh implementation
 */
template <unsigned DIM>
class ConcreteMesh : public AbstractMesh<DIM, DIM>
{
public:
    /**
     * Default Constructor
     */
    ConcreteMesh();

    /**
     * Destructor
     */
    ~ConcreteMesh();

    /**
     * Scale the mesh by a factor
     */
    void Scale(const double factor) override;
};

#endif // _CONCRETE_MESH_HPP
