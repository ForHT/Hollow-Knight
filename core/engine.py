"""
��Ϸ��������
����Э������ϵͳ������
"""
import pygame
from typing import Dict, Optional
from game.interfaces import ISceneManager, IResourceManager, EventManager

class GameEngine:
    def __init__(self):
        """��ʼ����Ϸ����"""
        pygame.init()
        self.running = False
        self.screen: Optional[pygame.Surface] = None
        self.clock = pygame.time.Clock()
        self.scene_manager: Optional[ISceneManager] = None
        self.resource_manager: Optional[IResourceManager] = None
        
    def init(self, screen_width: int = 1440, screen_height: int = 900) -> None:
        """��ʼ����Ϸ���ں�ϵͳ"""
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Hollow Knight Clone")
        # TODO: ��ʼ������������
        # TODO: ��ʼ����Դ������
        
    def run(self) -> None:
        """������Ϸ��ѭ��"""
        if not self.screen:
            raise RuntimeError("Game engine not initialized. Call init() first.")
            
        self.running = True
        screen = self.screen  # ���ͼ��������Ϊ�������һ����pygame.Surface
        
        while self.running:
            # �����¼�
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    
            # ������Ϸ״̬
            dt = self.clock.tick(60) / 1000.0  # ת��Ϊ��
            if self.scene_manager:
                self.scene_manager.update(dt)
            
            # ��Ⱦ
            screen.fill((0, 0, 0))  # �����Ļ
            if self.scene_manager:
                self.scene_manager.draw(screen)  # ʹ���Ѿ����ͼ�����screen����
            pygame.display.flip()
            
    def quit(self) -> None:
        """�˳���Ϸ"""
        self.running = False
        pygame.quit() 