import string

li = []
li.append(string.digits*2)
print(li)
li2 = ''.join(li)
print(''.join(li))
print(string.digits*2)
print(li2, type(li2))
print(list(li2))
