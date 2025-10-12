import turtle as t

t.bgcolor("black")
t.pensize(2)
t.speed(0)

for i in range(6):
    for colours in ["red", "magenta", "blue", "cyan", "green", "yellow" , "white"]:
        t.color(colours)
        t.circle(100)
        t.left(10)
            
t.hideturtle()

