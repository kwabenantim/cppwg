#include "MeshFactory.hpp"
#include "PottsMesh.hpp"

template <class MESH>
MeshFactory<MESH>::MeshFactory(): mMeshGen()
{
}

template <class MESH>
MeshFactory<MESH>::~MeshFactory()
{
}

template class MeshFactory<PottsMesh<2> >;
template class MeshFactory<PottsMesh<3> >;
