# ��Ϸ�ӿ�˵���ֲ�

��Һã�����������Ϸ�Ľӿ�˵���ֲᡣ������ü򵥵Ļ�����ÿ��ϵͳ����ô������Ϲ����ġ�

## ��Ϸ���� (GameEngine)

����������Ϸ�Ĵ�ܼң�����Э������ϵͳ������

### ��Ҫ���ܣ�
1. ��Ϸѭ��
   - ÿһ֡������� update() �� draw()
   - update() ���������Ϸ״̬�������ɫλ�á������ȣ�
   - draw() ��������ж���������Ļ��

2. ��Դ����
   - load_image("ͼƬ·��") ��ȡͼƬ
   - load_sound("��Ч·��") ��ȡ��Ч
   - ����ǵõ��� unload() �ͷŵ�

3. ��������
   - change_scene("������") �л����³���
   - ��������˵��л�����Ϸ����

## ����ϵͳ (Physics)

��������Ϸ�������Ч����������ײ�������ȡ�

### ��ô�ã�
1. ����������
   ```python
   # ����һ��������󣨱�����ң�
   player = PhysicsObject(x=100, y=100, width=32, height=32)
   physics.add_object(player)
   ```

2. �����ײ
   ```python
   # �������Ƿ������˵���
   if physics.check_collision(player, ground):
       player.can_jump = True
   ```

3. ��������
   ```python
   # ������������Ӱ��
   physics.apply_gravity(player)
   ```

## ����ϵͳ (Animation)

��������Ϸ�����ж���Ч����

### �����÷���
1. ��������
   ```python
   # ����һ�����ܶ���
   run_anim = Animation()
   run_anim.add_frame("�ܲ�1.png")
   run_anim.add_frame("�ܲ�2.png")
   run_anim.add_frame("�ܲ�3.png")
   ```

2. ���Ŷ���
   ```python
   # ��ʼ����
   player.play_animation(run_anim)
   
   # ֹͣ����
   player.stop_animation()
   ```

## ���ϵͳ (Player)

��������ҽ�ɫ��һ�����顣

### ��Ҫ���ܣ�
1. ���봦��
   ```python
   # ��鰴�����ƶ�
   if input.is_pressed("�Ҽ�ͷ"):
       player.move_right()
   if input.is_pressed("�ո�"):
       player.jump()
   ```

2. ״̬����
   ```python
   # ��ҿ����в�ͬ״̬
   player.set_state("վ��")
   player.set_state("��Ծ")
   player.set_state("����")
   ```

## ս��ϵͳ (Combat)

��������Ϸ���ս��������ݡ�

### ��ô�ã�
1. �����ж�
   ```python
   # ��鹥���Ƿ�����
   if combat.check_hit(player_attack, enemy):
       # �����ˣ������˺�
       damage = combat.calculate_damage(player_attack, enemy)
       enemy.take_damage(damage)
   ```

2. �˺�����
   ```python
   # �����˺� + �����˺� - ���׷���
   final_damage = base_damage + weapon.damage - target.defense
   ```

## ϵͳ֮������ô���������

1. ��ҹ�������ʱ��
   - ���ϵͳ����⵽��������
   - ����ϵͳ�����Ź�������
   - ս��ϵͳ�������Ƿ����к��˺�
   - ����ϵͳ���������Ч��

2. ����ƶ�ʱ��
   - ���ϵͳ������ƶ�����
   - ����ϵͳ�������ƶ�����ײ
   - ����ϵͳ�������ƶ�����

## ע������

1. ����˳�����Ҫ��
   - �ȴ�������
   - �ٸ�������
   - ��������Ⱦ����

2. �������⣺
   - �������û���ţ�����ǲ������ǵ��� update()
   - �����ײû��Ӧ����������Ƿ���ȷ��ӵ�����ϵͳ
   - �������û��Ӧ������Ƿ�����ȷ�ĵط���������

ϣ������ֲ�����а����������ʲô�����׵ģ���ʱ������Ŷ�� 