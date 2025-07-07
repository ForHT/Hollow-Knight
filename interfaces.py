"""
�ӿ�Լ���ļ�
�����˸���ϵͳ֮��Ľ����ӿ�
"""
from typing import List, Tuple, Dict, Callable, Optional, Any
import pygame
from dataclasses import dataclass
from enum import Enum, auto

# ============= �������Ͷ��� =============
@dataclass
class Vector2:
    x: float
    y: float

@dataclass
class Rectangle:
    x: float
    y: float
    width: float
    height: float

class EntityType(Enum):
    PLAYER = auto()
    ENEMY = auto()
    PROJECTILE = auto()
    EFFECT = auto()

class AnimationState(Enum):
    IDLE = auto()
    WALK = auto()
    JUMP = auto()
    ATTACK = auto()
    DASH = auto()
    DAMAGE = auto()

# ============= ���Ľӿڶ��� =============
class Entity:
    """������Ϸʵ��Ļ���"""
    def __init__(self, entity_type: EntityType, position: Vector2):
        self.entity_type = entity_type
        self.position = position
        self.velocity = Vector2(0, 0)
        self.hitbox = Rectangle(0, 0, 0, 0)
        self.current_animation: Optional[str] = None
        self.facing_right: bool = True
        
    def update(self, dt: float) -> None:
        """����ʵ��״̬"""
        raise NotImplementedError
        
    def draw(self, surface: pygame.Surface) -> None:
        """����ʵ��"""
        raise NotImplementedError

class IPhysicsSystem:
    """����ϵͳ�ӿ�"""
    def add_entity(self, entity: Entity) -> None:
        raise NotImplementedError
        
    def remove_entity(self, entity: Entity) -> None:
        raise NotImplementedError
        
    def update(self, dt: float) -> None:
        raise NotImplementedError
        
    def check_collision(self, entity1: Entity, entity2: Entity) -> bool:
        raise NotImplementedError

class IAnimationSystem:
    """����ϵͳ�ӿ�"""
    def load_animation(self, name: str, sprite_sheet: pygame.Surface, 
                      frame_count: int, frame_time: float) -> None:
        raise NotImplementedError
        
    def play_animation(self, entity: Entity, animation_name: str, 
                      loop: bool = True) -> None:
        raise NotImplementedError
        
    def update(self, dt: float) -> None:
        raise NotImplementedError

class ICombatSystem:
    """ս��ϵͳ�ӿ�"""
    def register_attack(self, attacker: Entity, attack_data: Dict) -> None:
        raise NotImplementedError
        
    def check_hits(self) -> List[Tuple[Entity, Entity]]:
        raise NotImplementedError
        
    def apply_damage(self, target: Entity, damage: int) -> None:
        raise NotImplementedError

class IInputHandler:
    """���봦��ӿ�"""
    def handle_input(self, events: List[pygame.event.Event]) -> Dict[str, bool]:
        raise NotImplementedError
        
    def get_action(self) -> Optional[str]:
        raise NotImplementedError

class IResourceManager:
    """��Դ����ӿ�"""
    def load_image(self, path: str) -> pygame.Surface:
        raise NotImplementedError
        
    def load_sound(self, path: str) -> pygame.mixer.Sound:
        raise NotImplementedError
        
    def get_animation(self, name: str) -> List[pygame.Surface]:
        raise NotImplementedError

class ISceneManager:
    """��������ӿ�"""
    def change_scene(self, scene_name: str) -> None:
        raise NotImplementedError
        
    def update(self, dt: float) -> None:
        raise NotImplementedError
        
    def draw(self, surface: pygame.Surface) -> None:
        raise NotImplementedError

class IUIManager:
    """UI����ӿ�"""
    def update(self, game_state: Dict) -> None:
        raise NotImplementedError
        
    def draw(self, surface: pygame.Surface) -> None:
        raise NotImplementedError
        
    def handle_input(self, event: pygame.event.Event) -> bool:
        raise NotImplementedError

# ============= �¼�ϵͳ =============
class EventManager:
    """�¼�������������ϵͳ��ͨ��"""
    _subscribers: Dict[str, List[Callable]] = {}
    
    @classmethod
    def subscribe(cls, event_type: str, callback: Callable) -> None:
        if event_type not in cls._subscribers:
            cls._subscribers[event_type] = []
        cls._subscribers[event_type].append(callback)
    
    @classmethod
    def emit(cls, event_type: str, data: Any = None) -> None:
        if event_type in cls._subscribers:
            for callback in cls._subscribers[event_type]:
                callback(data) 