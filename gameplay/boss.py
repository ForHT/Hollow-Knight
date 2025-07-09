import pygame
from typing import Optional

from ..interfaces import Entity, EntityType, AnimationState, Vector2, Rect
from ..config import BOSS_HEALTH, BOSS_ATTACK_POWER, BOSS_BODY_DAMAGE, ENEMY_GROUND_Y

class Boss(Entity):
    def __init__(self, pos: Vector2, size: tuple[int, int]):
        super().__init__(EntityType.BOSS, pos, size, ENEMY_GROUND_Y)
        
        self.max_health = BOSS_HEALTH
        self.health = self.max_health
        self.attack_power = BOSS_ATTACK_POWER
        self.body_damage = BOSS_BODY_DAMAGE
        self.invincible_duration = 0.2

    def update(self, dt: float, player_pos: Vector2):
        if self.invincible_timer > 0:
            self.invincible_timer -= dt
        # 简单的AI: 走向玩家
        if abs(player_pos.x - self.position.x) > 50:
            if player_pos.x < self.position.x:
                self.velocity.x = -3
                self.facing_right = False
            else:
                self.velocity.x = 3
                self.facing_right = True
        else:
            self.velocity.x = 0

    def take_damage(self, amount: int):
        if self.invincible_timer <= 0:
            self.health -= amount
            self.invincible_timer = self.invincible_duration
            print(f"Boss took {amount} damage, health: {self.health}")
            if self.health <= 0:
                self.state = AnimationState.DEAD

    def draw(self, surface: pygame.Surface, camera_offset: Vector2):
        color = (255, 0, 0) # Red
        pygame.draw.rect(surface, color, self.hitbox.move(-camera_offset.x, -camera_offset.y))