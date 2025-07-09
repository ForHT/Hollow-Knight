
# 动画系统实现
from typing import Dict, List, Optional, Callable
import pygame
from dataclasses import dataclass

from interfaces import IAnimationSystem, Entity, EntityType, Vector2

@dataclass
class AnimationState:
    """动画状态数据"""
    name: str                         # 动画全名 (e.g., "walk_left")
    frames: List[pygame.Surface]      # 动画的所有帧
    intervals: List[float]            # 每帧的持续时间 (秒)
    displacements: List[Vector2]      # 每帧的位移
    loop: bool = True                 # 是否循环播放
    next_state: Optional[str] = None  # 动画结束后要转换到的状态
    effects: Optional[List[Dict]] = None # 在特定帧触发的特效
    is_new: bool = True               # 用于标记动画是否是第一次播放
    current_frame: int = 0            # 当前帧索引
    time_accumulated: float = 0.0     # 累积的时间
    end_callback: Optional[Callable[[], None]] = None  # 动画结束回调

class AnimationSystem(IAnimationSystem):
    def __init__(self):
        # 新的数据结构，存储解析后的动画数据
        self.animation_data: Dict[str, Dict] = {}
        # 实体当前的动画状态
        self.entity_states: Dict[Entity, AnimationState] = {}
        
    def load_animations(self, config: Dict):
        """从新的配置字典中加载所有动画。"""
        for state_name, directions in config.items():
            for direction, data in directions.items():
                animation_name = f"{state_name}_{direction}"
                
                frames = []
                path_template = data["path_template"]
                for i in range(data["frame_count"]):
                    path = path_template.format(i)
                    try:
                        frames.append(pygame.image.load(path).convert_alpha())
                    except pygame.error as e:
                        print(f"Error loading frame {path}: {e}")
                        continue
                
                # 将C++的帧数（1/60秒）转换为秒
                intervals_in_seconds = [t * (1/60.0) for t in data["frame_intervals"]]
                
                displacements_as_vectors = [Vector2(d) for d in data["displacements"]]

                self.animation_data[animation_name] = {
                    "frames": frames,
                    "intervals": intervals_in_seconds,
                    "displacements": displacements_as_vectors,
                    "loop": data["loop"],
                    "next_state": data.get("next_state"),
                    "effects": data.get("effects") # 加载特效触发数据
                }
        print("Animation loading complete.")
        
    def play_animation(self, entity: Entity, state_name: str, loop_override: Optional[bool] = None):
        """根据状态名和朝向播放动画。"""
        direction = "right" if entity.facing_right else "left"
        animation_name = f"{state_name}_{direction}"

        # 如果动画不存在，则不执行任何操作
        if animation_name not in self.animation_data:
            # print(f"Animation '{animation_name}' not found.")
            return
            
        # 如果已经在播放此动画，则不打断
        if entity in self.entity_states and self.entity_states[entity].name == animation_name:
            return
            
        data = self.animation_data[animation_name]
        loop = loop_override if loop_override is not None else data["loop"]
        
        new_state = AnimationState(
            name=animation_name,
            frames=data["frames"],
            intervals=data["intervals"],
            displacements=data["displacements"],
            loop=loop,
            next_state=data["next_state"],
            effects=data["effects"], # 传递特效数据
            is_new=True # 确保新动画被标记
        )
        self.entity_states[entity] = new_state
        
    def update(self, dt: float) -> List[Dict]:
        """
        更新所有实体的动画状态，应用dmove位移，并返回需要生成的特效列表。
        返回列表格式: [{"name": str, "pos": Vector2, "facing_right": bool}]
        """
        effects_to_spawn = []
        for entity, state in list(self.entity_states.items()):
            # 如果是新动画，立即检查并触发第0帧的特效
            if state.is_new:
                if state.effects:
                    for effect_data in state.effects:
                        if effect_data["frame"] == 0:
                            offset = Vector2(effect_data["offset"]["x"], effect_data["offset"]["y"])
                            spawn_pos = entity.hitbox.center + offset
                            effects_to_spawn.append({
                                "name": effect_data["name"],
                                "pos": spawn_pos,
                                "facing_right": entity.facing_right
                            })
                state.is_new = False

            # 更新动画帧
            state.time_accumulated += dt
            
            if state.current_frame >= len(state.intervals):
                state.current_frame = len(state.intervals) - 1

            current_interval = state.intervals[state.current_frame]

            # 应用当前帧的位移 (在帧切换之前)
            if state.current_frame < len(state.displacements):
                displacement = state.displacements[state.current_frame]
                entity.position.x += displacement[0]
                entity.position.y += displacement[1]

            while state.time_accumulated >= current_interval:
                state.time_accumulated -= current_interval
                
                # 在增加帧数之前，记录旧帧，用于触发特效
                old_frame = state.current_frame
                state.current_frame += 1
                
                # 检查是否需要触发后续帧的特效
                if state.effects:
                    for effect_data in state.effects:
                        if effect_data["frame"] == state.current_frame:
                            offset = Vector2(effect_data["offset"]["x"], effect_data["offset"]["y"])
                            # 特效位置 = 实体中心 + 偏移
                            spawn_pos = entity.hitbox.center + offset
                            effects_to_spawn.append({
                                "name": effect_data["name"],
                                "pos": spawn_pos,
                                "facing_right": entity.facing_right
                            })

                if state.current_frame >= len(state.frames):
                    if state.loop:
                        state.current_frame = 0
                    else:
                        state.current_frame = len(state.frames) - 1
                        # 当非循环动画结束时，触发状态转换
                        if state.next_state:
                            # 确保实体有set_state方法
                            if hasattr(entity, 'set_state') and callable(getattr(entity, 'set_state')):
                                # 检查实体是否为Effect的实例，如果是，则不改变其状态
                                # 这可以防止特效自身的动画结束时改变玩家的状态
                                if not isinstance(entity, Effect):
                                    entity.set_state(state.next_state)
                
                # 更新时间间隔以匹配新帧
                if state.current_frame < len(state.intervals):
                    current_interval = state.intervals[state.current_frame]
                else:
                    break
        return effects_to_spawn

    def get_current_frame(self, entity: Entity) -> Optional[pygame.Surface]:
        """获取实体当前的动画帧。不再需要翻转，因为我们加载了左右两个版本。"""
        if entity not in self.entity_states:
            return None
        
        state = self.entity_states[entity]
        if not state.frames or state.current_frame >= len(state.frames):
            return None # 防止索引越界
            
        return state.frames[state.current_frame]

