import pygame

score = 0
total_score = 0
health = 100
word_amount = 3 # Falling word every 10 seconds or words/10s
level = 1 # Start at level 1

def status(health):
    if (health == 0):
        return ("Game Over") # If a single falling word hit the floor, minus 100 health or that means GAME OVER!
    else:
        return ("You're still alive!")

def player_score(score):
    global total_score
    total_score += score
    return (total_score)

def difficulty(total_score):
    global level, word_amount
    level = level + total_score // 25
    for i in range(level):
        word_amount += 2
    return (word_amount)

player_score(75)
player_score(1)
player_score(0)
difficulty(total_score)
print("Total Player Score: ", total_score)
print("Game Level: ", level)
print("Falling Word Amount: ", word_amount)
print("status: ", status(100)) # The falling word hasn't hit the floor yet!
print("Status: ", status(0)) # The falling word has hit the floor!
