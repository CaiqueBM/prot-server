import subprocess
import schedule
import time
import os
import datetime

# Variável para contar o número de falhas de ping
num_failures = 0
# Variável para rastrear o estado anterior da conexão
previous_state = "connected"

# Constantes de trabalho

#IP_MODEM = "192.168.33.61"
IP_MODEM = "192.168.15.1"
NUM_MAX_FALHAS = 10
TEMPO_ENTRE_TESTES = 0.01  # tempo em minutos para cada teste

# Função para registrar no log
def log_message(message):
    current_time = datetime.datetime.now()
    log_message = f"{message} na data {current_time.strftime('%d/%m/%Y')} às {current_time.strftime('%H:%M')}\n"
    with open("ping_log.txt", "a") as file:
        file.write(log_message)

def check_ping():
    global num_failures, previous_state

    # Comando ping
    ping_command = ["ping", "-c", "4", IP_MODEM]

    # Executar o comando ping
    process = subprocess.Popen(
        ping_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    output, error = process.communicate()

    # Verificar se o ping foi bem-sucedido
    if process.returncode == 0:
        print("O modem está respondendo ao ping.")
        if previous_state == "disconnected":
            log_message("Conexão reestabelecida")
        previous_state = "connected"
        num_failures = 0  # Resetar o contador de falhas
    else:
        print("O modem NÃO está respondendo ao ping.")
        log_message("Falha de ping")  # Registrar cada falha de ping
        previous_state = "disconnected"
        num_failures += 1  # Incrementar o contador de falhas

        # Se o número de falhas for igual ao máximo de tentativas, executar o shutdown
        if num_failures == NUM_MAX_FALHAS:
            print("Máximo de falhas consecutivas de ping atingido. Executando shutdown...")
            log_message("Servidor desligado devido ao máximo de falhas de ping")

            from run import enviar_mensagem

            mensagem = "Servidor desligando devido ao máximo de falhas de ping"

            with open('/home/abs/Aplicativos/leitura_ults/numeros.txt', 'r') as arquivo:
                linhas = arquivo.readlines()

            for linha in linhas:
                numero = str(linha.strip())
                numero = numero + '@c.us'
                enviar_mensagem(numero, mensagem)

            os.system('''sudo sh -c "sudo shutdown -h now"''')  # Comando para desligar o PC
            #Envio de mensagens para o whatsapp
            

# Agendar a execução da função check_ping a cada 1 minuto
schedule.every(TEMPO_ENTRE_TESTES).minutes.do(check_ping)

# Loop principal para manter o programa em execução
while True:
    schedule.run_pending()
    time.sleep(1)
