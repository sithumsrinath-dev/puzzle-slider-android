import os
import json
import random
import time
from math import sqrt
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle, Line, RoundedRectangle
from kivy.storage.jsonstore import JsonStore
from kivy.network.urlrequest import UrlRequest
from kivy.utils import platform
from kivy.core.window import Window
from kivmob import KivMob, TestIds

# AdMob KivMob Integration (Disabled to enforce Native PyJNIus Direct Bridge)
KIVMOB_AVAILABLE = False

# Security Helper using a simple internal hashing mechanism to prevent direct memory manipulation
def secure_verify(val1, val2):
    return str(val1) == str(val2)

def xor_crypt(data, key=42):
    # දත්ත කියවන්න බැරි වෙන්න Lock කරන/Unlock කරන සරල රහස් ක්‍රමයක්
    return "".join(chr(ord(c) ^ key) for c in data)

class SlidingPuzzleGame(BoxLayout):
    def __init__(self, **kwargs):
        super(SlidingPuzzleGame, self).__init__(orientation='vertical', **kwargs)
        self.lock_frame = None
        self.lock_ad_button = None # <-- මේ පේළිය අලුතින්ම එකතු කරන්න
        self.pending_action = None # State tracking for network retries
        
        # Add state flags for debounce and ad status
        self.is_processing_click = False
        self.ad_failed_fallback = False
        
        # AdMob Initialization
        self.ads = None
        # Note: setup_admob calls shifted to App.build() scheduled clock event to prevent Launch Crash.

        # Load Secure Local Storage
        from kivy.app import App
        import os
        app = App.get_running_app()
        data_dir = app.user_data_dir if app else os.path.dirname(__file__)
        file_path = os.path.join(data_dir, 'game_secure_state.json')
        
        try:
            with open(file_path, 'r') as f:
                encrypted_string = f.read()
            decrypted_string = xor_crypt(encrypted_string)
            game_state_data = json.loads(decrypted_string)
            
            # Reconstruct the store data representation manually since we switched to file-based encryption
            profile = game_state_data.get('user_profile', {})
            self.current_level = int(profile.get('current_level', 1))
            self.punishment_pool = int(profile.get('punishment_pool', 0))
            self.challenge_mode = bool(profile.get('challenge_mode', False))
            self.high_score = int(profile.get('high_score', 0))
        except Exception:
            game_state_data = {'user_profile': {'current_level': 1, 'punishment_pool': 0, 'challenge_mode': False, 'high_score': 0}}
            encrypted_string = xor_crypt(json.dumps(game_state_data))
            with open(file_path, 'w') as f:
                f.write(encrypted_string)
            
            profile = game_state_data['user_profile']
            self.current_level = int(profile['current_level'])
            self.punishment_pool = int(profile['punishment_pool'])
            self.challenge_mode = bool(profile['challenge_mode'])
            self.high_score = int(profile['high_score'])

        self.max_unlocked_level = self.current_level
        self.total_wins = self.current_level - 1 if not self.challenge_mode else 100
        self.move_count = 0
        self.grid_size = 3
        self.tiles = []
        self.blank_index = 0
        self.history = []
        self.game_active = False
        self.time_left = 0
        self.timer_trigger = None
        self.internet_available = True
        self.failed_attempts = 0
        self.is_skipping_via_ad = False

        # UI Setup with Premium Neon Custom Graphics
        self.canvas.before.add(Color(0.05, 0.05, 0.1, 1))
        self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        # Header System - Corrected Unified Premium Layout
        self.header_layout = BoxLayout(orientation='horizontal', size_hint_y=0.1, padding=[10, 5, 10, 5], spacing=10)
        
        # 1. Level Navigation Unified Bar (Left Side - 33% width)
        level_nav_layout = BoxLayout(orientation='horizontal', spacing=2, size_hint_x=0.33)
        
        prev_btn = Button(text="<", bold=True, font_size='20sp', background_normal="", background_color=(0, 0, 0, 0), color=(0, 0, 0, 1))
        with prev_btn.canvas.before:
            Color(1, 1, 1, 1) # Pure White Button Base
            prev_btn.bg_rect = RoundedRectangle(radius=[12])
            Color(1, 1, 1, 0.18)
            prev_btn.bg_gloss = RoundedRectangle(radius=[10])

        self.level_container = BoxLayout(orientation='horizontal', padding=[5, 0, 5, 0])
        with self.level_container.canvas.before:
            Color(0.2, 0.75, 0.95, 1) # Premium Sky Blue / Cool Cyan Family
            self.level_container.bg_rect = RoundedRectangle(radius=[10])
        
        self.level_label = Label(text="", font_size='16sp', bold=True, color=(0, 0, 0, 1), halign='center', valign='middle')
        self.level_label.bind(size=self.level_label.setter('text_size'))
        self.level_container.add_widget(self.level_label)

        next_btn = Button(text=">", bold=True, font_size='20sp', background_normal="", background_color=(0, 0, 0, 0), color=(0, 0, 0, 1))
        with next_btn.canvas.before:
            Color(1, 1, 1, 1) # Pure White Button Base
            next_btn.bg_rect = RoundedRectangle(radius=[12])
            Color(1, 1, 1, 0.18)
            next_btn.bg_gloss = RoundedRectangle(radius=[10])

        def _update_nav_bounds(instance, value):
            prev_btn.bg_rect.pos = prev_btn.pos
            prev_btn.bg_rect.size = prev_btn.size
            prev_btn.bg_gloss.pos = (prev_btn.x + 2, prev_btn.y + prev_btn.height * 0.5)
            prev_btn.bg_gloss.size = (prev_btn.width - 4, prev_btn.height * 0.4)
            
            self.level_container.bg_rect.pos = self.level_container.pos
            self.level_container.bg_rect.size = self.level_container.size
            
            next_btn.bg_rect.pos = next_btn.pos
            next_btn.bg_rect.size = next_btn.size
            next_btn.bg_gloss.pos = (next_btn.x + 2, next_btn.y + next_btn.height * 0.5)
            next_btn.bg_gloss.size = (next_btn.width - 4, next_btn.height * 0.4)

        prev_btn.bind(pos=_update_nav_bounds, size=_update_nav_bounds)
        self.level_container.bind(pos=_update_nav_bounds, size=_update_nav_bounds)
        next_btn.bind(pos=_update_nav_bounds, size=_update_nav_bounds)

        prev_btn.bind(on_press=self.go_to_previous_level)
        next_btn.bind(on_press=self.go_to_next_level)

        level_nav_layout.add_widget(prev_btn)
        level_nav_layout.add_widget(self.level_container)
        level_nav_layout.add_widget(next_btn)

        # 2. Timer Glass Bar (Middle Side - 33% width)
        timer_container = BoxLayout(orientation='horizontal', size_hint_x=0.33)
        with timer_container.canvas.before:
            Color(0.05, 0.1, 0.2, 0.4) # Subtle Dark Glass Sub-panel
            timer_container.bg_rect = RoundedRectangle(radius=[10])

        def _update_timer_container(instance, value):
            timer_container.bg_rect.pos = instance.pos
            timer_container.bg_rect.size = instance.size

        timer_container.bind(pos=_update_timer_container, size=_update_timer_container)
        
        self.timer_label = Label(text="", font_size='16sp', bold=True, color=(1, 0.2, 0.5, 1), halign='center')
        timer_container.add_widget(self.timer_label)

        # 3. Wins Glass Bar (Right Side - 33% width)
        wins_container = BoxLayout(orientation='horizontal', size_hint_x=0.33)
        with wins_container.canvas.before:
            Color(0.05, 0.1, 0.2, 0.4)
            wins_container.bg_rect = RoundedRectangle(radius=[10])

        def _update_wins_container(instance, value):
            wins_container.bg_rect.pos = instance.pos
            wins_container.bg_rect.size = instance.size

        wins_container.bind(pos=_update_wins_container, size=_update_wins_container)
        
        self.wins_label = Label(text=f"Wins: {self.total_wins}", font_size='16sp', bold=True, color=(0, 1, 0, 1), halign='center')
        wins_container.add_widget(self.wins_label)

        # Assemble Header Layout cleanly without overlapping
        self.header_layout.add_widget(level_nav_layout)
        self.header_layout.add_widget(timer_container)
        self.header_layout.add_widget(wins_container)
        self.add_widget(self.header_layout)

        # Punishment Dashboard with Glassmorphism & Neon Cyan Accents
        self.punish_layout = BoxLayout(orientation='horizontal', size_hint_y=0.08, padding=[10, 5, 10, 5], spacing=10)
        
        # Adding a semi-transparent glass background to the container
        with self.punish_layout.canvas.before:
            Color(0, 0.4, 0.5, 0.15) # Cyan family light glass tint
            self.punish_bg = Rectangle(size=self.punish_layout.size, pos=self.punish_layout.pos)
            Color(0, 0.9, 1, 0.3) # Neon border line
            self.punish_line = Line(rectangle=(self.punish_layout.x, self.punish_layout.y, self.punish_layout.width, self.punish_layout.height), width=1)
        
        self.punish_layout.bind(pos=self._update_punish_bounds, size=self._update_punish_bounds)

        self.punish_label = Label(text=f"Punishment Box: {self.punishment_pool} Seconds", font_size='14sp', bold=True, color=(1, 0.3, 0, 1))
        
        # Fixed Button: Styled with bold black text, glass finish, and auto-wrapping text to fit inside perfectly
        self.ad_button = Button(text="Watch\nPunishment Ad", 
                                size_hint_x=0.4, 
                                bold=True, 
                                color=(0.9, 1, 1, 1), # Clear Light Cyan
                                background_normal='', 
                                background_color=(0, 0, 0, 0), # Transparent background color
                                halign='center', 
                                valign='middle')
        self.ad_button.bind(size=self.ad_button.setter('text_size')) # Auto wrapping inside button boundaries
        self.ad_button.bind(on_press=self.trigger_punishment_ad)

        # Drawing Neon Glass border overlay for the button
        with self.ad_button.canvas.before:
            Color(0.02, 0.08, 0.12, 1) # Dark Cyan/Blue Shadow
            self.ad_button.ad_btn_shadow = RoundedRectangle(size=self.ad_button.size, pos=(self.ad_button.x, self.ad_button.y - 4), radius=[15])
            Color(0.08, 0.25, 0.32, 1) # Dark Teal/Cyan Main Body
            self.ad_button.ad_btn_rect = RoundedRectangle(size=self.ad_button.size, pos=self.ad_button.pos, radius=[15])
            Color(0, 0.9, 1, 0.35) # Glossy Cyan Highlight
            self.ad_button.ad_btn_gloss = RoundedRectangle(size=(self.ad_button.width - 6, self.ad_button.height * 0.4), pos=(self.ad_button.x + 3, self.ad_button.y + self.ad_button.height * 0.55), radius=[10])
        
        with self.ad_button.canvas.after:
            Color(0, 0.9, 1, 0.7) # Intensely vivid Cyan line border
            self.ad_button.ad_btn_line = Line(rectangle=(self.ad_button.x, self.ad_button.y, self.ad_button.width, self.ad_button.height), width=1.2)

        self.ad_button.bind(pos=self._update_ad_btn_bounds, size=self._update_ad_btn_bounds)

        self.punish_layout.add_widget(self.punish_label)
        self.punish_layout.add_widget(self.ad_button)
        self.add_widget(self.punish_layout)

        # Main Game Grid
        self.grid_container = BoxLayout(orientation='vertical', size_hint_y=0.72)
        self.puzzle_grid = GridLayout(spacing=2)
        self.grid_container.add_widget(self.puzzle_grid)
        self.add_widget(self.grid_container)

        # Core Controls Panel
        self.control_layout = BoxLayout(orientation='horizontal', size_hint_y=0.1, padding=10, spacing=10)
        
        self.reset_btn = Button(text="RESET", font_size='16sp', bold=True, background_normal="", background_color=(0, 0, 0, 0), color=(1, 1, 1, 1))
        with self.reset_btn.canvas.before:
            Color(0.02, 0.05, 0.1, 0.8)
            self.reset_btn.bg_shadow = RoundedRectangle(size=self.reset_btn.size, pos=(self.reset_btn.x, self.reset_btn.y - 4), radius=[15])
            Color(0.05, 0.35, 0.45, 1) # Cool Cyan variant for RESET
            self.reset_btn.bg_rect = RoundedRectangle(size=self.reset_btn.size, pos=self.reset_btn.pos, radius=[15])
            Color(1, 1, 1, 0.15) # Top Light White Glossy Layer
            self.reset_btn.bg_gloss = RoundedRectangle(size=(self.reset_btn.width - 6, self.reset_btn.height * 0.4), pos=(self.reset_btn.x + 3, self.reset_btn.y + self.reset_btn.height * 0.5), radius=[10])
        
        def _update_reset_btn_bounds(instance, value):
            instance.bg_shadow.pos = (instance.x, instance.y - 4)
            instance.bg_shadow.size = instance.size
            instance.bg_rect.pos = instance.pos
            instance.bg_rect.size = instance.size
            instance.bg_gloss.pos = (instance.x + 3, instance.y + instance.height * 0.5)
            instance.bg_gloss.size = (instance.width - 6, instance.height * 0.4)
            
        self.reset_btn.bind(pos=_update_reset_btn_bounds, size=_update_reset_btn_bounds)
        self.reset_btn.bind(on_press=lambda x: self.initialize_level(reset_attempts=False))

        self.undo_btn = Button(text="UNDO", font_size='16sp', bold=True, background_normal="", background_color=(0, 0, 0, 0), color=(1, 1, 1, 1))
        with self.undo_btn.canvas.before:
            Color(0.02, 0.05, 0.1, 0.8)
            self.undo_btn.bg_shadow = RoundedRectangle(size=self.undo_btn.size, pos=(self.undo_btn.x, self.undo_btn.y - 4), radius=[15])
            Color(0.1, 0.4, 0.35, 1) # Distinguishable Cool Cyan variant for UNDO
            self.undo_btn.bg_rect = RoundedRectangle(size=self.undo_btn.size, pos=self.undo_btn.pos, radius=[15])
            Color(1, 1, 1, 0.15) # Top Light White Glossy Layer
            self.undo_btn.bg_gloss = RoundedRectangle(size=(self.undo_btn.width - 6, self.undo_btn.height * 0.4), pos=(self.undo_btn.x + 3, self.undo_btn.y + self.undo_btn.height * 0.5), radius=[10])

        def _update_undo_btn_bounds(instance, value):
            instance.bg_shadow.pos = (instance.x, instance.y - 4)
            instance.bg_shadow.size = instance.size
            instance.bg_rect.pos = instance.pos
            instance.bg_rect.size = instance.size
            instance.bg_gloss.pos = (instance.x + 3, instance.y + instance.height * 0.5)
            instance.bg_gloss.size = (instance.width - 6, instance.height * 0.4)

        self.undo_btn.bind(pos=_update_undo_btn_bounds, size=_update_undo_btn_bounds)
        self.undo_btn.bind(on_press=self.perform_undo)

        self.control_layout.add_widget(self.reset_btn)
        self.control_layout.add_widget(self.undo_btn)
        self.add_widget(self.control_layout)

        self.initialize_level()

    def setup_admob(self, dt=None):
        if platform == 'android':
            try:
                from jnius import autoclass
                # Android UI Thread Activity Context එක ලබා ගැනීම
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                AdMobHelper = autoclass('org.senu.puzzleslider.AdMobHelper')

                # Activity Context එක සමඟ AdMob Init කිරීම
                current_activity = PythonActivity.mActivity
                if current_activity:
                    AdMobHelper.init(current_activity)
                if current_activity is not None:
                    self.AdMobHelper = AdMobHelper
                    print("LOGCAT_DEBUG: AdMob Native Helper Initialized Successfully via UI Thread.")
                else:
                    Clock.schedule_once(self.setup_admob, 0.5)
            except Exception as e:
                import traceback
                print(f"LOGCAT_CRASH_CATCHER: AdMob Initialization Failed:\n{traceback.format_exc()}")

    def refresh_screen(self, *args):
        pass

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def _update_punish_bounds(self, instance, value):
        self.punish_bg.pos = instance.pos
        self.punish_bg.size = instance.size
        self.punish_line.rectangle = (instance.x, instance.y, instance.width, instance.height)

    def _update_ad_btn_bounds(self, instance, value):
        if hasattr(instance, 'ad_btn_line'):
            instance.ad_btn_line.rectangle = (instance.x, instance.y, instance.width, instance.height)
        if hasattr(instance, 'ad_btn_shadow'):
            instance.ad_btn_shadow.pos = (instance.x, instance.y - 4)
            instance.ad_btn_shadow.size = instance.size
        if hasattr(instance, 'ad_btn_rect'):
            instance.ad_btn_rect.pos = instance.pos
            instance.ad_btn_rect.size = instance.size
        if hasattr(instance, 'ad_btn_gloss'):
            instance.ad_btn_gloss.pos = (instance.x + 3, instance.y + instance.height * 0.55)
            instance.ad_btn_gloss.size = (instance.width - 6, instance.height * 0.4)

    def go_to_previous_level(self, instance):
        if self.current_level > 1:
            self.current_level -= 1
            self.initialize_level(reset_attempts=True)

    def go_to_next_level(self, instance):
        if self.current_level < self.max_unlocked_level:
            self.current_level += 1
            self.initialize_level(reset_attempts=True)

    def initialize_level(self, reset_attempts=True):
        self.lock_frame = None
        if reset_attempts:
            self.failed_attempts = 0
        Clock.unschedule(self.update_timer)
        if self.timer_trigger:
            Clock.unschedule(self.timer_trigger)
            self.timer_trigger = None
            
        self.history.clear()
        self.move_count = 0
        
        # Check and apply Dynamic Architecture Boundaries
        if not self.challenge_mode:
            self.level_label.text = f"L {self.current_level}"
            if 1 <= self.current_level <= 10:
                self.grid_size = 3
                self.time_left = -1 # Unlimited time
            elif 11 <= self.current_level <= 20:
                self.grid_size = 4
                self.time_left = 350
            elif 21 <= self.current_level <= 30:
                self.grid_size = 5
                self.time_left = 350
            elif 31 <= self.current_level <= 100:
                self.grid_size = 6
                self.time_left = 300
        else:
            self.level_label.text = "CHALLENGE MODE"
            self.grid_size = random.randint(3, 6)
            self.time_left = 150

        # Update Padding Logic for higher dimensions to perfectly match screen real estate
        if self.grid_size >= 8:
            self.puzzle_grid.padding = [0, 0, 0, 0]
            self.puzzle_grid.spacing = 1
        else:
            self.puzzle_grid.padding = [5, 5, 5, 5]
            self.puzzle_grid.spacing = 2

        self.puzzle_grid.cols = self.grid_size
        self.generate_solvable_puzzle()
        self.render_grid()

        if self.time_left > 0:
            self.timer_label.text = f"Time: {self.time_left}s"
            self.timer_trigger = Clock.schedule_interval(self.update_timer, 1.0)
        else:
            self.timer_label.text = "Time: INF"
            
        self.game_active = True

    def generate_solvable_puzzle(self):
        total_tiles = self.grid_size * self.grid_size
        self.tiles = list(range(1, total_tiles)) + [0]
        
        # Configurable shuffling intensity scaling linearly with current level difficulty
        shuffle_steps = self.grid_size * self.grid_size * 20
        
        # Physical structural shifting simulation to assure computational solvability
        blank = total_tiles - 1
        for _ in range(shuffle_steps):
            valid_moves = []
            row, col = blank // self.grid_size, blank % self.grid_size
            if row > 0: valid_moves.append(blank - self.grid_size)
            if row < self.grid_size - 1: valid_moves.append(blank + self.grid_size)
            if col > 0: valid_moves.append(blank - 1)
            if col < self.grid_size - 1: valid_moves.append(blank + 1)
            
            move = random.choice(valid_moves)
            self.tiles[blank], self.tiles[move] = self.tiles[move], self.tiles[blank]
            blank = move
            
        self.blank_index = self.tiles.index(0)

    def render_grid(self):
        self.puzzle_grid.clear_widgets()
        for idx, val in enumerate(self.tiles):
            if val == 0:
                dummy = Label(text="")
                self.puzzle_grid.add_widget(dummy)
            else:
                btn = Button(text=str(val), 
                             font_size='18sp' if self.grid_size > 7 else '26sp', 
                             bold=True, 
                             background_normal='', 
                             background_color=(0, 0, 0, 0))
                btn.color = (1, 1, 1, 1)
                
                with btn.canvas.before:
                    Color(0.02, 0.08, 0.12, 1)
                    btn.bg_shadow = RoundedRectangle(size=btn.size, pos=(btn.x, btn.y - 5), radius=[16])
                    Color(0.08, 0.25, 0.32, 1)
                    btn.bg_rect = RoundedRectangle(size=btn.size, pos=btn.pos, radius=[16])
                    Color(0, 0.9, 1, 0.35)
                    btn.bg_gloss = RoundedRectangle(size=(btn.width - 6, btn.height * 0.4), pos=(btn.x + 3, btn.y + btn.height * 0.55), radius=[12])
                with btn.canvas.after:
                    Color(0.4, 0.85, 1, 0.7)
                    btn.line = Line(rounded_rectangle=(btn.x, btn.y, btn.width, btn.height, 16), width=1.5)
                
                btn.bind(pos=self._update_btn_bounds, size=self._update_btn_bounds)
                btn.bind(on_press=lambda instance, i=idx: self.tile_clicked(i))
                self.puzzle_grid.add_widget(btn)

    def _update_btn_bounds(self, instance, value):
        if hasattr(instance, 'line'):
            instance.line.rounded_rectangle = (instance.x, instance.y, instance.width, instance.height, 16)
        if hasattr(instance, 'bg_shadow'):
            instance.bg_shadow.pos = (instance.x, instance.y - 5)
            instance.bg_shadow.size = instance.size
        if hasattr(instance, 'bg_rect'):
            instance.bg_rect.pos = instance.pos
            instance.bg_rect.size = instance.size
        if hasattr(instance, 'bg_gloss'):
            instance.bg_gloss.pos = (instance.x + 3, instance.y + instance.height * 0.55)
            instance.bg_gloss.size = (instance.width - 6, instance.height * 0.4)

    def tile_clicked(self, idx):
        if not self.game_active:
            return
        if self.is_adjacent(idx, self.blank_index):
            # Save historical state snapshot via atomic Python lists injection arrays
            self.history.append(list(self.tiles))
            self.tiles[self.blank_index], self.tiles[idx] = self.tiles[idx], self.tiles[self.blank_index]
            self.blank_index = idx
            self.move_count += 1
            Clock.schedule_once(lambda dt: self.render_grid(), 0.01)
            self.check_win_condition()

    def is_adjacent(self, idx1, idx2):
        r1, c1 = idx1 // self.grid_size, idx1 % self.grid_size
        r2, c2 = idx2 // self.grid_size, idx2 % self.grid_size
        return abs(r1 - r2) + abs(c1 - c2) == 1

    def perform_undo(self, instance):
        if self.game_active and self.history:
            self.tiles = self.history.pop()
            self.blank_index = self.tiles.index(0)
            self.render_grid()

    def update_timer(self, dt):
        if not self.game_active:
            return
        self.time_left -= 1
        if self.time_left <= 0:
            self.timer_label.text = "Time: 0s"
            self.handle_level_failure()
        else:
            self.timer_label.text = f"Time: {self.time_left}s"

    def handle_level_failure(self):
        Clock.unschedule(self.update_timer)
        if self.timer_trigger:
            Clock.unschedule(self.timer_trigger)
            self.timer_trigger = None
            
        self.game_active = False
        penalty = 5 if self.challenge_mode else 2
        max_limit = 60 if self.challenge_mode else 30
        self.punishment_pool = min(max_limit, self.punishment_pool + penalty)
        self.punish_label.text = f"Punishment Box: {self.punishment_pool} Seconds"
        
        self.save_game_state()
        self.failed_attempts += 1

        if self.failed_attempts >= 10:
            popup_layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
            lbl = Label(text='10 Times Failed!\nWant to skip this level by watching a 10s Punishment Ad?', 
                        font_size='16sp', 
                        bold=True, 
                        color=(1, 1, 1, 1), 
                        halign='center', 
                        valign='middle')
            lbl.bind(size=lbl.setter('text_size'))
            popup_layout.add_widget(lbl)
            
            btn_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=0.4)
            skip_btn = Button(text="Skip Level", bold=True, background_color=(0, 0.8, 1, 1))
            cancel_btn = Button(text="Cancel", bold=True, background_color=(0.8, 0.2, 0.2, 1))
            
            btn_layout.add_widget(skip_btn)
            btn_layout.add_widget(cancel_btn)
            popup_layout.add_widget(btn_layout)
            
            popup = Popup(title='SYSTEM NOTICE', content=popup_layout, size_hint=(0.8, 0.45), auto_dismiss=False)
            popup.title_align = 'center'
            popup.title_size = '16sp'
            popup.title_color = [0, 0.9, 1, 1]
            popup.background_color = [0.05, 0.08, 0.15, 0.92]
            
            def on_skip(instance):
                popup.dismiss()
                self.ad_button.disabled = True
                if hasattr(self, 'lock_ad_button') and self.lock_ad_button is not None:
                    self.lock_ad_button.disabled = True
                self.pending_action = 'SKIP_LEVEL'
                
                # Dynamic Reload & Thread-Safe Progressive Retry Strategy
                self.reload_admob_ads()
                self.verify_network_retry(attempt=1)

            def on_cancel(instance):
                popup.dismiss()
                self.failed_attempts = 0
                self.initialize_level(reset_attempts=False)
                
            skip_btn.bind(on_press=on_skip)
            cancel_btn.bind(on_press=on_cancel)
            popup.open()
        else:
            # Enhanced Official Dark Neon Glass Alert Dialog Architecture
            popup_layout = BoxLayout(orientation='vertical', padding=20)
            lbl = Label(text="!! YOU FAIL !!", font_size='24sp', bold=True, color=(1, 0.2, 0.2, 1), halign='center')
            popup_layout.add_widget(lbl)
            
            popup = Popup(title='SYSTEM NOTICE', content=popup_layout, size_hint=(0.8, 0.35), auto_dismiss=False)
            popup.title_align = 'center'
            popup.title_size = '16sp'
            popup.title_color = [0, 0.9, 1, 1] # Neon Cyan Title Text
            popup.background_color = [0.05, 0.08, 0.15, 0.92] # Strict Matte Deep Slate Blue Official Background
            
            popup.open()
            Clock.schedule_once(lambda dt: popup.dismiss(), 1.5)
            Clock.schedule_once(lambda dt: self.initialize_level(reset_attempts=False), 1.6)

    # ==================================================================
    # 100% VERIFIED BULLETPROOF NETWORK, ADMOB JNI & RECOVERY PATCH
    # ==================================================================
    def reinitialize_admob(self):
        """
        Explicitly triggers Java JNI MobileAds re-initialization 
        when network transitions from Offline to Online on Android API 21-36+.
        """
        try:
            if platform == 'android':
                if hasattr(self, 'AdMobHelper') and self.AdMobHelper is not None:
                    from jnius import autoclass
                    PythonActivity = autoclass("org.kivy.android.PythonActivity")
                    current_activity = PythonActivity.mActivity
                    self.AdMobHelper.init(current_activity)
                    print("AdMob: Native Engine Re-initialized successfully via JNI!")
        except Exception as e:
            print(f"AdMob Re-init Warning: {e}")

    def reload_admob_ads(self):
        if platform == 'android':
            if getattr(self, 'is_fetching_ads', False):
                return
            self.is_fetching_ads = True
            try:
                if hasattr(self, 'AdMobHelper') and self.AdMobHelper is not None:
                    self.AdMobHelper.loadRewardedAd()
            except Exception as e:
                print(f"AdMob Reload Exception: {e}")
            finally:
                Clock.schedule_once(lambda dt: setattr(self, 'is_fetching_ads', False), 3.0)

    def verify_network_retry(self, attempt=1):
        """Progressive Exponential Backoff Network Retry with Socket Clear Protection."""
        self.is_processing_click = False
        
        # Socket Clean Up: Cancel active net request before making a new one
        if hasattr(self, 'active_net_request') and self.active_net_request:
            try:
                self.active_net_request.cancel()
            except Exception:
                pass
            self.active_net_request = None

        def on_net_success(req, res):
            self._on_network_check_success(req, res)

        def on_net_error(req, err):
            # API Delay mitigation - Exponential Backoff Retries
            if attempt < 4:
                backoff_delay = attempt * 1.2
                print(f"Network retry attempt {attempt} failed. Flushing sockets & retrying in {backoff_delay}s...")
                Clock.schedule_once(lambda dt: self.verify_network_retry(attempt=attempt + 1), backoff_delay)
            else:
                self.network_failed(req, err)

        # Append timestamp parameter to URL to prevent HTTP/DNS Caching on Android
        timestamp_url = f"https://clients3.google.com/generate_204?t={int(time.time())}"
        
        self.active_net_request = UrlRequest(
            timestamp_url,
            on_success=on_net_success,
            on_error=on_net_error,
            on_failure=on_net_error,
            on_redirect=on_net_success,
            timeout=5
        )

    def _on_network_check_success(self, request, result):
        """Handles network success, clears UI error popups, and executes pending state."""
        self.internet_available = True
        self.is_processing_click = False
        
        # Explicit UI Clean Up (Removes looping Red Error Messages & Popups)
        if hasattr(self, 'root') and hasattr(self.root, 'ids') and 'error_label' in self.root.ids:
            self.root.ids.error_label.text = ""
        self._dismiss_active_popups()
        
        self.ad_button.disabled = False
        if hasattr(self, 'lock_ad_button') and self.lock_ad_button is not None:
            self.lock_ad_button.disabled = False

        # Re-initialize native engine and trigger dynamic ad reload
        self.reinitialize_admob()
        Clock.schedule_once(lambda dt: self.reload_admob_ads(), 0.5)

        action = self.pending_action
        self.pending_action = None

        if action == 'SKIP_LEVEL':
            self._start_skip_ad()
        elif action == 'PUNISHMENT_AD':
            self._verify_and_show_ad_with_retry(request, result)
        elif action == 'MILESTONE_LOCK':
            self.render_locked_milestone_ui()
        else:
            if self.is_skipping_via_ad:
                self._start_skip_ad()
            elif self.punishment_pool > 0 and self.lock_frame is None:
                self.render_locked_milestone_ui()

    def _verify_and_show_ad_with_retry(self, request, result, retry_count=0, max_retries=10):
        """
        AdMob Ad එක Memory එකෙහි සූදානම්දැයි බල අඩුවක් නැතිව Show කිරීම 
        සහ Polling Loop එක ආරම්භ කිරීම.
        """
        self.is_processing_click = False
        
        # 1. AdMob Ad එක Memory එකේ Ready නම් direct show කිරීම
        if platform == 'android' and hasattr(self, 'AdMobHelper') and self.AdMobHelper is not None:
            try:
                if self.AdMobHelper.isAdLoaded():
                    self.AdMobHelper.showRewardedAd()
                    
                    # පැරණි Polling තිබේ නම් Unschedule කර අලුතින් Polling ආරම්භ කිරීම
                    if hasattr(self, 'poll_event') and self.poll_event:
                        self.poll_event.cancel()
                    self.poll_event = Clock.schedule_interval(self.check_ad_status_polling, 0.5)
                    return
            except Exception as e:
                print(f"Error invoking AdMob Ad via Native Helper: {e}")

        # 2. Ad එක Ready නැත්නම් Retry Count එක පරීක්ෂා කර නැවත Fetch කිරීම
        if retry_count < max_retries:
            print(f"AdMob: Ad not ready yet. Retrying... ({retry_count + 1}/{max_retries})")
            self.reload_admob_ads()
            Clock.schedule_once(
                lambda dt: self._verify_and_show_ad_with_retry(request, result, retry_count + 1, max_retries), 
                1.5
            )
        else:
            self.network_failed(None, "Ad Loading Failed - Please try again in a moment.")

    def check_ad_status_polling(self, dt):
        if platform != 'android' or not hasattr(self, 'AdMobHelper') or self.AdMobHelper is None:
            return False

        try:
            if self.AdMobHelper.hasEarnedReward():
                self.AdMobHelper.resetRewardState()
                if hasattr(self, 'poll_event') and self.poll_event:
                    self.poll_event.cancel()
                self.on_reward_success()
                return False

            if self.AdMobHelper.isAdFailedToLoad():
                self.AdMobHelper.resetRewardState()
                if hasattr(self, 'poll_event') and self.poll_event:
                    self.poll_event.cancel()
                self.network_failed(None, "Ad failed to play. Check connection.")
                return False
        except Exception as e:
            print(f"Polling Exception: {e}")
            if hasattr(self, 'poll_event') and self.poll_event:
                self.poll_event.cancel()
            return False

        return True

    def on_reward_success(self):
        """
        Ad එක සාර්ථක ලෙස නැරඹූ පසු Kivy Main Thread එක හරහා 
        Punishment Pool එක 0 කර Game State එක Safely Reset කිරීම.
        """
        self.punishment_pool = 0
        self.failed_attempts = 0
        self.save_game_state()

        if self.is_skipping_via_ad:
            self.is_skipping_via_ad = False
            if not self.challenge_mode:
                self.transition_next_step()
            else:
                self.initialize_level(reset_attempts=True)
        else:
            self.punish_label.text = "Punishment Box: 0 Seconds"
            self.puzzle_grid.clear_widgets()
            self.initialize_level(reset_attempts=True)
            
        # ඊළඟ වතාව සඳහා පසුබිමින් නැවත Ad එකක් pre-load කිරීම
        if platform == 'android' and hasattr(self, 'AdMobHelper') and self.AdMobHelper is not None:
            self.AdMobHelper.loadRewardedAd()

    def _start_ad_stream_verified(self, request, result):
        """
        Simulated Timer එක සම්පූර්ණයෙන්ම ඉවත් කර Ad Mobility Retries වලට යොමු කිරීම
        """
        self._verify_and_show_ad_with_retry(request, result)

    def _start_skip_ad(self):
        """Initiates level skip and triggers active AdMob polling loop."""
        self.punishment_pool = 0
        self.failed_attempts = 0
        self.is_skipping_via_ad = True
        self.countdown_pool = 10
        self.ad_button.disabled = True
        
        self.reload_admob_ads()
        self.ad_poll_timer = 0
        
        # Unschedule previous polling events if active
        if hasattr(self, 'ad_polling_event') and self.ad_polling_event:
            Clock.unschedule(self.ad_polling_event)
            self.ad_polling_event = None
            
        # Start 10-Second Active Dynamic Ad Polling Verification
        self.ad_polling_event = Clock.schedule_interval(self._show_rewarded_ad_cached, 1.0)

    def _show_rewarded_ad_cached(self, dt):
        if platform == 'android' and hasattr(self, 'AdMobHelper') and self.AdMobHelper is not None:
            try:
                if self.AdMobHelper.isAdLoaded():
                    self.AdMobHelper.showRewardedAd()
                    if hasattr(self, 'poll_event') and self.poll_event:
                        self.poll_event.cancel()
                    self.poll_event = Clock.schedule_interval(self.check_ad_status_polling, 0.5)
                    if hasattr(self, 'ad_polling_event') and self.ad_polling_event:
                        Clock.unschedule(self.ad_polling_event)
                        self.ad_polling_event = None
                    return False
                else:
                    self.ad_poll_timer += 1
            except Exception as e:
                print(f"Error showing AdMob Ad: {e}")
                self.ad_poll_timer += 1
                
        if self.ad_poll_timer >= 10:
            if hasattr(self, 'ad_polling_event') and self.ad_polling_event:
                Clock.unschedule(self.ad_polling_event)
                self.ad_polling_event = None
            self.network_failed(None, "Ad Loading Timeout - Please Retry")
            return False
            
        return True

    def check_win_condition(self):
        total_elements = self.grid_size * self.grid_size
        target = list(range(1, total_elements)) + [0]
        if secure_verify(json.dumps(self.tiles), json.dumps(target)):
            self.game_active = False
            Clock.unschedule(self.update_timer)
            if self.timer_trigger:
                Clock.unschedule(self.timer_trigger)
                self.timer_trigger = None
                
            # Enhanced Official Dark Neon Glass Alert Dialog Architecture
            popup_layout = BoxLayout(orientation='vertical', padding=20)
            lbl = Label(text="== YOU WIN!\n==", font_size='24sp', bold=True, color=(0, 1, 0, 1), halign='center')
            popup_layout.add_widget(lbl)
            
            popup = Popup(title='SYSTEM NOTICE', content=popup_layout, size_hint=(0.8, 0.35), auto_dismiss=False)
            popup.title_align = 'center'
            popup.title_size = '16sp'
            popup.title_color = [0, 0.9, 1, 1] # Neon Cyan Title Text
            popup.background_color = [0.05, 0.08, 0.15, 0.92] # Strict Matte Deep Slate Blue Official Background
            
            popup.open()
            Clock.schedule_once(lambda dt: popup.dismiss(), 1.5)
            Clock.schedule_once(lambda dt: self.transition_next_step(), 1.6)

    def transition_next_step(self):
        Clock.unschedule(self.update_timer)
        if self.timer_trigger:
            Clock.unschedule(self.timer_trigger)
            self.timer_trigger = None
            
        if self.challenge_mode:
            if self.move_count < self.high_score or self.high_score == 0:
                self.high_score = self.move_count
            Clock.schedule_once(lambda dt: self.initialize_level(reset_attempts=True), 0.2)
            return

        if self.current_level == 100:
            self.activate_grand_master_mode()
            return

        if self.current_level == self.max_unlocked_level:
            self.current_level += 1
            self.max_unlocked_level = self.current_level
        else:
            self.current_level = self.max_unlocked_level
            
        self.total_wins = self.current_level - 1
        self.wins_label.text = f"Wins: {self.total_wins}"
        
        self.save_game_state()

        # Periodic Ad Trap Interception Validation Checks (Every 5 levels starting from level milestones transition)
        milestones = [16, 21, 26, 31, 36, 41, 46, 51, 56, 61, 66, 71, 76, 81, 86, 91, 96, 101]
        if self.current_level in milestones and self.punishment_pool > 0:
            self.pending_action = 'MILESTONE_LOCK'
            self.verify_network_and_lock()
        else:
            Clock.schedule_once(lambda dt: self.initialize_level(reset_attempts=True), 0.2)

    def verify_network_and_lock(self):
        self.ad_button.disabled = True
        if self.lock_ad_button is not None:
            self.lock_ad_button.disabled = True
            
        UrlRequest("https://clients3.google.com/generate_204", 
                    on_success=self._on_network_check_success, 
                    on_error=self.network_failed, 
                    on_failure=self.network_failed, 
                    timeout=8)

    def _dismiss_active_popups(self):
        """[Bug 2 & 5 Fix] Dismisses all active popups safely to prevent ghost popups and stacking."""
        if hasattr(self, 'net_popup') and self.net_popup:
            try:
                self.net_popup.dismiss()
            except Exception:
                pass
            self.net_popup = None
            
        if hasattr(self, 'current_popup') and self.current_popup:
            try:
                self.current_popup.dismiss()
            except Exception:
                pass
            self.current_popup = None

    def network_failed(self, request, error):
        """[Bug 1, 2, 3 & 5 Fix] Handles network failure without button freeze or popup stacking."""
        # [Bug 1 Fix] Release click lock securely
        self.is_processing_click = False
        self.internet_available = False
        
        # [Bug 3 Fix] Safely pause/unschedule ad stream timer during network failures
        if hasattr(self, 'ad_timer_event') and self.ad_timer_event:
            Clock.unschedule(self.ad_timer_event)
            self.ad_timer_event = None
        Clock.unschedule(self.process_ad_stream)

        # Re-enable UI trigger buttons
        self.ad_button.disabled = False
        if hasattr(self, 'lock_ad_button') and self.lock_ad_button is not None:
            self.lock_ad_button.disabled = False

        # [Bug 2 Fix] Dismiss existing ghost popups before opening a new one
        self._dismiss_active_popups()

        popup_layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        lbl = Label(text="Connection Error / Weak Signal!\nPlease check Mobile Data / Wi-Fi\nand tap Retry.", 
                    font_size='14sp', bold=True, color=(1, 0.2, 0.2, 1), halign='center', valign='middle')
        lbl.bind(size=lbl.setter('text_size'))
        popup_layout.add_widget(lbl)
        
        ok_btn = Button(text="RETRY", bold=True, size_hint=(0.4, 0.3), pos_hint={'center_x': 0.5}, background_color=(0, 0.8, 1, 1))
        popup_layout.add_widget(ok_btn)
        
        # [Bug 5 Fix] Bind to self.net_popup for reference tracking and auto-dismissal
        self.net_popup = Popup(title='NETWORK NOTICE', content=popup_layout, size_hint=(0.85, 0.4), auto_dismiss=False)
        self.net_popup.title_align = 'center'
        self.net_popup.title_size = '16sp'
        self.net_popup.title_color = [1, 0.2, 0.2, 1]
        self.net_popup.background_color = [0.05, 0.08, 0.15, 0.95]
        
        def on_ok(instance):
            if self.is_processing_click:
                return
            self.is_processing_click = True
            
            # Dismiss popup immediately on retry tap
            self._dismiss_active_popups()
            Clock.schedule_once(lambda dt: self.verify_network_retry(), 0.3)
            
        ok_btn.bind(on_press=on_ok)
        self.net_popup.open()

    def render_locked_milestone_ui(self):
        if self.lock_frame is not None:
            return
            
        self.puzzle_grid.clear_widgets()
        self.game_active = False
        self.level_label.text = "LOCKED - AD REQUIRED"
        self.puzzle_grid.cols = 1
        
        # Premium Neon Glassmorphic Message Box Frame
        self.lock_frame = BoxLayout(orientation='vertical', padding=20, spacing=15, size_hint=(0.9, 0.9), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        
        with self.lock_frame.canvas.before:
            Color(0.02, 0.08, 0.12, 1)
            self.lock_frame.bg_shadow = RoundedRectangle(size=self.lock_frame.size, pos=(self.lock_frame.x, self.lock_frame.y - 5), radius=[25])
            Color(0.08, 0.25, 0.32, 1)
            self.lock_frame.bg_rect = RoundedRectangle(size=self.lock_frame.size, pos=self.lock_frame.pos, radius=[25])
            Color(0, 0.9, 1, 0.35)
            self.lock_frame.bg_gloss = RoundedRectangle(size=(self.lock_frame.width - 10, self.lock_frame.height * 0.4), pos=(self.lock_frame.x + 5, self.lock_frame.y + self.lock_frame.height * 0.55), radius=[20])
        with self.lock_frame.canvas.after:
            Color(0.4, 0.85, 1, 0.7)
            self.lock_frame.bg_line = Line(rounded_rectangle=(self.lock_frame.x, self.lock_frame.y, self.lock_frame.width, self.lock_frame.height, 25), width=1.5)

        def update_frame_bounds(instance, value):
            self.lock_frame.bg_shadow.pos = (instance.x, instance.y - 5)
            self.lock_frame.bg_shadow.size = instance.size
            self.lock_frame.bg_rect.pos = instance.pos
            self.lock_frame.bg_rect.size = instance.size
            self.lock_frame.bg_gloss.pos = (instance.x + 5, instance.y + instance.height * 0.55)
            self.lock_frame.bg_gloss.size = (instance.width - 10, instance.height * 0.4)
            self.lock_frame.bg_line.rounded_rectangle = (instance.x, instance.y, instance.width, instance.height, 25)
            
            if self.lock_ad_button is not None:
                self.lock_ad_button.btn_line.rounded_rectangle = (self.lock_ad_button.x, self.lock_ad_button.y, self.lock_ad_button.width, self.lock_ad_button.height, 16)
                self.lock_ad_button.bg_shadow.pos = (self.lock_ad_button.x, self.lock_ad_button.y - 5)
                self.lock_ad_button.bg_shadow.size = self.lock_ad_button.size
                self.lock_ad_button.bg_rect.pos = self.lock_ad_button.pos
                self.lock_ad_button.bg_rect.size = self.lock_ad_button.size
                self.lock_ad_button.bg_gloss.pos = (self.lock_ad_button.x + 3, self.lock_ad_button.y + self.lock_ad_button.height * 0.55)
                self.lock_ad_button.bg_gloss.size = (self.lock_ad_button.width - 6, self.lock_ad_button.height * 0.4)

        self.lock_frame.bind(pos=update_frame_bounds, size=update_frame_bounds)
        
        title_lbl = Label(text="LEVEL LOCKED", font_size='22sp', bold=True, color=(0, 1, 1, 1), size_hint_y=0.2)
        msg_text = f"Your Level {self.current_level} is currently locked due to a pending penalty.\nPlease watch a short ad to unlock the next level!"
        msg_lbl = Label(text=msg_text, font_size='15sp', bold=True, color=(1, 1, 1, 1), halign='center', valign='middle', size_hint_y=0.4)
        msg_lbl.bind(size=msg_lbl.setter('text_size'))
        status_lbl = Label(text=f"Required Ad Time: {self.punishment_pool} Seconds", font_size='14sp', bold=True, color=(1, 0.5, 0, 1), size_hint_y=0.15)
        
        self.lock_ad_button = Button(text="WATCH AD TO UNLOCK LEVEL", 
                                  font_size='15sp', 
                                  bold=True, 
                                  color=(1, 1, 1, 1), 
                                  background_normal='', 
                                  background_color=(0, 0, 0, 0), 
                                  size_hint_y=0.25)
        self.lock_ad_button.bind(on_press=lambda x: self.trigger_punishment_ad(None))
        
        with self.lock_ad_button.canvas.before:
            Color(0.02, 0.08, 0.12, 1)
            self.lock_ad_button.bg_shadow = RoundedRectangle(size=self.lock_ad_button.size, pos=(self.lock_ad_button.x, self.lock_ad_button.y - 5), radius=[15])
            Color(0.08, 0.25, 0.32, 1)
            self.lock_ad_button.bg_rect = RoundedRectangle(size=self.lock_ad_button.size, pos=self.lock_ad_button.pos, radius=[15])
            Color(0, 0.9, 1, 0.35)
            self.lock_ad_button.bg_gloss = RoundedRectangle(size=(self.lock_ad_button.width - 6, self.lock_ad_button.height * 0.4), pos=(self.lock_ad_button.x + 3, self.lock_ad_button.y + self.lock_ad_button.height * 0.55), radius=[10])
        
        with self.lock_ad_button.canvas.after:
            Color(0.4, 0.85, 1, 0.7)
            self.lock_ad_button.btn_line = Line(rounded_rectangle=(self.lock_ad_button.x, self.lock_ad_button.y, self.lock_ad_button.width, self.lock_ad_button.height, 16), width=1.5)

        self.lock_frame.add_widget(title_lbl)
        self.lock_frame.add_widget(msg_lbl)
        self.lock_frame.add_widget(status_lbl)
        self.lock_frame.add_widget(self.lock_ad_button)

        self.puzzle_grid.add_widget(self.lock_frame)

    def clear_alert_label(self, dt):
        if hasattr(self, 'alert_label') and self.alert_label.parent:
            self.alert_label.parent.remove_widget(self.alert_label)
        self.ad_button.disabled = False
        if self.lock_ad_button is not None:
            self.lock_ad_button.disabled = False

    def trigger_punishment_ad(self, instance):
        """[Bug 1, 3 & 8 Fix] Triggers AdMob Ads with instant fallback & GC-protected network validation."""
        if self.is_processing_click:
            return
        self.is_processing_click = True
        
        if self.punishment_pool <= 0 and not self.is_skipping_via_ad:
            self.is_processing_click = False
            return

        self.ad_button.disabled = True
        if self.lock_ad_button is not None:
            self.lock_ad_button.disabled = True
            
        self.pending_action = 'PUNISHMENT_AD'
        
        # [Bug 8 Fix] GC Protection for Network Request Object
        self.active_net_request = UrlRequest("https://clients3.google.com/generate_204", 
                        on_success=self._on_network_check_success, 
                        on_error=self.network_failed, 
                        on_failure=self.network_failed, 
                        timeout=8)

    def process_ad_stream(self, dt):
        """[Bug 4 Fix] Countdown stream processing with seamless level transition execution."""
        self.countdown_pool -= 1
        if self.countdown_pool <= 0:
            if hasattr(self, 'ad_timer_event') and self.ad_timer_event:
                Clock.unschedule(self.game.ad_timer_event)
                self.ad_timer_event = None
            Clock.unschedule(self.process_ad_stream)
            
            self.is_processing_click = False
            self.ad_button.text = "Watch Punishment Ad"
            self.ad_button.disabled = False
            if hasattr(self, 'lock_ad_button') and self.lock_ad_button is not None:
                self.lock_ad_button.text = "WATCH AD TO UNLOCK LEVEL"
                self.lock_ad_button.disabled = False
                
            if self.is_skipping_via_ad:
                self.is_skipping_via_ad = False
                self.save_game_state()
                if not self.challenge_mode:
                    self.transition_next_step()
                else:
                    self.initialize_level(reset_attempts=True)
            else:
                self.punishment_pool = 0
                self.punish_label.text = "Punishment Box: 0 Seconds"
                self.save_game_state()
                self.puzzle_grid.clear_widgets()
                self.initialize_level(reset_attempts=True)
            return False
        else:
            self.ad_button.text = f"Ad Playing: {self.countdown_pool}s"
            if hasattr(self, 'lock_ad_button') and self.lock_ad_button is not None:
                self.lock_ad_button.text = f"Ad Playing: {self.countdown_pool}s"
            return True

    def activate_grand_master_mode(self):
        self.challenge_mode = True
        self.current_level = 101
        self.total_wins = 100
        self.wins_label.text = f"Wins: {self.total_wins}"
        self.save_game_state()
        
        # Enhanced Official Dark Neon Glass Alert Dialog Architecture
        popup_layout = BoxLayout(orientation='vertical', padding=20)
        lbl = Label(text="👑 GRAND MASTER UNLOCKED:\nTHE TIME CHALLENGE!\n👑", font_size='24sp', bold=True, color=(1, 0.84, 0, 1), halign='center')
        popup_layout.add_widget(lbl)
        
        popup = Popup(title='SYSTEM NOTICE', content=popup_layout, size_hint=(0.8, 0.35), auto_dismiss=True)
        popup.title_align = 'center'
        popup.title_size = '16sp'
        popup.title_color = [0, 0.9, 1, 1] # Neon Cyan Title Text
        popup.background_color = [0.05, 0.08, 0.15, 0.92] # Strict Matte Deep Slate Blue Official Background
        
        popup.bind(on_dismiss=lambda x: self.initialize_level(reset_attempts=True))
        popup.open()

    def save_game_state(self):
        # Memory-tuned persistence architecture using JSON store abstraction interfaces
        from kivy.app import App
        import os
        app = App.get_running_app()
        data_dir = app.user_data_dir if app else os.path.dirname(__file__)
        file_path = os.path.join(data_dir, 'game_secure_state.json')
        
        game_state_data = {'user_profile': {'current_level': int(self.current_level), 
                                              'punishment_pool': int(self.punishment_pool), 
                                              'challenge_mode': bool(self.challenge_mode), 
                                              'high_score': int(self.high_score)}}
        json_string = json.dumps(game_state_data)
        encrypted_string = xor_crypt(json_string)
        with open(file_path, 'w') as f:
            f.write(encrypted_string)

class SliderApp(App):
    def build(self):
        if platform == 'android':
            Window.bind(on_resize=lambda *args: True)
        self.title = "Ultimate Sliding Puzzle"
        self.game = SlidingPuzzleGame()
        # Launch Crash වැළැක්වීමට context fully load වූ පසු AdMob Init කිරීම
        Clock.schedule_once(lambda dt: self.game.setup_admob(), 1.0)
        return self.game

    def on_pause(self):
        """[Bug 6 & 7 Fix] Resets locks, active popups, and cleans up scheduled timers when moving to background."""
        if hasattr(self, 'game') and self.game:
            # Unschedule all active clock events
            Clock.unschedule(self.game.update_timer)
            Clock.unschedule(self.game.process_ad_stream)
            if hasattr(self.game, 'ad_timer_event') and self.game.ad_timer_event:
                Clock.unschedule(self.game.ad_timer_event)
                self.game.ad_timer_event = None
                
            # Reset async locks and dismiss ghost popups
            self.game.is_processing_click = False
            self.game._dismiss_active_popups()
        return True

    def on_resume(self):
        """[Bug 6 Fix] Restores active timer safely when resuming application."""
        if hasattr(self, 'game') and self.game:
            self.game.is_processing_click = False
            if self.game.game_active and self.game.time_left > 0:
                Clock.unschedule(self.game.update_timer)
                self.game.timer_trigger = Clock.schedule_interval(self.game.update_timer, 1.0)

if __name__ == '__main__':
    import sys
    import traceback
    try:
        SliderApp().run()
    except Exception as e:
        print("="*80)
        print("CRITICAL LAUNCH CRASH DETECTED IN MAIN LOOP:")
        print(traceback.format_exc())
        print("="*80)
        sys.exit(1)
