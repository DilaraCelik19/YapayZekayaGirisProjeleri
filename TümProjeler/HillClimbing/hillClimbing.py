import random




# Resimdeki queen yerleşimi başlangıç durumu olarak alınacak.
def initialize_board_from_image():
    # Resimdeki "queen" koordinatları (satır ve sütun indexleri):
    # Örneğin, 8x8 tahta için bu koordinatlar manuel olarak girilmiştir.
    # [Satır, Sütun] formatında girilmiştir.
    return [4, 5, 6, 3, 4, 5, 6, 5]   # Resimden çıkarılan örnek koordinatlar

# Tahtayı ekranda gösterme
def show_board(board):
    size = len(board)
    for i in range(size):
        for j in range(size):
            if board[j] == i:
                print("Q", end=" ")
            else:
                print(".", end=" ")
        print()
    print()

# Heuristic fonksiyonu: Çakışan queen sayısını hesaplar
def determine_h_cost(board):
    h = 0
    size = len(board)
    for i in range(size):
        for j in range(i + 1, size):
            # Aynı satırda veya sütunda olan vezirler
            if board[i] == board[j] or abs(board[i] - board[j]) == abs(i - j):
                h += 1
    return h

# En iyi hamleyi belirleme
def best_move(board):
    size = len(board)
    moves = []
    current_h = determine_h_cost(board)

    for col in range(size):
        for row in range(size):
            if board[col] == row:
                continue
            new_board = list(board)
            new_board[col] = row
            h = determine_h_cost(new_board)
            moves.append((new_board, h))

    # En düşük heuristic değerine sahip hamleyi seç
    best_moves = [move for move in moves if move[1] < current_h]
    return random.choice(best_moves)[0] if best_moves else board

# Hill Climbing algoritması
def hill_climbing(board):
    current_h = determine_h_cost(board)
    steps = 0

    while True:
        print(f"Step {steps}:")
        show_board(board)
        print(f"h = {current_h}\n")

        next_board = best_move(board)
        next_h = determine_h_cost(next_board)

        if next_h == 0:  # Küresel optimum bulundu (h = 0)
            return next_board, next_h, steps

        if next_h >= current_h:  # Yerel maksimum
            return board, current_h, steps

        board = next_board
        current_h = next_h
        steps += 1

# Rastgele yeniden başlama ile Hill Climbing algoritması
def hill_climbing_with_restart(board, max_restarts=10):
    restarts = 0
    while restarts < max_restarts:
        solution, final_h, steps = hill_climbing(board)
        if final_h == 0:  # Küresel optimum bulundu
            return solution, final_h, steps, restarts
        board = [random.randint(0, len(board) - 1) for _ in range(len(board))]
        restarts += 1
    return board, determine_h_cost(board), 0, restarts

# Başlangıç tahtası (resimden alınan)
board = initialize_board_from_image()
print("Initial board:")
show_board(board)

# Algoritmayı çalıştır
solution, final_h, steps, restarts = hill_climbing_with_restart(board)

# Çözümü göster
print("Final board:")
show_board(solution)
print("Final h cost:", final_h)
print("Steps taken:", steps)
print("Restarts:", restarts)
