# 游戏接口说明手册

大家好！这是我们游戏的接口说明手册。这里会用简单的话解释每个系统是怎么互相配合工作的。

## 游戏引擎 (GameEngine)

这是整个游戏的大管家，负责协调所有系统工作。

### 主要功能：
1. 游戏循环
   - 每一帧都会调用 update() 和 draw()
   - update() 负责更新游戏状态（比如角色位置、动画等）
   - draw() 负责把所有东西画到屏幕上

2. 资源管理
   - load_image("图片路径") 读取图片
   - load_sound("音效路径") 读取音效
   - 用完记得调用 unload() 释放掉

3. 场景管理
   - change_scene("场景名") 切换到新场景
   - 比如从主菜单切换到游戏画面

## 物理系统 (Physics)

负责处理游戏里的物理效果，比如碰撞、重力等。

### 怎么用：
1. 添加物理对象
   ```python
   # 创建一个物理对象（比如玩家）
   player = PhysicsObject(x=100, y=100, width=32, height=32)
   physics.add_object(player)
   ```

2. 检查碰撞
   ```python
   # 检查玩家是否碰到了地面
   if physics.check_collision(player, ground):
       player.can_jump = True
   ```

3. 设置重力
   ```python
   # 让物体受重力影响
   physics.apply_gravity(player)
   ```

## 动画系统 (Animation)

负责处理游戏里所有动画效果。

### 基本用法：
1. 创建动画
   ```python
   # 创建一个奔跑动画
   run_anim = Animation()
   run_anim.add_frame("跑步1.png")
   run_anim.add_frame("跑步2.png")
   run_anim.add_frame("跑步3.png")
   ```

2. 播放动画
   ```python
   # 开始播放
   player.play_animation(run_anim)
   
   # 停止播放
   player.stop_animation()
   ```

## 玩家系统 (Player)

负责处理玩家角色的一切事情。

### 主要功能：
1. 输入处理
   ```python
   # 检查按键并移动
   if input.is_pressed("右箭头"):
       player.move_right()
   if input.is_pressed("空格"):
       player.jump()
   ```

2. 状态管理
   ```python
   # 玩家可以有不同状态
   player.set_state("站立")
   player.set_state("跳跃")
   player.set_state("攻击")
   ```

## 战斗系统 (Combat)

负责处理游戏里的战斗相关内容。

### 怎么用：
1. 攻击判定
   ```python
   # 检查攻击是否命中
   if combat.check_hit(player_attack, enemy):
       # 命中了，计算伤害
       damage = combat.calculate_damage(player_attack, enemy)
       enemy.take_damage(damage)
   ```

2. 伤害计算
   ```python
   # 基础伤害 + 武器伤害 - 护甲防御
   final_damage = base_damage + weapon.damage - target.defense
   ```

## 系统之间是怎么互相合作的

1. 玩家攻击敌人时：
   - 玩家系统：检测到攻击按键
   - 动画系统：播放攻击动画
   - 战斗系统：计算是否命中和伤害
   - 物理系统：处理击退效果

2. 玩家移动时：
   - 玩家系统：检测移动按键
   - 物理系统：处理移动和碰撞
   - 动画系统：播放移动动画

## 注意事项

1. 调用顺序很重要：
   - 先处理输入
   - 再更新物理
   - 最后才是渲染画面

2. 常见问题：
   - 如果动画没播放，检查是不是忘记调用 update()
   - 如果碰撞没反应，检查物体是否正确添加到物理系统
   - 如果按键没反应，检查是否在正确的地方处理输入

希望这个手册对你有帮助！如果有什么不明白的，随时问我们哦！ 