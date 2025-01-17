#include "Node.hpp"

#include <boost/numeric/ublas/vector.hpp>

#include <array>
#include <vector>

template <unsigned SPACE_DIM>
Node<SPACE_DIM>::Node()
    : Node({0.0, 0.0, 0.0})
{
}

template <unsigned SPACE_DIM>
Node<SPACE_DIM>::Node(std::vector<double> coords)
    : mIndex(0), mLocation()
{
    for (unsigned i = 0; i < SPACE_DIM; ++i)
    {
        mLocation[i] = coords[i];
    }
}

template <unsigned SPACE_DIM>
Node<SPACE_DIM>::Node(boost::numeric::ublas::c_vector<double, SPACE_DIM> coords)
    : mIndex(0), mLocation()
{
    for (unsigned i = 0; i < SPACE_DIM; ++i)
    {
        mLocation[i] = coords[i];
    }
}

template <unsigned SPACE_DIM>
Node<SPACE_DIM>::~Node()
{
}

template <unsigned SPACE_DIM>
unsigned Node<SPACE_DIM>::GetIndex() const
{
    return mIndex;
}

template <unsigned SPACE_DIM>
boost::numeric::ublas::c_vector<double, SPACE_DIM> Node<SPACE_DIM>::GetLocation()
{
    return mLocation;
}

template <unsigned SPACE_DIM>
void Node<SPACE_DIM>::Translate(const boost::numeric::ublas::c_vector<double, SPACE_DIM> &rDisplacement)
{
    for (unsigned i = 0; i < SPACE_DIM; ++i)
    {
        mLocation[i] += rDisplacement[i];
    }
}

template class Node<2>;
template class Node<3>;
