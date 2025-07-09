"""
接口约定文件
定义了各个系统之间的交互接口
"""
from typing import List, Tuple, Dict, Callable, Optional, Any
import pygame
from dataclasses import dataclass
from enum import Enum, auto

# ============= 数据类型定义 =============
Vector2 = pygame.math.Vector2
Rect = pygame.Rect

class GameState(Enum):
    START_SCREEN = auto()
    PLAYING = auto()
    VICTORY = auto()
    GAME_OVER = auto()

class EntityType(Enum):
    PLAYER = auto()
    ENEMY = auto()
    BOSS = auto() # 添加BOSS类型
    PROJECTILE = auto()
    EFFECT = auto()

class AnimationState(Enum):
    IDLE = auto()
    WALK = auto()
    JUMP = auto()
    FALL = auto()
    ATTACK = auto()
    ATTACK_UP = auto()
    ATTACK_DOWN = auto()
    DASH = auto()
    HURT = auto()
    DEAD = auto()
    DAMAGE = auto()

    # Boss专属状态
    B_WALK = auto()
    B_JUMP = auto()
    B_DASH =  auto()
    B_JUMPDASH = auto()
    B_JUMPFINAL = auto()
    B_LAND = auto()
    B_THROWSIDE = auto()

# ============= 核心接口定义 =============
class Entity:
    """所有游戏实体的基类"""
    def __init__(self, entity_type: EntityType, pos: Vector2, size: tuple[int, int], ground_y: float):
        self.entity_type = entity_type
        self.current_animation: Optional[str] = None
        # 物理属性
        self.position = pos  # 代表hitbox的midbottom
        self.velocity = Vector2(0, 0)
        self.acceleration = Vector2(0, 0)
        self.hitbox = Rect(0, 0, size[0], size[1])
        self.hitbox.midbottom = (int(self.position.x), int(self.position.y))
        self.on_ground = False
        self.ground_y = ground_y # 每个实体可以有自己的地面高度

        # 游戏逻辑属性
        self.state: AnimationState = AnimationState.IDLE
        self.facing_right: bool = True
        
        # 战斗属性
        self.max_health: int = 1
        self.health: int = 1
        self.attack_power: int = 1
        self.body_damage: int = 1
        self.invincible_timer: float = 0.0
        
    def update(self, dt: float, **kwargs):
        """更新实体状态"""
        raise NotImplementedError

    def draw(self, surface: pygame.Surface, camera_offset: Vector2):
        """绘制实体"""
        raise NotImplementedError
    
    def take_damage(self, amount: int):
        """处理受伤的通用接口"""
        raise NotImplementedError

    def get_attack_hitbox(self) -> Optional[Rect]:
        """获取当前攻击的判定框"""
        return None

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

    def get_current_frame(self, entity: Entity) -> Optional[pygame.Surface]:
        """获取实体当前的动画帧"""
        raise NotImplementedError

    def set_animation_end_callback(self, entity: Entity, callback: Callable[[], None]) -> None:
        """设置动画结束时的回调函数
        
        Args:
            entity: 要设置回调的实体
            callback: 动画结束时调用的无参回调函数
        """
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