#ifndef _POTTS_MESH_HPP
#define _POTTS_MESH_HPP

#include "AbstractMesh.hpp"

/**
 * A Potts mesh implementation
 */
template <unsigned DIM>
class PottsMesh : public AbstractMesh<DIM, DIM>
{
public:
    /**
     * Default Constructor
     */
    PottsMesh();

    /**
     * Destructor
     */
    ~PottsMesh();

    /**
     * Scale the mesh by a factor
     */
    void Scale(const double factor) override;
};

#endif // _POTTS_MESH_HPP
