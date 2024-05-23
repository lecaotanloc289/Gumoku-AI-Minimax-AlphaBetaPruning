import turtle #
import random

global move_history

# trả về 1 bảng trống kiểu [[" ", " ", " “], [” ", " ", " “], [” ", " ", " "]] 
# tùy thuộc vào size
def make_empty_board(size):
    board = []
    for i in range(size):
        board.append([" "] * size)
    return board

# kiểm tra xem bảng có trống hay không
def is_empty(board):
    return board == [[" "] * len(board)] * len(board)

# kiểm tra 1 điểm có nằm bên trong bảng hay không
def is_in(board, y, x):
    return 0 <= y < len(board) and 0 <= x < len(board)

# kiểm tra thắng
def is_win(board):
    black = score_of_col(board, "b")
    white = score_of_col(board, "w")

    sum_sumcol_values(black)
    sum_sumcol_values(white)

    if 5 in black and black[5] == 1:
        return "Black won"
    elif 5 in white and white[5] == 1:
        return "White won"

    if (
        sum(black.values()) == black[-1]
        and sum(white.values()) == white[-1]
        or possible_moves(board) == []
    ):
        return "Draw"

    return "Continue playing"


##AI Engine
def march(board, y, x, dy, dx, length):
    """
    tìm vị trí xa nhất trong dy,dx trong khoảng length

    """
    yf = y + length * dy
    xf = x + length * dx
    # chừng nào yf,xf không có trong board
    while not is_in(board, yf, xf):
        yf -= dy
        xf -= dx

    return yf, xf
def score_ready(scorecol):
    """
    Khởi tạo hệ thống điểm

    """
    sumcol = {0: {}, 1: {}, 2: {}, 3: {}, 4: {}, 5: {}, -1: {}}
    for key in scorecol:
        for score in scorecol[key]:
            if key in sumcol[score]:
                sumcol[score][key] += 1
            else:
                sumcol[score][key] = 1

    return sumcol
def sum_sumcol_values(sumcol):
    """
    hợp nhất điểm của mỗi hướng
    """

    for key in sumcol:
        if key == 5:
            sumcol[5] = int(1 in sumcol[5].values())
        else:
            sumcol[key] = sum(sumcol[key].values())

    # hàm kiểm tra xem 1 hàng | cột | đường chéo trong bảng có thể dành chiến thắng hay không
def score_of_list(lis, col):
    blank = lis.count(" ")
    filled = lis.count(col)

    if blank + filled < 5:
        return -1
    elif blank == 5:
        return 0
    else:
        return filled      
    
    # trả về một danh sách các phần tử của bảng cờ theo một hướng cho trước.
def row_to_list(board, y, x, dy, dx, yf, xf):
    """
    trả về list của y,x từ yf,xf

    """
    row = []
    while y != yf + dy or x != xf + dx:
        row.append(board[y][x])
        y += dy
        x += dx
    return row
def score_of_row(board, cordi, dy, dx, cordf, col):
    """
    trả về một list với mỗi phần tử đại diện cho số điểm của 5 khối

    """
    colscores = []
    y, x = cordi
    yf, xf = cordf
    row = row_to_list(board, y, x, dy, dx, yf, xf)
    for start in range(len(row) - 4):
        score = score_of_list(row[start : start + 5], col)
        colscores.append(score)

    return colscores
def score_of_col(board, col):
    """
    tính toán điểm số mỗi hướng của column dùng cho is_win;
    """

    f = len(board)
    # scores của 4 hướng đi
    scores = {(0, 1): [], (-1, 1): [], (1, 0): [], (1, 1): []}
    for start in range(len(board)):
        scores[(0, 1)].extend(
            score_of_row(board, (start, 0), 0, 1, (start, f - 1), col)
        )
        scores[(1, 0)].extend(
            score_of_row(board, (0, start), 1, 0, (f - 1, start), col)
        )
        scores[(1, 1)].extend(
            score_of_row(board, (start, 0), 1, 1, (f - 1, f - 1 - start), col)
        )
        scores[(-1, 1)].extend(score_of_row(board, (start, 0), -1, 1, (0, start), col))

        if start + 1 < len(board):
            scores[(1, 1)].extend(
                score_of_row(board, (0, start + 1), 1, 1, (f - 2 - start, f - 1), col)
            )
            scores[(-1, 1)].extend(
                score_of_row(board, (f - 1, start + 1), -1, 1, (start + 1, f - 1), col)
            )

    return score_ready(scores)
