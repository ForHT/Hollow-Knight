
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
                    "next_state": data.get("next_state") # 安全地获取next_state
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
            next_state=data["next_state"]
        )
        self.entity_states[entity] = new_state
        
    def update(self, dt: float) -> None:
        """更新所有实体的动画状态，并应用dmove位移。"""
        for entity, state in list(self.entity_states.items()):
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
                state.current_frame += 1
                
                if state.current_frame >= len(state.frames):
                    if state.loop:
                        state.current_frame = 0
                    else:
                        state.current_frame = len(state.frames) - 1
                        # 当非循环动画结束时，触发状态转换
                        if state.next_state:
                            # 确保实体有set_state方法
                            if hasattr(entity, 'set_state') and callable(getattr(entity, 'set_state')):
                                entity.set_state(state.next_state)
                
                # 更新时间间隔以匹配新帧
                if state.current_frame < len(state.intervals):
                    current_interval = state.intervals[state.current_frame]
                else:
                    break

    def get_current_frame(self, entity: Entity) -> Optional[pygame.Surface]:
        """获取实体当前的动画帧。不再需要翻转，因为我们加载了左右两个版本。"""
        if entity not in self.entity_states:
            return None
        
        state = self.entity_states[entity]
        if not state.frames or state.current_frame >= len(state.frames):
            return None # 防止索引越界
            
        return state.frames[state.current_frame]

    # 旧的/不再使用的方法可以删除或标记为废弃
    # play_animation_by_name, load_animations_from_config, set_animation_end_callback ...
    # 为了简洁，这里直接省略它们