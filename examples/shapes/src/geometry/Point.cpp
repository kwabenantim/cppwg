#include "Point.hpp"

template <unsigned DIM>
Point<DIM>::Point()
    : Point(0.0, 0.0, 0.0)
{
}

template <unsigned DIM>
Point<DIM>::Point(double x, double y, double z)
    : mIndex(0), mLocation()
{
    mLocation[0] = x;
    mLocation[1] = y;
    if (DIM == 3)
    {
        mLocation[2] = z;
    }
}

template <unsigned DIM>
Point<DIM>::Point(int x, int y, int z)
    : Point(static_cast<double>(x),
            static_cast<double>(y),
            static_cast<double>(z))
{
}

template <unsigned DIM>
Point<DIM>::~Point()
{
}

template <unsigned DIM>
std::array<double, DIM> Point<DIM>::GetLocation() const
{
    return mLocation;
}

template <unsigned DIM>
const std::array<double, DIM> &Point<DIM>::rGetLocation() const
{
    return mLocation;
}

template <unsigned DIM>
unsigned Point<DIM>::GetIndex() const
{
    return mIndex;
}

template <unsigned DIM>
void Point<DIM>::SetIndex(unsigned index)
{
    mIndex = index;
}

template <unsigned DIM>
void Point<DIM>::SetLocation(const std::array<double, DIM> &rLocation)
{
    mLocation = rLocation;
}

template <unsigned DIM>
void Point<DIM>::ExcludedMethod()
{
    // Excluded method
}

template class Point<2>;
template class Point<3>;
