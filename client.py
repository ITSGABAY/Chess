import socket
import pygame
from pygame.locals import QUIT
from Game import OnlineChessGame
from Pieces import *
from pprint import pprint
import sys

def start_client():
    # Create a socket and connect to the server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "192.168.7.8"
    port = 12345
    print("Client Starting")
    
    try:
        client_socket.connect((host, port))
    except socket.error as e:
        print(f"Failed to connect to the server: {e}")
        sys.exit(1)

    # Get the room ID from the user
    room_id = input("Enter room ID: ")

    try:
        # Send room ID to the server (encode the string to bytes)
        client_socket.send(room_id.encode())

        # Receive color from the server
        color = client_socket.recv(1024).decode()

        # Initialize and run the ChessGame
        chess = OnlineChessGame(color, client_socket)
        chess.run_game()

    except Exception as e:
        print(f"Error in client: {e}")

    finally:
        # Close the client socket
        client_socket.close()

if __name__ == "__main__":
    start_client()
