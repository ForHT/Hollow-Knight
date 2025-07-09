PLAYER_ANIMATIONS = {
    "idle": {
        "frames": 9,
        "frame_time": 0.1,
        "loop": True
    },
    "walk": {
        "frames": 8,
        "frame_time": 0.1,
        "loop": True
    },
    "jump_start": {
        "frames": 4,  # 根据实际帧数调整
        "frame_time": 0.08,
        "loop": False,
        "next_state": "jump_loop"  # 添加下一个状态
    },
    "jump_loop": {
        "frames": 3,  # 根据实际帧数调整
        "frame_time": 0.1,
        "loop": True,
        "interrupt_states": ["jump_land"]  # 可以被中断的状态
    },
    "jump_land": {
        "frames": 3,  # 根据实际帧数调整
        "frame_time": 0.08,
        "loop": False,
        "next_state": "idle"  # 落地后回到idle状态
    },
    "attack": {
        "frames": 4,  # 根据实际帧数调整
        "frame_time": 0.08,
        "loop": False,
        "next_state": "idle"  # 攻击结束回到idle
    },
    "attack_up": {
        "frames": 4,  # 根据实际帧数调整
        "frame_time": 0.08,
        "loop": False,
        "next_state": "idle"
    },
    "attack_down": {
        "frames": 4,  # 根据实际帧数调整
        "frame_time": 0.08,
        "loop": False,
        "next_state": "idle"
    },
    "dash": {
        "frames": 5,  # 根据Dash文件夹中的图片数量
        "frame_time": 0.06,  # 冲刺动画稍快
        "loop": False,
        "next_state": "idle"
    },
   
}
EFFECT_ANIMATIONS = {
    "dash_effect": {
        "frames": 5,  # 根据实际图片数量调整
        "frame_time": 0.05,
        "loop": False
    }
}

# 可以添加其他实体的动画配置
ENEMY_ANIMATIONS = {
    "idle": {
        "frames": 4,
        "frame_time": 0.2,
        "loop": True
    },
    # ... 其他敌人动画
}

# 动画状态机：定义状态之间的合法转换
PLAYER_STATE_MACHINE = {
    "idle": ["walk", "jump_start", "attack", "attack_up", "attack_down", "dash"],  # 待机可以转换到所有动作
    "walk": ["idle", "jump_start", "attack", "attack_up", "attack_down", "dash"],  # 行走可以转换到所有动作
    "jump_start": ["jump_loop"],  # 跳跃开始必然转到循环
    "jump_loop": ["jump_land", "attack", "attack_up", "attack_down"],   # 空中可以攻击
    "jump_land": ["idle"],        # 落地后回到待机
    "attack": ["idle", "walk"],   # 攻击结束可以回到idle或walk
    "attack_up": ["idle", "walk"],
    "attack_down": ["idle", "walk"],
    "dash": ["idle", "attack", "attack_up", "attack_down"]  # 冲刺可以直接接攻击
}

# 资源路径配置
ANIMATION_PATHS = {
    "player": {
        "idle": "assets/sprites/player/idle/{frame}.PNG",
        "walk": "assets/sprites/player/walk/{frame}.PNG",
        "jump_start": "assets/sprites/player/jump/start/{frame}.PNG",
        "jump_loop": "assets/sprites/player/jump/loop/{frame}.PNG",
        "jump_land": "assets/sprites/player/jump/land/{frame}.PNG",
        "attack": "assets/sprites/player/attack/normal/{frame}.PNG",
        "attack_up": "assets/sprites/player/attack/up/{frame}.PNG",
        "attack_down": "assets/sprites/player/attack/down/{frame}.PNG",
        "dash": "assets/sprites/player/dash/{frame}.PNG",
        "dash_effect": "assets/sprites/player/dasheffect/{frame}.png"
    },
    "enemy": "assets/sprites/enemy/{state}/{frame}.PNG",
    "effects":{
    "dash_effect": "assets/sprites/player/dasheffect/{frame}.png"
    }
}