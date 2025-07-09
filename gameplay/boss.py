import pygame
import random
from typing import Optional

from interfaces import Entity, EntityType, Vector2, Rect
from configs import (
    BOSS_HEALTH, BOSS_ATTACK_POWER, BOSS_BODY_DAMAGE, ENEMY_GROUND_Y,
    BOSS_ACTION_COOLDOWN, BOSS_WALK_COOLDOWN, BOSS_JUMP_COOLDOWN, 
    BOSS_JUMPDASH_COOLDOWN, BOSS_DASH_COOLDOWN, BOSS_JUMPFINAL_COOLDOWN
)

class Boss(Entity):
    def __init__(self, pos: Vector2, size: tuple[int, int]):
        super().__init__(
            pos=pos, 
            size=size, 
            ground_y=ENEMY_GROUND_Y,
            entity_type=EntityType.BOSS
        )
        
        self.max_health = BOSS_HEALTH
        self.health = self.max_health
        self.attack_power = BOSS_ATTACK_POWER
        self.body_damage = BOSS_BODY_DAMAGE
        self.invincible_duration = 0.2 * 60 # 将秒转换为帧

        # AI状态
        self.action_cooldown = 0
        self.walk_cooldown = 0
        self.jump_cooldown = 0
        self.jumpdash_cooldown = 0
        self.dash_cooldown = 0
        self.jumpfinal_cooldown = 0
        self.action_timer = 0
        self.state = "idle"


    def decide_action(self, player_pos: Vector2):
        """决定下一步行动的核心AI逻辑。"""
        self.action_cooldown = BOSS_ACTION_COOLDOWN
        
        # 判断朝向玩家的方向
        player_is_to_the_right = player_pos.x > self.position.x
        self.facing_right = player_is_to_the_right

        # 创建一个可用招式的列表
        available_moves = []
        if self.walk_cooldown <= 0: available_moves.append(self.walk)
        if self.jump_cooldown <= 0: available_moves.append(self.jump)
        if self.dash_cooldown <= 0: available_moves.append(self.dash)
        if self.jumpdash_cooldown <= 0: available_moves.append(self.jumpdash)
        if self.jumpfinal_cooldown <= 0: available_moves.append(self.jumpfinal)

        if not available_moves:
            self.walk() # 如果没有可用招式，则执行默认行动
            return

        # 随机选择并执行一个招式
        chosen_move = random.choice(available_moves)
        chosen_move()

    def walk(self):
        self.state = "b_walk"
        self.walk_cooldown = BOSS_WALK_COOLDOWN
        self.action_timer = 60 # 行走60帧
        
    def jump(self):
        self.state = "b_jump"
        self.jump_cooldown = BOSS_JUMP_COOLDOWN
        self.velocity.y = -60 # 来自C++代码
        self.action_timer = 120 # 大概的持续时间

    def dash(self):
        self.state = "b_dash"
        self.dash_cooldown = BOSS_DASH_COOLDOWN
        self.action_timer = 30 # 冲刺30帧

    def jumpdash(self):
        self.state = "b_jumpdash"
        self.jumpdash_cooldown = BOSS_JUMPDASH_COOLDOWN
        self.action_timer = 100 # 大概的持续时间

    def jumpfinal(self):
        self.state = "b_jumpfinal"
        self.jumpfinal_cooldown = BOSS_JUMPFINAL_COOLDOWN
        self.velocity.y = -60
        self.action_timer = 180 # 大概的持续时间

    def update(self, player_pos: Vector2):
        # 0. 检查死亡状态
        if self.health <= 0:
            self.state = "dead"
            self.velocity.x = 0
            return

        # 1. 更新计时器和冷却时间
        if self.invincible_timer > 0: self.invincible_timer -= 1
        if self.action_cooldown > 0: self.action_cooldown -= 1
        if self.walk_cooldown > 0: self.walk_cooldown -= 1
        if self.jump_cooldown > 0: self.jump_cooldown -= 1
        if self.dash_cooldown > 0: self.dash_cooldown -= 1
        if self.jumpdash_cooldown > 0: self.jumpdash_cooldown -= 1
        if self.jumpfinal_cooldown > 0: self.jumpfinal_cooldown -= 1
        if self.action_timer > 0: self.action_timer -= 1

        # 2. AI决策
        if self.action_cooldown <= 0 and self.state in ["idle", "b_walk"]:
             self.decide_action(player_pos)
        
        # 3. 执行状态逻辑
        if self.state == "idle":
             self.velocity.x = 0
        elif self.state == "b_walk":
            self.velocity.x = 3 if self.facing_right else -3
            if self.action_timer <= 0:
                self.state = "idle"
        elif self.state == "b_dash":
            self.velocity.x = 15 if self.facing_right else -15
            if self.action_timer <= 0:
                self.state = "idle"

        # --- 攻击状态逻辑 ---
        elif self.state == "b_jump":
            # 简单跳跃，水平移动较少
            if self.on_ground and self.velocity.y == 0:
                self.state = "idle"
        elif self.state == "b_jumpdash":
            # 一个更复杂的冲刺跳跃，暂时当作普通跳跃处理
            if self.on_ground and self.velocity.y == 0:
                self.state = "idle"
        elif self.state == "b_jumpfinal":
            # 追踪跳跃攻击
            direction_to_player = 1 if player_pos.x > self.position.x else -1
            # 在C++中，这是由dmove处理的。我们用速度来模拟它。
            # 攻击的空中部分。
            if not self.on_ground:
                 self.velocity.x = 25 * direction_to_player
            else:
                 self.velocity.x = 0 # 落地后停止水平移动

            if self.on_ground and self.action_timer < 100: # 假设这是动画的落地部分
                self.state = "idle"


    def take_damage(self, amount: int):
        if self.invincible_timer <= 0:
            self.health -= amount
            self.invincible_timer = self.invincible_duration
            print(f"Boss took {amount} damage, health: {self.health}")

    def draw(self, surface: pygame.Surface, camera_offset: Vector2):
        color = (255, 0, 0) # Red
        if self.state != "dead":
            pygame.draw.rect(surface, color, self.hitbox.move(-camera_offset.x, -camera_offset.y))