# beginners.py - Quản lý điểm và cấp độ chơi

class ScoreManager:
    def __init__(self):
        self.score = 0
        self.level = 1
    
    def add_point(self):
        self.score += 1
        if self.score % 5 == 0:  # Tăng cấp độ mỗi 5 điểm
            self.level += 1

    def get_score(self):
        return self.score

    def get_level(self):
        return self.level

# Kiểm tra tính năng
if __name__ == "__main__":
    sm = ScoreManager()
    for _ in range(10):
        sm.add_point()
        print(f"Điểm: {sm.get_score()}, Cấp độ: {sm.get_level()}")