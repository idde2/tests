import random
size = 2
count_all = 0
for i in range(10):
    win = False
    count = 0
    while not win:
        x = [1] * size
        y = [1] * size
        for i in range(size):
            x[i] = random.randint(1,size)
            y[i] = random.randint(1,size)
        count += 1
        print(x, "\n", y)
        win = x == y
    print(count)
    count_all += count
print(count_all/10)