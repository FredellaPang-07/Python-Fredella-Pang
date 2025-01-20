# CPSC217S24A2-FredellaPangBONUS.py

# DO NOT EDIT THE FOLLOWING LINES
# COURSE CPSC 217 Spring 2024
# INSTRUCTOR: Jonathan Hudson
# XywaW4RTguuM1XLxXdlD
# DO NOT EDIT THE ABOVE LINES

# INFORMATION FOR YOUR TA
# Name: Fredella Pang
# Student UCID: 30247875
""" Description: This program asks for user input in order to draw constellations cycling through six colors. 
It will also name stars and constellations as well as draw boxes around constellations if prompted by user.
"""

from SimpleGraphics import *

# STYLE CONSTANTS
BORDER = 25
DIRECTION_OFFSET = 15
BKG_COLOR = "black"
LINE_COLOR = "white"
COLOR_LIST = ["red", "yellow", "green", "blue", "violet", "pink"]
NAMEOFFSET = 10
BOXBORDER = 15

# AXIS CONSTANTS
XAXIS_STEP = 0.1
YAXIS_STEP = 0.1
TICKLENGTH = 10
XNUMBER_TICKS = 9  # excluding zero/center
YNUMBER_TICKS = 9
XAXISPOS = 0.1
XAXISNEG = -0.1
YAXISPOS = 0.1
YAXISNEG = -0.1
YAXIS_STEP = 0.1
OFFSET = 15 

# WINDOW
size = 0  # Assume invalid size
while size < 600:  # Ask until size no longer unvalid (>=600 pixels)
    # Get user input on size of window
    size = int(input("Choose an integer pixel size >= 600 for the constellation: "))
# Set up the window to draw in
border_size = size + (BORDER * 2)  # Total window size = window size input with borders
resize(border_size, border_size)
background(BKG_COLOR)
center = border_size / 2
# Draw directions
setFont("arial", "bold")
setOutline(LINE_COLOR)
text(DIRECTION_OFFSET, center, "W")  # Left border
text(border_size - DIRECTION_OFFSET, center, "E")  # Right border
text(center, DIRECTION_OFFSET, "N")  # Top border
text(center, border_size - DIRECTION_OFFSET, "S")  # Bottom border

# AXES
# POST-SIZE INPUT CALCULATIONS AND CONSTANTS (FOR AXES)
tick_calc = TICKLENGTH / 2  # ticks are drawn (ticklength * 0.5) pixels away from center
xtotal_steps = (XNUMBER_TICKS * 2) + 2  # used to calculate stepsize
ytotal_steps = (YNUMBER_TICKS * 2) + 2  # ^^
axislocationxpos = center
axislocationxneg = center
axislocationypos = center
axislocationyneg = center
xaxis_stepsize = (size / xtotal_steps)  # distance between each tick
yaxis_stepsize = (size / ytotal_steps)  # ^^

# Get user input to show axis
axis_visible = False
axis_continue = False
axis_input = "x"  # Assume invalid axis input in order to enter while loop --> which exits when a 'y' or 'n' is entered
while axis_continue == False:
    if axis_input.upper() == "Y":  # Allows for uppercase and lowercase Y
        axis_continue = True  # Change flag to exit loop
        axis_visible = True
    elif axis_input.upper() == "N":  # Allows for uppercase and lowercase N
        axis_continue = True  # Change flag to exit loop
        axis_visible = False
    else:
        axis_input = (input("Enter Y/N to show/hide axis: "))

