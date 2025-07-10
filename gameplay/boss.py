import pygame
import random
from typing import Optional

from interfaces import Entity, EntityType, Vector2, Rect
from configs import (
    BOSS_HEALTH, BOSS_ATTACK_POWER, BOSS_BODY_DAMAGE, ENEMY_GROUND_Y,
    BOSS_ACTION_COOLDOWN, BOSS_WALK_COOLDOWN, BOSS_JUMP_COOLDOWN, 
    BOSS_JUMPDASH_COOLDOWN, BOSS_DASH_COOLDOWN, BOSS_JUMPFINAL_COOLDOWN,
    BOSS_AI_CLOSE_DISTANCE, BOSS_AI_MEDIUM_DISTANCE
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
        
        # 1. 判断朝向玩家的方向
        if self.state in ["idle", "walk"]: # 只有在地面非攻击状态下才转身
            player_is_to_the_right = player_pos.x > self.position.x
            self.facing_right = player_is_to_the_right

        # 2. 计算与玩家的距离
        distance_to_player = abs(player_pos.x - self.position.x)

        # 3. 获取所有冷却结束的招式
        available_moves = []
        if self.walk_cooldown <= 0: available_moves.append(self.walk)
        if self.jump_cooldown <= 0: available_moves.append(self.jump)
        if self.dash_cooldown <= 0: available_moves.append(self.dash)
        if self.jumpdash_cooldown <= 0: available_moves.append(self.jumpdash)
        if self.jumpfinal_cooldown <= 0: available_moves.append(self.jumpfinal)

        # 如果所有技能都在冷却，则什么都不做
        if not available_moves:
            self.state = "idle"
            return

        # 4. 根据距离筛选出合适的招式列表
        preferred_moves = []
        if distance_to_player < BOSS_AI_CLOSE_DISTANCE:
            # 近距离：使用普通跳跃拉开距离
            preferred_moves.append(self.jump)
        elif distance_to_player < BOSS_AI_MEDIUM_DISTANCE:
            # 中距离：使用舞丝攻击或行走调整位置
            preferred_moves.append(self.jumpfinal)
            preferred_moves.append(self.walk)
        else: # 远距离
            # 远距离：使用冲刺或跳跃冲刺来接近
            preferred_moves.append(self.dash)
            preferred_moves.append(self.jumpdash)
        
        # 5. 找出当前可用且合适的招式
        valid_moves = [move for move in preferred_moves if move in available_moves]

        # 6. 决策
        if valid_moves:
            # 从合适的招式中随机选择一个执行
            chosen_move = random.choice(valid_moves)
            chosen_move()
        else:
            # 如果当前距离下没有合适的招式可用（比如都在CD），
            # 则从所有可用的招式中选择一个执行，优先选择行走
            if self.walk in available_moves:
                self.walk()
            else:
                # 如果行走也在CD，就从剩下可用的里面随便选一个
                if available_moves:
                    random.choice(available_moves)()
                else:
                    self.state = "idle" # 如果真的一个技能都用不了，就待机

    def walk(self):
        self.state = "walk"
        self.walk_cooldown = BOSS_WALK_COOLDOWN
        self.action_timer = 60 # 行走60帧
        
    def jump(self):
        self.state = "jump"
        self.jump_cooldown = BOSS_JUMP_COOLDOWN
        self.velocity.y = -60 # 来自C++代码
        self.action_timer = 120 # 大概的持续时间

    def dash(self):
        self.state = "dash"
        self.dash_cooldown = BOSS_DASH_COOLDOWN
        self.action_timer = 30 # 冲刺30帧

    def jumpdash(self):
        self.state = "jump_dash"
        self.jumpdash_cooldown = BOSS_JUMPDASH_COOLDOWN
        self.action_timer = 100 # 大概的持续时间

    def jumpfinal(self):
        self.state = "jump_final"
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
        if self.action_cooldown <= 0 and self.state in ["idle", "walk"]:
             self.decide_action(player_pos)
        
        # 3. 执行状态逻辑
        if self.state == "idle":
             self.velocity.x = 0
        elif self.state == "walk":
            self.velocity.x = 7 if self.facing_right else -7
            if self.action_timer <= 0:
                self.state = "idle"
        elif self.state == "dash":
            self.velocity.x = 15 if self.facing_right else -15
            if self.action_timer <= 0:
                self.state = "idle"

        # --- 攻击状态逻辑 ---
        elif self.state == "jump":
            # 简单跳跃，水平移动较少
            if self.on_ground and self.velocity.y == 0:
                self.state = "idle"
        elif self.state == "jump_dash":
            # 一个更复杂的冲刺跳跃，暂时当作普通跳跃处理
            if self.on_ground and self.velocity.y == 0:
                self.state = "idle"
        elif self.state == "jump_final":
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
        pass