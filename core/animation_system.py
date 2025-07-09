
# 动画系统实现
from typing import Dict, List, Optional, Callable
import pygame
from dataclasses import dataclass

from interfaces import IAnimationSystem, Entity

@dataclass
class AnimationState:
    """动画状态数据"""
    frames: List[pygame.Surface]      # 动画的所有帧
    frame_time: float                 # 每帧持续时间
    current_frame: int = 0            # 当前帧索引
    time_accumulated: float = 0.0     # 累积的时间
    loop: bool = True                 # 是否循环播放
    end_callback: Optional[Callable[[], None]] = None  # 动画结束回调

class AnimationSystem(IAnimationSystem):
    def __init__(self):
        self.animations: Dict[str, List[pygame.Surface]] = {}  # 存储所有动画的帧
        self.animation_states: Dict[Entity, AnimationState] = {}  # 每个实体的动画状态
        self.frame_times: Dict[str, float] = {}  # 每个动画的帧时间
        
    def load_animation(self, name: str, sprite_sheet: pygame.Surface, 
                      frame_count: int, frame_time: float) -> None:
        """加载动画
        对于我们的单帧图片情况，sprite_sheet 实际上是单帧，
        我们需要收集 frame_count 个这样的帧
        """
        if name not in self.animations:
            self.animations[name] = []
        self.animations[name].append(sprite_sheet)
        self.frame_times[name] = frame_time
        
    def play_animation(self, entity: Entity, animation_name: str, 
                      loop: bool = True) -> None:
        """播放动画"""
        if animation_name not in self.animations:
            print(f"Animation {animation_name} not found!")
            return
            
        # 如果实体已经在播放这个动画，不需要重新开始
        if (entity in self.animation_states and 
            entity.current_animation == animation_name):
            return
            
        # 创建新的动画状态
        self.animation_states[entity] = AnimationState(
            frames=self.animations[animation_name],
            frame_time=self.frame_times[animation_name],
            loop=loop
        )
        entity.current_animation = animation_name
        
    def update(self, dt: float) -> None:
        """更新所有实体的动画状态"""
        for entity, state in list(self.animation_states.items()):
            state.time_accumulated += dt
            
            # 检查是否需要切换到下一帧
            while state.time_accumulated >= state.frame_time:
                state.time_accumulated -= state.frame_time
                state.current_frame += 1
                
                # 处理循环或结束
                if state.current_frame >= len(state.frames):
                    if state.loop:
                        state.current_frame = 0
                    else:
                        state.current_frame = len(state.frames) - 1
                        # 触发动画完成回调
                        if state.end_callback:
                            state.end_callback()

    def get_current_frame(self, entity: Entity) -> Optional[pygame.Surface]:
        """获取实体当前的动画帧"""
        if entity not in self.animation_states:
            return None
        
        state = self.animation_states[entity]
        return state.frames[state.current_frame]

    def set_animation_end_callback(self, entity: Entity, callback: Callable[[], None]) -> None:
        """设置动画结束时的回调函数"""
        if entity in self.animation_states:
            self.animation_states[entity].end_callback = callback