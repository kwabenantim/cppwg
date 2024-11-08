#ifndef _MESH_FACTORY_HPP
#define _MESH_FACTORY_HPP

#include <memory>

/**
 * A concrete mesh implementation
 */
template <class MESH>
class MeshFactory
{
public:
    /**
     * Default Constructor
     */
    MeshFactory();

    /**
     * Destructor
     */
    ~MeshFactory();

    /**
     * Generate a mesh
     */
    std::shared_ptr<MESH> generateMesh();
};

#endif // _MESH_FACTORY_HPP
