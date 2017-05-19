# counter
首先，虽然进行比较的state和result均是执行完call之后的结果，但是，最终表达式中的```State.counter```的值并没有被加到本身中去，求解约束之后得到的结果就是初始的```State```值。  
在比较```s1```和```s2```的时候，就会出现一次分支判断```p```，在之前的约束集合中分别添加上```p```与```~p```，在对这两个约束进行求解，这就是为什么```sys_inc```和```sys_iszero```会有两个结果，一个commute，另一个diverge了。其他的同种比较却有两种结果的输出也是这样的原因了。  
那么这两个结果的意义呢？实际上应该是需要化简的，这个好像在[第713次commit](https://github.com/XingGaoY/commuter/tree/a602acd494cdfde1cbb404e414eb283e7a8e3788)中完成了。而counter中的两个result diverge都是初始值的原因导致的。

# pipe
这个pipe的实现基于一个```SList```以及一个记录现在读出位置的索引```nread```，读出后的数据就相当于删除了，存储是有顺序的。这里，先写入a还是b出现了state diverge的情况，当a和b相同的时候，两个写入commute。写入和读出同样有diverge，这是由于初始```nread```不同导致的，```Slist```并未指定初始的```nread```，即使有写入，也有可能读不出元素。这样，两个```read```的result diverge原因也是如此。

# unorder pipe
- **SBag**  
  相比于之前的pipe，只是将```SList```更换为```SBag```，存储没有顺序。这样，两次写入就commute了。
- **SBag中choose的实现**  
  这是一个有意思的地方，实现的结果是从SBag中随机取出一个元素，代码如下：

```
    def choose(self):
        self._choices = self._choices + 1
        choicevar = anyInt('%s.choose.%d' % (self._name_prefix, self._choices))

        for i in range(0, len(self._items)):
            if choicevar == i:
                return self._items[i]
```

咋看起来```choicevar```并没有被赋予一个确定的值，我去测试了一下代码，通过```anyInt```得到的值确定是0。z3的文档描述如下：
```
    def z3py.Int(
        name, ctx = None )
```

# Symbolic Execution
果然之前的疑问是我的理解有问题。  
SE执行的过程中，实际上有两次添加约束的过程：实际的两次call和之后进行state比较的时候。  
那么choose的实现也就可以理解了，确实choicevar没有被赋予确定的值，但是在之后的循环里增加了与其相关的约束，在一次写一次读的测试中，i最大为1，当然所有的值都是零了。
