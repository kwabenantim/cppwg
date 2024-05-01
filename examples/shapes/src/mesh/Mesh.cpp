#include "Mesh.hpp"

template <unsigned ELEMENT_DIM, unsigned SPACE_DIM = ELEMENT_DIM>
Mesh<DIM>::Mesh() : mIndex(0)
{
}

template <unsigned DIM>
Mesh<DIM>::~Mesh()
{
}

template <unsigned DIM>
unsigned Mesh<DIM>::GetIndex() const
{
    return mIndex;
}

template <unsigned DIM>
void Mesh<DIM>::SetIndex(unsigned index)
{
    mIndex = index;
}

template class Mesh<2, 2>;
template class Mesh<3, 3>;
