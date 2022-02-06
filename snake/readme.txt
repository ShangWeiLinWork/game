=== Overview ===
There are two versions of snake game, one with excel and one with pygame
Both versions were created by following Clear Code's exremely clear tutorials. Thank you Clear Code!

tutorial links:
- Snake in Excel with Python (& xlwings): https://www.youtube.com/watch?v=kayebcQ8pFw
- Learning pygame by creating Snake [python tutorial]: https://www.youtube.com/watch?v=QFvqStqPCRU

Overall
- it was fun and not difficult with the clear instructions. Again, thank you Clear Code!
- I felt satisfied when I got the game running
- I got to practice xlwings, pygame, and writing class in Python

=== Some Custom Changes ===
I basically followed the logic of clear code
but I did tweek some details so they made more sense to me, so there are some minor differences, and here are a few noticible ones (that I remember):

snake_xlwings.py
- I used python index convention when setting the board size, incase we want super large board that exceed the z column
- When I use excel index convention, I didn't reformat (I kept $A$1, instead of changing it to A1)

snake_pygame.py
- I drew the snake and apple graphics with paint, and record the sound effect; I used a different font I downloaded
font link: https://www.dafont.com/little-comet.font
- I used a different logic when plotting the checkerboard (by checking if row + col is even or odd)

=== Bugs ===
Here are some bugs I am aware of but haven't fixed yet.
Since I did tweek some code, and not just the one I listed above, these bugs may just exist in my code and not in Clear Code's original version

snake_pygame.py
- when I press really fast in a certain way, I think the head can turn 180 degrees and hit itself. The code currently only prevents turning 180 degrees in one key press.


