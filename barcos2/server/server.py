import socket

def main():
    # Inicializa el tablero vacío
    board = [["~" for _ in range(4)] for _ in range(4)]
    hits = set()
    ship_positions = set()  # Posiciones del barco del servidor

    # Coloca el barco del servidor (automático)
    ship_positions.add((1, 1))
    ship_positions.add((1, 2))
    ship_positions.add((1, 3))
    print(f"Server's ship positions: {ship_positions}")

    # Configuración del servidor
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 8080))  # Escucha en todas las interfaces
    server.listen(1)
    print("Server is ready and listening on port 8080.")

    # Acepta la conexión del cliente
    conn, addr = server.accept()
    print(f"Connection established with {addr}.")
    conn.send("Welcome to Battleship! Please place your ship (3 positions).\n".encode("utf-8"))

    # Recibe las posiciones del barco del cliente
    while len(ship_positions) < 3:
        try:
            conn.send("Enter your ship position as 'x,y': ".encode("utf-8"))
            move = conn.recv(1024).decode("utf-8").strip()
            x, y = map(int, move.split(","))
            if (x, y) in ship_positions:
                conn.send("Position already occupied. Try again.\n".encode("utf-8"))
            elif x < 0 or x > 3 or y < 0 or y > 3:
                conn.send("Invalid position. Coordinates must be between 0 and 3.\n".encode("utf-8"))
            else:
                ship_positions.add((x, y))
                conn.send(f"Position ({x},{y}) registered.\n".encode("utf-8"))
        except ValueError:
            conn.send("Invalid format! Enter position as 'x,y'.\n".encode("utf-8"))

    # Mensaje de inicio del juego
    conn.send("All ships placed! Let's start the game.\n".encode("utf-8"))

    while True:
        try:
            # Recibe el ataque del cliente
            conn.send("Enter your attack position as 'x,y': ".encode("utf-8"))
            move = conn.recv(1024).decode("utf-8").strip()
            if not move:
                print("Client disconnected.")
                break

            x, y = map(int, move.split(","))
            if (x, y) in hits:
                conn.send("You already attacked this position.\n".encode("utf-8"))
            elif (x, y) in ship_positions:
                hits.add((x, y))
                board[x][y] = "X"
                conn.send("Hit! You hit part of the ship!\n".encode("utf-8"))
            else:
                board[x][y] = "O"
                conn.send("Miss! No ship at this position.\n".encode("utf-8"))
        except ValueError:
            conn.send("Invalid format! Enter your attack as 'x,y'.\n".encode("utf-8"))
        except (BrokenPipeError, ConnectionResetError) as e:
            print(f"Connection error: {e}")
            break

    conn.close()
    print("Connection closed.")

if __name__ == "__main__":
    main()
