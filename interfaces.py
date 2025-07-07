"""
接口约定文件
定义了各个系统之间的交互接口
"""
from typing import List, Tuple, Dict, Callable, Optional, Any
import pygame
from dataclasses import dataclass
from enum import Enum, auto

# ============= 数据类型定义 =============
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

# ============= 核心接口定义 =============
class Entity:
    """所有游戏实体的基类"""
    def __init__(self, entity_type: EntityType, position: Vector2):
        self.entity_type = entity_type
        self.position = position
        self.velocity = Vector2(0, 0)
        self.hitbox = Rectangle(0, 0, 0, 0)
        self.current_animation: Optional[str] = None
        self.facing_right: bool = True
        
    def update(self, dt: float) -> None:
        """更新实体状态"""
        raise NotImplementedError
        
    def draw(self, surface: pygame.Surface) -> None:
        """绘制实体"""
        raise NotImplementedError

class IPhysicsSystem:
    """物理系统接口"""
    def add_entity(self, entity: Entity) -> None:
        raise NotImplementedError
        
    def remove_entity(self, entity: Entity) -> None:
        raise NotImplementedError
        
    def update(self, dt: float) -> None:
        raise NotImplementedError
        
    def check_collision(self, entity1: Entity, entity2: Entity) -> bool:
        raise NotImplementedError

class IAnimationSystem:
    """动画系统接口"""
    def load_animation(self, name: str, sprite_sheet: pygame.Surface, 
                      frame_count: int, frame_time: float) -> None:
        raise NotImplementedError
        
    def play_animation(self, entity: Entity, animation_name: str, 
                      loop: bool = True) -> None:
        raise NotImplementedError
        
    def update(self, dt: float) -> None:
        raise NotImplementedError

class ICombatSystem:
    """战斗系统接口"""
    def register_attack(self, attacker: Entity, attack_data: Dict) -> None:
        raise NotImplementedError
        
    def check_hits(self) -> List[Tuple[Entity, Entity]]:
        raise NotImplementedError
        
    def apply_damage(self, target: Entity, damage: int) -> None:
        raise NotImplementedError

class IInputHandler:
    """输入处理接口"""
    def handle_input(self, events: List[pygame.event.Event]) -> Dict[str, bool]:
        raise NotImplementedError
        
    def get_action(self) -> Optional[str]:
        raise NotImplementedError

class IResourceManager:
    """资源管理接口"""
    def load_image(self, path: str) -> pygame.Surface:
        raise NotImplementedError
        
    def load_sound(self, path: str) -> pygame.mixer.Sound:
        raise NotImplementedError
        
    def get_animation(self, name: str) -> List[pygame.Surface]:
        raise NotImplementedError

class ISceneManager:
    """场景管理接口"""
    def change_scene(self, scene_name: str) -> None:
        raise NotImplementedError
        
    def update(self, dt: float) -> None:
        raise NotImplementedError
        
    def draw(self, surface: pygame.Surface) -> None:
        raise NotImplementedError

class IUIManager:
    """UI管理接口"""
    def update(self, game_state: Dict) -> None:
        raise NotImplementedError
        
    def draw(self, surface: pygame.Surface) -> None:
        raise NotImplementedError
        
    def handle_input(self, event: pygame.event.Event) -> bool:
        raise NotImplementedError

# ============= 事件系统 =============
class EventManager:
    """事件管理器，用于系统间通信"""
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