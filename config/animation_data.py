"""
这个文件包含了从C++源代码中提取的、所有动画的硬编码数据。
这是我们新的“真值来源”。
"""

# C++中的 frameinterval 单位似乎是 1/60 秒 (帧)
# 我们在Pygame中用秒，所以需要转换。1帧 = 1/60秒 ≈ 0.0167秒
FRAME_TIME = 1 / 60.0

PLAYER_ANIMATIONS = {
    "idle": {
        "left": {
            "path_template": "resource/img/hollow knight/Idle/{}.PNG",
            "frame_count": 9,
            "frame_intervals": [4, 4, 4, 4, 4, 4, 4, 4, 4],
            "displacements": [(0, 0)] * 9, # C++代码中未指定，默认为0
            "loop": True,
        },
        "right": {
            "path_template": "resource/img/hollow knight/IdleR/{}.PNG",
            "frame_count": 9,
            "frame_intervals": [4, 4, 4, 4, 4, 4, 4, 4, 4],
            "displacements": [(0, 0)] * 9,
            "loop": True,
        }
    },
    "walk": {
        "left": {
            "path_template": "resource/img/hollow knight/Walk/{}.PNG",
            "frame_count": 8,
            "frame_intervals": [2, 2, 2, 2, 2, 2, 2, 2],
            "displacements": [(0, 0)] * 8, # C++代码中指定为0
            "loop": True,
        },
        "right": {
            "path_template": "resource/img/hollow knight/WalkR/{}.PNG",
            "frame_count": 8,
            "frame_intervals": [2, 2, 2, 2, 2, 2, 2, 2],
            "displacements": [(0, 0)] * 8,
            "loop": True,
        }
    },
    "dash": {
        "left": {
            "path_template": "resource/img/hollow knight/Dash/{}.PNG",
            "frame_count": 5,
            "frame_intervals": [1, 1, 1, 3, 3],
            "displacements": [(-45, 0), (-45, 0), (-45, 0), (-45, 0), (-45, 0)],
            "loop": False,
            "next_state": "idle"
        },
        "right": {
            "path_template": "resource/img/hollow knight/DashR/{}.PNG",
            "frame_count": 5,
            "frame_intervals": [1, 1, 1, 3, 3],
            "displacements": [(45, 0), (45, 0), (45, 0), (45, 0), (45, 0)],
            "loop": False,
            "next_state": "idle"
        }
    },
    "attack": {
        "left": {
            "path_template": "resource/img/hollow knight/Attack/Attack/1/{}.PNG",
            "frame_count": 5,
            "frame_intervals": [2, 1, 2, 2, 2],
            "displacements": [(0, 0), (0, 0), (0, 0), (-2, 0), (0, 0)],
            "loop": False,
            "next_state": "idle"
        },
        "right": {
            "path_template": "resource/img/hollow knight/AttackR/Attack/1/{}.PNG",
            "frame_count": 5,
            "frame_intervals": [2, 1, 2, 2, 2],
            "displacements": [(0, 0), (0, 0), (0, 0), (2, 0), (0, 0)],
            "loop": False,
            "next_state": "idle"
        }
    },
    "attack_up": {
        "left": {
            "path_template": "resource/img/hollow knight/Attack/AttackUp/{}.PNG",
            "frame_count": 5,
            "frame_intervals": [2, 2, 2, 2, 2],
            "displacements": [(0, 0)] * 5,
            "loop": False,
            "next_state": "idle"
        },
        "right": {
            "path_template": "resource/img/hollow knight/AttackR/AttackUp/{}.PNG",
            "frame_count": 5,
            "frame_intervals": [2, 2, 2, 2, 2],
            "displacements": [(0, 0)] * 5,
            "loop": False,
            "next_state": "idle"
        }
    },
    "attack_down": {
        "left": {
            "path_template": "resource/img/hollow knight/Attack/AttackDown/{}.PNG",
            "frame_count": 5,
            "frame_intervals": [2, 2, 2, 2, 2],
            "displacements": [(0, 0)] * 5,
            "loop": False,
            "next_state": "idle"
        },
        "right": {
            "path_template": "resource/img/hollow knight/AttackR/AttackDown/{}.PNG",
            "frame_count": 5,
            "frame_intervals": [2, 2, 2, 2, 2],
            "displacements": [(0, 0)] * 5,
            "loop": False,
            "next_state": "idle"
        }
    },
    "jump_start": {
        "left": {
            "path_template": "resource/img/hollow knight/Jump/Start/{}.PNG",
            "frame_count": 9,
            "frame_intervals": [2, 2, 2, 2, 2, 2, 2, 2, 2],
            "displacements": [(0, 0)] * 9,
            "loop": False,
            "next_state": "jump_loop"
        },
        "right": {
            "path_template": "resource/img/hollow knight/JumpR/Start/{}.PNG",
            "frame_count": 9,
            "frame_intervals": [2, 2, 2, 2, 2, 2, 2, 2, 2],
            "displacements": [(0, 0)] * 9,
            "loop": False,
            "next_state": "jump_loop"
        }
    },
    "jump_loop": {
         "left": {
            "path_template": "resource/img/hollow knight/Jump/Loop/{}.PNG",
            "frame_count": 3,
            "frame_intervals": [2, 2, 2],
            "displacements": [(0, 0)] * 3,
            "loop": True,
        },
        "right": {
            "path_template": "resource/img/hollow knight/JumpR/Loop/{}.PNG",
            "frame_count": 3,
            "frame_intervals": [2, 2, 2],
            "displacements": [(0, 0)] * 3,
            "loop": True,
        }
    },
    "hurt": {
        "left": {
            "path_template": "resource/img/hollow knight/Damage/{}.PNG",
            "frame_count": 6,
            "frame_intervals": [4, 4, 4, 4, 4, 4],
            "displacements": [(-5, -10)] + [(0,0)]*5, # Add knockback on first frame
            "loop": False,
            "next_state": "idle"
        },
        "right": {
            "path_template": "resource/img/hollow knight/DamageR/{}.PNG",
            "frame_count": 6,
            "frame_intervals": [4, 4, 4, 4, 4, 4],
            "displacements": [(5, -10)] + [(0,0)]*5, # Add knockback on first frame
            "loop": False,
            "next_state": "idle"
        }
    },
     "damage": {
        "left": {
            "path_template": "resource/img/hollow knight/Damage/{}.PNG",
            "frame_count": 6,
            "frame_intervals": [4, 4, 4, 4, 4, 4],
            "displacements": [(0, 0)] * 6, # 击退效果由速度脉冲处理，dmove清零
            "loop": False,
            "next_state": "idle"
        },
        "right": {
            "path_template": "resource/img/hollow knight/DamageR/{}.PNG",
            "frame_count": 6,
            "frame_intervals": [4, 4, 4, 4, 4, 4],
            "displacements": [(0, 0)] * 6, # 击退效果由速度脉冲处理，dmove清零
            "loop": False,
            "next_state": "idle"
        }
    }
}

# TODO: 以后我们还会在这里添加 BOSS_ANIMATIONS 和 EFFECT_ANIMATIONS
# C++ 代码中的特效是和攻击动画绑定的，我们需要一个新的系统来处理
# 暂时将特效数据注释掉，后续再整合
"""
EFFECT_DATA = {
    "player_dash_left": {
        "path_template": "resource/img/hollow knight/DashEffect/{}.png",
        "frame_count": 4,
        "displacements": [(20, -100), (24, -100), (28, -100), (32, -100)]
    },
    "player_dash_right": {
        "path_template": "resource/img/hollow knight/DashEffectR/{}.png",
        "frame_count": 4,
        "displacements": [(-430, -100), (-426, -100), (-422, -100), (-418, -100)]
    },
    ...
}
""" 