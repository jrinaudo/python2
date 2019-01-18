# implementation of card game - Memory
import simplegui
import random

cards = range(8) * 2

# helper function to initialize globals
def new_game():
    global cards, state, turns, exposed, lastexposed
    random.shuffle(cards)
    state = 0
    turns = 0
    label.set_text("Turns = 0")
    exposed = [False] * len(cards)
    lastexposed = [0, 0]
    
# define event handlers
def mouseclick(pos):
    global exposed, state, turns, lastexposed
    x = pos[0] // 50
    if state == 0:
        exposed[x] = True
        lastexposed[0] = x
        turns += 1
        label.set_text("Turns = " + str(turns))
        state = 1
    elif state == 1 and not exposed[x]:
        exposed[x] = True
        lastexposed[1] = x
        state = 2
    elif state == 2 and not exposed[x]:
        if cards[lastexposed[0]] != cards[lastexposed[1]]:
            exposed[lastexposed[0]] = False
            exposed[lastexposed[1]] = False
        exposed[x] = True
        lastexposed[0] = x
        turns += 1
        label.set_text("Turns = " + str(turns))
        state = 1

# cards are logically 50x100 pixels in size    
def draw(canvas):
    x = 10
    for i in range(len(cards)):
        if exposed[i]:
            canvas.draw_text(str(cards[i]), (x, 70), 60, 'White')
        else:
            canvas.draw_polygon([[x-10, 0], [x+40, 0], [x+40, 100], [x-10, 100]], 1, 'Black', 'Green')
        x += 50

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric