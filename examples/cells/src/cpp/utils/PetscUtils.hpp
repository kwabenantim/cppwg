#ifndef PETSCUTILS_HPP_
#define PETSCUTILS_HPP_

#include <petsc.h>
#include <petscvec.h>
#include <petscmat.h>
#include <petscsys.h>

#include <vector>

class PetscUtils
{
public:
    static void Initialise();

    static bool IsInitialised();

    static int GetSize();
    static int GetRank();

    static Vec CreateVec(int size);
};

#endif // PETSCUTILS_HPP_
