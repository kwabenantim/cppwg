#include "Scene.hpp"

template <unsigned DIM>
Scene<DIM>::Scene()
    : mpRenderer(vtkSmartPointer<vtkRenderer>::New())
{
    mpRenderer->SetBackground(0.0, 0.0, 0.0);
}

template <unsigned DIM>
Scene<DIM>::~Scene()
{
}

template <unsigned DIM>
vtkSmartPointer<vtkRenderer> Scene<DIM>::GetRenderer()
{
    return mpRenderer;
}

template class Scene<2>;
template class Scene<3>;
