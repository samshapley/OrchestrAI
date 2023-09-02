from story import Story

class Game:
    def __init__(self):
        self.story = Story()
    
    def start_game(self):
        print("Welcome to the Space Adventure!")
        print("Your goal is to navigate through space, make the right decisions and reach your destination.")
        print("Good luck!")
        self.game_loop()
    
    def game_loop(self):
        while True:
            current_scene = self.story.get_current_scene()
            print(current_scene['description'])
            for i, option in enumerate(current_scene['options'], start=1):
                print(f'{i}. {option}')
            decision = input("Enter your decision: ")
            if not decision.isdigit() or int(decision) not in range(1, len(current_scene['options']) + 1):
                print("Invalid decision, please enter a valid number.")
            else:
                self.story.next_scene(int(decision))
                if self.story.game_over:
                    print("Game Over!")
                    break

if __name__ == "__main__":
    game = Game()
    game.start_game()
