import turtle

def draw_branch(t, length, width, level):
    if level > 4:  # Stop after 4 levels of branching
        return
    # Make branches thinner as they go up
    t.pensize(width)
    
    # Draw current branch
    t.forward(length)
    
    if level < 4:  # Only branch if not at max level
        pos = t.pos()
        angle = t.heading()
        
        # Right branch
        t.right(30)
        draw_branch(t, length * 0.7, width * 0.6, level + 1)  # More dramatic length reduction
        
        # Return to branch point
        t.penup()
        t.goto(pos)
        t.setheading(angle)
        t.pendown()
        
        # Left branch
        t.left(30)
        draw_branch(t, length * 0.7, width * 0.6, level + 1)  # More dramatic length reduction
        
        # Return to start
        t.penup()
        t.goto(pos)
        t.setheading(angle)
        t.pendown()

# Set up the screen
screen = turtle.Screen()
screen.bgcolor("white")
t = turtle.Turtle()
t.speed(0)  # Fastest speed
t.left(90)  # Point upward


# Start position
t.penup()
t.goto(0, -200)  # Started lower to accommodate longer trunk
t.pendown()

# Draw trunk (brown)
t.color("brown")
t.pensize(13)
t.forward(110)  # Made trunk twice as long

# Draw main branches (darker green)
t.color("#006400")  # Dark green color
start_pos = t.pos()
start_angle = t.heading()

# First right main branch
t.right(30)
draw_branch(t, 70, 10, 1)  # Shorter initial branch length

# Return and draw left main branch
t.penup()
t.goto(start_pos)
t.setheading(start_angle)
t.pendown()
t.left(30)
draw_branch(t, 70, 10, 1)  # Shorter initial branch length

# Hide turtle and keep window open
t.hideturtle()
screen.mainloop()