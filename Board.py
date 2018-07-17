import pygame
import random

pygame.init()
screen = pygame.display.set_mode((800, 800), 0, 32)
pygame.display.set_caption("五子棋")
font = pygame.font.Font("C:\Windows\Fonts\SimHei.ttf", 40)
w_success = font.render("白棋赢了！", True, (255, 255, 255))
b_success = font.render("黑棋赢了！", True, (0, 0, 0))

USER = 1
ROBOT = 2
PLAY = True  # True:人下白棋   False：机下黑棋

# 棋子状态： 0：空置  1：white 2：black
list_board_status = [[] for i in range(15)]
for i in range(0, 15):
	for j in range(0, 15):
		list_board_status[i].append(0)

# 棋子坐标
list_board_pos = [[] for i in range(15)]
for i in range(0, 15):
	posY = i * 40 + 120
	for j in range(0, 15):
		posX = j * 40 + 120
		list_board_pos[i].append((posX, posY))
		# print(list_board_pos[i][j])


def draw_board():
	bgColor = (213, 176, 146)
	screen.fill(bgColor)
	lineColor = (0, 0, 0)
	borderWidth = 4
	lineWidth = 2
	# startP = 120
	# endP = 680
	# 画边框
	pygame.draw.line(screen, lineColor, (120, 120), (680, 120), borderWidth)  # 上
	pygame.draw.line(screen, lineColor, (120, 680), (680, 680), borderWidth)  # 下
	pygame.draw.line(screen, lineColor, (120, 120), (120, 680), borderWidth)  # 左
	pygame.draw.line(screen, lineColor, (680, 120), (680, 680), borderWidth)  # 右

	# 画棋盘
	for i in range(1, 14):
		y = 120 + i * 40
		x = 120 + i * 40
		startP_row = (120, y)
		endP_row = (680, y)
		startP_col = (x, 120)
		endP_col = (x, 680)
		pygame.draw.line(screen, lineColor, startP_row, endP_row, lineWidth)  # 横线
		pygame.draw.line(screen, lineColor, startP_col, endP_col, lineWidth)  # 竖线

	# 画标 5 个记点 (400, 400) (240, 240) (240, 560) (560, 240) (560, 560)
	pygame.draw.circle(screen, lineColor, (400, 400), 4, 0)
	pygame.draw.circle(screen, lineColor, (240, 240), 4, 0)
	pygame.draw.circle(screen, lineColor, (240, 560), 4, 0)
	pygame.draw.circle(screen, lineColor, (560, 240), 4, 0)
	pygame.draw.circle(screen, lineColor, (560, 560), 4, 0)


class DrawChess:
	def __init__(self, pos=None, chess=None):
		self.pos = pos
		self.chess = chess
		self.white = (255, 255, 255)
		self.black = (0, 0, 0)
		# 棋子状态： 0：空置  1：white 2：black
		if self.chess == 1:
			self.draw_white()
		elif self.chess == 2:
			self.draw_black()
		else:
			pass

	def draw_white(self):
		pygame.draw.circle(screen, self.white, self.pos, 20, 0)

	def draw_black(self):
		pygame.draw.circle(screen, self.black, self.pos, 20, 0)


class AI:
	def __init__(self, list_status=None):
		self.list_status = list_status

	def re(self):
		return self.list_status


