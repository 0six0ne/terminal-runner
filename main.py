import time
import sys
import random
import os

# Clear the console screen (cross-platform)
os.system('cls||clear')


class GameState:
    """Holds the player’s current state: score and
    whether they have fire armor."""
    def __init__(self):
        self.score = 10
        self.has_fire_armor = False

    def modify_score(self, amount):
        """
        Adjust the player’s score.
        Args:
            amount (int): Points to add (or subtract, if negative).
        Returns:
            int: The updated score.
        """
        self.score += amount
        return self.score

    def is_game_over(self):
        """Check if the player’s score has dropped to zero or below."""
        return self.score <= 0


def print_lines_with_pause(lines, pause_time=1.5):
    """
    Print each line with a typing effect and pause afterwards.
    Args:
        lines (list[str]): Text lines to display.
        pause_time (float): Seconds to wait after each line.
    """
    for line in lines:
        type_text(line)
        time.sleep(pause_time)


def print_pause(text):
    """
    Print text with typing effect, then pause for a default duration.
    Args:
        text (str): Text to display.
    """
    type_text(text)
    time.sleep(1.5)


def type_text(text):
    """
    Simulate typing effect: print one character at a time.
    Args:
        text (str): The full string to display.
    """
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.05)
    print()  # Newline after completing the text


def get_valid_input(prompt, valid_options, error_msg=None):
    """
    Prompt the user until they enter one of the valid options.
    Args:
        prompt (str): The input prompt text.
        valid_options (list[str]): Allowed lowercase responses.
        error_msg (str, optional): Custom error message on invalid input.
    Returns:
        str: The user's validated input (lowercase).
    """
    while True:
        user_input = input(prompt).lower()
        if user_input in valid_options:
            return user_input
        # Use custom or default error message
        error_text = (
            error_msg
            or f"Invalid choice. Choose: {', '.join(valid_options)}"
        )
        print(error_text)


def handle_play_again(game_state, is_ending=False):
    """
    Ask the player if they want to restart after ending or losing.
    Args:
        game_state (GameState): Current game state instance.
        is_ending (bool): True if called after a successful ending.
    Returns:
        None or re-starts the game loop.
    """
    # Different prompt for loss vs. win
    prompt = (
        "Would you like to play again? (Y/N): "
        if is_ending else "You lost, play again? (Y/N): "
    )
    choice = get_valid_input(prompt, ["y", "n", ""])
    if choice in ["y", ""]:
        time.sleep(0.5)
        return reset_game(game_state)
    type_text("Thanks for playing!")
    sys.exit()  # Exit the program if they choose not to replay


def reset_game(game_state):
    """
    Reset the game state and restart the intro and main loop.
    Args:
        game_state (GameState): Instance to reinitialize.
    """
    game_state = GameState()      # Create a fresh GameState
    os.system("cls||clear")       # Clear the screen
    intro(game_state)             # Show the intro narrative
    main_game_loop(game_state)    # Enter the main game loop


def intro(game_state):
    """
    Display the game’s opening narrative with a typing effect.
    Args:
        game_state (GameState): Current game state (unused here).
    """
    time.sleep(1)
    print_lines_with_pause([
        "You wake up in a strange, dark place with tangled wires.",
        "As you wander a bit, you begin to realize you're inside a...",
        "Computer system."
    ])


def show_path_choices():
    """Present the two initial paths the player can choose."""
    print_lines_with_pause([
        "Ahead of you, there are two paths:",
        "1. A corridor with a red light labeled 'Firewall.'",
        "2. A pitch black tunnel labeled 'Core Access.'"
    ])


def handle_jump_sequence(success_callback, game_state):
    """
    Ask the player to type 'JUMP' to clear an obstacle.
    Args:
        success_callback (callable): Function to call on success.
        game_state (GameState): Current game state.
    """
    type_text('Type "JUMP" to jump to the opposite side')
    user_input = input("> ").upper()
    if user_input == "JUMP":
        print("Phew, that was really close!")
        time.sleep(0.5)
        success_callback(game_state)  # Continue along the successful path
    else:
        print("Looks like you made a typo.")
        handle_play_again(game_state)  # Treat typo as failure


