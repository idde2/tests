import turtle
import math

def real_pow_23(x):
    return (x*x)**(1/3)

t = turtle.Turtle()
t.speed(0)
t.penup()

axis = turtle.Turtle()
axis.speed(0)

axis.penup()
axis.goto(-300, 0)
axis.pendown()
axis.goto(300, 0)

axis.penup()
axis.goto(0, -300)
axis.pendown()
axis.goto(0, 300)


first = True

for i in range(2000):

    x = (i - 1000) / 300  # Bereich ca. -3.3 bis +3.3

    inside = 3 - x*x
    if inside < 0:
        continue

    try:
        # y = real_pow_23(x) + math.sqrt(inside) * math.sin(16 * math.pi * x) #heart
        # y = (inside ** math.sin(inside * math.pi)) #random gebirge
        #y = 1.5*math.e**(-0.3*((x+2)**2 + x**2)) + 1.5*math.e**(-0.3*((x-2)**2 + x**2))
        y = math.log(inside)
    except ZeroDivisionError:
        y = 1

    if first:
        t.goto(x * 80, y * 80)
        t.pendown()
        first = False
    else:
        t.goto(x * 80, y * 80)



turtle.done()
