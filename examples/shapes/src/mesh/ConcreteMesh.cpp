#include "AbstractMesh.hpp"
#include "ConcreteMesh.hpp"

template <unsigned DIM>
ConcreteMesh<DIM>::ConcreteMesh() : AbstractMesh<DIM, DIM>()
{
}

template <unsigned DIM>
ConcreteMesh<DIM>::~ConcreteMesh()
{
}
template <unsigned DIM>
void ConcreteMesh<DIM>::Scale(const double factor){
    // Scale the mesh
};

template class ConcreteMesh<2>;
template class ConcreteMesh<3>;
