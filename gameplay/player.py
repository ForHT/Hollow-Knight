import pygame
from typing import Dict, Optional

from ..interfaces import Entity, EntityType, AnimationState, Vector2, Rect
from ..config import PLAYER_HEALTH, PLAYER_ATTACK_POWER, PLAYER_GROUND_Y, PLAYER_RUN_SPEED, PLAYER_JUMP_VELOCITY

class Player(Entity):
    def __init__(self, pos: Vector2, size: tuple[int, int]):
        super().__init__(EntityType.PLAYER, pos, size, PLAYER_GROUND_Y)
        
        self.max_health = PLAYER_HEALTH
        self.health = self.max_health
        self.attack_power = PLAYER_ATTACK_POWER
        self.body_damage = 0 # 玩家身体不造成伤害
        self.invincible_duration = 1.5

        self.move_speed = PLAYER_RUN_SPEED
        self.jump_velocity = PLAYER_JUMP_VELOCITY

    def handle_input(self, keys: dict):
        if self.state in [AnimationState.HURT, AnimationState.ATTACK]:
            self.velocity.x = 0 # 受伤或攻击时不能移动
            return

        if keys[pygame.K_LEFT]:
            self.velocity.x = -self.move_speed
            self.facing_right = False
        elif keys[pygame.K_RIGHT]:
            self.velocity.x = self.move_speed
            self.facing_right = True
        else:
            self.velocity.x = 0
        
        if keys[pygame.K_z] and self.on_ground:
            self.velocity.y = self.jump_velocity
            self.on_ground = False
        
        if keys[pygame.K_x]: # 假设x是攻击键
             self.state = AnimationState.ATTACK

    def update_state(self):
        # 状态机逻辑
        if self.state in [AnimationState.ATTACK, AnimationState.HURT]:
             # 假设这些状态有固定持续时间，结束后回到fall/idle
             # 实际项目中这里会由动画系统或计时器控制
            if self.invincible_timer <= 0: # 简单用无敌时间判断受伤结束
                self.state = AnimationState.IDLE
            return

        if not self.on_ground:
            self.state = AnimationState.JUMP if self.velocity.y < 0 else AnimationState.FALL
        else:
            if self.velocity.x != 0:
                self.state = AnimationState.WALK
            else:
                self.state = AnimationState.IDLE

    def update(self, dt: float, keys: dict):
        if self.invincible_timer > 0:
            self.invincible_timer -= dt
        
        self.handle_input(keys)
        self.update_state()
        
    def take_damage(self, amount: int):
        if self.invincible_timer <= 0:
            self.health -= amount
            self.invincible_timer = self.invincible_duration
            self.state = AnimationState.HURT
            self.velocity.x = -5 if self.facing_right else 5 # 轻微击退
            self.velocity.y = -10
            print(f"Player took {amount} damage, health: {self.health}")
            if self.health <= 0:
                self.state = AnimationState.DEAD

    def get_attack_hitbox(self) -> Optional[Rect]:
        if self.state != AnimationState.ATTACK:
            return None
        
        hitbox = Rect(0, 0, 100, 80)
        if self.facing_right:
            hitbox.midleft = self.hitbox.midright
        else:
            hitbox.midright = self.hitbox.midleft
        return hitbox

    def draw(self, surface: pygame.Surface, camera_offset: Vector2):
        # 简单绘制
        color = (0, 255, 0) # Green
        if self.invincible_timer > 0 and int(self.invincible_timer * 10) % 2 == 0:
            return # 闪烁
        pygame.draw.rect(surface, color, self.hitbox.move(-camera_offset.x, -camera_offset.y))