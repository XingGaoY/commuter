# basic testcasegen
由```Solver.model```求解得到一个初始的state值，转换成json后写出。

具体的过程：
-  In the symbolic part, when the result diverges, append 'r' to return value, when the state diverges, append 's' to the return value. Thus, return '' when commute, and combination of '', 'r' and 's' when diverge according to different condition. 
-  Thus, we are able to catagorize the condition with the val of ```rv```.
  - ```pc```: precondition that commute
  - ```pr``` & ``ps```: precondition that result or state diverges
- And we have ```ps2 = ps & ~exist(pc) & ~exist(pr)``` etc, to represent the precondition of differnt res.
> I need to find the reason why? Not really understand his intentions  
- Then just find the solutino of differnt preconditions

也就是说，testcase是可求解的初始state和调用
大概的形式是
```
{
  "vars":{
    ...:[
      ...
    ]
  },
  "calls":[
    ...
  ]
}
```
但是可以看到会出现有```vars```中有“k!844”这样奇怪的值。
应该是求解器出现的bug， 如果是作者那里没有问题的话，我应该去检查一下我的z3为什么会这样，或者之后如何修复的该问题。