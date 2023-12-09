import socket
import selectors

class Room:
    def __init__(self, room_id, player1):
        self.id = room_id
        self.player1 = player1
        self.player2 = None
        self.turn = 1
        self.sel = selectors.DefaultSelector()

    def add_player(self, player2):
        self.player2 = player2
        self.sel.register(self.player1, selectors.EVENT_READ, data=self.player1)
        self.sel.register(self.player2, selectors.EVENT_READ, data=self.player2)
        print("player 2 added")
        self.handle_players()

    def handle_players(self):
        while True:
            events = self.sel.select()
            for key, mask in events:
                player = key.data
                data = player.recv(1024)
                if not data:
                    print(f"Player {player} left the game")
                    self.sel.unregister(player)
                    player.close()
                    return

                if player == self.player1:
                    self.turn = 3 - self.turn

                other_player = self.player2 if player == self.player1 else self.player1
                other_player.sendall(data)

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "192.168.7.8"
    port = 12345

    server_socket.bind((host, port))
    server_socket.listen(5)

    rooms = []

    print(f"Server listening on {host}:{port}")

    while True:
        client_socket, addr = server_socket.accept()
        print("🐍 File: Chess/server.py | Line: 50 | start_server ~ addr",addr)
        flag = False

        data = client_socket.recv(1024).decode()
        data_parts = data.split(":")
        room_id = data_parts[0]

        for room in rooms:
            if room.id == room_id:
                room.add_player(client_socket)
                flag = True
                client_socket.send("black".encode())
                break  

        if not flag:
            new_room = Room(room_id, client_socket)
            rooms.append(new_room)
            client_socket.send("white".encode())
        
        

        client_socket.close()

if __name__ == "__main__":
    start_server()
