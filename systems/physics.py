"""
物理系统
负责处理游戏中的物理相关计算
"""
import pygame
from typing import List
from configs import GRAVITY, SCREEN_RECT, FPS
from interfaces import IPhysicsSystem, Entity, Vector2, Rect

class PhysicsSystem(IPhysicsSystem):
    """
    一个实现了欧拉积分的平台跳跃物理系统。
    负责处理重力、运动、以及与环境的碰撞。
    """
    def __init__(self, screen_rect: Rect, gravity: float = GRAVITY):
        """
        初始化物理系统。
        param screen_rect: 游戏窗口的Rect，用于动态边界检测。
        param gravity: 全局重力加速度值。
        """
        self.entities: list[Entity] = []
        self.gravity_force = Vector2(0, gravity)
        self.screen_rect = screen_rect # 存储窗口大小
        
    def add_entity(self, entity: Entity) -> None:
        """向物理系统注册一个实体"""
        if entity not in self.entities:
            self.entities.append(entity)
        
    def remove_entity(self, entity: Entity) -> None:
        """从物理系统移除一个实体"""
        if entity in self.entities:
            self.entities.remove(entity)
        
    def update(self) -> None:
        """
        为所有注册的实体更新一帧的物理状态 (per-frame update).
        """
        for entity in self.entities:
            # 新增：检查实体是否处于“冻结”状态
            if hasattr(entity, 'is_frozen') and entity.is_frozen:
                entity.velocity = Vector2(0, 0)
                # 我们还需要重置加速度，以防止任何残留的力（如重力）被应用
                entity.acceleration = Vector2(0, 0)
                continue # 跳过该实体的所有其他物理计算

            # 冲刺和死亡状态下不受重力影响
            is_physics_active = entity.state not in ["dash", "dead"]

            if is_physics_active:
                # 1. 应用重力
                entity.acceleration = self.gravity_force
            else:
                entity.acceleration = Vector2(0, 0)

            # 2. 运动学积分 (逐帧更新)
            # v = v + a
            entity.velocity.y += entity.acceleration.y
            
            # p = p + v
            # 重新应用水平和垂直速度
            entity.position += entity.velocity
            
            # 同步hitbox的位置到新的物理位置
            entity.hitbox.midbottom = (int(entity.position.x), int(entity.position.y))

            # 3. 碰撞检测
            entity.on_ground = False

            # a. 与各自的地面碰撞
            if entity.hitbox.bottom >= entity.ground_y:
                entity.hitbox.bottom = int(entity.ground_y)
                entity.velocity.y = 0
                entity.on_ground = True
            
            # b. 与窗口边界碰撞
            if entity.hitbox.left < self.screen_rect.left:
                entity.hitbox.left = self.screen_rect.left
                entity.velocity.x = 0 
            elif entity.hitbox.right > self.screen_rect.right:
                entity.hitbox.right = self.screen_rect.right
                entity.velocity.x = 0
            
            if entity.hitbox.top < self.screen_rect.top:
                entity.hitbox.top = self.screen_rect.top
                entity.velocity.y = 0
            
            # 最终同步物理位置
            entity.position = Vector2(entity.hitbox.midbottom)
            
    def check_collision(self, entity1: Entity, entity2: Entity) -> bool:
        """检查两个实体之间是否发生碰撞(AABB碰撞检测)"""
        return entity1.hitbox.colliderect(entity2.hitbox)