import pygame

# ==============================================================================
# >> 窗口与显示设置 (Window & Display Settings)
# ==============================================================================
# 游戏窗口的尺寸，与C++项目保持一致
SCREEN_WIDTH = 1440
SCREEN_HEIGHT = 900

# 游戏的目标帧率
FPS = 60

# 创建一个全局的窗口Rect对象，方便物理系统进行边界检测
SCREEN_RECT = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)


# ==============================================================================
# >> 物理与世界常量 (Physics & World Constants)
# ==============================================================================
# 全局重力加速度。C++项目中的值为2.5，逐帧累加。
GRAVITY = 2.5

# 玩家在地面上时，其hitbox.bottom所在的Y坐标
# 对应C++代码中的: if (player.position.y > 680)
PLAYER_GROUND_Y = 820

# Boss在地面上时，其hitbox.bottom所在的Y坐标
# C++代码中的值为585，但为了统一，这里也使用和玩家一样的高度
ENEMY_GROUND_Y = 840

# ==============================================================================
# >> 玩家属性 (Player Attributes)
# ==============================================================================
# 玩家的初始和最大生命值
PLAYER_HEALTH = 7

# 玩家的攻击力
PLAYER_ATTACK_POWER = 1

# 玩家的水平移动速度 (像素/帧)
# 对应C++代码中的: speed.vx = -10;
PLAYER_RUN_SPEED = 10

# 玩家跳跃时获得的初始垂直速度 (负数表示向上)
# 对应C++代码中的: Player.speed.vy = -43;
PLAYER_JUMP_VELOCITY = -43

# 玩家冲刺的速度 (像素/帧)
PLAYER_DASH_SPEED = 45

# 玩家冲刺的持续时间 (帧)
PLAYER_DASH_DURATION = 9

# 玩家冲刺的冷却时间 (帧)
PLAYER_DASH_COOLDOWN = 30


# ==============================================================================
# >> Boss 属性 (Boss Attributes)
# ==============================================================================
# Boss的初始和最大生命值
BOSS_HEALTH = 10

# Boss的攻击特效造成的伤害
BOSS_ATTACK_POWER = 1

# Boss的身体接触对玩家造成的伤害
BOSS_BODY_DAMAGE = 1

# --- Boss AI 冷却时间 (帧) ---
BOSS_ACTION_COOLDOWN = 60       # 两次行动之间的通用冷却时间
BOSS_WALK_COOLDOWN = 75
BOSS_JUMP_COOLDOWN = 120
BOSS_JUMPDASH_COOLDOWN = 240
BOSS_DASH_COOLDOWN = 100
BOSS_JUMPFINAL_COOLDOWN = 480

# --- Boss AI 距离阈值 (像素) ---
BOSS_AI_CLOSE_DISTANCE = 250   # 小于该值视为近距离
BOSS_AI_MEDIUM_DISTANCE = 700  # 小于该值视为中距离，大于等于则为远距离


# ==============================================================================
# >> 调试开关 (Debug Flags)
# ==============================================================================
# 是否默认开启调试模式（例如，绘制hitbox）
DEBUG_MODE = True