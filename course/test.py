data=[0,1,2,3,4,5,6,7,8,9,]
for i in data:
    if (i % 2 == 0):
        ind = data.index(i)
        data.pop(ind)
print(data)


