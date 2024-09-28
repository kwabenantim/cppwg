#include "ConcreteMesh.hpp"

#include "MeshFactory.hpp"

template <class MESH>
MeshFactory<MESH>::MeshFactory(): mMeshGen()
{
}

template <class MESH>
MeshFactory<MESH>::~MeshFactory()
{
}

template class MeshFactory<ConcreteMesh<2> >;
template class MeshFactory<ConcreteMesh<3> >;