def score_of_col_one(board, col, y, x):
    """
    trả lại điểm số của column trong y,x theo 4 hướng,
    key: điểm số khối đơn vị đó -> chỉ ktra 5 khối thay vì toàn bộ
    """

    scores = {(0, 1): [], (-1, 1): [], (1, 0): [], (1, 1): []}

    scores[(0, 1)].extend(
        score_of_row(
            board, march(board, y, x, 0, -1, 4), 0, 1, march(board, y, x, 0, 1, 4), col
        )
    )

    scores[(1, 0)].extend(
        score_of_row(
            board, march(board, y, x, -1, 0, 4), 1, 0, march(board, y, x, 1, 0, 4), col
        )
    )

    scores[(1, 1)].extend(
        score_of_row(
            board, march(board, y, x, -1, -1, 4), 1, 1, march(board, y, x, 1, 1, 4), col
        )
    )

    scores[(-1, 1)].extend(
        score_of_row(
            board,
            march(board, y, x, -1, 1, 4),
            1,
            -1,
            march(board, y, x, 1, -1, 4),
            col,
        )
    )

    return score_ready(scores)
def possible_moves(board):
    """
    khởi tạo danh sách tọa độ có thể có tại ranh giới các nơi đã đánh phạm vi 3 đơn vị
    """
    # mảng taken lưu giá trị của người chơi và của máy trên bàn cờ
    taken = []
    # mảng directions lưu hướng đi (8 hướng)
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (-1, 1), (1, -1)]
    # cord: lưu các vị trí không đi
    cord = {}

    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] != " ":
                taken.append((i, j))
    """ duyệt trong hướng đi và mảng giá trị trên bàn cờ của người chơi và máy, kiểm tra nước không thể đi(trùng với 
    nước đã có trên bàn cờ)
    """
    for direction in directions:
        dy, dx = direction
        for coord in taken:
            y, x = coord
            for length in [1, 2, 3, 4]:
                move = march(board, y, x, dy, dx, length)
                if move not in taken and move not in cord:
                    cord[move] = False
    return cord
def TF34score(score3, score4):
    """
    trả lại trường hợp chắc chắn có thể thắng(4 ô liên tiếp)
    """
    for key4 in score4:
        if score4[key4] >= 1:
            for key3 in score3:
                if key3 != key4 and score3[key3] >= 2:
                    return True
    return False
def stupid_score(board, col, anticol, y, x):
    """
    cố gắng di chuyển y,x
    trả về điểm số tượng trưng lợi thế
    """

    global colors
    M = 1000
    res, adv, dis = 0, 0, 0

    # tấn công
    board[y][x] = col
    # draw_stone(x,y,colors[col])
    sumcol = score_of_col_one(board, col, y, x)
    a = winning_situation(sumcol)
    adv += a * M
    sum_sumcol_values(sumcol)
    # {0: 0, 1: 15, 2: 0, 3: 0, 4: 0, 5: 0, -1: 0}
    adv += sumcol[-1] + sumcol[1] + 4 * sumcol[2] + 8 * sumcol[3] + 16 * sumcol[4]

    # phòng thủ
    board[y][x] = anticol
    sumanticol = score_of_col_one(board, anticol, y, x)
    d = winning_situation(sumanticol)
    dis += d * (M - 100)
    sum_sumcol_values(sumanticol)
    dis += (
        sumanticol[-1]
        + sumanticol[1]
        + 4 * sumanticol[2]
        + 8 * sumanticol[3]
        + 16 * sumanticol[4]
    )

    res = adv + dis

    board[y][x] = " "
    return res
def winning_situation(sumcol):
    """
    trả lại tình huống chiến thắng dạng như:
    {0: {}, 1: {(0, 1): 4, (-1, 1): 3, (1, 0): 4, (1, 1): 4}, 2: {}, 3: {}, 4: {}, 5: {}, -1: {}}
    1-5 lưu điểm có độ nguy hiểm từ thấp đến cao,
    -1 là rơi vào trạng thái tồi, cần phòng thủ
    """

    if 1 in sumcol[5].values():
        return 5
    elif len(sumcol[4]) >= 2 or (len(sumcol[4]) >= 1 and max(sumcol[4].values()) >= 2):
        return 4
    elif TF34score(sumcol[3], sumcol[4]):
        return 4
    else:
        score3 = sorted(sumcol[3].values(), reverse=True)
        if len(score3) >= 2 and score3[0] >= score3[1] >= 2:
            return 3
    return 0

