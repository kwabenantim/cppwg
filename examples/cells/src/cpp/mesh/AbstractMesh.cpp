#include "AbstractMesh.hpp"
#include "Node.hpp"

template <unsigned ELEMENT_DIM, unsigned SPACE_DIM>
AbstractMesh<ELEMENT_DIM, SPACE_DIM>::AbstractMesh() : mIndex(0)
{
}

template <unsigned ELEMENT_DIM, unsigned SPACE_DIM>
AbstractMesh<ELEMENT_DIM, SPACE_DIM>::~AbstractMesh()
{
}

template <unsigned ELEMENT_DIM, unsigned SPACE_DIM>
unsigned AbstractMesh<ELEMENT_DIM, SPACE_DIM>::GetIndex() const
{
    return mIndex;
}

template <unsigned ELEMENT_DIM, unsigned SPACE_DIM>
void AbstractMesh<ELEMENT_DIM, SPACE_DIM>::SetIndex(unsigned index)
{
    mIndex = index;
}

template <unsigned ELEMENT_DIM, unsigned SPACE_DIM>
void AbstractMesh<ELEMENT_DIM, SPACE_DIM>::AddNode(Node<SPACE_DIM> node)
{
}

template class AbstractMesh<2, 2>;
template class AbstractMesh<3, 3>;
