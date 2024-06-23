import socket
import json
import sys
import struct

def cliente(user_name):
  # Dados do usuário em formato de dicionário
  usuario = {
    "user": None,
    "data": None
  }

  # Coletar dados do usuário
  usuario["user"] = user_name

  # Configurações do servidor
  SERVER_IP = '224.3.29.71'
  SERVER_PORT = 5007

  # Criar socket
  cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

  ttl = struct.pack('b', 1)

  # Conectar ao servidor
  cliente_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

  # Enviar JSON
  while usuario["data"] != "sair":
    usuario["data"] = input("Digite a mensagem: ")

    # Converter dicionário para JSON
    usuario_json = json.dumps(usuario)
    cliente_socket.sendto(usuario_json.encode('utf-8'), (SERVER_IP, SERVER_PORT))

  # Fechar o socket do cliente
  cliente_socket.close()

def servidor():
  # Configurações do servidor
  MULTICAST_GROUP = '224.3.29.71'
  MULTICAST_PORT = 5007

  # Criar socket
  servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
  servidor_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

  # Vincular o socket ao endereço e porta
  servidor_socket.bind(('', MULTICAST_PORT))

  # Group multicast
  group = socket.inet_aton(MULTICAST_GROUP)
  mreq = struct.pack('4sL', group, socket.INADDR_ANY)
  servidor_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

  # Receber dados JSON
  mensagem = ""
  while mensagem != "sair":
    print("Aguardando mensagem...")
    data, _ = servidor_socket.recvfrom(1024)
    dados_json = data.decode("utf-8")
    dados = json.loads(dados_json)
    # Exibir dados recebidos
    print("Dados recebidos:")
    print(f"Mensagem de {dados['user']}. Mensagem: {dados['data']}.")
    mensagem = dados["data"]

  # Fechar a conexão
  servidor_socket.close()


if __name__ == '__main__':
  user_type = sys.argv[1]

  if user_type == 'servidor':
    servidor()
  elif user_type == 'cliente':
    user_name = sys.argv[2]
    cliente(user_name)
  else:
    print("Tipo de usuário inválido. Use 'servidor' ou 'cliente'.")