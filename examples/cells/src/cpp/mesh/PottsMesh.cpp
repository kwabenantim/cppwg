#include "AbstractMesh.hpp"
#include "PottsMesh.hpp"

template <unsigned DIM>
PottsMesh<DIM>::PottsMesh() : AbstractMesh<DIM, DIM>()
{
}

template <unsigned DIM>
PottsMesh<DIM>::~PottsMesh()
{
}
template <unsigned DIM>
void PottsMesh<DIM>::Scale(const double factor){
    // Scale the mesh
};

template class PottsMesh<2>;
template class PottsMesh<3>;
