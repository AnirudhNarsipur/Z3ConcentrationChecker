from z3 import *

s = Solver()


a = Const("a",IntSort())

a = Const("a",SetSort(IntSort()))

a = Store(a,7,True)
a = Store(a,5,True)

# # s.add(Store(a,3,True) == True)
# b =  Const("b",SetSort(IntSort()))
# b = Store(b,2,True)
# c =  Const("c",SetSort(IntSort()))
# s.add(SetUnion(a,b) == c)
x = Int('x') 
y=  Int('y')
s.add(Select(a,x) == True)
s.add(Select(a,y) == True)

s.add(x != y)
print(f"Res {s.check()}")
print(f"Model : {s.model()}")