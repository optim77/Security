import argparse
from scapy.all import IP, TCP, sr1

def syn_scan(target_ip):
    print(f"[INFO] Rozpoczynanie skanowania SYN dla {target_ip}...")
    
    open_ports = []
    for port in range(1, 65536):
        # Tworzenie pakietu SYN
        packet = IP(dst=target_ip) / TCP(dport=port, flags="S")
        response = sr1(packet, timeout=1, verbose=False)  # Wysłanie pakietu i oczekiwanie na odpowiedź
        
        if response:
            # Sprawdzanie, czy odpowiedź zawiera flagę SYN-ACK (port otwarty)
            if response.haslayer(TCP) and response[TCP].flags == "SA":
                open_ports.append(port)
                print(f"[OPEN] Port {port} jest otwarty")
    
    if open_ports:
        print(f"\n[RESULT] Otwartych portów: {len(open_ports)}")
        print(", ".join(map(str, open_ports)))
    else:
        print("\n[RESULT] Nie znaleziono otwartych portów.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Skanowanie SYN na wszystkich portach dla podanego adresu IP.")
    parser.add_argument("target", help="Adres IP celu do skanowania")
    args = parser.parse_args()
    
    try:
        syn_scan(args.target)
    except KeyboardInterrupt:
        print("\n[INFO] Skanowanie przerwane przez użytkownika.")
    except Exception as e:
        print(f"[ERROR] Wystąpił błąd: {e}")
