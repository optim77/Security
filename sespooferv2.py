from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Adres odbiorcy i szczegóły nadawcy
receiver = 'plajerowy@gmail.com'
receiver_name = "AA"
fromaddr = 'Name <xd@gmail.com>'
smtp_server = "gmail-smtp-in.l.google.com"

# Tworzenie wiadomości
msg = MIMEMultipart()
msg['Subject'] = 'XD'
msg['From'] = fromaddr
msg['To'] = receiver

# Wczytanie szablonu HTML z pliku
try:
    with open('index.html', 'r') as file:
        message = file.read()  # Wczytaj treść pliku
        msg.attach(MIMEText(message, "html"))  # Dołącz treść w formacie HTML
except FileNotFoundError:
    print("[ERROR] Plik 'index.html' nie istnieje.")
    exit(1)

# Wysyłanie wiadomości
try:
    with SMTP(smtp_server, 25) as sm:
        sm.starttls()  # Aktywacja szyfrowania TLS
        print("[INFO] Połączenie z serwerem SMTP zostało ustanowione.")
        sm.sendmail(fromaddr, receiver, msg.as_string())  # Wysyłanie wiadomości
        print("[INFO] E-mail wysłany pomyślnie!")
except Exception as e:
    print(f"[ERROR] Wystąpił błąd: {e}")
