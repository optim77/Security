import smtplib
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email_with_template(from_address, to_address, subject, template_file, smtp_server, smtp_port, username, password):
    try:
        # Wczytanie treści wiadomości z pliku
        with open(template_file, 'r') as file:
            message_content = file.read()
        
        # Tworzenie wiadomości e-mail
        msg = MIMEMultipart()
        msg['From'] = from_address
        msg['To'] = to_address
        msg['Subject'] = subject
        msg.attach(MIMEText(message_content, 'plain'))
        
        # Łączenie z serwerem SMTP
        print(f"[INFO] Łączenie z serwerem SMTP {smtp_server}:{smtp_port}...")
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Aktywacja szyfrowania TLS
            print("[INFO] TLS aktywowane.")
            
            # Logowanie do serwera
            server.login(username, password)
            print("[INFO] Zalogowano do serwera SMTP.")
            
            # Wysyłanie wiadomości
            server.sendmail(from_address, to_address, msg.as_string())
            print("[INFO] E-mail wysłany pomyślnie!")
    
    except FileNotFoundError:
        print(f"[ERROR] Plik szablonu '{template_file}' nie istnieje.")
    except smtplib.SMTPAuthenticationError:
        print("[ERROR] Błąd uwierzytelniania. Sprawdź nazwę użytkownika i hasło.")
    except Exception as e:
        print(f"[ERROR] Wystąpił błąd: {e}")

if __name__ == "__main__":
    # Sprawdzanie argumentów wiersza poleceń
    if len(sys.argv) != 8:
        print("Użycie: python3 secure_email.py <from_address> <to_address> <subject> <template_file> <smtp_server> <smtp_port> <username> <password>")
        sys.exit(1)
    
    from_address = sys.argv[1]
    to_address = sys.argv[2]
    subject = sys.argv[3]
    template_file = sys.argv[4]
    smtp_server = sys.argv[5]
    smtp_port = int(sys.argv[6])
    username = sys.argv[7]
    password = sys.argv[8]
    
    send_email_with_template(from_address, to_address, subject, template_file, smtp_server, smtp_port, username, password)
