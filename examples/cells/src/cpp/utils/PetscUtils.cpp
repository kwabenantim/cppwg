#include "PetscUtils.hpp"

#include <petsc.h>
#include <petscksp.h>
#include <petscvec.h>
#include <petscmat.h>
#include <petscsys.h>

#include <vector>

void PetscUtils::Initialise()
{
    if (!PetscUtils::IsInitialised())
    {
        PetscInitialize(PETSC_NULL, PETSC_NULL, PETSC_NULL, PETSC_NULL);
    }
}

bool PetscUtils::IsInitialised()
{
    PetscBool isInitialised;
    PetscInitialized(&isInitialised);
    return (bool)isInitialised;
}

int PetscUtils::GetSize()
{
    if (!PetscUtils::IsInitialised())
    {
        return -1;
    }

    PetscInt size;
    MPI_Comm_size(PETSC_COMM_WORLD, &size);
    return (unsigned)size;
}

int PetscUtils::GetRank()
{
    if (!PetscUtils::IsInitialised())
    {
        return -1;
    }

    PetscInt rank;
    MPI_Comm_rank(PETSC_COMM_WORLD, &rank);
    return (unsigned)rank;
}

Vec PetscUtils::CreateVec(int size)
{
    Vec vec;
    VecCreate(PETSC_COMM_WORLD, &vec);
    VecSetSizes(vec, PETSC_DECIDE, size);
    VecSetType(vec, VECMPI);
    return vec;
}
