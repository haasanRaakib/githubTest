import turtle

def draw_subtree(branch, size, thickness, depth, max_depth, left_turn, right_turn, shrink_factor):
    if depth > max_depth:
        return
    branch.pensize(thickness)
    branch.forward(size)
    
    if depth < max_depth:
        current_pos = branch.pos()
        current_angle = branch.heading()
        
        branch.right(right_turn)
        draw_subtree(branch, size * shrink_factor, thickness * 0.7, depth + 1, max_depth, left_turn, right_turn, shrink_factor)
        
        branch.penup()
        branch.goto(current_pos)
        branch.setheading(current_angle)
        branch.pendown()
        
        branch.left(left_turn + right_turn)
        draw_subtree(branch, size * shrink_factor, thickness * 0.7, depth + 1, max_depth, left_turn, right_turn, shrink_factor)
        
        branch.penup()
        branch.goto(current_pos)
        branch.setheading(current_angle)
        branch.pendown()

def grow_tree():
    left_turn = float(input("Enter the left branch angle (degrees): "))
    right_turn = float(input("Enter the right branch angle (degrees): "))
    initial_size = float(input("Enter the starting branch length (pixels): "))
    max_depth = int(input("Enter the node number: "))
    shrink_factor = float(input("Enter the branch length reduction factor (e.g., 0.7 for 70%): "))

    canvas = turtle.Screen()
    canvas.bgcolor("white")
    
    branch = turtle.Turtle()
    branch.speed(0)
    branch.left(90)

    branch.penup()
    branch.goto(0, -200)
    branch.pendown()
    
    branch.color("brown")
    branch.pensize(13)
    branch.forward(initial_size)
    
    branch.color("#006400")
    draw_subtree(branch, initial_size * 0.7, 10, 1, max_depth, left_turn, right_turn, shrink_factor)
    
    branch.hideturtle()
    canvas.mainloop()

grow_tree()
