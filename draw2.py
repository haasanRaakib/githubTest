import turtle

# Recursive function to draw branches
def draw_branch(t, length, width, level, max_level, left_angle, right_angle, reduction_factor):
    if level > max_level:  # Stop after the max recursion depth
        return
    
    # Set the pen size based on the branch width
    t.pensize(width)
    
    # Draw the current branch
    t.forward(length)
    
    # If we haven't reached the max recursion depth, draw the sub-branches
    if level < max_level:
        # Save the current position and angle
        pos = t.pos()
        angle = t.heading()
        
        # Draw the right sub-branch
        t.right(right_angle)
        draw_branch(t, length * reduction_factor, width * 0.7, level + 1, max_level, left_angle, right_angle, reduction_factor)
        
        # Return to the original position and heading
        t.penup()
        t.goto(pos)
        t.setheading(angle)
        t.pendown()
        
        # Draw the left sub-branch
        t.left(left_angle + right_angle)  # Adjust the angle to the left
        draw_branch(t, length * reduction_factor, width * 0.7, level + 1, max_level, left_angle, right_angle, reduction_factor)
        
        # Return to the original position and heading
        t.penup()
        t.goto(pos)
        t.setheading(angle)
        t.pendown()

# Main function to set up the turtle and gather user input
def draw_tree():
    # Ask for user input
    left_angle = float(input("Enter the left branch angle (degrees): "))
    right_angle = float(input("Enter the right branch angle (degrees): "))
    start_length = float(input("Enter the starting branch length (pixels): "))
    max_depth = int(input("Enter the node number: "))
    reduction_factor = float(input("Enter the branch length reduction factor (e.g., 0.7 for 70%): "))
    
    # Set up the screen
    screen = turtle.Screen()
    screen.bgcolor("white")
    
    # Create a turtle object
    t = turtle.Turtle()
    t.speed(0)  # Fastest speed
    t.left(90)  # Point upward

    # Start drawing from the trunk position
    t.penup()
    t.goto(0, -200)  # Move the turtle lower for the trunk
    t.pendown()
    
    # Set the initial branch color and width
    t.color("brown")
    t.pensize(13)
    
    # Draw the trunk (the first branch)
    t.forward(start_length)
    
    # Draw the tree with recursive branches (using user input)
    t.color("#006400")  # Dark green color for branches
    draw_branch(t, start_length * 0.7, 10, 1, max_depth, left_angle, right_angle, reduction_factor)
    
    # Hide the turtle after drawing
    t.hideturtle()
    
    # Keep the window open
    screen.mainloop()

# Call the main function to start the program
draw_tree()