# If showing axis, draw circle, axes and ticks
if axis_visible == True:
    setOutline(LINE_COLOR)
    setFill(BKG_COLOR)
    # Draw circle
    ellipse(BORDER, BORDER, size, size)
    # Draw x and y axis (centered)
    line(BORDER, center, border_size - BORDER, center)
    line(center, BORDER, center, border_size - BORDER)
    # Draw and label x-axis ticks
    for x in range(XNUMBER_TICKS):
        # positive axis ticks
        axislocationxpos += xaxis_stepsize  # ticks move right
        text(axislocationxpos, center + OFFSET, f"{XAXISPOS:.1f}")
        line(axislocationxpos, center + tick_calc, axislocationxpos, center - tick_calc)
        XAXISPOS += XAXIS_STEP  # number goes up by 0.1
        # negative axis ticks
        axislocationxneg -= xaxis_stepsize  # ticks move left
        text(axislocationxneg, (center + OFFSET), f"{XAXISNEG:.1f}")
        line(axislocationxneg, (center + tick_calc), axislocationxneg, (center - tick_calc))
        XAXISNEG -= XAXIS_STEP  # number goes down by 0.1
    # Draw and label y axis ticks
    for y in range(YNUMBER_TICKS):
        # positive axis ticks
        axislocationypos -= yaxis_stepsize  # ticks move down
        text(center + OFFSET, axislocationypos, f"{YAXISPOS:.1f}")
        line(center + tick_calc, axislocationypos, center - tick_calc, axislocationypos)
        YAXISPOS += YAXIS_STEP  # number goes up by 0.1
        # negative axis ticks
        axislocationyneg += yaxis_stepsize  # ticks move up
        text(center + OFFSET, axislocationyneg, f"{YAXISNEG:.1f}")
        line(center + tick_calc, axislocationyneg, center - tick_calc, axislocationyneg)
        YAXISNEG -= YAXIS_STEP  # number goes down by 0.1

# BONUS QUESTIONS:

# Get user input to show star name
sname_flag = False
sname_visible = False
sname_input = "0"  # (input("Enter Y/N to input star names: "))
while sname_flag == False:
    if sname_input.upper() == "Y":  # allows for uppercase and lowercase Y
        sname_flag = True
        sname_visible = True
    elif sname_input.upper() == "N":  # allows for uppercase and lowercase N
        sname_flag = True
        sname_visible = False
    else:
        sname_input = (input("Enter Y/N to input star names: "))
# Get user input to show constellation box
cbox_flag = False
cbox_visible = False
cbox_input = "0"
while cbox_flag == False:
    if cbox_input.upper() == "Y":  # allows for uppercase and lowercase Y
        cbox_flag = True
        cbox_visible = True
    elif cbox_input.upper() == "N":  # allows for uppercase and lowercase N
        cbox_flag = True
        cbox_visible = False
    else:
        cbox_input = (input("Enter Y/N to input show/hide constellation box: "))
# Get user input to show constellation name
cname_flag = False
cname_visible = False
cname_input = (input("Enter Y/N to input show/hide constellation name: "))
while cname_flag == False:
    if cname_input.upper() == "Y":  # Allows for uppercase and lowercase Y
        cname_flag = True
        cname_visible = True
    elif cname_input.upper() == "N":  # Allows for uppercase and lowercase N
        cname_flag = True
        cname_visible = False
    else:
        cname_input = (input("Enter Y/N to input show/hide constellation name: "))

# *** CONSTELLATIONS ***

