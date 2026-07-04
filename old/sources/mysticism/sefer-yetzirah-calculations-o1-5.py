#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
import matplotlib.pyplot as plt
import numpy as np

##################################################
# 1) Data from Previous Diagram
##################################################

# The 22 standard letters used in Sefer Yetzirah
ALL_LETTERS_22 = [
    'א','ב','ג','ד','ה','ו','ז','ח','ט','י',
    'כ','ל','מ','נ','ס','ע','פ','צ','ק','ר','ש','ת'
]

# Categories (from the text) to color them differently:
MOTHERS = ['א','מ','ש']                # 3 Mothers
DOUBLES = ['ב','ג','ד','כ','פ','ר','ת'] # 7 Doubles
# The 12 Simples = the rest
SIMPLES = sorted(set(ALL_LETTERS_22) - set(MOTHERS) - set(DOUBLES), key=ALL_LETTERS_22.index)

# 10 Sefirot in Hebrew (just as placeholders):
SEFIROT_HEBREW = ['כתר','חכמה','בינה','חסד','גבורה','תפארת','נצח','הוד','יסוד','מלכות']

##################################################
# 2) A Placeholder 72 Triplets
##################################################
# In actual practice, the 72 Names might differ or include final forms.
# Here’s a simple placeholder list. Adjust or replace with your actual list:
PLACEHOLDER_72_TRIPLETS = [
    "והו", "ילי", "סיט", "עלמ", "מהש", "ללה", "אכא", "ךהת", "הזי", "אלד", "לאו", "ההע", "יזל", "םבה", "הרי", "הקם", "לאו", "ךלי", "לוו", "פהל", "נלך", "ייי", "מלה", "חהו", "נתה", "האא", "ירת", "שאה", "ריי", "אום", "לךב", "ושר", "יחו", "להח", "ךוק", "מןד", "אני", "חעם", "רהע", "ייז", "ההה", "םיכ", "וול", "ילה", "סאל", "ערי", "עשל", "מיה", "והו", "דני", "החש", "עמם", "נןא", "ןית", "מבה", "פוי", "נםם", "ייל", "הרח", "םצר", "ומב", "יהה", "ענו", "מחי", "דמב", "מןק", "איע", "חבו", "ראה", "יבמ", "היי", "םום"
    # ... up to 72 total. Fill as needed.
]
# For demonstration, we won't define all 72 here. If you have the full set, just expand it.

##################################################
# 3) Helper: circle positions, gates, etc.
##################################################
def circle_positions(num_points, radius=1.0, start_angle=0.0):
    """
    Return (x,y) for num_points equally spaced around a circle.
    """
    coords = []
    for i in range(num_points):
        angle_deg = start_angle + i*(360.0/num_points)
        angle = math.radians(angle_deg)
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        coords.append((x,y))
    return coords

def generate_231_gates(letters):
    """
    Return all 2-letter combos among the given letters (231 if letters=22).
    """
    pairs = []
    n = len(letters)
    for i in range(n):
        for j in range(i+1, n):
            pairs.append((letters[i], letters[j]))
    return pairs

##################################################
# 4) The Visualization
##################################################
def visualize_sefer_yetzirah_trigrams():
    """
    1) Plots the 22 letters on a circle, color-coded by category.
    2) Draws 231 gates (light gray lines).
    3) Plots 6 directions from center: Up/Down/East/West/North/South.
    4) Plots 10 Sefirot on an inner ring.
    5) Adds a rainbow-colored path for each of the 72 triplets (total 216 letters).
    """
    fig, ax = plt.subplots(figsize=(10,10))
    ax.set_aspect('equal')
    ax.set_title("Sefer Yetzirah: Letters, Gates, Directions, Sefirot, and 72 Trigrams")

    ax.axis('off')  # no axes

    # 4.1) Outer ring for 22 letters
    letter_positions = circle_positions(num_points=22, radius=8.0, start_angle=90.0)
    letter_coords = {}
    for letter, (x,y) in zip(ALL_LETTERS_22, letter_positions):
        letter_coords[letter] = (x,y)

    # Plot letters with color coding
    for letter in ALL_LETTERS_22:
        (x,y) = letter_coords[letter]
        if letter in MOTHERS:
            color = 'red'
        elif letter in DOUBLES:
            color = 'green'
        else:
            color = 'blue'
        ax.plot(x, y, marker='o', markersize=12, color=color, zorder=5)
        ax.text(x, y, letter, ha='center', va='center', fontsize=14, color='white', zorder=6)

    # 4.2) 231 gates in light gray
    gates = generate_231_gates(ALL_LETTERS_22)
    for (l1, l2) in gates:
        x1,y1 = letter_coords[l1]
        x2,y2 = letter_coords[l2]
        ax.plot([x1,x2],[y1,y2], color='gray', linewidth=0.5, alpha=0.3, zorder=1)

    # 4.3) 6 directions
    directions = {
        'Up': (0,1),
        'Down': (0,-1),
        'East': (1,0),
        'West': (-1,0),
        'North': (0.7,0.7),
        'South': (-0.7,-0.7)
    }
    length = 5.5
    for dname, (dx,dy) in directions.items():
        ax.plot([0,dx*length],[0,dy*length], color='black', linewidth=1.5, zorder=2)
        ax.text(dx*length, dy*length, dname, fontsize=9, ha='center', va='center')

    # 4.4) 10 Sefirot on an inner ring
    sefirah_positions = circle_positions(num_points=10, radius=3.0, start_angle=90.0)
    for sef, (sx,sy) in zip(SEFIROT_HEBREW, sefirah_positions):
        ax.plot(sx, sy, marker='o', markersize=8, color='purple', zorder=5)
        ax.text(sx, sy, sef, ha='center', va='center', fontsize=10, color='white', zorder=6)

    # 4.5) Plot the 72 trigrams in rainbow
    # We'll do a color for each triplet from a rainbow colormap:
    cmap = plt.get_cmap('rainbow')
    num_triplets = len(PLACEHOLDER_72_TRIPLETS)
    for i, triplet in enumerate(PLACEHOLDER_72_TRIPLETS):
        color = cmap(i / max(num_triplets-1,1))  # rainbow scaling
        # Each triplet is 3 letters, e.g. "והו"
        # We'll parse them, ignoring if some letter isn't in the 22
        # Then draw lines letter1 -> letter2 -> letter3
        if len(triplet) != 3:
            continue  # skip if not exactly 3 letters
        coords_list = []
        for letter in triplet:
            if letter in letter_coords:
                coords_list.append(letter_coords[letter])
            else:
                # If the letter isn't in the 22 standard forms, skip or fallback
                # But for demonstration, we'll skip
                pass
        if len(coords_list) == 3:
            (x1,y1), (x2,y2), (x3,y3) = coords_list
            # Draw lines from letter1->letter2->letter3
            ax.plot([x1,x2], [y1,y2], color=color, linewidth=2, zorder=3)
            ax.plot([x2,x3], [y2,y3], color=color, linewidth=2, zorder=3)
            # Optionally mark a small circle in the midpoint
            # or an arrow, etc. But let's keep it simple.

    # Final adjustments
    ax.set_xlim(-9,9)
    ax.set_ylim(-9,9)
    plt.show()

def main():
    visualize_sefer_yetzirah_trigrams()

if __name__ == "__main__":
    main()
