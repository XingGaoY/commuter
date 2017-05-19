# slot
FS的state有两个，```fn_to_ino```与```ino_to_data```，其中第一个表示文件是否存在，即是否有对应的inode，第二个表示该文件中是否有数据。  
这两个属性均是SDict，由两个数组构成，一个记录该key是否存在，对应一个bool值，另一个记录该key对应的value，在fs中用一个z3.Int表示。

# 具体的函数实现
返回一个Bool，其中```fn```, ```creat```, ```excl```, ```trunc```均可以认为是传入的参数，分别和Unix open中的```path```, ```O_CREAT```, ```O_EXCL```以及```O_TRUNC```相对应。  
函数检查是否有```creat```的flag，如果存在，进一步检查```excl```，存在则返回false，不存在，则创建新文件。如果没有```creat```且文件不存在则返回false。之后那么文件存在，根据是否有flag```trunc```来决定是否将旧数据置零。  
可以看见函数中有6个判断分支，检查commute的时候，出现了很多的子进程。
```
    def open(self, which):
        fn = simsym.anyInt('Fs.open.fn.%s' % which)
        creat = simsym.anyInt('Fs.open.creat.%s' % which)
        excl = simsym.anyInt('Fs.open.excl.%s' % which)
        trunc = simsym.anyInt('Fs.open.trunc.%s' % which)

        if creat != 0:
            if self.fn_to_ino.contains(fn):
                if excl != 0: return False
                if which == 'a':
                    self.fn_to_ino[fn] = 11
                else:
                    self.fn_to_ino[fn] = 12

        if not self.fn_to_ino.contains(fn):
            return False

        if trunc != 0:
            self.ino_to_data[self.fn_to_ino[fn]] = 0

        return True
```
这个函数没有做任何的检查，直接在```SDict._valid```队列中将对应的值置为false。
```
    def unlink(self, which):
        fn = simsym.anyInt('Fs.unlink.fn.%s' % which)
        del self.fn_to_ino[fn]
```
读文件，如果文件不存在，则返回none，如果文件中没有对应的数据也返回none，其他的情况返回文件中的数据。
```
    def read(self, which):
        fn = simsym.anyInt('Fs.read.fn.%s' % which)

        if not self.fn_to_ino.contains(fn):
            return None

        ino = self.fn_to_ino[fn]

        if not self.ino_to_data.contains(ino):
            return None

        return self.ino_to_data[ino]
```
写文件，文件不存在则返回none，文件存在，则写入数据。
```
    def write(self, which):

        fn = simsym.anyInt('Fs.write.fn.%s' % which)

        if not self.fn_to_ino.contains(fn):
            return None

        ino = self.fn_to_ino[fn]
        data = simsym.anyInt('Fs.write.data.%s' % which)
        self.ino_to_data[ino] = data

        return True
```