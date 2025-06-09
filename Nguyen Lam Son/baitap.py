import pygame  # Nhập thư viện pygame để xây dựng trò chơi
import random  # Nhập thư viện random để tạo số ngẫu nhiên

# Khởi tạo Pygame
pygame.init()  

# Thiết lập màn hình
SCREEN_WIDTH = 1280  # Độ rộng của cửa sổ trò chơi
SCREEN_HEIGHT = 720  # Độ cao của cửa sổ trò chơi
FPS = 50  # Số khung hình mỗi giây

# Màu sắc (dùng cho trường hợp không có hình ảnh)
WHITE = (255, 255, 255)  # Màu trắng
BLUE = (0, 0, 255)  # Màu xanh dương
ORANGE = (255, 165, 0)  # Màu cam
RED = (255, 0, 0)  # Màu đỏ

# Thiết lập cửa sổ hiển thị trò chơi
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Khởi tạo cửa sổ với kích thước xác định
pygame.display.set_caption("Pizza Catching Game")  # Đặt tiêu đề cửa sổ trò chơi
clock = pygame.time.Clock()  # Khởi tạo đồng hồ để kiểm soát tốc độ khung hình

# Tải và điều chỉnh kích thước hình nền
try:
    background = pygame.image.load("background.jpg")  # Cố gắng tải hình ảnh nền
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Điều chỉnh kích thước hình nền
except pygame.error:
    background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))  # Nếu lỗi, tạo nền màu trắng
    background.fill(WHITE)

# Tải và điều chỉnh kích thước hình ảnh chảo
try:
    pan_image = pygame.image.load("pan.jpg")  # Cố gắng tải hình ảnh chảo
    pan_image = pygame.transform.scale(pan_image, (120, 45))  # Điều chỉnh kích thước chảo
except pygame.error:
    pan_image = pygame.Surface((120, 45))  # Nếu lỗi, tạo hình chữ nhật màu xanh dương
    pan_image.fill(BLUE)

# Tải và điều chỉnh kích thước hình ảnh pizza
try:
    pizza_image = pygame.image.load("pizza.jpg")  # Cố gắng tải hình ảnh pizza
    pizza_image = pygame.transform.scale(pizza_image, (100, 100))  # Điều chỉnh kích thước pizza
except pygame.error:
    pizza_image = pygame.Surface((100, 100), pygame.SRCALPHA)  # Nếu lỗi, tạo hình tròn màu cam
    pygame.draw.circle(pizza_image, ORANGE, (50, 50), 50)

# Lớp đại diện cho chảo
class Pan:
    def __init__(self):
        self.image = pan_image  # Sử dụng hình ảnh chảo đã tải
        self.rect = self.image.get_rect()  # Lấy hình chữ nhật bao quanh hình ảnh
        self.rect.y = 600  # Vị trí của chảo trên trục Y
        self.rect.x = SCREEN_WIDTH // 2  # Vị trí ban đầu ở giữa màn hình

    def update(self):
        self.rect.x = pygame.mouse.get_pos()[0]  # Chảo di chuyển theo con trỏ chuột
        if self.rect.left < 0:  # Kiểm tra nếu chảo đi quá bên trái
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:  # Kiểm tra nếu chảo đi quá bên phải
            self.rect.right = SCREEN_WIDTH

    def draw(self):
        screen.blit(self.image, self.rect)  # Vẽ chảo lên màn hình

# Lớp đại diện cho pizza
class Pizza:
    def __init__(self, game):
        self.image = pizza_image  # Sử dụng hình ảnh pizza
        self.rect = self.image.get_rect()  # Lấy hình chữ nhật bao quanh pizza
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)  # Tạo vị trí ngẫu nhiên theo chiều ngang
        self.rect.y = 0  # Bắt đầu từ trên cùng màn hình
        self.speed = random.randint(2, 5)  # Tốc độ rơi ngẫu nhiên
        self.game = game  # Tham chiếu tới trò chơi

    def update(self):
        self.rect.y += self.speed  # Pizza rơi xuống theo tốc độ đã đặt
        if self.rect.top > SCREEN_HEIGHT:  # Nếu pizza rơi khỏi màn hình
            self.game.missed_pizza += 1  # Tăng số pizza bị bỏ lỡ
            self.game.pizzas.remove(self)  # Xóa pizza khỏi danh sách
        if self.rect.colliderect(self.game.pan.rect):  # Nếu pizza va vào chảo
            self.game.score += 1  # Tăng điểm số
            self.game.pizzas.append(Pizza(self.game))  # Thêm pizza mới vào trò chơi
            self.game.pizzas.remove(self)  # Xóa pizza đã bắt được

    def draw(self):
        screen.blit(self.image, self.rect)  # Vẽ pizza lên màn hình

# Lớp quản lý trò chơi
class Game:
    def __init__(self):
        self.pan = Pan()  # Tạo đối tượng chảo
        self.pizzas = []  # Danh sách chứa các pizza
        self.score = 0  # Điểm số ban đầu
        self.missed_pizza = 0  # Số pizza bị bỏ lỡ ban đầu
        self.font = pygame.font.SysFont("Comic Sans MS", 36, bold=True)  # Tạo font chữ
        self.game_over = False  # Trạng thái trò chơi ban đầu
        self.start_pizza_drop()  # Bắt đầu thả pizza

    def start_pizza_drop(self):
        for _ in range(3):  # Bắt đầu trò chơi với 3 pizza rơi
            self.pizzas.append(Pizza(self))

    def reset(self):
        self.__init__()  # Đặt lại trạng thái trò chơi

    def update(self):
        if not self.game_over:
            self.pan.update()  # Cập nhật chảo
            for pizza in self.pizzas[:]:  # Cập nhật các pizza
                pizza.update()
            if self.missed_pizza >= 3:  # Nếu số pizza bị bỏ lỡ đạt 3
                self.game_over = True

    def draw(self):
        screen.blit(background, (0, 0))  # Vẽ hình nền
        self.pan.draw()  # Vẽ chảo
        for pizza in self.pizzas:  # Vẽ pizza
            pizza.draw()
        score_text = self.font.render(f"Score: {self.score}", True, RED)  # Hiển thị điểm số
        missed_text = self.font.render(f"Missed: {self.missed_pizza}", True, RED)  # Hiển thị số pizza bị bỏ lỡ
        screen.blit(score_text, (SCREEN_WIDTH - 200, 20))
        screen.blit(missed_text, (SCREEN_WIDTH - 200, 60))
        if self.game_over:  # Nếu trò chơi kết thúc
            game_over_text = self.font.render("Game Over - Press R to Restart", True, RED)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2))

# Hàm chính để chạy trò chơi
def main():
    game = Game()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if game.game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                game.reset()

        game.update()
        game.draw()
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()