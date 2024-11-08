#include "Scene.hpp"

#include <vtkAutoInit.h>
#include <vtkOpenGLRenderer.h>
#include <vtkRenderWindow.h>
#include <vtkSmartPointer.h>

template <unsigned DIM>
Scene<DIM>::Scene()
    : mpRenderer(vtkSmartPointer<vtkRenderer>::New()),
      mpRenderWindow(vtkSmartPointer<vtkRenderWindow>::New())
{
    mpRenderer->SetBackground(1.0, 1.0, 1.0);
    mpRenderWindow->AddRenderer(mpRenderer);
    mpRenderWindow->SetSize(800.0, 600.0);
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
