"""
游戏引擎主类
负责协调各个系统的运行
"""
import pygame
from typing import Dict, Optional
from game.interfaces import ISceneManager, IResourceManager, EventManager

class GameEngine:
    def __init__(self):
        """初始化游戏引擎"""
        pygame.init()
        self.running = False
        self.screen: Optional[pygame.Surface] = None
        self.clock = pygame.time.Clock()
        self.scene_manager: Optional[ISceneManager] = None
        self.resource_manager: Optional[IResourceManager] = None
        
    def init(self, screen_width: int = 1440, screen_height: int = 900) -> None:
        """初始化游戏窗口和系统"""
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Hollow Knight Clone")
        # TODO: 初始化场景管理器
        # TODO: 初始化资源管理器
        
    def run(self) -> None:
        """运行游戏主循环"""
        if not self.screen:
            raise RuntimeError("Game engine not initialized. Call init() first.")
            
        self.running = True
        screen = self.screen  # 类型检查器会认为这个变量一定是pygame.Surface
        
        while self.running:
            # 处理事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    
            # 更新游戏状态
            dt = self.clock.tick(60) / 1000.0  # 转换为秒
            if self.scene_manager:
                self.scene_manager.update(dt)
            
            # 渲染
            screen.fill((0, 0, 0))  # 清空屏幕
            if self.scene_manager:
                self.scene_manager.draw(screen)  # 使用已经类型检查过的screen变量
            pygame.display.flip()
            
    def quit(self) -> None:
        """退出游戏"""
        self.running = False
        pygame.quit() 