# def best_move(board, col):
    """
    trả lại điểm số của mảng trong lợi thế của từng màu
    """
    if col == "w":
        anticol = "b"
    else:
        anticol = "w"

    movecol = (0, 0)
    maxscorecol = ""
    # kiểm tra nếu bàn cờ rỗng thì cho vị trí random nếu không thì đưa ra giá trị trên bàn cờ nên đi
    if is_empty(board):
        movecol = (
            int((len(board)) * random.random()),
            int((len(board[0])) * random.random()),
        )
    else:
        moves = possible_moves(board)

        for move in moves:
            y, x = move
            if maxscorecol == "":
                scorecol = stupid_score(board, col, anticol, y, x)
                maxscorecol = scorecol
                movecol = move
            else:
                scorecol = stupid_score(board, col, anticol, y, x)
                if scorecol > maxscorecol:
                    maxscorecol = scorecol
                    movecol = move
    return movecol

def best_move(board, col, depth):
    if col == "w":
        anticol = "b"
    else:
        anticol = "w"

    movecol = (0, 0)
    maxscorecol = ""

    if is_empty(board):
        movecol = (
            int((len(board)) * random.random()),
            int((len(board[0])) * random.random()),
        )
    else:
        moves = possible_moves(board)

        for move in moves:
            y, x = move
            if maxscorecol == "":
                # Call the search function to find the best move using minimax algorithm
                scorecol, _ = search(board, col, anticol, depth, -float("inf"), float("inf"), True)
                maxscorecol = scorecol
                movecol = _
            else:
                scorecol, _ = search(board, col, anticol, depth, -float("inf"), float("inf"), True)
                if scorecol > maxscorecol:
                    maxscorecol = scorecol
                    movecol = scorecol

    return movecol

# Hàm đánh giá thế cờ, trả về điểm của máy trừ điểm của người
def evaluate(board, computer, human):
    score = 0
    # Kiểm tra các hàng
    for i in range(len(board)):
        row = board[i]
        score += score_of_list(row, computer) - score_of_list(row, human)
    # Kiểm tra các cột
    for j in range(len(board[0])):
        col = [board[i][j] for i in range(len(board))]
        score += score_of_list(col, computer) - score_of_list(col, human)
    # Kiểm tra các đường chéo chính
    for k in range(-len(board) + 5, len(board[0]) - 4):
        diag = [board[i][i + k] for i in range(len(board)) if 0 <= i + k < len(board[0])]
        score += score_of_list(diag, computer) - score_of_list(diag, human)
    # Kiểm tra các đường chéo phụ
    for k in range(-len(board) + 5, len(board[0]) - 4):
        diag = [board[i][len(board[0]) - 1 - i - k] for i in range(len(board)) if 0 <= len(board[0]) - 1 - i - k < len(board[0])]
        score += score_of_list(diag, computer) - score_of_list(diag, human)
    return score

# Hàm kiểm tra xem trò chơi cờ caro đã kết thúc hay chưa
def game_over(board):
    # Kiểm tra các hàng
    for i in range(len(board)):
        row = board[i]
        if score_of_list(row, "X") == 5 or score_of_list(row, "O") == 5:
            return True
    # Kiểm tra các cột
    for j in range(len(board[0])):
        col = [board[i][j] for i in range(len(board))]
        if score_of_list(col, "X") == 5 or score_of_list(col, "O") == 5:
            return True
    # Kiểm tra các đường chéo chính
    for k in range(-len(board) + 5, len(board[0]) - 4):
        diag = [board[i][i + k] for i in range(len(board)) if 0 <= i + k < len(board[0])]
        if score_of_list(diag, "X") == 5 or score_of_list(diag, "O") == 5:
            return True
    # Kiểm tra các đường chéo phụ
    for k in range(-len(board) + 5, len(board[0]) - 4):
        diag = [board[i][len(board[0]) - 1 - i - k] for i in range(len(board)) if 0 <= len(board[0]) - 1 - i - k < len(board[0])]
        if score_of_list(diag, "X") == 5 or score_of_list(diag, "O") == 5:
            return True
    # Kiểm tra xem còn ô trống nào trên bảng cờ hay không
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == " ":
                return False
    # Nếu không có ô trống nào, trò chơi kết thúc và hòa
    return True