def enter_firewall_path(game_state):
    """
    Handle the choices and obstacles when entering the Firewall path.
    Args:
        game_state (GameState): Current game state.
    """
    if game_state.has_fire_armor:
        # If player already has armor, bridge is broken—force a jump
        print_lines_with_pause([
            "You walk back into the corridor.",
            "You need to jump high this time; the bridge is broken."
        ])
        handle_jump_sequence(handle_firewall_obstacle, game_state)
    else:
        # First time through: ask if they want to risk crossing the lava bridge
        print_lines_with_pause([
            "You walk into the long, creepy corridor...",
            "You must cross a bridge with lava underneath."
        ])
        prompt = "It sounds risky. Will you do it? (Y/N): "
        if get_valid_input(prompt, ["y", "n"]) == "y":
            handle_bridge_crossing(game_state)
        else:
            print_pause("You decided not to risk it and go back.")


def handle_bridge_crossing(game_state):
    """
    Show suspense halfway across the bridge, then require a jump.
    Args:
        game_state (GameState): Current game state.
    """
    print_lines_with_pause([
        "You're halfway across the bridge, but something feels off...",
        "..",
        "..."
    ])
    handle_jump_sequence(handle_firewall_obstacle, game_state)


def handle_firewall_obstacle(game_state):
    """
    Resolve the firewall obstacle—either allow passage or force a choice.
    Args:
        game_state (GameState): Current game state.
    """
    print_pause("You make it across the bridge.")
    if game_state.has_fire_armor:
        # With armor: auto-win ending
        print_lines_with_pause([
            "The huge wall of fire blocks your path again, but you're ready.",
            "You step forward into the fire..",
            "It was hot, but you survived!",
            "You've unlocked the 'Wall Of Fire' ending!"
        ])
        type_text("Thanks for playing!")
        handle_play_again(game_state, True)
    else:
        # Without armor: present risky choices
        print_lines_with_pause([
            "A huge wall of fire is blocking your path.",
            "The heat is overwhelming—you can't pass through.",
            "There has to be a way through, right?"
        ])
        while True:
            print("Do you want to:")
            print("1. Risk walking through the fire")
            print("2. Go back")
            choice = get_valid_input("> ", ["1", "2"])
            if choice == "1":
                # 50% chance to survive fire
                print_lines_with_pause([
                    "You step into the fire..",
                    "The heat is unbearable."
                ])
                if random.random() < 0.5:
                    print_lines_with_pause([
                        "Lucky day! You emerge on the other side,",
                        "smoking but alive!",
                        "You've unlocked the 'Wall Of Fire' ending!"
                    ])
                    type_text("Thanks for playing!")
                    handle_play_again(game_state, True)
                else:
                    print_pause("Within seconds, your body gives in.")
                    handle_play_again(game_state)
                break
            elif choice == "2":
                print_pause("You decided to go back.")
                break  # Return to main loop


def handle_fan_obstacle(game_state):
    """
    Present the spinning fan obstacle in the Core Access tunnel.
    Args:
        game_state (GameState): Current game state.
    """
    print_lines_with_pause([
        "The temperature rises the further you walk...",
        "A large fan blocks your path!",
        "Its blades spin dangerously fast."
    ])
    while True:
        print("Do you want to:")
        print("1. Try to jump through the fan")
        print("2. Go back")
        choice = get_valid_input("> ", ["1", "2"])
        if choice == "1":
            # 50% chance to pass the fan unscathed
            print_lines_with_pause([
                "You take a deep breath and prepare to jump...",
                "This is going to be risky!"
            ])
            if random.random() < 0.5:
                print_lines_with_pause([
                    "Perfect timing! You pass through safely!",
                    "You've unlocked the 'Spinning Blades' ending!"
                ])
                type_text("Thanks for playing!")
                handle_play_again(game_state, True)
            else:
                print_pause("The fan's blades were too fast...")
                handle_play_again(game_state)
            break
        elif choice == "2":
            # Return to main area
            print_pause("You decide to go back to the main area.")
            main_game_loop(game_state)
            break


