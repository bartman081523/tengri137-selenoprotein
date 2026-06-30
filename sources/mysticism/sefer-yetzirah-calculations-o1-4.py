import math
import matplotlib.pyplot as plt
import numpy as np

###############################################################################
# 1) Definitions from Sefer Yetzirah perspective
###############################################################################

# Hebrew letters broken down by category:
MOTHERS = ['א', 'מ', 'ש']  # 3 Mothers
DOUBLES = ['ב', 'ג', 'ד', 'כ', 'פ', 'ר', 'ת']  # 7 Doubles
# The total 22 standard letters:
ALL_LETTERS_22 = [
    'א','ב','ג','ד','ה','ו','ז','ח','ט','י',
    'כ','ל','מ','נ','ס','ע','פ','צ','ק','ר','ש','ת'
]
# The 12 Simples = the rest (22 minus 3 mothers minus 7 doubles)
SIMPLES = sorted(
    set(ALL_LETTERS_22) - set(MOTHERS) - set(DOUBLES),
    key=ALL_LETTERS_22.index
)

# A list of the 10 Sefirot, as often enumerated (in a later tradition):
# Keter, Chokhmah, Binah, Chesed, Gevurah, Tiferet, Netzach, Hod, Yesod, Malkhut
# We'll label them in Hebrew or abbreviated references for demonstration.
SEFIROT_HEBREW = [
    'כתר','חכמה','בינה','חסד','גבורה',
    'תפארת','נצח','הוד','יסוד','מלכות'
]

# Combine them for reference
NUM_SEFIROT = 10

###############################################################################
# 2) Helper functions to get circular coordinates
###############################################################################

def circle_positions(num_points, radius=1.0, start_angle=0.0):
    """
    Return a list of (x,y) coordinates equally spaced around a circle.
    :param num_points: number of points to place
    :param radius: radius of the circle
    :param start_angle: offset in degrees for the first point
    :return: list of tuples (x,y)
    """
    coords = []
    for i in range(num_points):
        # angle in radians
        angle = math.radians(start_angle + i*(360.0/num_points))
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        coords.append((x, y))
    return coords

###############################################################################
# 3) Building the 231 "Gates"
###############################################################################

def generate_231_gates(letters):
    """
    Generate list of all combos (pairs) of the 22 letters, ignoring order.
    As Sefer Yetzirah says: 'א' with all, 'ב' with all, etc...
    That yields 231 distinct pairs.
    """
    pairs = []
    n = len(letters)
    for i in range(n):
        for j in range(i+1, n):
            pairs.append((letters[i], letters[j]))
    return pairs

###############################################################################
# 4) Main Visualization
###############################################################################

def visualize_sefer_yetzirah():
    """
    Visualize a stylized arrangement:
    1) Outer ring with the 22 letters.
    2) Draw 231 lines between every pair of letters (the 231 'gates').
    3) 6 directions from center (Up, Down, East, West, North, South).
    4) An inner ring with 10 Sefirot plotted as points around a smaller circle.
    """
    # Setup figure
    fig, ax = plt.subplots(figsize=(10,10))
    ax.set_aspect('equal')
    ax.set_title("Sefer Yetzirah: Letters, Gates, Directions, and Sefirot\n(אִמּוֹת, כְּפוּלוֹת, פְּשׁוּטוֹת)")

    # Hide axes
    ax.axis('off')

    ########### 4.1) Outer ring for the 22 letters ###########
    letter_positions = circle_positions(num_points=22, radius=8.0, start_angle=90.0)
    # We store a dict { letter: (x,y) } for easy referencing
    letter_coords = {}
    for letter, (x,y) in zip(ALL_LETTERS_22, letter_positions):
        letter_coords[letter] = (x,y)

    ########### 4.2) Plot the letters, color-coded ###########
    # We'll color mothers as red, doubles as green, simples as blue
    for letter in ALL_LETTERS_22:
        (x, y) = letter_coords[letter]

        if letter in MOTHERS:
            color = 'red'
        elif letter in DOUBLES:
            color = 'green'
        else:
            color = 'blue'

        # Plot a point
        ax.plot(x, y, marker='o', markersize=12, color=color, zorder=5)

        # Add text label (the letter)
        ax.text(x, y, letter, ha='center', va='center', fontsize=14, color='white', zorder=6)

    ########### 4.3) 231 Gates: draw lines between each pair ###########
    gates = generate_231_gates(ALL_LETTERS_22)
    # We'll draw each line in a light gray alpha so it doesn't overshadow
    for (l1, l2) in gates:
        x1, y1 = letter_coords[l1]
        x2, y2 = letter_coords[l2]
        ax.plot([x1, x2], [y1, y2], color='gray', linewidth=0.5, alpha=0.3, zorder=1)

    ########### 4.4) 6 directions from center ###########
    # The text references “מעלה ומטה, מזרח ומערב, צפון ודרום”
    # We'll interpret them as lines from the center (0,0).
    directions = {
        'Up': (0, 1),
        'Down': (0, -1),
        'East': (1, 0),
        'West': (-1, 0),
        'North': (0.7, 0.7),   # stylized NW or NE? We'll pick something
        'South': (-0.7, -0.7)
    }
    # We can simply scale them so they reach near the ring of letters
    length = 5.5
    for dir_name, (dx, dy) in directions.items():
        # End coords
        x2 = dx*length
        y2 = dy*length
        ax.plot([0,x2], [0,y2], color='black', linewidth=1.5, zorder=2)
        # Optionally label them
        ax.text(x2, y2, dir_name, fontsize=10, ha='center', va='center', color='black')

    ########### 4.5) The 10 Sefirot as an inner ring ###########
    # We place them on a smaller circle
    sefirah_positions = circle_positions(num_points=10, radius=3.0, start_angle=90.0)
    for (sef_name, (sx,sy)) in zip(SEFIROT_HEBREW, sefirah_positions):
        # Plot a small circle
        ax.plot(sx, sy, marker='o', markersize=8, color='purple', zorder=5)
        # Label with the Hebrew Sefirah name
        ax.text(sx, sy, sef_name, ha='center', va='center', fontsize=10, color='white', zorder=6)

    # Adjust plot limits
    ax.set_xlim(-9, 9)
    ax.set_ylim(-9, 9)

    # Show or save
    plt.show()

###############################################################################
# 5) main
###############################################################################

def main():
    visualize_sefer_yetzirah()

if __name__ == "__main__":
    main()
