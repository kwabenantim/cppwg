#ifndef SCENE_HPP_
#define SCENE_HPP_

#include <vtkAutoInit.h>
#include <vtkOpenGLRenderer.h>
#include <vtkRenderWindow.h>
#include <vtkSmartPointer.h>

VTK_MODULE_INIT(vtkRenderingOpenGL2);

template <unsigned DIM>
class Scene
{
    vtkSmartPointer<vtkRenderer> mpRenderer;
    vtkSmartPointer<vtkRenderWindow> mpRenderWindow;

public:
    Scene();

    virtual ~Scene();

    vtkSmartPointer<vtkRenderer> GetRenderer();
};

#endif // SCENE_HPP_
