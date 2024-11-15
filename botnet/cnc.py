import socketserver
import time

class BotHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # Odbieranie danych od klienta
        self.data = self.request.recv(1024).strip()
        print(f"Bot with IP {self.client_address[0]} sent:")
        print(self.data.decode())

        # Odczyt danych z pliku z poleceniami
        try:
            with open("commands.txt", "r") as file:
                commands = file.readlines()
        except FileNotFoundError:
            print("[ERROR] Plik commands.txt nie istnieje. Upewnij się, że jest w katalogu.")
            self.request.sendall(b"[ERROR] Nie znaleziono pliku z poleceniami.")
            return

        # Wysyłanie poleceń do klienta
        for command in commands:
            command = command.strip()  # Usunięcie znaków nowej linii
            if command:  # Pomijanie pustych linii
                print(f"[SENDING] Wysyłam polecenie: {command}")
                self.request.sendall(command.encode())
                time.sleep(1)  # Dodanie opóźnienia między wysyłanymi poleceniami

if __name__ == "__main__":
    HOST, PORT = "", 8000
    tcpServer = socketserver.TCPServer((HOST, PORT), BotHandler)
    try:
        print("[INFO] Serwer uruchomiony i nasłuchuje...")
        tcpServer.serve_forever()
    except KeyboardInterrupt:
        print("\n[INFO] Serwer zatrzymany.")
    except Exception as e:
        print(f"[ERROR] Wystąpił błąd: {e}")
