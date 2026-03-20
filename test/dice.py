import random

def dice(eyes):
    if eyes == 1:
        print("   ")
        print(" * ")
        print("   ")
    if eyes == 2:
        print("  *")
        print("   ")
        print("*  ")
    if eyes == 3:
        print("  *")
        print(" * ")
        print("*  ")
    if eyes == 4:
        print("* *")
        print("   ")
        print("* *")
    if eyes == 5:
        print("* *")
        print(" * ")
        print("* *")
    if eyes == 6:
        print("* *")
        print("* *")
        print("* *")

for i in range(10):
    dice(random.randint(1,6))
    print("---")