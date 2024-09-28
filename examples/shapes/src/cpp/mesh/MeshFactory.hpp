#ifndef _MESH_FACTORY_HPP
#define _MESH_FACTORY_HPP

#include "MeshGen.hpp"

/**
 * A concrete mesh implementation
 */
template <class MESH>
class MeshFactory
{
private:
    MeshGen mMeshGen;

public:
    /**
     * Default Constructor
     */
    MeshFactory();

    /**
     * Destructor
     */
    ~MeshFactory();
};

#endif // _MESH_FACTORY_HPP
