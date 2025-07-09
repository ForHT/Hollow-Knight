import pygame
from typing import Dict, Optional

from interfaces import Entity, EntityType, Vector2, Rect
from configs import (
    PLAYER_HEALTH, PLAYER_ATTACK_POWER, PLAYER_GROUND_Y, 
    PLAYER_JUMP_VELOCITY, PLAYER_DASH_DURATION, PLAYER_DASH_COOLDOWN, FPS,
    PLAYER_RUN_SPEED
)
from config.animation_data import PLAYER_ANIMATIONS
# from config.states import PLAYER_STATE_MACHINE # We will create a new one based on animation data

# A more dynamic state machine can be built from the animation data keys
PLAYER_STATE_MACHINE = {
    state: list(PLAYER_ANIMATIONS.keys()) for state in PLAYER_ANIMATIONS
}
# TODO: Refine state machine with more specific transition rules later


class Player(Entity):
    def __init__(self, pos: Vector2, size: tuple[int, int]):
        super().__init__(EntityType.PLAYER, pos, size, PLAYER_GROUND_Y)
        
        self.state = "idle" # 初始状态
        
        # 统计数据
        self.max_health = PLAYER_HEALTH
        self.health = self.max_health
        self.attack_power = PLAYER_ATTACK_POWER
        self.body_damage = 0

        # 移动 (不再需要硬编码的速度)
        self.run_speed = PLAYER_RUN_SPEED
        self.jump_velocity_val = PLAYER_JUMP_VELOCITY

        # 冲刺
        # self.dash_speed = PLAYER_DASH_SPEED
        self.dash_duration = PLAYER_DASH_DURATION
        self.dash_cooldown_max = PLAYER_DASH_COOLDOWN
        self.dash_cooldown = 0
        self.dash_timer = 0

        # 攻击
        self.attack_cooldown_max = 30
        self.attack_cooldown = 0
        # self.attack_timer is no longer needed

        # 无敌与受伤
        self.invincible_duration_frames = 1.5 * 60
        self.invincible_timer = 0
        self.hurt_duration_frames = 5
        self.hurt_timer = 0
        
        self.was_on_ground = True # 用于检测落地瞬间

    def set_state(self, new_state: str):
        """设置玩家状态，会检查状态转换是否合法。"""
        # 总是允许从任何状态转换到受伤或死亡
        if new_state in ["damage", "dead"]:
            if self.state != new_state:
                # print(f"Player state changed to: {new_state}") # For debugging
                self.state = new_state
            return

        # 检查转换是否在状态机中定义为合法
        if self.state in PLAYER_STATE_MACHINE and new_state in PLAYER_STATE_MACHINE[self.state]:
            if self.state != new_state:
                # print(f"Player state changed to: {new_state}") # For debugging
                self.state = new_state
        else:
            # 只有在尝试进行非法转换时才打印警告
            if self.state != new_state:
                # print(f"Warning: Illegal state transition attempted from {self.state} to {new_state}") # For debugging
                pass

    def handle_input(self, keys):
        """处理输入，并根据输入和当前状态请求状态变更。"""
        # 在硬直时忽略所有输入
        if self.hurt_timer > 0:
            return
        
        # 1. 优先处理攻击、冲刺等会打断其他动作的输入
        if keys[pygame.K_j] and self.attack_cooldown <= 0:
            if keys[pygame.K_w]:
                self.attack_up()
            elif keys[pygame.K_s] and not self.on_ground:
                self.attack_down()
            else:
                self.attack()
            return

        if keys[pygame.K_l] and self.dash_cooldown <= 0 and self.state != 'dash':
            self.dash()
            return
            
        # 2. 如果没有攻击或冲刺，再处理跳跃和移动
        # 只有在地面时才能起跳
        if keys[pygame.K_k] and self.on_ground:
            self.jump()
            # 跳跃后，本帧不再处理移动
            return

        # 3. 只有在可移动的状态下，才处理移动逻辑
        # C++代码是在特定状态下，直接修改位置
        if self.state in ["idle", "walk", "jump_land", "jump_start", "jump_loop"]:
            is_moving = False
            if keys[pygame.K_a]:
                self.position.x -= self.run_speed # 直接修改位置
                self.facing_right = False
                is_moving = True
            elif keys[pygame.K_d]:
                self.position.x += self.run_speed # 直接修改位置
                self.facing_right = True
                is_moving = True
            
            # 在地面时，根据移动设置 idle/walk 状态
            if self.on_ground:
                if is_moving:
                    self.set_state("walk")
                else:
                    self.set_state("idle")

    def jump(self):
        self.velocity.y = self.jump_velocity_val
        self.on_ground = False
        self.set_state("jump_start")

    def attack(self):
        self.set_state("attack")
        self.attack_cooldown = self.attack_cooldown_max

    def attack_up(self):
        self.set_state("attack_up")
        self.attack_cooldown = self.attack_cooldown_max

    def attack_down(self):
        self.set_state("attack_down")
        self.attack_cooldown = self.attack_cooldown_max

    def pogo_bounce(self):
        self.velocity.y = self.jump_velocity_val * 0.9

    def dash(self):
        self.set_state("dash")
        self.dash_timer = self.dash_duration
        self.dash_cooldown = self.dash_cooldown_max
        self.invincible_timer = self.dash_duration

    def update(self, keys, animation_system): # 接收 animation_system
        # 1. 递减计时器
        if self.invincible_timer > 0: self.invincible_timer -= 1
        if self.hurt_timer > 0: self.hurt_timer -= 1
        if self.dash_cooldown > 0: self.dash_cooldown -= 1
        if self.attack_cooldown > 0: self.attack_cooldown -= 1
        if self.dash_timer > 0: self.dash_timer -= 1

        # 2. 处理输入（会改变状态和位置）
        self.handle_input(keys)
        
        # 3. 水平速度衰减
        # 这使得我们可以有速度脉冲（如击退），同时又不会无限滑行
        friction = 0.8
        self.velocity.x *= friction
        if abs(self.velocity.x) < 0.1:
            self.velocity.x = 0

        # 4. 根据状态应用特殊逻辑 (不再需要从动画获取速度)
        if self.state == "dash":
            if self.dash_timer <= 0:
                self.set_state("idle") # 冲刺结束后回到待机
            else:
                self.velocity.y = 0 # 冲刺时无重力
        
        # 5. 处理非输入驱动的状态转换（如落地）
        # 检测落地瞬间
        is_landing = self.on_ground and not self.was_on_ground
        if is_landing and self.state in ["jump_loop", "jump_start"]:
            self.set_state("idle") # TODO: C++里没有jump_land, 暂时先回到idle

        # 更新上一帧的在的状况
        self.was_on_ground = self.on_ground

        # 6. 受伤状态处理
        if self.state == "damage" and self.hurt_timer <= 0:
            self.set_state("idle")

    def take_damage(self, amount: int):
        if self.invincible_timer <= 0:
            self.health -= amount
            self.invincible_timer = self.invincible_duration_frames
            self.hurt_timer = self.hurt_duration_frames
            self.set_state("damage")
            # 恢复C++中的速度脉冲逻辑以实现明显的击退效果
            self.velocity.x = 5 if self.facing_right else -5 
            self.velocity.y = -20 # 稍微增强向上的力道以获得更好的手感
            print(f"Player took {amount} damage, health: {self.health}")
            if self.health <= 0:
                self.set_state("dead")

    def get_attack_hitbox(self) -> Optional[Rect]:
        if "attack" not in self.state:
            return None
        
        base_rect = self.hitbox

        if self.state == "attack":
            hitbox = Rect(0, 0, 100, 80)
            if self.facing_right:
                hitbox.midleft = base_rect.midright
            else:
                hitbox.midright = base_rect.midleft
            return hitbox
        
        elif self.state == "attack_up":
            hitbox = Rect(0, 0, 80, 100)
            hitbox.midbottom = base_rect.midtop
            return hitbox

        elif self.state == "attack_down":
            hitbox = Rect(0, 0, 80, 100)
            hitbox.midtop = base_rect.midbottom
            return hitbox
        
        return None

    def draw(self, surface: pygame.Surface, camera_offset: Vector2):
        # 绘制逻辑已经完全由AnimationSystem处理，该方法保留用于调试
        # color = (0, 255, 0)
        # if self.invincible_timer > 0 and (self.invincible_timer // 3) % 2 == 0:
        #     return
        # pygame.draw.rect(surface, color, self.hitbox.move(-camera_offset.x, -camera_offset.y))
        pass


class Effect(Entity):
    def __init__(self, pos: Vector2, size: tuple[int, int] = (0, 0)):
        super().__init__(EntityType.EFFECT, pos, size, 0)
        self.state = "dash_effect"
    
    def update(self, *args, **kwargs):
        pass # 特效实体通常由其他系统管理

    def draw(self, *args, **kwargs):
        pass # 绘制由AnimationSystem处理 