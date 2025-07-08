"""
娓告垙寮曟搸涓荤被
璐熻矗鍗忚皟鍚勪釜绯荤粺鐨勮繍琛�
"""
import pygame
from typing import Dict, Optional
from game.interfaces import (
    ISceneManager, 
    IResourceManager, 
    EventManager,
    IPhysicsSystem,
    IAnimationSystem,
    ICombatSystem,
    IInputHandler,
    IUIManager
)

class GameEngine:
    def __init__(self):
        """鍒濆鍖栨父鎴忓紩鎿�"""
        pygame.init()
        self.running = False
        self.screen: Optional[pygame.Surface] = None
        self.clock = pygame.time.Clock()
        # 系统管理器
        self.scene_manager: Optional[ISceneManager] = None
        self.resource_manager: Optional[IResourceManager] = None
        self.physics_system: Optional[IPhysicsSystem] = None
        self.animation_system: Optional[IAnimationSystem] = None
        self.combat_system: Optional[ICombatSystem] = None
        self.input_handler: Optional[IInputHandler] = None
        self.ui_manager: Optional[IUIManager] = None
        
    def init(self, screen_width: int = 1440, screen_height: int = 900) -> None:
        """初始化游戏窗口和系统"""
        # 初始化显示
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Hollow Knight Clone")
        
        # TODO: 初始化各个系统
        # self.scene_manager = SceneManager()
        # self.resource_manager = ResourceManager()
        # self.physics_system = PhysicsSystem()
        # self.animation_system = AnimationSystem()
        # self.combat_system = CombatSystem()
        # self.input_handler = InputHandler()
        # self.ui_manager = UIManager()
        
    def run(self) -> None:
        """杩愯娓告垙涓诲惊鐜�"""
        if not self.screen:
            raise RuntimeError("Game engine not initialized. Call init() first.")
            
        self.running = True
        screen = self.screen  # 绫诲瀷妫€鏌ュ櫒浼氳涓鸿繖涓彉閲忎竴瀹氭槸pygame.Surface
        
        while self.running:
            # 处理事件
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                    
                # UI事件处理
                if self.ui_manager:
                    if self.ui_manager.handle_input(event):
                        continue  # UI消耗了此事件
            
            # 输入处理
            if self.input_handler:
                self.input_handler.handle_input(events)
            
            # 更新游戏状态
            dt = self.clock.tick(60) / 1000.0  # 转换为秒
            
            # 按顺序更新各个系统
            if self.physics_system:
                self.physics_system.update(dt)
            if self.animation_system:
                self.animation_system.update(dt)
            if self.combat_system:
                self.combat_system.check_hits()
            if self.scene_manager:
                self.scene_manager.update(dt)
            if self.ui_manager:
                self.ui_manager.update({})  # TODO: 传入实际的游戏状态
            
            # 渲染
            screen.fill((0, 0, 0))  # 清空屏幕
            
            # 按顺序渲染各个层
            if self.scene_manager:
                self.scene_manager.draw(screen)
            if self.ui_manager:
                self.ui_manager.draw(screen)
                
            pygame.display.flip()
            
    def quit(self) -> None:
        """閫€鍑烘父鎴�"""
        self.running = False
        pygame.quit() 