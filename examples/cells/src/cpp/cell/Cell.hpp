#ifndef CELL_HPP_
#define CELL_HPP_

class Cell
{
private:
    /**
     * Cell index
     */
    unsigned mIndex;

public:
    /**
     * Default Constructor
     */
    Cell();

    /**
     * Destructor
     */
    virtual ~Cell();

    /**
     * Return the index
     */
    unsigned GetCellId() const;
};

#endif // CELL_HPP_
