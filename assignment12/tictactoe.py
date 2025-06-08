class TictactoeException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class Board:
    valid_moves = [
        "upper left",
        "upper center",
        "upper right",
        "middle left",
        "center",
        "middle right",
        "lower left",
        "lower center",
        "lower right",
    ]

    def __init__(self):
        self.board_array = [[" " for _ in range(3)] for _ in range(3)]
        self.turn = "X"

    def __str__(self):
        lines = []
        lines.append(
            f" {self.board_array[0][0]} | {self.board_array[0][1]} | {self.board_array[0][2]} \n"
        )
        lines.append("-----------\n")
        lines.append(
            f" {self.board_array[1][0]} | {self.board_array[1][1]} | {self.board_array[1][2]} \n"
        )
        lines.append("-----------\n")
        lines.append(
            f" {self.board_array[2][0]} | {self.board_array[2][1]} | {self.board_array[2][2]} \n"
        )
        return "".join(lines)

    def move(self, move_string):
        if not move_string in Board.valid_moves:
            raise TictactoeException("That's not a valid move.")
        move_index = Board.valid_moves.index(move_string)
        row = move_index // 3
        column = move_index % 3
        if self.board_array[row][column] != " ":
            raise TictactoeException("That spot is taken.")
        self.board_array[row][column] = self.turn
        self.turn = "O" if self.turn == "X" else "X"

    def whats_next(self):
        cat = True
        for row in self.board_array:
            if " " in row:
                cat = False
                break
        if cat:
            return (True, "Cat's Game.")

        # Check if there is a winner:
        for row in self.board_array:
            if row[0] != " " and row[0] == row[1] == row[2]:
                return (True, f"{row[0]} wins!")

        for col in range(3):
            if (
                self.board_array[0][col] != " "
                and self.board_array[0][col]
                == self.board_array[1][col]
                == self.board_array[2][col]
            ):
                return (True, f"{self.board_array[0][col]} wins!")

        if self.board_array[1][1] != " ":
            if (
                self.board_array[0][0]
                == self.board_array[1][1]
                == self.board_array[2][2]
            ) or (
                self.board_array[0][2]
                == self.board_array[1][1]
                == self.board_array[2][0]
            ):
                return (True, f"{self.board_array[1][1]} wins!")

        # If no winner and game not over
        return (False, f"{self.turn}'s turn")


def play_game():
    board = Board()
    print("Start Tic Tac Toe!")
    print("Valid moves are: " + ", ".join(Board.valid_moves))

    while True:
        print("\nCurrent board:")
        print(board)

        game_over, message = board.whats_next()
        if game_over:
            print(message)
            break

        print(message)
        move = input("Next move: ").strip().lower()

        try:
            board.move(move)
        except TictactoeException as e:
            print(f"Invalid move: {e.message}")
            print(Board.valid_moves)


if __name__ == "__main__":
    play_game()