def enter_core_access(game_state):
    """
    Handl the choices when entering the Core Access tunnel.
    Args:
        game_state (GameState): Current game state.
    """
    print_pause("You enter the Core Access tunnel.")
    if game_state.has_fire_armor:
        # If already have armor, proceed to fan
        print_pause("You continue on your way.")
        handle_fan_obstacle(game_state)
    else:
        # Otherwise, offer to press a mysterious button
        print_pause("It's dark and quiet, but you spot a button...")
        prompt = "Do you press the button? (Y/N): "
        if get_valid_input(prompt, ["y", "n"]) == "y":
            handle_random_event(game_state)
        else:
            print_pause("You don't press the button and continue.")
            handle_fan_obstacle(game_state)


def handle_random_event(game_state):
    """
    Randomly trigger an explosion (death) or reveal fire armor.
    Args:
        game_state (GameState): Current game state.
    """
    if random.choice(["explosion", "door_open"]) == "explosion":
        print_lines_with_pause([
            "You feel the ground shaking heavily...",
            "What's that sound?",
            "..",
            "IT'S AN EXPLOSIO- 💥"
        ])
        handle_play_again(game_state)
    else:
        print_lines_with_pause([
            "The button opens a hidden door in the wall...",
            "You step through and find a shining fire protection armor!"
        ])
        start_trivia_game(game_state)


def return_to_core_access(game_state):
    """
    Aftr trivia (or failure), let the player decide where to go next.
    Args:
        game_state (GameState): Current game state.
    """
    prompt = "Go to the firewall corridor? (Y/N): "
    choice = get_valid_input(prompt, ["y", "n"])
    if choice == "y":
        enter_firewall_path(game_state)
    else:
        print_lines_with_pause([
            "You're back in the Core Access tunnel.",
            "You try to locate the button again...",
            "But it's vanished. You continue on."
        ])
        handle_fan_obstacle(game_state)


def start_trivia_game(game_state):
    """
    Present a tech trivia question.

    Correct answer awards fire armor; incorrect one penalizes score.
    Args:
        game_state (GameState): Current game state.
    """
    print_pause("To claim it, pass a fun trivia question.")
    questions = [
        {
            "question": "What does CPU stand for?",
            "options": (
                "A) Central Processing Unit  B) Computer Personal Unit  "
                "C) Central Peripheral Unit"
            ),
            "answer": "a"
        },
        {
            "question": "Which of these is an OS?",
            "options": "A) Python  B) Linux  C) HTML",
            "answer": "b"
        },
        {
            "question": "What does RAM stand for?",
            "options": (
                "A) Random Access Memory  B) Readily Available Memory  "
                "C) Rapid Action Module"
            ),
            "answer": "a"
        }
    ]
    # Pick a random question
    question = random.choice(questions)
    print_pause(question["question"])
    print(question["options"])
    user_input = get_valid_input("> ", ["a", "b", "c"])
    if user_input == question["answer"]:
        # Reward correct answer
        print_lines_with_pause([
            "Correct! You've earned the fire protection armor.",
            "Now revisit the firewall..."
        ])
        game_state.modify_score(5)
        game_state.has_fire_armor = True
    else:
        # Penalize incorrect answer
        print_lines_with_pause([
            "Incorrect! The armor stays locked.",
            "The floor splits open!"
        ])
        game_state.modify_score(-5)
    # Return to core vs. firewall based on choice
    return_to_core_access(game_state)


def main_game_loop(game_state):
    """
    Repeatedly show path choices until the game ends or player quits.
    Args:
        game_state (GameState): Current game state.
    """
    while True:
        show_path_choices()
        # If score has dropped, prompt for replay
        if game_state.is_game_over():
            handle_play_again(game_state)
        choice = get_valid_input(
            "Where do you go from here? The choice is yours: ", ["1", "2"]
        )
        if choice == "1":
            enter_firewall_path(game_state)
        elif choice == "2":
            enter_core_access(game_state)


if __name__ == '__main__':
    # Initialize and start the game
    game_state = GameState()
    os.system("cls||clear")
    intro(game_state)
    main_game_loop(game_state)
