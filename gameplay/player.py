"""
玩家类
处理玩家相关的逻辑
"""
import pygame
from typing import Dict, Optional
from ..interfaces import Entity, EntityType, Vector2, Rectangle, AnimationState

class Player(Entity):
    def __init__(self, position: Vector2):
        super().__init__(EntityType.PLAYER, position)
        self.health = 7
        self.max_health = 7
        self.attack_power = 1
        self.is_attacking = False
        self.is_dashing = False
        self.can_jump = True
        self.jump_force = 43
        self.move_speed = 10
        self.dash_speed = 45
        self.dash_duration = 0.2
        self.dash_cooldown = 0.5
        self.dash_timer = 0
        self.dash_cooldown_timer = 0
        self.animation_state = AnimationState.IDLE
        
    def update(self, dt: float) -> None:
        """更新玩家状态"""
        # TODO: 处理玩家移动
        # TODO: 处理玩家跳跃
        # TODO: 处理玩家攻击
        # TODO: 处理玩家冲刺
        # TODO: 更新动画状态
        pass
        
    def handle_input(self, keys: Dict[str, bool]) -> None:
        """处理输入"""
        # TODO: 实现输入处理逻辑
        pass
        
    def take_damage(self, damage: int) -> None:
        """受到伤害"""
        if not self.is_dashing:  # 冲刺时无敌
            self.health = max(0, self.health - damage)
            self.animation_state = AnimationState.DAMAGE
            
    def draw(self, surface: pygame.Surface) -> None:
        """绘制玩家"""
        # TODO: 实现玩家绘制逻辑
        pass 