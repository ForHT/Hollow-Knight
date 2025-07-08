import pygame
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from game.core.animation_system import AnimationSystem
from game.interfaces import Entity, EntityType, Vector2
from game.config.states import PLAYER_ANIMATIONS, PLAYER_STATE_MACHINE, ANIMATION_PATHS

# 初始化 Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# 创建动画系统
animation_system = AnimationSystem()

# 加载所有玩家动画
for state, config in PLAYER_ANIMATIONS.items():
    frames_path = ANIMATION_PATHS["player"][state]  # 更新路径获取方式
    for frame in range(config["frames"]):
        path = frames_path.format(frame=frame)
        try:
            frame_surface = pygame.image.load(path).convert_alpha()
            animation_system.load_animation(
                f"player_{state}", 
                frame_surface, 
                config["frames"], 
                config["frame_time"]
            )
        except pygame.error as e:
            print(f"Error loading animation frame: {path}")
            print(f"Error details: {e}")

# 创建玩家实体
player = Entity(EntityType.PLAYER, Vector2(400, 300))
current_state = "idle"

# 状态切换函数
def change_state(new_state: str):
    global current_state
    # 检查是否是合法的状态转换
    if new_state in PLAYER_STATE_MACHINE[current_state]:
        current_state = new_state
        config = PLAYER_ANIMATIONS[new_state]
        animation_system.play_animation(
            player, 
            f"player_{new_state}", 
            config["loop"]
        )
        
        # 检查是否有自动下一个状态
        if not config["loop"] and "next_state" in config:
            # 在动画结束时自动转换到下一个状态
            animation_system.set_animation_end_callback(
                player,
                lambda: change_state(config["next_state"])
            )

# 开始播放初始动画
animation_system.play_animation(
    player, 
    "player_idle", 
    PLAYER_ANIMATIONS["idle"]["loop"]
)

# 游戏主循环
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1 or event.key == pygame.K_KP1:  # 支持小键盘
                change_state("idle")
            elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                change_state("walk")
            elif event.key == pygame.K_3 or event.key == pygame.K_KP3:
                change_state("jump_start")
            elif event.key in [pygame.K_j, pygame.K_KP_4]:   # J键或小键盘4普通攻击
                change_state("attack")
            elif event.key in [pygame.K_k, pygame.K_KP_5]:   # K键或小键盘5上攻
                change_state("attack_up")
            elif event.key in [pygame.K_l, pygame.K_KP_6]:   # L键或小键盘6下攻
                change_state("attack_down")
            elif event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:  # 支持左右Shift
                change_state("dash")
            elif event.key == pygame.K_SPACE:  # 空格键触发落地
                if current_state == "jump_loop":
                    change_state("jump_land")

    dt = clock.tick(60) / 1000.0
    
    # 更新动画
    animation_system.update(dt)
    
    # 绘制
    screen.fill((0, 0, 0))
    current_frame = animation_system.get_current_frame(player)
    if current_frame:
        screen.blit(current_frame, (player.position.x, player.position.y))
    
    # 显示当前状态
    font = pygame.font.Font(None, 36)
    state_text = font.render(f"Current State: {current_state}", True, (255, 255, 255))
    screen.blit(state_text, (10, 10))
    
    pygame.display.flip()