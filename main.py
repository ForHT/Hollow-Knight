"""
��Ϸ�����
"""
from core.engine import GameEngine

def main():
    # ������Ϸ����ʵ��
    engine = GameEngine()
    
    try:
        # ��ʼ����Ϸ
        engine.init()
        
        # ������Ϸ
        engine.run()
    except Exception as e:
        print(f"��Ϸ��������: {e}")
    finally:
        # ȷ����ȷ�˳�
        engine.quit()

if __name__ == "__main__":
    main() 