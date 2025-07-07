"""
物理系统
负责处理游戏中的物理相关计算
"""
from typing import List, Dict, Set
from ..interfaces import IPhysicsSystem, Entity, Vector2, Rectangle

class PhysicsSystem(IPhysicsSystem):
    def __init__(self):
        self.entities: Set[Entity] = set()
        self.gravity = 9.8
        
    def add_entity(self, entity: Entity) -> None:
        """添加实体到物理系统"""
        self.entities.add(entity)
        
    def remove_entity(self, entity: Entity) -> None:
        """从物理系统移除实体"""
        self.entities.remove(entity)
        
    def update(self, dt: float) -> None:
        """更新物理状态"""
        for entity in self.entities:
            # 应用重力
            entity.velocity.y += self.gravity * dt
            
            # 更新位置
            entity.position.x += entity.velocity.x * dt
            entity.position.y += entity.velocity.y * dt
            
            # TODO: 添加地面碰撞检测
            # TODO: 添加墙体碰撞检测
            
    def check_collision(self, entity1: Entity, entity2: Entity) -> bool:
        """检查两个实体之间是否发生碰撞"""
        # TODO: 实现AABB碰撞检测
        rect1 = entity1.hitbox
        rect2 = entity2.hitbox
        
        return (rect1.x < rect2.x + rect2.width and
                rect1.x + rect1.width > rect2.x and
                rect1.y < rect2.y + rect2.height and
                rect1.y + rect1.height > rect2.y) 