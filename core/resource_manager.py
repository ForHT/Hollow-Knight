import os
import pygame
from typing import Dict, Optional

class ResourceManager:
    def __init__(self):
        """初始化资源管理器"""
        self.sprite_sheets = {}  # 存储精灵表
        self.sounds = {}        # 存储音效

    def load_sprite_sheet(self, name: str, path: str) -> pygame.Surface:
        """加载精灵表"""
        image = pygame.image.load(path)
        self.sprite_sheets[name] = image
        return image

    def get_sprite_sheet(self, name: str) -> Optional[pygame.Surface]:
        """获取已加载的精灵表"""
        return self.sprite_sheets.get(name)

    def load_sound(self, path: str) -> pygame.mixer.Sound:
        """加载音效"""
        sound = pygame.mixer.Sound(path)
        self.sounds[path] = sound
        return sound 