count_color = -1  # When first constellation is displayed, it will use COLOR_LIST[0], which is red
count_stars = 1  # Assume making one constellation
while count_stars > 0:  # Continue to make constellations until given 0 or a negative number of star count --> exit program + display done message (Pre-test)
    # Get constellation star count
    count_stars = (input("Input how many stars to plot for constellation (<= to exit): "))

    if count_stars == "":
        count_stars = 1
        continue
    else:
        count_stars = int(count_stars)
    # STARS
    for star in range(count_stars):  # Loop to get input and draw each star
        # Get input for star (magnitude, followed by x and then y coordinates)
        star_magnitude = float(input("Give star magnitude: "))
        x_star = float(input("Give star x coordinate: "))
        y_star = float(input("Give star y coordinate: "))

        # Do conversions for drawing
        star_size = 13 / (star_magnitude + 2.5)
        x_star = (x_star / XAXIS_STEP * xaxis_stepsize) + center - (
                    star_size / 2)  # Convert to pixel coordinates then center it
        y_star = (-1 * y_star / YAXIS_STEP * yaxis_stepsize) + center - (star_size / 2)
        star_color = (1 - ((star_magnitude + 1.5) / 12)) * 255

        # Draw star
        setColor(star_color, star_color, star_color)
        ellipse(x_star, y_star, star_size, star_size)

        # If star name is shown, ask and display name
        if sname_visible == True:
            sname = input("What is star name: ")
            text(x_star + NAMEOFFSET, y_star - NAMEOFFSET, sname)

    if count_stars > 0:  # Proceed with remainder of program if user has not inputed 0 or negative number for star count (Post-test)
        
         # Calculates the pixel coordinates of inputted x coordinates (for lines only)
        def calcx(coord, step=XAXIS_STEP, stepsize=xaxis_stepsize, center=center):
            n = (coord / step * stepsize) + center
            return n
        # Calculates the pixel coordinates of inputted x coordinates (for lines only)
        def calcy(coord, step=YAXIS_STEP, stepsize=yaxis_stepsize, center=center):
            n = ((-1 * coord) / step * stepsize) + center
            return n
        
        # EDGES
        # Cycle 6 colors for constellation edges
        if count_color < 5:
            count_color += 1
        else:
            count_color = 0

        # Lists to store coordinates of edges (for borders)
        list_x_edge = []
        list_y_edge = []

        # Get number of edges to draw
        count_edge = int(input("Input how many edges to plot for constellation (<= to exit): "))

        if count_edge == 0 or count_edge == "": # If no edge is inputted, use star coordinates (pixel)
            list_x_edge.append(x_star)
            list_x_edge.append(x_star)
            list_y_edge.append(y_star)
            list_y_edge.append(y_star)
            count_edge = -1 #Allows the program to proceed to naming constellation --> bypass edge input loop

        # Loop to get input for each edge --> two (x, y) coordinates | start and end
        for edge in range(count_edge):  
            x_start = float(input("Give edge start x coordinate: "))
            y_start = float(input("Give edge start y coordinate: "))
            x_end = float(input("Give edge end x coordinate: "))
            y_end = float(input("Give edge end y coordinate: "))

            # Store edge coordinates into list (to be sorted)
            list_x_edge.append(x_start)
            list_x_edge.append(x_end)
            list_y_edge.append(y_start)
            list_y_edge.append(y_end)

            # Convert arbitrary coordinates to pixel coordinates for the edge lines
            x_start = calcx(x_start)
            y_start = calcy(y_start)
            x_end = calcx(x_end)
            y_end = calcy(y_end)

            # Draw  constellation edge
            setOutline(COLOR_LIST[count_color]) # Set color for edges of constellation (cycles 6 colours due to [count_color])
            line(x_start, y_start, x_end, y_end)

        # CONSTELLATION BOX
        # If constellation box is visible, draw box
        if cbox_visible == True:
            # Sort list in ascending order to allow outermost edge coordinates to be identified
            list_x_edge.sort()  # left to right
            list_y_edge.sort()  # top to bottom

            # Box calculations
            x_box = (calcx(list_x_edge[0]) - (BOXBORDER / 2)) # Left most edge coordinate + half of border
            y_box = (calcy(list_y_edge[-1]) - (BOXBORDER / 2)) # Top most edge coordinate + half of border
            width_box = calcx((list_x_edge[-1])) - calcx((list_x_edge[0])) + BOXBORDER # Right minus Left
            height_box = calcy(list_y_edge[0]) - calcy((list_y_edge[-1]))+ BOXBORDER # Bottom minus Top

            # If user had inputed no edge coordinates (set count_edge to "" or 0) --> disregard standard calculations and use star pixel coordinates
            if count_edge == -1:
                x_box = list_x_edge[0] - (BOXBORDER / 2)
                y_box = list_y_edge[-1] - (BOXBORDER / 2)
                width_box = BOXBORDER # No width or height to calculate --> width and height are set to border size
                height_box = BOXBORDER

            # Draw Constellation Box
            setOutline("orange")
            line(x_box, y_box, x_box + width_box, y_box, x_box + width_box, y_box + height_box, x_box,
                 y_box + height_box, x_box, y_box)

            # Empty lists to prepare for next constellation
            list_x_edge.clear()
            list_y_edge.clear()

        # CONSTELLATION NAME
        # If constellation name is visible, ask and display name --> centered and inside box
        if cname_visible == True:
            # Ask for name input
            cname = input("What is the constellation name: ")
            print(cname)

            # Name location calculations
            text_x = (width_box / 2) + x_box # centered
            text_y = y_box + NAMEOFFSET # inside box

            # Display constellation name
            setOutline(COLOR_LIST[count_color]) # Same color as constellation edges
            text(text_x, text_y, cname)
# DONE
print("Done plotting constellations")


"""
python CPSC217S24A2-FredellaPangBONUS.py< ConstellationsBonus.txt
python CPSC217S24A2-FredellaPangBONUS.py< ConstellationsOnlyBonus.txt
"""