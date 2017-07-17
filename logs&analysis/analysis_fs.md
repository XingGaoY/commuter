## slots
Two more slots are added:
  - ```ListofBool ialloc```: track the inode allocated or not
  - ```Int numialloc```: record the num of allocated inode

## open
Here, the number of inode has a upper bound. And the following code is used to check and count:
```
    if self.numialloc == self.ialloc._len:
        return ('err', errno.ENOSPC)
    self.numialloc = self.numialloc + 1
```

## unlink
As inode is taken into account, unlink needs to decrement ```numialloc``` and set the relevant ```ialloc``` false

## rename
Check the existence of original file name, and the new name is identical, set the ```fn_to_ino```'s index to the new fn
