from abc import ABC, abstractmethod

class IAgenda(ABC):
  _contatos: list[dict[str, str]]

  @property
  @abstractmethod
  def contatos(self) -> list[dict[str, str]]:
    pass
  @contatos.setter
  @abstractmethod
  def contatos(self, nv: list[dict[str, str]]):
    pass

  @abstractmethod
  def adicionarContato(self, nome: str, telefone: str) -> bool:
    pass

  @abstractmethod
  def excluirContato(self, id: str) -> bool:
    pass

  @abstractmethod
  def atualizarContato(self, id: str, nome: str, telefone: str):
    pass