class Judge:
	def __init__(self, list_status=None, play=None, chessindex=None):
		self.list_status = list_status  # 棋盘状态
		self.PLAY = play  # True人下白棋1， False机下黑棋2
		self.indexX, self.indexY = chessindex  # 当前放下棋子的坐标
		self.chessNum = 1  # 连棋个数
		self.searchAll = False  # 是否全部搜索完毕
		self.judge = False
		if self.PLAY:  # 现在在下棋的对象
			self.role = USER
		else:
			self.role = ROBOT
		self.main()

	def main(self):
		moveY = self.indexY
		moveX = self.indexX
		direction = True  # 遍历方向 True往右 下， False往左 上
		# 横向5个白棋  x坐标(行)不变
		if not self.searchAll:
			while moveY in range(0, 16):
				if direction:
					moveY += 1
				else:
					moveY -= 1

				if self.list_status[self.indexX][moveY] == self.role:
					self.chessNum += 1
				else:
					# 如果是搜索到左边，则搜索完毕
					if direction is False:
						if self.chessNum < 5:
							self.chessNum = 1  # 搜索完横向，但没有获胜条件，将连棋置为初始状态
							direction = True
							moveY = self.indexY
							moveX = self.indexX
							break
						else:
							pass
					# 只要有一个不匹配，改变方向，且moveX移至起点
					direction = False
					moveY = self.indexY

				if self.chessNum >= 5:
					self.judge = True
					self.searchAll = True
					break
				else:
					pass
		# 竖向5个白棋  y 坐标(列)不变
		if not self.searchAll:
			while moveX in range(0, 16):
				if direction:
					moveX += 1
				else:
					moveX -= 1

				if self.list_status[moveX][self.indexY] == self.role:
					self.chessNum += 1
				else:
					# 如果是搜索到左边，则搜索完毕
					if direction is False:
						if self.chessNum < 5:
							self.chessNum = 1  # 搜索完横向，但没有获胜条件，将连棋置为初始状态
							direction = True
							moveY = self.indexY
							moveX = self.indexX
							break
						else:
							pass
					# 只要有一个不匹配，改变方向，且moveX移至起点
					direction = False
					moveX = self.indexX

				if self.chessNum >= 5:
					self.judge = True
					self.searchAll = True
					break
				else:
					pass
		# 左上到右下斜角
		if not self.searchAll:
			while moveX in range(0, 16) and moveY in range(0, 16):
				if direction:
					moveX += 1
					moveY += 1
				else:
					moveX -= 1
					moveY -= 1

				if self.list_status[moveX][moveY] == self.role:
					self.chessNum += 1
				else:
					# 如果是搜索到左边，则搜索完毕
					if direction is False:
						if self.chessNum < 5:
							self.chessNum = 1  # 搜索完横向，但没有获胜条件，将连棋置为初始状态
							direction = True
							moveY = self.indexY
							moveX = self.indexX
							break
						else:
							pass
					# 只要有一个不匹配，改变方向，且moveX移至起点
					direction = False
					moveX = self.indexX
					moveY = self.indexY

				if self.chessNum >= 5:
					self.judge = True
					self.searchAll = True
					break
				else:
					pass
		# 左下到右上斜角
		if not self.searchAll:
			while moveX in range(0, 16) and moveY in range(0, 16):
				if direction:
					moveX += 1
					moveY -= 1
				else:
					moveX -= 1
					moveY += 1

				if self.list_status[moveX][moveY] == self.role:
					self.chessNum += 1
				else:
					# 如果是搜索到左边，则搜索完毕
					if direction is False:
						if self.chessNum < 5:
							self.chessNum = 1  # 搜索完横向，但没有获胜条件，将连棋置为初始状态
							direction = True
							moveY = self.indexY
							moveX = self.indexX
							break
						else:
							pass
					# 只要有一个不匹配，改变方向，且moveX移至起点
					direction = False
					moveX = self.indexX
					moveY = self.indexY

				if self.chessNum >= 5:
					self.judge = True
					self.searchAll = True
					break
				else:
					pass


# 先画个棋盘，避免开始黑屏
draw_board()


while True:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			exit()
		if event.type == pygame.MOUSEBUTTONDOWN:
			draw_board()
			# print(pygame.mouse.get_pos())
			mouseX, mouseY = pygame.mouse.get_pos()

			# 格子是40长宽的，棋子半径为20，
			mouseX = mouseX - mouseX % 20
			mouseY = mouseY - mouseY % 20
			# 获得修正值，使得棋子落在网格上
			offsetX = mouseX % 40
			offsetY = mouseY % 40
			# 修正坐标值
			if offsetX != 0:
				mouseX = mouseX + offsetX
			else:
				pass
			if offsetY != 0:
				mouseY = mouseY + offsetY
			else:
				pass
			mousePos = (mouseX, mouseY)

			# 找到点击时所在网格的索引值，用于修改棋盘的状态
			for i in range(15):
				try:
					index = (i, list_board_pos[i].index(mousePos))
					break
				except ValueError:
					pass

			# print(index)
			# 人机交替下棋，并修改棋盘状态
			if list_board_status[index[0]][index[1]] == 0:  # 当前位置没有棋子，才能放下棋子
				if PLAY:
					list_board_status[index[0]][index[1]] = USER
					print(index)
					judge = Judge(list_board_status, PLAY, (index[0], index[1]))
					if judge.judge:
						print("白棋赢了！")
						screen.blit(w_success, (300, 40))
					else:
						pass
					PLAY = False
				else:
					# 实现AI： 获取合理的 index[0] 和 index[1]
					list_board_status[index[0]][index[1]] = ROBOT
					judge = Judge(list_board_status, PLAY, (index[0], index[1]))
					if judge.judge:
						print("黑棋赢了！")
						screen.blit(b_success, (300, 40))
					else:
						pass
					PLAY = True
					t = AI(list_board_status)
					# print(t.re())
			else:
				pass

			# 画棋子
			for i in range(15):
				for j in range(15):
					if list_board_status[i][j] == USER:
						DrawChess(list_board_pos[i][j], USER)
					elif list_board_status[i][j] == ROBOT:
						DrawChess(list_board_pos[i][j], ROBOT)
					else:
						pass

	pygame.display.update()
