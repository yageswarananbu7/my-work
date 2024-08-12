import random

# Define the snake and ladder positions
snakes = {16: 6, 47: 26, 49: 11, 56: 53, 62: 19, 64: 60, 87: 24, 93: 73, 95: 75, 98: 78}
ladders = {1: 38, 4: 14, 9: 31, 21: 42, 28: 84, 36: 44, 51: 67, 71: 91, 80: 100}


# Function to roll the dice
def roll_dice():
    return random.randint(1, 6)


# Function to move the player
def move_player(player_pos, roll):
    player_pos += roll
    if player_pos > 100:
        player_pos -= roll
    elif player_pos in snakes:
        print(f"Oh no! Snake bite at {player_pos}. Go down to {snakes[player_pos]}.")
        player_pos = snakes[player_pos]
    elif player_pos in ladders:
        print(f"Yay! Ladder at {player_pos}. Climb up to {ladders[player_pos]}.")
        player_pos = ladders[player_pos]
    return player_pos


# Main function to play the game
def play_game():
    player1_pos = 0
    player2_pos = 0

    while player1_pos < 100 and player2_pos < 100:
        input("Player 1, press Enter to roll the dice.")
        roll = roll_dice()
        print(f"Player 1 rolled a {roll}.")
        player1_pos = move_player(player1_pos, roll)
        print(f"Player 1 is now at position {player1_pos}.")

        if player1_pos == 100:
            print("Player 1 wins!")
            break

        input("Player 2, press Enter to roll the dice.")
        roll = roll_dice()
        print(f"Player 2 rolled a {roll}.")
        player2_pos = move_player(player2_pos, roll)
        print(f"Player 2 is now at position {player2_pos}.")

        if player2_pos == 100:
            print("Player 2 wins!")
            break


if __name__ == "__main__":
    play_game()