# 为了避免循环导入，将Effect类从vfx_system移动到这里
class Effect(Entity):
    """代表一个独立的视觉特效（VFX）"""
    def __init__(self, pos: Vector2, animation_name: str, animation_system: "AnimationSystem", facing_right: bool, is_one_shot: bool = True):
        # 获取动画的第一帧来确定特效的大小
        temp_anim_name = f"{animation_name}_{'right' if facing_right else 'left'}"
        first_frame = animation_system.animation_data.get(temp_anim_name, {}).get("frames", [None])[0]
        size = first_frame.get_size() if first_frame else (0, 0)

        super().__init__(pos, size, entity_type=EntityType.EFFECT)
        
        self.facing_right = facing_right
        self.animation_name = animation_name
        self.animation_system = animation_system
        self.is_one_shot = is_one_shot
        self.is_alive = True
        
        self.animation_system.play_animation(self, animation_name, loop_override=not is_one_shot)

    def update(self, *args, **kwargs):
        if self.is_one_shot:
            state = self.animation_system.entity_states.get(self)
            if state and not state.loop and state.current_frame >= len(state.frames) - 1:
                self.is_alive = False
            
    def draw(self, surface: pygame.Surface):
        """绘制特效的当前帧"""
        current_frame = self.animation_system.get_current_frame(self)
        if current_frame:
            frame_rect = current_frame.get_rect(center=self.position)
            surface.blit(current_frame, frame_rect.topleft)

class VFXManager:
    """负责创建、更新和销毁所有视觉特效"""
    def __init__(self, animation_system: "AnimationSystem"):
        self.effects: List[Effect] = []
        self.animation_system = animation_system
        
    def create_effect(self, pos: Vector2, animation_name: str, facing_right: bool, is_one_shot: bool = True):
        """在指定位置创建一个新的特效"""
        effect = Effect(pos, animation_name, self.animation_system, facing_right, is_one_shot)
        self.effects.append(effect)
        
    def update(self, dt: float):
        """更新所有特效，并移除已经结束的"""
        for effect in self.effects:
            effect.update(dt)
        
        self.effects = [effect for effect in self.effects if effect.is_alive]

    def draw(self, surface: pygame.Surface):
        """绘制所有活动的特效"""
        for effect in self.effects:
            effect.draw(surface)