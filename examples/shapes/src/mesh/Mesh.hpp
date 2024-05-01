#ifndef _MESH_HPP
#define _MESH_HPP

/**
 * A mesh in SPACE_DIM space with ELEMENT_DIM dimensional elements
 */
template <unsigned ELEMENT_DIM, unsigned SPACE_DIM = ELEMENT_DIM>
class Mesh
{
private:
    /**
     * Mesh index
     */
    unsigned mIndex;

public:
    /**
     * Default Constructor
     */
    Mesh();

    /**
     * Destructor
     */
    ~Mesh();

    /**
     * Return the index
     */
    unsigned GetIndex() const;

    /**
     * Set the index
     */
    void SetIndex(unsigned index);
};

#endif // _MESH_HPP
