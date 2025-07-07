"""
游戏主入口
"""
from core.engine import GameEngine

def main():
    # 创建游戏引擎实例
    engine = GameEngine()
    
    try:
        # 初始化游戏
        engine.init()
        
        # 运行游戏
        engine.run()
    except Exception as e:
        print(f"游戏发生错误: {e}")
    finally:
        # 确保正确退出
        engine.quit()

if __name__ == "__main__":
    main() 