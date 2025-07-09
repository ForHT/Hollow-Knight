import pygame
import random
from typing import Optional

from interfaces import Entity, EntityType, AnimationState, Vector2, Rect
from config import (
    BOSS_HEALTH, BOSS_ATTACK_POWER, BOSS_BODY_DAMAGE, ENEMY_GROUND_Y,
    BOSS_ACTION_COOLDOWN, BOSS_WALK_COOLDOWN, BOSS_JUMP_COOLDOWN, 
    BOSS_JUMPDASH_COOLDOWN, BOSS_DASH_COOLDOWN, BOSS_JUMPFINAL_COOLDOWN
)

class Boss(Entity):
    def __init__(self, pos: Vector2, size: tuple[int, int]):
        super().__init__(EntityType.BOSS, pos, size, ENEMY_GROUND_Y)
        
        self.max_health = BOSS_HEALTH
        self.health = self.max_health
        self.attack_power = BOSS_ATTACK_POWER
        self.body_damage = BOSS_BODY_DAMAGE
        self.invincible_duration = 0.2 * 60 # Convert to frames

        # AI State
        self.action_cooldown = 0
        self.walk_cooldown = 0
        self.jump_cooldown = 0
        self.jumpdash_cooldown = 0
        self.dash_cooldown = 0
        self.jumpfinal_cooldown = 0
        self.action_timer = 0
        self.state = AnimationState.IDLE


    def decide_action(self, player_pos: Vector2):
        """The core AI logic to decide the next move."""
        self.action_cooldown = BOSS_ACTION_COOLDOWN
        
        # Determine direction towards player
        player_is_to_the_right = player_pos.x > self.position.x
        self.facing_right = player_is_to_the_right

        # Build a list of available moves
        available_moves = []
        if self.walk_cooldown <= 0: available_moves.append(self.walk)
        if self.jump_cooldown <= 0: available_moves.append(self.jump)
        if self.dash_cooldown <= 0: available_moves.append(self.dash)
        if self.jumpdash_cooldown <= 0: available_moves.append(self.jumpdash)
        if self.jumpfinal_cooldown <= 0: available_moves.append(self.jumpfinal)

        if not available_moves:
            self.walk() # Default action if nothing is available
            return

        # Choose and execute a random move
        chosen_move = random.choice(available_moves)
        chosen_move()

    def walk(self):
        self.state = AnimationState.B_WALK
        self.walk_cooldown = BOSS_WALK_COOLDOWN
        self.action_timer = 60 # Walk for 60 frames
        
    def jump(self):
        self.state = AnimationState.B_JUMP
        self.jump_cooldown = BOSS_JUMP_COOLDOWN
        self.velocity.y = -60 # From C++ code
        self.action_timer = 120 # Approximate duration

    def dash(self):
        self.state = AnimationState.B_DASH
        self.dash_cooldown = BOSS_DASH_COOLDOWN
        self.action_timer = 30 # Dash for 30 frames

    def jumpdash(self):
        self.state = AnimationState.B_JUMPDASH
        self.jumpdash_cooldown = BOSS_JUMPDASH_COOLDOWN
        self.action_timer = 100 # Approximate duration

    def jumpfinal(self):
        self.state = AnimationState.B_JUMPFINAL
        self.jumpfinal_cooldown = BOSS_JUMPFINAL_COOLDOWN
        self.velocity.y = -60
        self.action_timer = 180 # Approximate duration

    def update(self, player_pos: Vector2):
        # 0. Check for death
        if self.health <= 0:
            self.state = AnimationState.DEAD
            self.velocity.x = 0
            return

        # 1. Update timers and cooldowns
        if self.invincible_timer > 0: self.invincible_timer -= 1
        if self.action_cooldown > 0: self.action_cooldown -= 1
        if self.walk_cooldown > 0: self.walk_cooldown -= 1
        if self.jump_cooldown > 0: self.jump_cooldown -= 1
        if self.dash_cooldown > 0: self.dash_cooldown -= 1
        if self.jumpdash_cooldown > 0: self.jumpdash_cooldown -= 1
        if self.jumpfinal_cooldown > 0: self.jumpfinal_cooldown -= 1
        if self.action_timer > 0: self.action_timer -= 1

        # 2. AI Decision Making
        if self.action_cooldown <= 0 and self.state in [AnimationState.IDLE, AnimationState.B_WALK]:
             self.decide_action(player_pos)
        
        # 3. Execute state logic
        if self.state == AnimationState.IDLE:
             self.velocity.x = 0
        elif self.state == AnimationState.B_WALK:
            self.velocity.x = 3 if self.facing_right else -3
            if self.action_timer <= 0:
                self.state = AnimationState.IDLE
        elif self.state == AnimationState.B_DASH:
            self.velocity.x = 15 if self.facing_right else -15
            if self.action_timer <= 0:
                self.state = AnimationState.IDLE
        elif self.state in [AnimationState.B_JUMP, AnimationState.B_JUMPFINAL, AnimationState.B_JUMPDASH]:
            # Horizontal movement during jumps can be added here
            if self.on_ground and self.velocity.y == 0:
                self.state = AnimationState.IDLE

    def take_damage(self, amount: int):
        if self.invincible_timer <= 0:
            self.health -= amount
            self.invincible_timer = self.invincible_duration
            print(f"Boss took {amount} damage, health: {self.health}")

    def draw(self, surface: pygame.Surface, camera_offset: Vector2):
        color = (255, 0, 0) # Red
        if self.state != AnimationState.DEAD:
            pygame.draw.rect(surface, color, self.hitbox.move(-camera_offset.x, -camera_offset.y))