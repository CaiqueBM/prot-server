import subprocess
import schedule
import time
import os
import datetime

# Variável para contar o número de falhas de ping
num_failures = 0

# Constantes de trabalho

# Endereço IP ou domínio do modem
IP_MODEM = "192.168.18.1"
NUM_MAX_FALHAS = 10
TEMPO_ENTRE_TESTES = 1  # tempo em minutos para cada teste

# Função para registrar no log
def log_failure():
    current_time = datetime.datetime.now()
    log_message = f"Servidor desligado devido a falta de energia na data {current_time.strftime('%d/%m/%Y')} às {current_time.strftime('%H:%M')}\n"
    with open("ping_log.txt", "a") as file:
        file.write(log_message)

def check_ping():
    global num_failures

    # Comando ping
    ping_command = ["ping", "-c", "4", IP_MODEM]

    # Executar o comando ping
    process = subprocess.Popen(
        ping_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    output, error = process.communicate()

    # Verificar se o ping foi bem-sucedido
    if process.returncode == 0:
        print(f"O modem está respondendo ao ping.")
        num_failures = 0  # Resetar o contador de falhas
    else:
        print(f"O modem NÃO está respondendo ao ping.")
        num_failures += 1  # Incrementar o contador de falhas

        # Se o número de falhas for igual a 2, executar o shutdown
        if num_failures == NUM_MAX_FALHAS:
            print("Duas falhas consecutivas de ping. Executando shutdown...")
            log_failure()
            os.system('''sudo sh -c "sudo shutdown -h now"''')  # Comando para desligar o PC


# Agendar a execução da função check_ping a cada 5 minutos
schedule.every(TEMPO_ENTRE_TESTES).minutes.do(check_ping)

# Loop principal para manter o programa em execução
while True:
    schedule.run_pending()
    time.sleep(1)
