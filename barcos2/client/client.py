import socket

def display_board(board):
    for row in board:
        print(" ".join(row))

def main():
    # Inicializa el tablero vacío
    board = [["~" for _ in range(4)] for _ in range(4)]
    ship_positions = set()

    # Configuración del cliente
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Attempting to connect to the server...")
    client.connect(("server", 8080))  # Se conecta al nombre del servicio en Docker

    # Recibe el mensaje de bienvenida
    print(client.recv(1024).decode("utf-8"))

    # Coloca el barco del cliente (3 posiciones)
    while len(ship_positions) < 3:
        display_board(board)
        position = input("Enter your ship position (x,y): ")
        client.send(position.encode("utf-8"))
        response = client.recv(1024).decode("utf-8")
        print(response)
        try:
            x, y = map(int, position.split(","))
            if "registered" in response:
                board[x][y] = "S"  # Marca la posición del barco
                ship_positions.add((x, y))
        except ValueError:
            print("Invalid input. Try again.")

    print("All ships placed! Waiting for game to start...")

    while True:
        # Muestra el tablero actual
        display_board(board)

        # Enviar ataque al servidor
        move = input("Enter your attack position (x,y): ")
        if move.lower() == "quit":
            print("Exiting the game...")
            break

        client.send(move.encode("utf-8"))
        response = client.recv(1024).decode("utf-8")
        print(response)

        try:
            x, y = map(int, move.split(","))
            if "Hit" in response:
                board[x][y] = "X"
            elif "Miss" in response:
                board[x][y] = "O"
        except ValueError:
            print("Invalid input. Try again.")

if __name__ == "__main__":
    main()
