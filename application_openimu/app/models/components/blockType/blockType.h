#ifndef BLOCKTYPE_H
#define BLOCKTYPE_H


class BlockType
{
public:
    BlockType();
    ~BlockType();
    virtual void work() = 0;
};

#endif // BLOCKTYPE_H
