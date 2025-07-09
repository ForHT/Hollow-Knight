import pygame
from typing import Dict, Optional

from interfaces import Entity, EntityType, AnimationState, Vector2, Rect
from configs import (
    PLAYER_HEALTH, PLAYER_ATTACK_POWER, PLAYER_GROUND_Y, PLAYER_RUN_SPEED, 
    PLAYER_JUMP_VELOCITY, PLAYER_DASH_SPEED, PLAYER_DASH_DURATION, PLAYER_DASH_COOLDOWN
)

class Player(Entity):
    def __init__(self, pos: Vector2, size: tuple[int, int]):
        super().__init__(EntityType.PLAYER, pos, size, PLAYER_GROUND_Y)
        
        # 统计数据
        self.max_health = PLAYER_HEALTH
        self.health = self.max_health
        self.attack_power = PLAYER_ATTACK_POWER
        self.body_damage = 0 # 玩家身体不造成伤害
        
        # 移动
        self.move_speed = PLAYER_RUN_SPEED
        self.jump_velocity_val = PLAYER_JUMP_VELOCITY

        # 冲刺
        self.dash_speed = PLAYER_DASH_SPEED
        self.dash_duration = PLAYER_DASH_DURATION
        self.dash_cooldown_max = PLAYER_DASH_COOLDOWN
        self.dash_cooldown = 0
        self.dash_timer = 0

        # 攻击
        self.attack_cooldown_max = 30  # 从C++代码中获取
        self.attack_cooldown = 0
        self.attack_timer = 0
        self.up_attack_cooldown = 0
        self.down_attack_cooldown = 0

        # 无敌与受伤
        self.invincible_duration_frames = 1.5 * 60  # 将秒转换为帧
        self.invincible_timer = 0
        self.hurt_duration_frames = 5 # 受伤硬直状态的持续时间（帧）
        self.hurt_timer = 0

    def handle_input(self, keys):
        """此函数仅设置意图或触发即时操作，如攻击/跳跃。"""
        # 在硬直、攻击、冲刺时，忽略大部分输入
        if self.hurt_timer > 0 or self.state in [AnimationState.ATTACK, AnimationState.ATTACK_UP, AnimationState.ATTACK_DOWN, AnimationState.DASH]:
            return

        # 水平移动
        if keys[pygame.K_a]:
            self.velocity.x = -self.move_speed
            self.facing_right = False
        elif keys[pygame.K_d]:
            self.velocity.x = self.move_speed
            self.facing_right = True
        else:
            self.velocity.x = 0
        
        # 跳跃
        if keys[pygame.K_k] and self.on_ground:
            self.jump()
        
        # 攻击 (J key)
        if keys[pygame.K_j] and self.attack_cooldown <= 0:
            # Check for up or down attacks first
            if keys[pygame.K_w]:
                self.attack_up()
            elif keys[pygame.K_s] and not self.on_ground:
                self.attack_down()
            else:
                self.attack()

        # 冲刺
        if keys[pygame.K_l] and self.dash_cooldown <= 0:
            self.dash()

    def jump(self):
        """处理跳跃逻辑。"""
        if self.on_ground:
            self.velocity.y = self.jump_velocity_val
            self.on_ground = False
            self.state = AnimationState.JUMP

    def attack(self):
        """处理攻击逻辑。"""
        self.state = AnimationState.ATTACK
        self.velocity.x = 0
        self.attack_cooldown = self.attack_cooldown_max
        self.attack_timer = 15  # 攻击动画持续15帧

    def attack_up(self):
        """处理上挑攻击。"""
        self.state = AnimationState.ATTACK_UP
        self.velocity.x = 0
        self.attack_cooldown = self.attack_cooldown_max # 与普通攻击共享冷却时间
        self.attack_timer = 15

    def attack_down(self):
        """处理下劈攻击。"""
        self.state = AnimationState.ATTACK_DOWN
        self.attack_cooldown = self.attack_cooldown_max
        self.attack_timer = 15

    def pogo_bounce(self):
        """在下劈命中后提供的弹力。"""
        self.velocity.y = self.jump_velocity_val * 0.9 # 比完整跳跃稍弱的弹力

    def dash(self):
        """处理冲刺逻辑。"""
        self.state = AnimationState.DASH
        self.dash_timer = self.dash_duration
        self.dash_cooldown = self.dash_cooldown_max
        self.invincible_timer = self.dash_duration  # 冲刺时无敌

    def update_state(self):
        """核心状态机逻辑。"""
        # 如果一次性动画正在播放，让它完成
        if self.state in [AnimationState.ATTACK, AnimationState.ATTACK_UP, AnimationState.ATTACK_DOWN]:
            if self.attack_timer <= 0:
                self.state = AnimationState.IDLE
            return
        
        if self.state == AnimationState.DASH:
            if self.dash_timer <= 0:
                self.velocity.x = 0  # 停止冲刺
                self.state = AnimationState.IDLE
            return

        # 受伤状态只在硬直结束后才允许恢复
        if self.state == AnimationState.HURT:
            if self.hurt_timer <= 0:
                self.state = AnimationState.IDLE
            return

        # 否则，根据物理状态确定状态
        if not self.on_ground:
            self.state = AnimationState.JUMP if self.velocity.y < 0 else AnimationState.FALL
        else:
            if self.velocity.x != 0:
                self.state = AnimationState.WALK
            else:
                self.state = AnimationState.IDLE

    def update(self, keys):
        """每帧更新玩家。"""
        # 1. 递减计时器
        if self.invincible_timer > 0:
            self.invincible_timer -= 1
        if self.hurt_timer > 0:
            self.hurt_timer -= 1
        if self.dash_cooldown > 0:
            self.dash_cooldown -= 1
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        if self.attack_timer > 0 and self.state in [AnimationState.ATTACK, AnimationState.ATTACK_UP, AnimationState.ATTACK_DOWN]:
            self.attack_timer -= 1
        if self.dash_timer > 0 and self.state == AnimationState.DASH:
            self.dash_timer -= 1

        # 2. 处理输入以改变状态
        self.handle_input(keys)

        # 3. 应用基于状态的逻辑
        if self.state == AnimationState.DASH:
            self.velocity.y = 0
            self.velocity.x = self.dash_speed if self.facing_right else -self.dash_speed
        
        # 4. 根据物理和计时器更新状态
        self.update_state()
        
    def take_damage(self, amount: int):
        if self.invincible_timer <= 0:
            self.health -= amount
            self.invincible_timer = self.invincible_duration_frames
            self.hurt_timer = self.hurt_duration_frames
            self.state = AnimationState.HURT
            # 轻微击退
            self.velocity.x = -5 if self.facing_right else 5 
            self.velocity.y = -10
            print(f"Player took {amount} damage, health: {self.health}")
            if self.health <= 0:
                self.state = AnimationState.DEAD

    def get_attack_hitbox(self) -> Optional[Rect]:
        if self.state not in [AnimationState.ATTACK, AnimationState.ATTACK_UP, AnimationState.ATTACK_DOWN]:
            return None
        
        # Base hitbox centered on player for calculation
        base_rect = self.hitbox

        if self.state == AnimationState.ATTACK:
            hitbox = Rect(0, 0, 100, 80)
            if self.facing_right:
                hitbox.midleft = base_rect.midright
            else:
                hitbox.midright = base_rect.midleft
            return hitbox
        
        elif self.state == AnimationState.ATTACK_UP:
            hitbox = Rect(0, 0, 80, 100)
            hitbox.midbottom = base_rect.midtop
            return hitbox

        elif self.state == AnimationState.ATTACK_DOWN:
            hitbox = Rect(0, 0, 80, 100)
            hitbox.midtop = base_rect.midbottom
            return hitbox
        
        return None


    def draw(self, surface: pygame.Surface, camera_offset: Vector2):
        # 简单绘制
        color = (0, 255, 0) # Green
        # 无敌时闪烁
        if self.invincible_timer > 0 and (self.invincible_timer // 3) % 2 == 0:
            return 
        pygame.draw.rect(surface, color, self.hitbox.move(-camera_offset.x, -camera_offset.y))

class Effect(Player):
    def __init__(self, pos: Vector2, size: tuple[int, int] = (0, 0)):
        super().__init__(pos, size)
        