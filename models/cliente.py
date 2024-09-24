import Pyro4
from models.i_agenda import IAgenda

class Cliente:
  def __init__(self, nome: str) -> None:
    self.nome = nome
    self.agendas: dict[str, IAgenda] = {}
    self.agendaAtual: str = ""

  def inicializaCliente(self) -> None:
    for i in range(3):
      nomeAgenda = f"agenda{i+1}"
      uri = f"PYRONAME:{nomeAgenda}"
      self.agendas[nomeAgenda] = Pyro4.Proxy(uri)

  def adicionarContato(self, novoAmigo: str):
    topico = f"{self.nome}/{novoAmigo}"
    self.client.subscribe(topico)

  def excluirContato(self, novoAmigo: str):
    self.client.unsubscribe(f"{self.nome}/{novoAmigo}")

  def atualizarContato(self, novoAmigo: str):
    self.client.unsubscribe(f"{self.nome}/{novoAmigo}")


