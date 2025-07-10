import pygame
from typing import List, Dict, Tuple

from configs import SCREEN_WIDTH, SCREEN_HEIGHT

class UIManager:
    def __init__(self):
        # 使用字典来存储图片资源
        self.images: Dict[str, pygame.Surface] = {}
        # 使用字典来存储动画帧
        self.animations: Dict[str, List[pygame.Surface]] = {}
        self.fonts = {}
        
        # UI状态
        self.last_player_health: int = 0
        # 存储正在播放的受伤动画 (位置, 动画帧索引, 计时器)
        self.health_damage_animations: List[Tuple[Tuple[int, int], int, float]] = []
        
        self.load_assets()

    def load_assets(self):
        """加载所有UI图片和字体"""
        # 加载血量UI
        self.images["health_empty"] = pygame.image.load("resource/img/hollow knight/UI/Blood/empty.png").convert_alpha()
        self.images["health_full"] = pygame.image.load("resource/img/hollow knight/UI/Blood/0.png").convert_alpha() # 暂时只用第一帧代表满血
        
        # 加载开始/结束界面资源并进行缩放
        game_bg = pygame.image.load("resource/img/hollow knight/background.png").convert()
        start_bg = pygame.image.load("resource/UI/openground.png").convert()
        
        self.images["game_background"] = pygame.transform.scale(game_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.images["start_background"] = pygame.transform.scale(start_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.images["title"] = pygame.image.load("resource/UI/title_chinese.png").convert_alpha()
        self.images["press_to_start"] = pygame.image.load("resource/UI/press_to_start.png").convert_alpha()
        self.images["play_again"] = pygame.image.load("resource/UI/playagain.png").convert_alpha()

        # 预加载血量动画帧 (暂不使用)
        self.animations["health_damage"] = [
            pygame.image.load(f"resource/img/hollow knight/UI/Blood/Damage/{i}.png").convert_alpha() for i in range(6)
        ]
        self.animations["health_appear"] = [
            pygame.image.load(f"resource/img/hollow knight/UI/Blood/{i}.png").convert_alpha() for i in range(6)
        ]

    def update(self, dt: float, game_state: str, player_health: int, max_health: int):
        """根据游戏状态更新UI元素"""
        # 1. 检测血量变化以触发受伤动画
        if player_health < self.last_player_health:
            # 计算损失了多少血
            lost_health = self.last_player_health - player_health
            for i in range(lost_health):
                # 在掉血的位置启动动画
                health_index = self.last_player_health - 1 - i
                if health_index >= 0:
                    pos = self._get_health_icon_pos(health_index)
                    # (位置, 动画起始帧, 计时器)
                    self.health_damage_animations.append((pos, 0, 0.0))

        # 2. 更新正在播放的受伤动画
        updated_animations = []
        damage_anim_duration = 0.08 # 每帧持续时间，可调整
        for pos, frame_index, timer in self.health_damage_animations:
            timer += dt
            if timer >= damage_anim_duration:
                frame_index += 1
                timer = 0
            # 如果动画没有播放完，则保留
            if frame_index < len(self.animations["health_damage"]):
                updated_animations.append((pos, frame_index, timer))
        self.health_damage_animations = updated_animations
        
        # 3. 更新上一帧的血量
        self.last_player_health = player_health

    def draw(self, surface, game_state, player_health, max_health):
        """根据游戏状态绘制UI"""
        if game_state == "PLAYING":
            # surface.blit(self.images["game_background"], (0, 0)) # 背景绘制移到主循环
            self._draw_player_health(surface, player_health, max_health)
        elif game_state == "START_SCREEN":
             self._draw_start_screen(surface)
        elif game_state == "GAME_OVER":
            surface.fill((0, 0, 0)) # 使用黑色背景
            self._draw_game_over_screen(surface)
        elif game_state == "VICTORY":
            surface.fill((0, 0, 0)) # 使用黑色背景
            self._draw_victory_screen(surface)

    def _get_health_icon_pos(self, index: int) -> Tuple[int, int]:
        """根据索引计算血量图标的位置"""
        start_x = 50
        start_y = 50
        padding = 10
        icon_width = self.images["health_empty"].get_width()
        x = start_x + index * (icon_width + padding)
        return x, start_y

    def _draw_player_health(self, surface: pygame.Surface, player_health: int, max_health: int):
        """绘制玩家血量"""
        for i in range(max_health):
            pos = self._get_health_icon_pos(i)
            # 先绘制底层的空格子
            surface.blit(self.images["health_empty"], pos)
            # 如果当前生命值大于i，则在上面绘制满血图标
            if i < player_health:
                surface.blit(self.images["health_full"], pos)
        
        # 绘制正在播放的受伤动画
        for pos, frame_index, _ in self.health_damage_animations:
            frame = self.animations["health_damage"][frame_index]
            surface.blit(frame, pos)

    def _draw_start_screen(self, surface: pygame.Surface):
        """绘制开始界面"""
        surface.blit(self.images["start_background"], (0, 0))
        
        # 居中绘制标题
        title_rect = self.images["title"].get_rect(center=(surface.get_width() / 2, surface.get_height() / 2 - 100))
        surface.blit(self.images["title"], title_rect)

        # 绘制 "按键开始"
        press_start_rect = self.images["press_to_start"].get_rect(center=(surface.get_width() / 2, surface.get_height() / 2 + 100))
        surface.blit(self.images["press_to_start"], press_start_rect)


    def _draw_game_over_screen(self, surface: pygame.Surface):
        """绘制游戏结束界面"""
        # (之后会用图片替换文字)
        font_large = pygame.font.Font(None, 120)
        game_over_text = font_large.render("Game Over", True, (255, 0, 0))
        text_rect = game_over_text.get_rect(center=(surface.get_width() / 2, surface.get_height() / 2 - 100))
        surface.blit(game_over_text, text_rect)
        
        # 绘制 "再玩一次" 按钮
        play_again_rect = self.images["play_again"].get_rect(center=(surface.get_width() / 2, surface.get_height() / 2 + 50))
        surface.blit(self.images["play_again"], play_again_rect)

    def _draw_victory_screen(self, surface: pygame.Surface):
        """绘制胜利界面"""
        font_large = pygame.font.Font(None, 120)
        victory_text = font_large.render("You Win!", True, (255, 215, 0))
        text_rect = victory_text.get_rect(center=(surface.get_width() / 2, surface.get_height() / 2 - 100))
        surface.blit(victory_text, text_rect)

        # 绘制 "再玩一次" 按钮
        play_again_rect = self.images["play_again"].get_rect(center=(surface.get_width() / 2, surface.get_height() / 2 + 50))
        surface.blit(self.images["play_again"], play_again_rect)

    def is_restart_clicked(self, pos: Tuple[int, int]) -> bool:
        """检查“再玩一次”按钮是否被点击"""
        # 注意: 这个坐标需要和 _draw_game_over_screen/_draw_victory_screen 中的位置匹配
        play_again_rect = self.images["play_again"].get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50))
        return play_again_rect.collidepoint(pos) 