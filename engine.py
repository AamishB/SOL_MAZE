import numpy as np
import random
class SolMazeEngine:
    def __init__(self, grid_size=10, num_pillars=6, seed=42, mode="standard"):
        self.grid_size = grid_size
        self.seed = seed
        self.mode = mode
        self.rng = np.random.default_rng(seed) if hasattr(np.random, 'default_rng') else np.random.RandomState(seed)
        
        self.pillars = set()
        self.pits = set()
        self.sun_stones = set()
        self.moon_stones = set()
        self.player_pos = [0, 0]
        self.goal_pos = [grid_size - 1, grid_size - 1]
        
        if self.mode == "calendar_pride_maze":
            self.prism_order = ["red", "orange", "yellow", "green", "blue", "purple"]
            self.collected_prisms = []
            self.prisms = {}
            self.gates = {}
            self.rainbow_bridge_spawned = False
            
        if self.mode == "calendar_world_environment_day":
            self.player_pos = None  # Requires mouse click to place
            self.grass_tiles = set()
            self.trash_tiles = set()
            self.tree_spawned = False
            self.failed_on_trash = False
            
        if self.mode == "calendar_world_oceans_day":
            self.turtles = set()
            self.coral_reefs = set()
            self.deep_trenches = set()
            self.whirlpool_spawned = False
            self.is_high_tide = True
            self.tide_timer = 10
            self.failed_in_tide = False
        if self.mode == "calendar_juneteenth":
            self.freedom_stars = set()
            self.shadow_walls = set()
            self.freedom_bells = {} # maps bell_pos to list of wall_pos

        if self.mode == "calendar_fathers_day":
            self.collected_items = set()
            self.fathers_day_items = {}
            self.coffee_cups = set()
            self.dad_energy = 100.0
            self.failed_asleep = False
            self.backyard_obstacles = {}
        if self.mode == "calendar_world_music_day":
            self.note_sequence = []
            self.player_seq_idx = 0
            self.musical_notes = {}
            self.original_notes = {}
            self.speakers = {}
            self.beat_counter = 0
            self.soundwave_tiles = set()
            self.prev_player_pos = [0, 0]
            self.music_obstacles = {}
            self.correct_note_collected = False
            self.sequence_failed = False
            self.failed_dazed = False
        if self.mode == "solstice_shift":
            self.goal_pos_day = [grid_size - 1, grid_size - 1]
            self.goal_pos_night = [0, grid_size - 1]
            self.reached_day_goal = False
            self.reached_night_goal = False
            self.move_count = 0
            self.vision_buff_active = False
            self.failed_in_pit = False
            self.just_teleported = False
            
        # Sun parameters
        self.sun_angle = 0.0  # degrees, 0 to 360
        self.angle_step = 3.0  # degrees advanced per player move
        
        self.generate_layout(num_pillars)
        self.update_shadows()
        
    def teleport_entities(self, initial=False):
        pit_cells = [p for p in self.pits if p != tuple(self.player_pos)]
        non_pit_cells = [
            (r, c) for r in range(self.grid_size) for c in range(self.grid_size)
            if (r, c) not in self.pits and (r, c) != tuple(self.player_pos)
        ]
        self.rng.shuffle(non_pit_cells)
        self.rng.shuffle(pit_cells)
        
        if not self.reached_day_goal and len(non_pit_cells) > 0:
            self.goal_pos_day = list(non_pit_cells.pop())
            
        if not self.reached_night_goal and len(pit_cells) > 0:
            self.goal_pos_night = list(pit_cells.pop())
            
        num_sun = 3 if initial else len(self.sun_stones)
        self.sun_stones.clear()
        for _ in range(num_sun):
            if len(non_pit_cells) > 0:
                self.sun_stones.add(non_pit_cells.pop())
                
        num_moon = 3 if initial else len(self.moon_stones)
        self.moon_stones.clear()
        for _ in range(num_moon):
            if len(pit_cells) > 0:
                self.moon_stones.add(pit_cells.pop())
        self.just_teleported = True

    def generate_layout(self, num_pillars):
        if self.mode == "calendar_pride_maze":
            def is_solvable(prisms, gates, pillars):
                pos = (0, 0)
                collected = []
                for target_color in self.prism_order:
                    target_pos = None
                    for p_pos, p_color in prisms.items():
                        if p_color == target_color:
                            target_pos = p_pos
                            break
                    if not target_pos: return False
                    
                    q = [pos]
                    visited = set([pos])
                    found = False
                    
                    while q:
                        curr = q.pop(0)
                        if curr == target_pos:
                            found = True
                            pos = target_pos
                            collected.append(target_color)
                            break
                            
                        for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
                            nr, nc = curr[0], curr[1]
                            path_cells = []
                            for _ in range(2):
                                nnr, nnc = nr + dr, nc + dc
                                if 0 <= nnr < self.grid_size and 0 <= nnc < self.grid_size:
                                    if (nnr, nnc) in pillars: break
                                    if (nnr, nnc) in gates and gates[(nnr, nnc)] not in collected: break
                                    nr, nc = nnr, nnc
                                    path_cells.append((nr, nc))
                                else:
                                    break
                                    
                            if target_pos in path_cells:
                                found = True
                                pos = (nr, nc)
                                collected.append(target_color)
                                break
                                
                            if path_cells:
                                end_pos = (nr, nc)
                                if end_pos not in visited:
                                    visited.add(end_pos)
                                    q.append(end_pos)
                                    
                        if found: break
                    if not found: return False
                return True

            attempts = 0
            while attempts < 500:
                attempts += 1
                self.pillars.clear()
                self.prisms.clear()
                self.gates.clear()
                
                valid_cells = [(r, c) for r in range(self.grid_size) for c in range(self.grid_size) if (r, c) != (0, 0)]
                self.rng.shuffle(valid_cells)
                
                for _ in range(num_pillars):
                    if valid_cells: self.pillars.add(valid_cells.pop())
                    
                for color in self.prism_order:
                    if valid_cells: self.prisms[valid_cells.pop()] = color
                    
                for color in ["red", "orange", "yellow", "green", "blue"]:
                    for _ in range(2):
                        if valid_cells: self.gates[valid_cells.pop()] = color
                        
                if is_solvable(self.prisms, self.gates, self.pillars):
                    break
                    
            if attempts >= 500:
                self.gates.clear()
                
            self.goal_pos = [-1, -1]
            return

        if self.mode == "calendar_world_environment_day":
            self.pillars.clear()
            self.trash_tiles.clear()
            
            valid_cells = [(r, c) for r in range(self.grid_size) for c in range(self.grid_size)]
            self.rng.shuffle(valid_cells)
            
            for _ in range(7):
                if valid_cells: self.trash_tiles.add(valid_cells.pop())
                
            self.goal_pos = [-1, -1]
            return
            
        if self.mode == "calendar_world_oceans_day":
            self.pillars.clear()
            self.coral_reefs.clear()
            self.deep_trenches.clear()
            self.turtles.clear()
            
            valid_cells = [(r, c) for r in range(self.grid_size) for c in range(self.grid_size) if (r, c) != (0, 0)]
            self.rng.shuffle(valid_cells)
            
            for _ in range(15):
                if valid_cells: self.coral_reefs.add(valid_cells.pop())
            for _ in range(15):
                if valid_cells: self.deep_trenches.add(valid_cells.pop())
            for _ in range(4):
                if valid_cells: self.turtles.add(valid_cells.pop())
                
            self.goal_pos = [-1, -1]
            return

        if self.mode == "calendar_juneteenth":
            self.pillars.clear()
            self.shadow_walls.clear()
            self.freedom_stars.clear()
            self.freedom_bells.clear()
            
            valid_cells = [(r, c) for r in range(self.grid_size) for c in range(self.grid_size) if (r, c) != (0, 0)]
            self.rng.shuffle(valid_cells)
            
            # Scatter some random pillars to make a maze structure
            for _ in range(15):
                if valid_cells: self.pillars.add(valid_cells.pop())
            
            # Place 3 stars, each with 4 shadow walls around it
            for _ in range(3):
                if valid_cells: 
                    star_pos = valid_cells.pop()
                    self.freedom_stars.add(star_pos)
                    
                    # Create shadow walls around the star
                    star_walls = []
                    r, c = star_pos
                    for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < self.grid_size and 0 <= nc < self.grid_size and (nr, nc) != (0, 0):
                            if (nr, nc) not in self.freedom_stars and (nr, nc) not in self.pillars:
                                self.shadow_walls.add((nr, nc))
                                star_walls.append((nr, nc))
                                if (nr, nc) in valid_cells:
                                    valid_cells.remove((nr, nc))
                                    
            # Place a bell for this star
                    if valid_cells:
                        bell_pos = valid_cells.pop()
                        self.freedom_bells[bell_pos] = star_walls
                
            self.goal_pos = [-1, -1]
            return

        if self.mode == "calendar_fathers_day":
            self.pillars.clear()
            self.fathers_day_items.clear()
            self.coffee_cups.clear()
            self.backyard_obstacles.clear()
            
            valid_cells = [(r, c) for r in range(self.grid_size) for c in range(self.grid_size) if (r, c) != (0, 0)]
            self.rng.shuffle(valid_cells)
            
            # Place 10 backyard obstacles
            obstacle_types = ["gnome", "bush", "hose"]
            for _ in range(10):
                if valid_cells:
                    pos = valid_cells.pop()
                    self.pillars.add(pos)
                    self.backyard_obstacles[pos] = self.rng.choice(obstacle_types)
                    
            # Place Grill, Tie, Mug far from each other and player
            def dist(p1, p2):
                return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
                
            placed_positions = [(0, 0)]
            items = ["grill", "tie", "mug"]
            min_dist = 6
            for item in items:
                candidates = []
                for cell in valid_cells:
                    if all(dist(cell, p) >= min_dist for p in placed_positions):
                        candidates.append(cell)
                if not candidates:
                    for d_fallback in range(min_dist - 1, 0, -1):
                        candidates = [cell for cell in valid_cells if all(dist(cell, p) >= d_fallback for p in placed_positions)]
                        if candidates:
                            break
                if candidates:
                    chosen = tuple(self.rng.choice(candidates))
                    self.fathers_day_items[chosen] = item
                    placed_positions.append(chosen)
                    if chosen in valid_cells:
                        valid_cells.remove(chosen)
                else:
                    if valid_cells:
                        chosen = valid_cells.pop()
                        self.fathers_day_items[chosen] = item
                        placed_positions.append(chosen)
                    
            # Place 3 initial coffee cups
            for _ in range(3):
                if valid_cells:
                    self.coffee_cups.add(valid_cells.pop())
                    
            self.goal_pos = [-1, -1]
            return

        if self.mode == "calendar_world_music_day":
            self.pillars.clear()
            self.musical_notes.clear()
            self.original_notes.clear()
            self.speakers.clear()
            self.music_obstacles.clear()
            
            valid_cells = [(r, c) for r in range(self.grid_size) for c in range(self.grid_size) if (r, c) != (0, 0)]
            self.rng.shuffle(valid_cells)
            
            # Place 6 instrument obstacles: 3 drums, 3 mics
            for i in range(6):
                if valid_cells:
                    pos = valid_cells.pop()
                    self.pillars.add(pos)
                    self.music_obstacles[pos] = "drum" if i < 3 else "mic"
            
            # Place 4 speakers with random cardinal blast ranges (between 2 and 5 tiles)
            for _ in range(4):
                if valid_cells:
                    pos = valid_cells.pop()
                    self.speakers[pos] = int(self.rng.choice([2, 3, 4, 5]))
                    self.pillars.add(pos)
                    
            # Setup sequence order
            colors = ["red", "blue", "green", "yellow"]
            self.rng.shuffle(colors)
            self.note_sequence = list(colors)
            
            # Place 4 notes far from each other
            def dist(p1, p2):
                return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
                
            placed_positions = [(0, 0)]
            min_dist = 4
            for color in self.note_sequence:
                candidates = []
                for cell in valid_cells:
                    if all(dist(cell, p) >= min_dist for p in placed_positions):
                        candidates.append(cell)
                if not candidates:
                    for d_fallback in range(min_dist - 1, 0, -1):
                        candidates = [cell for cell in valid_cells if all(dist(cell, p) >= d_fallback for p in placed_positions)]
                        if candidates:
                            break
                if candidates:
                    chosen = tuple(self.rng.choice(candidates))
                    self.musical_notes[chosen] = color
                    placed_positions.append(chosen)
                    if chosen in valid_cells:
                        valid_cells.remove(chosen)
                else:
                    if valid_cells:
                        chosen = valid_cells.pop()
                        self.musical_notes[chosen] = color
                        placed_positions.append(chosen)
            
            self.original_notes = dict(self.musical_notes)
            self.goal_pos = [-1, -1]
            return

        if self.mode == "solstice_shift":
            self.pillars.clear()
            self.pits.clear()
            
            valid_cells = [
                (r, c) for r in range(self.grid_size) for c in range(self.grid_size)
                if (r, c) not in [(0, 0), (self.grid_size - 1, self.grid_size - 1), (0, self.grid_size - 1)]
            ]
            
            # Scatter 15 random pits (more than standard walls)
            num_pits = 15
            pit_indices = self.rng.choice(len(valid_cells), size=num_pits, replace=False)
            for idx in pit_indices:
                self.pits.add(valid_cells[idx])
                
            self.teleport_entities(initial=True)
            return

        # Place pillars randomly, ensuring start and goal are clear
        valid_cells = [
            (r, c) for r in range(self.grid_size) for c in range(self.grid_size)
            if (r, c) not in [(0, 0), (self.grid_size - 1, self.grid_size - 1), (0, self.grid_size - 1)]
        ]
        self.rng.shuffle(valid_cells)
        
        for _ in range(num_pillars):
            if valid_cells: self.pillars.add(valid_cells.pop())
            
        for _ in range(3):
            if valid_cells: self.sun_stones.add(valid_cells.pop())
            if valid_cells: self.moon_stones.add(valid_cells.pop())
                
    def is_in_shadow(self, r, c, angle):
        """
        Check if grid cell (r, c) is in shadow from any pillar.
        We cast a ray from the center of (r, c) in the direction of the sun (angle).
        If the ray hits a pillar cell, then (r, c) is in shadow.
        """
        if (r, c) in self.pillars:
            return False  # pillars themselves aren't in shadow for movement purposes (they are walls anyway)
            
        # Convert angle to radians
        rad = np.radians(angle)
        dx = np.cos(rad)
        dy = np.sin(rad)
        
        # Start at cell center
        cx = c + 0.5
        cy = r + 0.5
        
        # Step along the ray
        step = 0.1
        dist = 0.6  # start slightly outside self
        max_dist = self.grid_size * 1.414
        
        while dist < max_dist:
            tx = cx + dx * dist
            ty = cy + dy * dist
            
            # Convert to grid indices
            gr = int(ty)
            gc = int(tx)
            
            # Check bounds
            if gr < 0 or gr >= self.grid_size or gc < 0 or gc >= self.grid_size:
                break
                
            if (gr, gc) in self.pillars:
                return True
                
            dist += step
            
        return False
        
    def update_shadows(self):
        """Compute the light/shadow map for the current sun angle."""
        self.shadow_map = np.zeros((self.grid_size, self.grid_size), dtype=bool)
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                if self.is_in_shadow(r, c, self.sun_angle):
                    self.shadow_map[r, c] = True

    @property
    def is_day(self):
        """Day phase when sun is above horizon (0 to 180 degrees)."""
        return 0 <= self.sun_angle < 180

    def is_passable(self, r, c):
        """Check if cell (r, c) is currently walkable."""
        # Boundaries
        if r < 0 or r >= self.grid_size or c < 0 or c >= self.grid_size:
            return False
            
        # Pillars are always impassable
        if (r, c) in self.pillars:
            return False
            
        if self.mode == "calendar_pride_maze":
            if (r, c) in self.gates and self.gates[(r, c)] not in self.collected_prisms:
                return False
            return True
        if self.mode == "calendar_world_environment_day":
            if (r, c) in self.trash_tiles:
                return True # Passable so player can step on it and trigger fail
            
            coverage = len(self.grass_tiles)
            required = int(0.8 * self.grid_size ** 2)
            if coverage < required:
                if (r, c) in self.grass_tiles:
                    return False
            return True
            
        if self.mode == "calendar_world_oceans_day":
            if self.is_high_tide:
                # Deep Trenches are impassable
                if (r, c) in self.deep_trenches:
                    return False
            else:
                # Coral Reefs are impassable
                if (r, c) in self.coral_reefs:
                    return False
            return True
            
        if self.mode == "calendar_juneteenth":
            if (r, c) in self.shadow_walls:
                return False
            return True
            
        if self.mode in ["calendar_fathers_day", "calendar_world_music_day"]:
            return True
            
        if self.mode == "solstice_shift":
            is_pit = (r, c) in self.pits
            if self.is_day:
                return not is_pit  # Open field is passable, pits are impassable
            else:
                return True        # Everything is passable at night (pits become bridges, field remains open but dark)
                
        in_shadow = self.shadow_map[r, c]
        # Solstice Inversion rule
        if self.is_day:
            # Day Phase: Light is passable, shadow is wall
            return not in_shadow
        else:
            # Night Phase: Shadow is passable, light is wall
            return in_shadow

    def is_trapped(self):
        """Check if the player has no valid moves in Environment Day mode."""
        if self.mode != "calendar_world_environment_day" or self.player_pos is None:
            return False
            
        r, c = self.player_pos
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in directions:
            if self.is_passable(r + dr, c + dc):
                return False
        return True

    def check_encircle(self):
        if self.mode != "calendar_world_environment_day":
            return
            
        # BFS from boundary non-grass tiles
        q = []
        visited = set()
        
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                if r == 0 or r == self.grid_size - 1 or c == 0 or c == self.grid_size - 1:
                    if (r, c) not in self.grass_tiles:
                        q.append((r, c))
                        visited.add((r, c))
                        
        while q:
            cr, cc = q.pop(0)
            for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
                nr, nc = cr + dr, cc + dc
                if 0 <= nr < self.grid_size and 0 <= nc < self.grid_size:
                    if (nr, nc) not in visited and (nr, nc) not in self.grass_tiles:
                        visited.add((nr, nc))
                        q.append((nr, nc))
                        
        # Any cell not visited and not grass is encircled!
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                if (r, c) not in visited and (r, c) not in self.grass_tiles:
                    self.grass_tiles.add((r, c))
                    if (r, c) in self.trash_tiles:
                        self.trash_tiles.remove((r, c))
            
    def move_player(self, dr, dc):
        if self.mode == "calendar_world_environment_day" and self.player_pos is None:
            return False
            
        self.prev_player_pos = list(self.player_pos) if self.player_pos else [0, 0]
        if self.mode == "calendar_world_music_day":
            self.correct_note_collected = False
            self.sequence_failed = False
            self.failed_dazed = False
            
        # If dr == 0 and dc == 0, it's a WAIT action
        if dr == 0 and dc == 0:
            self.advance_sun()
            self.collect_stones()
            if self.mode == "calendar_world_oceans_day":
                self.advance_tide()
            if self.mode == "calendar_fathers_day":
                self.dad_energy -= (4.0 + len(self.collected_items) * 2.0)
                if self.dad_energy <= 0.0:
                    self.dad_energy = 0.0
                    self.failed_asleep = True
            return True
            
        if self.mode == "calendar_world_oceans_day":
            nr = self.player_pos[0] + dr
            nc = self.player_pos[1] + dc
            if self.is_passable(nr, nc):
                self.player_pos = [nr, nc]
                
                # Check for turtles
                if tuple(self.player_pos) in self.turtles:
                    self.turtles.remove(tuple(self.player_pos))
                    self.check_goal_reach()
                    
                # 20% chance for a random ocean current to push the player 1 tile
                if random.random() < 0.2:
                    current_dr, current_dc = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
                    push_r = self.player_pos[0] + current_dr
                    push_c = self.player_pos[1] + current_dc
                    if 0 <= push_r < self.grid_size and 0 <= push_c < self.grid_size:
                        self.player_pos = [push_r, push_c]
                        if not self.is_passable(push_r, push_c):
                            self.failed_in_current = True
                        elif tuple(self.player_pos) in self.turtles:
                            self.turtles.remove(tuple(self.player_pos))
                            self.check_goal_reach()
                    
                self.advance_tide()
                return True
            return False
            
        steps = 2 if self.mode == "calendar_pride_maze" else 1
        success = False
        
        for _ in range(steps):
            nr = self.player_pos[0] + dr
            nc = self.player_pos[1] + dc
            
            if self.is_passable(nr, nc):
                self.player_pos = [nr, nc]
                
                if self.mode == "calendar_world_environment_day":
                    if tuple(self.player_pos) in self.trash_tiles:
                        self.failed_on_trash = True
                        break
                    self.grass_tiles.add(tuple(self.player_pos))
                    self.check_encircle()
                    
                    # Spawn tree if 80% reached
                    coverage = len(self.grass_tiles)
                    required = int(0.8 * self.grid_size ** 2)
                    if coverage >= required and not self.tree_spawned:
                        self.tree_spawned = True
                        # Pick random empty spot
                        empty = [(r, c) for r in range(self.grid_size) for c in range(self.grid_size) if (r, c) not in self.grass_tiles and (r, c) not in self.trash_tiles]
                        if empty:
                            self.goal_pos = list(self.rng.choice(empty))
                        else:
                            self.goal_pos = list(self.player_pos)
                
                self.collect_stones()
                self.check_goal_reach()
                success = True
            else:
                break
            
        self.advance_sun()
        self.collect_stones()
        self.check_goal_reach()
        if self.mode == "calendar_fathers_day" and success:
            self.dad_energy -= (4.0 + len(self.collected_items) * 2.0)
            if self.dad_energy <= 0.0:
                self.dad_energy = 0.0
                self.failed_asleep = True
        return success
        
    def check_goal_reach(self):
        """Check and mark if player reached the goals during the correct phase."""
        if self.mode == "calendar_world_oceans_day":
            if len(self.turtles) == 0 and not self.whirlpool_spawned:
                self.whirlpool_spawned = True
                self.goal_pos = [self.grid_size // 2, self.grid_size // 2]
                if tuple(self.goal_pos) in self.coral_reefs:
                    self.coral_reefs.remove(tuple(self.goal_pos))
                if tuple(self.goal_pos) in self.deep_trenches:
                    self.deep_trenches.remove(tuple(self.goal_pos))
            return
            
        if self.mode == "solstice_shift":
            if self.is_day and self.player_pos == self.goal_pos_day:
                self.reached_day_goal = True
            elif not self.is_day and self.player_pos == self.goal_pos_night:
                self.reached_night_goal = True
        
    def collect_stones(self):
        """Collect stones matching the current phase and cell state."""
        r, c = self.player_pos[0], self.player_pos[1]
        
        if self.mode == "calendar_world_music_day":
            if (r, c) in self.musical_notes:
                expected_color = self.note_sequence[self.player_seq_idx]
                note_color = self.musical_notes[(r, c)]
                if note_color == expected_color:
                    self.player_seq_idx += 1
                    del self.musical_notes[(r, c)]
                    self.correct_note_collected = True
                    if self.player_seq_idx == 4:
                        self.goal_pos = [self.grid_size // 2, self.grid_size // 2]
                        center_tuple = tuple(self.goal_pos)
                        if center_tuple in self.pillars:
                            self.pillars.remove(center_tuple)
                        if center_tuple in self.speakers:
                            self.speakers.pop(center_tuple, None)
                        if center_tuple in self.music_obstacles:
                            del self.music_obstacles[center_tuple]
                else:
                    self.reset_musical_sequence()
                    self.sequence_failed = True
            return
            
        if self.mode == "solstice_shift":
            if self.is_day and (r, c) in self.sun_stones:
                self.sun_stones.remove((r, c))
                self.vision_buff_active = True
            elif not self.is_day and (r, c) in self.moon_stones:
                self.moon_stones.remove((r, c))
            return
            
        if self.mode == "calendar_pride_maze":
            if (r, c) in self.prisms:
                expected_color = self.prism_order[len(self.collected_prisms)]
                prism_color = self.prisms[(r, c)]
                if prism_color == expected_color:
                    del self.prisms[(r, c)]
                    self.collected_prisms.append(prism_color)
                    if len(self.prisms) == 0:
                        self.rainbow_bridge_spawned = True
                        self.goal_pos = [self.grid_size // 2, self.grid_size // 2]
                        if tuple(self.goal_pos) in self.pillars:
                            self.pillars.remove(tuple(self.goal_pos))
                        if tuple(self.goal_pos) in self.gates:
                            del self.gates[tuple(self.goal_pos)]
            return
            
        if self.mode == "calendar_juneteenth":
            if tuple(self.player_pos) in self.freedom_bells:
                walls_to_remove = self.freedom_bells[tuple(self.player_pos)]
                for w in walls_to_remove:
                    if w in self.shadow_walls:
                        self.shadow_walls.remove(w)
                del self.freedom_bells[tuple(self.player_pos)]
            if (r, c) in self.freedom_stars:
                self.freedom_stars.remove((r, c))
                if len(self.freedom_stars) == 0:
                    self.goal_pos = [self.grid_size // 2, self.grid_size // 2]
                    if tuple(self.goal_pos) in self.pillars:
                        self.pillars.remove(tuple(self.goal_pos))
                    if tuple(self.goal_pos) in self.shadow_walls:
                        self.shadow_walls.remove(tuple(self.goal_pos))
            return

        if self.mode == "calendar_fathers_day":
            if (r, c) in self.fathers_day_items:
                item_name = self.fathers_day_items.pop((r, c))
                self.collected_items.add(item_name)
                if len(self.fathers_day_items) == 0:
                    self.goal_pos = [self.grid_size // 2, self.grid_size // 2]
                    if tuple(self.goal_pos) in self.pillars:
                        self.pillars.remove(tuple(self.goal_pos))
                    if tuple(self.goal_pos) in self.backyard_obstacles:
                        del self.backyard_obstacles[tuple(self.goal_pos)]
            elif (r, c) in self.coffee_cups:
                self.coffee_cups.remove((r, c))
                self.dad_energy = min(100.0, self.dad_energy + 30.0)
                valid_cells = [
                    (tr, tc) for tr in range(self.grid_size) for tc in range(self.grid_size)
                    if (tr, tc) not in self.pillars 
                    and (tr, tc) not in self.coffee_cups 
                    and (tr, tc) not in self.fathers_day_items 
                    and (tr, tc) != tuple(self.player_pos)
                    and (tr, tc) != tuple(self.goal_pos)
                ]
                if valid_cells:
                    self.coffee_cups.add(random.choice(valid_cells))
            return
            
        in_shadow = self.shadow_map[r, c]
        if self.is_day and not in_shadow:
            if (r, c) in self.sun_stones:
                self.sun_stones.remove((r, c))
        elif not self.is_day and in_shadow:
            if (r, c) in self.moon_stones:
                self.moon_stones.remove((r, c))
                
    def reset_musical_sequence(self):
        self.player_seq_idx = 0
        self.musical_notes = dict(self.original_notes)
        self.goal_pos = [-1, -1]
        
    def advance_sun(self):
        """Advance the sun angle and update shadows."""
        self.just_teleported = False
        if self.mode in ["calendar_pride_maze", "calendar_world_environment_day", "calendar_world_oceans_day", "calendar_juneteenth", "calendar_fathers_day", "calendar_world_music_day"]:
            if self.mode == "calendar_world_music_day":
                self.beat_counter += 1
                # Randomize speaker ranges dynamically on every step
                for pos in self.speakers:
                    self.speakers[pos] = int(self.rng.choice([2, 3, 4, 5]))
                self.soundwave_tiles.clear()
                if self.beat_counter == 4:
                    # Emit Sonic Blast cardinally
                    for speaker_pos, s_range in self.speakers.items():
                        sr, sc = speaker_pos
                        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                            for dist in range(1, s_range + 1):
                                nr, nc = sr + dr * dist, sc + dc * dist
                                if 0 <= nr < self.grid_size and 0 <= nc < self.grid_size:
                                    if (nr, nc) in self.pillars and (nr, nc) not in self.speakers:
                                        break
                                    self.soundwave_tiles.add((nr, nc))
                                else:
                                    break
                    
                    if tuple(self.player_pos) in self.soundwave_tiles:
                        self.player_pos = list(self.prev_player_pos)
                        self.reset_musical_sequence()
                        self.failed_dazed = True
                        self.sequence_failed = True
                    self.beat_counter = 0
                else:
                    self.failed_dazed = False
            return # No sun progression in this mode
            
        if self.mode == "solstice_shift":
            self.move_count += 1
            if self.move_count % 10 == 0:
                was_night = not self.is_day
                self.sun_angle = 180.0 if self.sun_angle == 0.0 else 0.0
                
                if was_night:
                    # Shifting to Day: check if player is on a pit
                    if tuple(self.player_pos) in self.pits:
                        self.failed_in_pit = True
                        
                    # Teleport ONLY when going from Night to Day
                    self.teleport_entities(initial=False)
                    self.vision_buff_active = False
        else:
            self.sun_angle = (self.sun_angle + self.angle_step) % 360.0
        self.update_shadows()
        
    def advance_tide(self):
        if self.mode == "calendar_world_oceans_day":
            self.tide_timer -= 1
            if self.tide_timer <= 0:
                self.is_high_tide = not self.is_high_tide
                self.tide_timer = 10
                
                # Check if player is caught on an impassable tile after the tide shifts
                r, c = self.player_pos
                if not self.is_passable(r, c):
                    self.failed_in_tide = True
        
    def check_win(self):
        """Win condition: All stones collected and player reaches the goal."""
        if self.mode == "calendar_world_oceans_day":
            if self.whirlpool_spawned and self.player_pos == self.goal_pos:
                return True
            return False
            
        if self.mode == "solstice_shift":
            return (len(self.sun_stones) == 0 and 
                    len(self.moon_stones) == 0 and 
                    self.reached_day_goal and 
                    self.reached_night_goal)
        elif self.mode == "calendar_pride_maze":
            return self.rainbow_bridge_spawned and self.player_pos == self.goal_pos
        elif self.mode == "calendar_world_environment_day":
            return self.tree_spawned and self.player_pos == self.goal_pos
        elif self.mode == "calendar_juneteenth":
            return len(self.freedom_stars) == 0 and self.player_pos == self.goal_pos
        elif self.mode == "calendar_fathers_day":
            return len(self.fathers_day_items) == 0 and self.player_pos == self.goal_pos and not self.failed_asleep
        elif self.mode == "calendar_world_music_day":
            return self.player_seq_idx == 4 and self.player_pos == self.goal_pos
        else:
            return (len(self.sun_stones) == 0 and 
                    len(self.moon_stones) == 0 and 
                    self.player_pos == self.goal_pos)
                
    def get_state_grid(self):
        """
        Return a grid representation of the board:
        0: Passable path
        1: Pillar / Permanent wall
        2: Shadow wall (during Day) or Light wall (during Night)
        """
        grid = np.zeros((self.grid_size, self.grid_size), dtype=int)
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                if (r, c) in self.pillars:
                    grid[r, c] = 1
                elif not self.is_passable(r, c):
                    grid[r, c] = 2
        return grid
