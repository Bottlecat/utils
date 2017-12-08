```
for...else:
当迭代的对象迭代完并为空时，位于else的子句将执行，而如果在for循环中含有break时则直接终止循环，并不会执行else子句。
使用pylint检测代码时会提示 
```

```
2017/12/01
可迭代对象是指实现了__iter__方法的对象。
迭代器对象是指实现了__iter__和next方法的对象。
生成器是一种特殊的迭代器
```

```
iteritems省内存
```

```
Python中的对象之间赋值时是按引用传递的，如果需要拷贝对象，需要使用标准库中的copy模块。 
1. copy.copy 浅拷贝 只拷贝父对象，不会拷贝对象的内部的子对象。 
2. copy.deepcopy 深拷贝 拷贝对象及其子对象 
一个很好的例子：
  
  import copy  
  a = [1, 2, 3, 4, ['a', 'b']] #原始对象  

  b = a #赋值，传对象的引用  
  c = copy.copy(a) #对象拷贝，浅拷贝  
  d = copy.deepcopy(a) #对象拷贝，深拷贝  

  a.append(5) #修改对象a  
  a[4].append('c') #修改对象a中的['a', 'b']数组对象  

  print 'a = ', a  
  print 'b = ', b  
  print 'c = ', c  
  print 'd = ', d  
  
输出结果： 
  a = [1, 2, 3, 4, ['a', 'b', 'c'], 5] 
  b = [1, 2, 3, 4, ['a', 'b', 'c'], 5] 
  c = [1, 2, 3, 4, ['a', 'b', 'c']] 
  d = [1, 2, 3, 4, ['a', 'b']]

```
```
python中__get__,__getattr__,__getattribute__的区别
__get__,__getattr__和__getattribute都是访问属性的方法，但不太相同。 
object.__getattr__(self, name) 
当一般位置找不到attribute的时候，会调用getattr，返回一个值或AttributeError异常。 

object.__getattribute__(self, name) 
无条件被调用，通过实例访问属性。如果class中定义了__getattr__()，则__getattr__()不会被调用（除非显示调用或引发AttributeError异常） 

object.__get__(self, instance, owner) 
如果class定义了它，则这个class就可以称为descriptor。owner是所有者的类，instance是访问descriptor的实例，如果不是通过实例访问，而是通过类访问的话，instance则为None。（descriptor的实例自己访问自己是不会触发__get__，而会触发__call__，只有descriptor作为其它类的属性才有意义。）（所以下文的d是作为C2的一个属性被调用）

class C(object):
    a = 'abc'
    def __getattribute__(self, *args, **kwargs):
        print("__getattribute__() is called")
        return object.__getattribute__(self, *args, **kwargs)

    def __getattr__(self, name):
        print("__getattr__() is called ")
        return name + " from getattr"
    
    def __get__(self, instance, owner):
        print("__get__() is called", instance, owner)
        return self
    
    def foo(self, x):
        print(x)

class C2(object):
    d = C()
if __name__ == '__main__':
    c = C()
    c2 = C2()
    print(c.a)
    print(c.zzzzzzzz)
    c2.d
    print(c2.d.a)
    
__getattribute__() is called  
abc  
__getattribute__() is called  
__getattr__() is called   
zzzzzzzz from getattr  
__get__() is called <__main__.C2 object at 0x16d2310> <class '__main__.C2'>  
__get__() is called <__main__.C2 object at 0x16d2310> <class '__main__.C2'>  
__getattribute__() is called  
abc

小结：可以看出，每次通过实例访问属性，都会经过__getattribute__函数。而当属性不存在时，仍然需要访问__getattribute__，不过接着要访问__getattr__。这就好像是一个异常处理函数。 
每次访问descriptor（即实现了__get__的类），都会先经过__get__函数。 

需要注意的是，当使用类访问不存在的变量是，不会经过__getattr__函数。而descriptor不存在此问题，只是把instance标识为none而已。
```

```
类的私有属性
class Program(object):
  def __init__(self, weight):
    self.__weight = weight
    
__weight -> _Program__weight
```

```
logging模块、itertools模块、collections模块
单元测试、模块测试、性能调优、内存泄漏分析
```
