import pygame
from typing import List, Dict, Tuple, Optional

from configs import SCREEN_WIDTH, SCREEN_HEIGHT

class Button:
    """一个可交互的UI按钮，支持悬停高亮"""
    def __init__(self, rect: Tuple[int, int, int, int], text: str, font: pygame.font.Font):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.is_hovered = False

        # 定义颜色
        self.colors = {
            "base": (80, 80, 80),
            "hover": (120, 120, 120),
            "border": (255, 255, 255),
            "text": (255, 255, 255)
        }

    def handle_event(self, event: pygame.event.Event):
        """处理事件，更新悬停状态"""
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)

    def is_clicked(self, event: pygame.event.Event) -> bool:
        """检查按钮是否被点击"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.is_hovered
        return False

    def draw(self, surface: pygame.Surface):
        """绘制按钮"""
        # 根据是否悬停选择背景色
        color = self.colors["hover"] if self.is_hovered else self.colors["base"]
        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        # 绘制边框
        pygame.draw.rect(surface, self.colors["border"], self.rect, 2, border_radius=8)

        # 绘制文本
        text_surface = self.font.render(self.text, True, self.colors["text"])
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

class UIManager:
    def __init__(self):
        # 使用字典来存储图片资源
        self.images: Dict[str, pygame.Surface] = {}
        # 使用字典来存储动画帧
        self.animations: Dict[str, List[pygame.Surface]] = {}
        self.fonts = {}
        
        # 为了支持中文，尝试使用系统字体
        try:
            self.font_button = pygame.font.SysFont('SimHei', 40)
            self.font_title = pygame.font.SysFont('SimHei', 100)
        except pygame.error:
            # 如果找不到，则回退到默认字体
            self.font_button = pygame.font.Font(None, 50)
            self.font_title = pygame.font.Font(None, 120)

        # UI状态
        self.last_player_health: int = 0
        # 存储正在播放的受伤动画 (位置, 动画帧索引, 计时器)
        self.health_damage_animations: List[Tuple[Tuple[int, int], int, float]] = []
        
        self.load_assets()
        self._create_buttons()

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
        # self.images["play_again"] = pygame.image.load("resource/UI/playagain.png").convert_alpha() # 不再需要

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

    def handle_event(self, event: pygame.event.Event) -> Optional[str]:
        """处理UI事件，如按钮点击和悬停"""
        # 将事件传递给每个按钮以更新其悬停状态
        self.restart_button.handle_event(event)
        self.quit_button.handle_event(event)

        # 检查点击
        if self.restart_button.is_clicked(event):
            return "restart"
        if self.quit_button.is_clicked(event):
            return "quit"
        
        return None

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
        game_over_text = self.font_title.render("你已死亡", True, (200, 20, 20))
        text_rect = game_over_text.get_rect(center=(surface.get_width() / 2, surface.get_height() / 2 - 100))
        surface.blit(game_over_text, text_rect)
        
        # 添加 "是否重玩？" 提示
        prompt_text = self.font_button.render("是否重玩？", True, (255, 255, 255))
        prompt_rect = prompt_text.get_rect(center=(surface.get_width() / 2, surface.get_height() / 2 + 20))
        surface.blit(prompt_text, prompt_rect)

        # 绘制按钮
        self.restart_button.draw(surface)
        self.quit_button.draw(surface)

    def _draw_victory_screen(self, surface: pygame.Surface):
        """绘制胜利界面"""
        victory_text = self.font_title.render("胜 利", True, (255, 215, 0))
        text_rect = victory_text.get_rect(center=(surface.get_width() / 2, surface.get_height() / 2 - 100))
        surface.blit(victory_text, text_rect)

        # 添加 "是否重玩？" 提示
        prompt_text = self.font_button.render("是否重玩？", True, (255, 255, 255))
        prompt_rect = prompt_text.get_rect(center=(surface.get_width() / 2, surface.get_height() / 2 + 20))
        surface.blit(prompt_text, prompt_rect)

        # 绘制按钮
        self.restart_button.draw(surface)
        self.quit_button.draw(surface)

    def is_restart_clicked(self, pos: Tuple[int, int]) -> bool:
        """检查“再玩一次”按钮是否被点击 - 此方法已废弃"""
        return False

    def _create_buttons(self):
        """创建结束画面的按钮"""
        button_width, button_height = 160, 70
        button_y = int(SCREEN_HEIGHT / 2 + 80)
        
        # “是”按钮 (重新开始)
        restart_button_x = int(SCREEN_WIDTH / 2 - button_width - 30)
        self.restart_button = Button(
            (restart_button_x, button_y, button_width, button_height),
            "是",
            self.font_button
        )

        # “否”按钮 (退出)
        quit_button_x = int(SCREEN_WIDTH / 2 + 30)
        self.quit_button = Button(
            (quit_button_x, button_y, button_width, button_height),
            "否",
            self.font_button
        ) 