import pygame

score = 0
total_score = 0
health = 100
word_amount = 5

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
    if (total_score >= 25):
        return (word_amount + 2)
    elif (total_score >= 50):
        return (word_amount + 2)
    elif (total_score >= 75):
        return (word_amount + 2)
    elif (total_score >= 100):
        return (word_amount + 2)

for i in range (5):
    print(player_score(5))
    print(player_score(10))
print(status(100)) # The falling word hasn't hit the floor yet!
print(status(0)) # The falling word has hit the floor!