# Hàm tìm kiếm nước đi tốt nhất cho máy bằng giải thuật cắt tỉa alpha beta
def search(board, computer, human, depth, alpha, beta, is_max):
    # Nếu độ sâu bằng 0 hoặc trò chơi kết thúc, trả về điểm của thế cờ hiện tại
    if depth == 0 or game_over(board):
        return evaluate(board, computer, human), None
    # Nếu lượt của máy, tìm kiếm nước đi có điểm cao nhất
    if is_max:
        best_score = -float("inf")
        best_move = None
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == " ":
                    board[i][j] = computer
                    score, move = search(board, computer, human, depth - 1, alpha, beta, False)
                    board[i][j] = " "
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)
                    alpha = max(alpha, best_score)
                    if alpha >= beta:
                        break
        return best_score, best_move
    else:
        best_score = float("inf")
        best_move = None
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == " ":
                    board[i][j] = human
                    score, move = search(board, computer, human, depth - 1, alpha, beta, True)
                    board[i][j] = " "
                    if score < best_score:
                        best_score = score
                        best_move = (i, j)
                    beta = min(beta, best_score)
                    if alpha >= beta:
                        break
        return best_score, best_move


##Graphics Engine


def click(x, y):
    global board, colors, win, move_history

    x, y = getindexposition(x, y)

    if x == -1 and y == -1 and len(move_history) != 0:
        x, y = move_history[-1]

        del move_history[-1]
        board[y][x] = " "
        x, y = move_history[-1]

        del move_history[-1]
        board[y][x] = " "
        return

    if not is_in(board, y, x):
        return

    if board[y][x] == " ":
        draw_stone(x, y, colors["b"])
        board[y][x] = "b"

        move_history.append((x, y))

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            print(game_res)
            win = True
            return

        ay, ax = best_move(board, "w", 2)
        draw_stone(ax, ay, colors["w"])
        board[ay][ax] = "w"

        move_history.append((ax, ay))

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            print(game_res)
            win = True
            return

def initialize(size):
    global win, board, screen, colors, move_history

    # lưu lịch sử nước đi, trạng thái trò chơi, vẽ bảng trống cho trò chơi
    move_history = []
    win = False
    board = make_empty_board(size)

    # tạo 1 màn hình
    screen = turtle.Screen()
    
    # set onclick cho màn hình
    screen.onclick(click)
    
    # thiết lập kích thước màn hình đồ họa
    screen.setup(screen.screensize()[1] * 2, screen.screensize()[1] * 2)
    
    # thiết lập hệ tọa độ của bảng
    screen.setworldcoordinates(-1, size, size, -1)
    
    # màu nền của game
    screen.bgcolor("orange")
    
    # tốc độ vẽ đồ họa
    screen.tracer(500)

    colors = {"w": turtle.Turtle(), "b": turtle.Turtle(), "g": turtle.Turtle()}
    colors["w"].color("white")
    colors["b"].color("black")

    for key in colors:
        colors[key].ht()
        colors[key].penup()
        colors[key].speed(0)

    # Vẽ lưới bảng trò chơi
    border = turtle.Turtle()
    
    # tốc độ vẽ
    border.speed(9)
    
    # đặt trạng thái bút lên trên đễ không vẽ khi di chuyển đến các điểm bắt đầu vẽ
    border.penup()

    side = (size - 1) / 2
    
    # vẽ các line dọc từ (0, 0) -> (0, 10)
    # rồi sau đó tăng tọa độ x lên
    i = -1
    for start in range(size):
        border.goto(start, side + side * i)
        border.pendown()
        i *= -1
        border.goto(start, side + side * i)
        border.penup()

    # vẽ các line nga từ (0, 0) -> (0, 10)
    # rồi sau đó tăng tọa độ x lên
    i = 1
    for start in range(size):
        border.goto(side + side * i, start)
        border.pendown()
        i *= -1
        border.goto(side + side * i, start)
        border.penup()

    border.ht()

    screen.listen()
    screen.mainloop()


def getindexposition(x, y):
    """
    lấy index
    """
    intx, inty = int(x), int(y)
    dx, dy = x - intx, y - inty
    if dx > 0.5:
        x = intx + 1
    elif dx < -0.5:
        x = intx - 1
    else:
        x = intx
    if dy > 0.5:
        y = inty + 1
    elif dx < -0.5:
        y = inty - 1
    else:
        y = inty
    return x, y

    # Hàm vẽ quân cờ
def draw_stone(x, y, colturtle):
    colturtle.goto(x, y - 0.3)
    colturtle.pendown()
    colturtle.begin_fill()
    colturtle.circle(0.3)
    colturtle.end_fill()
    colturtle.penup()


if __name__ == "__main__":
    initialize(10)
