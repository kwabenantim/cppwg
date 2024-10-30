#include "Cell.hpp"

Cell::Cell() : mIndex(0)
{
}

Cell::~Cell()
{
}

unsigned Cell::GetCellId() const
{
    return mIndex;
}
