import pygame
import sys
import os
from typing import Optional

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from core.animation_system import AnimationSystem, VFXManager
from core.audio_manager import AudioManager # 导入
from interfaces import Entity, EntityType, Vector2, GameState
from config.animation_data import PLAYER_ANIMATIONS, EFFECT_ANIMATIONS, BOSS_ANIMATIONS
from configs import FPS, SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_GROUND_Y
from systems.combat import CombatSystem
from systems.physics import PhysicsSystem
from gameplay.player import Player, Effect
from gameplay.boss import Boss
from ui.ui_manager import UIManager

# # C++版本中UI是图片，我们暂时用这个简单的按钮类来处理交互
# class Button:
#     """一个简单的UI按钮类"""
#     def __init__(self, x, y, width, height, text, color, text_color):
#         self.rect = pygame.Rect(x, y, width, height)
#         self.text = text
#         self.color = color
#         self.text_color = text_color
#         self.font = pygame.font.Font(None, 50)

#     def draw(self, surface):
#         pygame.draw.rect(surface, self.color, self.rect)
#         text_surface = self.font.render(self.text, True, self.text_color)
#         text_rect = text_surface.get_rect(center=self.rect.center)
#         surface.blit(text_surface, text_rect)

#     def is_clicked(self, pos):
#         return self.rect.collidepoint(pos)

# 初始化 Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True

# 设置窗口标题
pygame.display.set_caption("Hollow Knight Clone")
game_state = GameState.START_SCREEN

# --- UI 元素 ---
# # 旧的UI元素，已被UIManager取代

# 为了保持交互性，我们暂时保留按钮的Rect用于点击检测，但不绘制它们
# start_button_rect = pygame.Rect(SCREEN_WIDTH/2 - 150, SCREEN_HEIGHT/2 + 80, 300, 80) # 不再需要
# restart_button_rect = pygame.Rect(SCREEN_WIDTH/2 - 150, SCREEN_HEIGHT/2 + 30, 300, 80) # 由 UIManager 处理
# TODO: 为Quit按钮也创建一个Rect，或者统一管理

# --- 系统初始化 ---
animation_system = AnimationSystem()
physics_system = PhysicsSystem(screen.get_rect())
vfx_manager = VFXManager(animation_system)
audio_manager = AudioManager() # 初始化
audio_manager.load_sounds() # 加载音频
combat_system = CombatSystem(physics_system, vfx_manager, audio_manager)
ui_manager = UIManager()

# 使用新的加载方法，为不同实体的动画添加前缀
animation_system.load_entity_animations("player", PLAYER_ANIMATIONS)
animation_system.load_entity_animations("effect", EFFECT_ANIMATIONS)
animation_system.load_entity_animations("boss", BOSS_ANIMATIONS)

# --- 实体变量 ---
player: Optional[Player] = None
boss: Optional[Boss] = None
entities: list = []

def reset_game():
    """重置游戏状态，重新初始化所有实体。"""
    global player, boss, entities
    
    physics_system.entities.clear()

    player = Player(pos=Vector2(200, PLAYER_GROUND_Y), size=(50, 80), audio_manager=audio_manager)
    boss = Boss(pos=Vector2(800, 585), size=(100, 150), audio_manager=audio_manager)
    entities = [player, boss]

    for entity in entities:
        physics_system.add_entity(entity)

# --- 主循环 ---
while running:
    dt = clock.tick(FPS) / 1000.0
    
    # --- 事件处理 ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if game_state == GameState.START_SCREEN:
            # 响应任意按键开始游戏
            if event.type == pygame.KEYDOWN:
                audio_manager.play_sound("ui_confirm")
                audio_manager.stop_music()
                audio_manager.play_music("battle")
                audio_manager.play_sound("boss_open")
                reset_game()
                game_state = GameState.PLAYING
        elif game_state in [GameState.GAME_OVER, GameState.VICTORY]:
            # 在结束界面，将事件交给UI管理器处理
            action = ui_manager.handle_event(event)
            if action == "restart":
                audio_manager.play_sound("ui_confirm")
                audio_manager.stop_music()
                audio_manager.play_music("battle")
                audio_manager.play_sound("boss_open")
                reset_game()
                game_state = GameState.PLAYING
            elif action == "quit":
                audio_manager.play_sound("ui_confirm")
                running = False
        else:
             # 游戏进行中的事件处理
            if event.type == pygame.KEYDOWN:
                # 这里可以处理游戏中的暂停等事件（如果需要）
                pass

    # --- 逻辑更新 ---
    if game_state == GameState.PLAYING and player and boss:
        keys = pygame.key.get_pressed()
        player.update(keys, animation_system)
        
        # Boss的更新现在会返回需要生成的特效
        effects_from_boss = boss.update(player.position, animation_system)

        physics_system.update()
        combat_system.update(player, [boss])
        
        animation_system.play_animation("player", player, player.state)
        animation_system.play_animation("boss", boss, boss.state)

        # 更新动画系统并获取动画触发的特效
        effects_from_anims = animation_system.update(dt)

        # 合并所有需要生成的特效
        effects_to_spawn = effects_from_anims
        if effects_from_boss:
            effects_to_spawn.extend(effects_from_boss)
            
        for effect_data in effects_to_spawn:
            vfx_manager.create_effect(
                pos=effect_data["pos"], 
                animation_name=effect_data["name"],
                facing_right=effect_data["facing_right"]
            )
        
        vfx_manager.update(dt)

        if boss.health <= 0:
            if game_state == GameState.PLAYING: # 确保只在第一次进入时执行
                audio_manager.stop_music()
                audio_manager.play_music("title")
            game_state = GameState.VICTORY
        elif player.health <= 0:
            if game_state == GameState.PLAYING: # 确保只在第一次进入时执行
                audio_manager.stop_music()
                audio_manager.play_music("title")
            game_state = GameState.GAME_OVER

    # --- 绘制 ---
    screen.fill((0, 0, 0)) # 绘制前清屏
    
    # UI Manager 会处理开始、结束等界面的绘制
    # 但在游戏进行时，我们需要手动控制绘制顺序
    if game_state == GameState.PLAYING:
        # 1. 绘制背景
        screen.blit(ui_manager.images["game_background"], (0, 0))
        
        # 2. 绘制游戏实体
        if player and boss:
            # 玩家绘制
            current_frame = animation_system.get_current_frame(player)
            if current_frame:
                frame_rect = current_frame.get_rect()
                frame_rect.midbottom = (int(player.position.x), int(player.position.y))
                screen.blit(current_frame, frame_rect.topleft)
            
            # Boss绘制
            boss_current_frame = animation_system.get_current_frame(boss)
            if boss_current_frame:
                boss_frame_rect = boss_current_frame.get_rect()
                boss_frame_rect.midbottom = (int(boss.position.x), int(boss.position.y))
                screen.blit(boss_current_frame, boss_frame_rect.topleft)
            
            # 绘制特效
            vfx_manager.draw(screen)
    
    # 3. 绘制UI层 (这会处理所有游戏状态)
    if player:
        ui_manager.update(dt, game_state.name, player.health, player.max_health)
        ui_manager.draw(screen, game_state.name, player.health, player.max_health)
    else:
        # 在没有玩家实体时（如开始菜单），也要绘制UI
        if game_state == GameState.START_SCREEN and not pygame.mixer.music.get_busy():
            audio_manager.play_music("title")
        ui_manager.update(dt, game_state.name, 0, 0)
        ui_manager.draw(screen, game_state.name, 0, 0)
    
    pygame.display.flip()

pygame.quit()
sys.exit()