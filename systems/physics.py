"""
����ϵͳ
��������Ϸ�е�������ؼ���
"""
from typing import List, Dict, Set
from ..interfaces import IPhysicsSystem, Entity, Vector2, Rectangle

class PhysicsSystem(IPhysicsSystem):
    def __init__(self):
        self.entities: Set[Entity] = set()
        self.gravity = 9.8
        
    def add_entity(self, entity: Entity) -> None:
        """���ʵ�嵽����ϵͳ"""
        self.entities.add(entity)
        
    def remove_entity(self, entity: Entity) -> None:
        """������ϵͳ�Ƴ�ʵ��"""
        self.entities.remove(entity)
        
    def update(self, dt: float) -> None:
        """��������״̬"""
        for entity in self.entities:
            # Ӧ������
            entity.velocity.y += self.gravity * dt
            
            # ����λ��
            entity.position.x += entity.velocity.x * dt
            entity.position.y += entity.velocity.y * dt
            
            # TODO: ��ӵ�����ײ���
            # TODO: ���ǽ����ײ���
            
    def check_collision(self, entity1: Entity, entity2: Entity) -> bool:
        """�������ʵ��֮���Ƿ�����ײ"""
        # TODO: ʵ��AABB��ײ���
        rect1 = entity1.hitbox
        rect2 = entity2.hitbox
        
        return (rect1.x < rect2.x + rect2.width and
                rect1.x + rect1.width > rect2.x and
                rect1.y < rect2.y + rect2.height and
                rect1.y + rect1.height > rect2.y) 