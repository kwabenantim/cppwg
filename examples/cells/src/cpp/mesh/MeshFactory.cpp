#include "MeshFactory.hpp"
#include "PottsMesh.hpp"

#include <memory>

template <class MESH>
MeshFactory<MESH>::MeshFactory()
{
}

template <class MESH>
MeshFactory<MESH>::~MeshFactory()
{
}

template <class MESH>
std::shared_ptr<MESH> MeshFactory<MESH>::generateMesh()
{
    return std::make_shared<MESH>();
}

template class MeshFactory<PottsMesh<2>>;
template class MeshFactory<PottsMesh<3>>;
