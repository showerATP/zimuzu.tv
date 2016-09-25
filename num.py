
import os
a=0
for i in range(10000,35000):
    path = "html/"+str(i)+".html"
    if not os.path.exists(path):
        print(i,"LOST")
        a = a + 1
print(a)
