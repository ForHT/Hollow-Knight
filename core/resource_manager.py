import os
import pygame
from typing import Dict, Optional

class ResourceManager:
    def __init__(self):
        """初始化资源管理器"""
        # 在这里初始化你的资源缓存字典
        pass

    def load_image(self, path: str) -> Optional[pygame.Surface]:
        """加载图片资源
        
        Args:
            path: 图片文件路径
            
        Returns:
            Optional[pygame.Surface]: 加载的图片surface，如果加载失败则返回None
        """
        pass

    def preload_resources(self, resource_list: list[str]) -> None:
        """预加载一组资源
        
        Args:
            resource_list: 需要预加载的资源路径列表
        """
        pass

    def clear_cache(self) -> None:
        """清除所有缓存的资源"""
        pass

    def get_resource(self, path: str) -> Optional[pygame.Surface]:
        """获取已加载的资源
        
        Args:
            path: 资源路径
            
        Returns:
            Optional[pygame.Surface]: 资源对象，如果不存在则返回None
        """
        pass 