class Story:
    def __init__(self):
        self.current_scene = 'intro'
        self.game_over = False
        self.scenes = {
            'intro': {
                'description': 'You are in your spaceship, ready to launch. Do you want to start the engine?',
                'options': ['Yes', 'No'],
            },
            'engine_start': {
                'description': 'The engine roars to life and your journey begins. Suddenly, an alien ship appears. Do you want to interact?',
                'options': ['Yes', 'No'],
            },
            'interact_alien': {
                'description': 'You decide to interact with the aliens. They turn out to be friendly and help you in your journey.',
                'options': ['Continue on your journey'],
            },
            'ignore_alien': {
                'description': 'You decide to ignore the alien ship and continue on your journey. But they take offense and attack your ship.',
                'options': ['Fight back', 'Try to escape'],
            },
            'fight_back': {
                'description': 'You fight back. Do you aim for their ship or try to disable their weapons?',
                'options': ['Aim for their ship', 'Disable their weapons'],
            },
            'escape': {
                'description': 'You try to escape. Do you head towards the nearest planet or into the asteroid belt?',
                'options': ['Head towards the nearest planet', 'Into the asteroid belt'],
            },
            'disable_weapons': {
                'description': 'You disable their weapons. Do you take the opportunity to attack or attempt to communicate with them?',
                'options': ['Attack', 'Attempt to communicate'],
            },
            'aim_ship': {
                'description': 'You aim for their ship. It explodes and you are now free to continue your journey.',
                'options': ['Continue on your journey'],
            },
            'communicate': {
                'description': 'You attempt to communicate with them. They apologize and promise to leave you alone.',
                'options': ['Continue on your journey'],
            },
            'attack': {
                'description': 'You attack. The alien ship is destroyed and you continue on your journey.',
                'options': ['Continue on your journey'],
            },
            'planet': {
                'description': 'You head towards the nearest planet. As you approach, you see a space station. Do you dock?',
                'options': ['Yes', 'No'],
            },
            'asteroid_belt': {
                'description': 'You head into the asteroid belt. It is dangerous, but you manage to navigate through. You are now on the other side, safe from the alien ship.',
                'options': ['Continue on your journey'],
            },
            'game_over': {
                'description': 'Your ship is destroyed. This is the end of your journey.',
                'options': [],
            },
        }

    def get_current_scene(self):
        return self.scenes[self.current_scene]

    def next_scene(self, decision):
        if self.current_scene == 'intro' and decision == 1:
            self.current_scene = 'engine_start'
        elif self.current_scene == 'intro' and decision == 2:
            self.current_scene = 'game_over'
            self.game_over = True
        elif self.current_scene == 'engine_start' and decision == 1:
            self.current_scene = 'interact_alien'
        elif self.current_scene == 'engine_start' and decision == 2:
            self.current_scene = 'ignore_alien'
        elif self.current_scene == 'ignore_alien' and decision == 1:
            self.current_scene = 'fight_back'
        elif self.current_scene == 'ignore_alien' and decision == 2:
            self.current_scene = 'escape'
        elif self.current_scene == 'fight_back' and decision == 1:
            self.current_scene = 'aim_ship'
        elif self.current_scene == 'fight_back' and decision == 2:
            self.current_scene = 'disable_weapons'
        elif self.current_scene == 'escape' and decision == 1:
            self.current_scene = 'planet'
        elif self.current_scene == 'escape' and decision == 2:
            self.current_scene = 'asteroid_belt'
        elif self.current_scene == 'disable_weapons' and decision == 1:
            self.current_scene = 'attack'
        elif self.current_scene == 'disable_weapons' and decision == 2:
            self.current_scene = 'communicate'
        elif self.current_scene == 'aim_ship' and decision == 1:
            self.current_scene = 'game_over'
            self.game_over = True
        elif self.current_scene == 'attack' and decision == 1:
            self.current_scene = 'game_over'
            self.game_over = True
        elif self.current_scene == 'communicate' and decision == 1:
            self.current_scene = 'game_over'
            self.game_over = True
        elif self.current_scene == 'planet' and decision == 1:
            self.current_scene = 'game_over'
            self.game_over = True
        elif self.current_scene == 'planet' and decision == 2:
            self.current_scene = 'game_over'
            self.game_over = True
        elif self.current_scene == 'asteroid_belt' and decision == 1:
            self.current_scene = 'game_over'
            self.game_over = True
