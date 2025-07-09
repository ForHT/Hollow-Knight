import pygame

going = True
pygame.init()
screen = pygame.display.set_mode((1200, 800))
"""角色状态"""
state = "idle"
FRAME_COUNTS = {
    "idle":9,
    "walk":6,
}

"""帧率设置"""
clock = pygame.time.Clock()
current_frame = 0 #当前帧 
time_accumulated = 0 #已累积的时间
ANIMATION_SPEED = 0.1 #设置时间间隔为0.1s

while going: #让屏幕不要退出
    # tick返回的是距离上一次调用经过的毫秒数
    dt = clock.tick(60) / 1000.0  # 转换为秒

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            going = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_0:
                state = "idle"
                current_frame = 0
            elif event.key == pygame.K_1:
                state = "walk"
                current_frame = 0

    max_frames = FRAME_COUNTS[state]   # 根据当前状态获取对应的总帧数

    time_accumulated += dt
    if time_accumulated >= ANIMATION_SPEED:
        time_accumulated = 0  # 重置累加器
        current_frame = (current_frame + 1) % max_frames


    screen.fill((0,0,0))
    player = pygame.image.load(f'assets/sprites/player/{state}/{current_frame}.png')
    screen.blit(player,(100,100))
    pygame.display.flip()
        