import Pyro4

class Agenda:
  def __init__(self) -> None:
    self._contatos: list[dict[str, str]] = []
    self._copia1: Agenda = None
    self._copia2: Agenda = None
    self.ultimoID = 0
    self.online = True

  def defineCopias(self, copia1: "Agenda", copia2: "Agenda"):
    self._copia1 = copia1
    self._copia2 = copia2

    # Sincronizando contatos
    if (copia1.ultimoID == copia2.ultimoID == self.ultimoID):
      return True
    
    if (copia1.ultimoID > copia2.ultimoID):
      copia2._contatos = copia1._contatos
      copia2.ultimoID = copia1.ultimoID
      self._contatos = copia1._contatos
      self.ultimoID = copia1.ultimoID
    else:
      copia1._contatos = copia2._contatos
      copia1.ultimoID = copia2.ultimoID
      self._contatos = copia2._contatos
      self.ultimoID = copia2.ultimoID

  def redefineUltimoID(self, id: int):
    self.ultimoID = id
    self._copia1.ultimoID = id
    self._copia2.ultimoID = id

  @property
  @Pyro4.expose
  def contatos(self) -> list[dict[str, str]]:
    if not self.online: raise Exception("Servidor Offline")
    return self._contatos

  @contatos.setter
  def contatos(self, nv: list[dict[str, str]]):
    if not self.online: raise Exception("Servidor Offline")
    self._contatos = nv

  @Pyro4.expose
  def adicionarContato(self, nome: str, telefone: str) -> bool:
    if not self.online: raise Exception("Servidor Offline")
    if len(list(filter(lambda ctt: ctt['nome'] == nome, self._contatos))) > 0:
      return False
    novoContato = {
      "id": f"{self.ultimoID + 1}",
      "nome": nome,
      "telefone": telefone,
    }
    novaLista = [ctt for ctt in self.contatos]
    novaLista.append(novoContato)

    self.contatos = novaLista
    self._copia1._contatos = novaLista
    self._copia2._contatos = novaLista
    self.redefineUltimoID(self.ultimoID+1)

    return True

  @Pyro4.expose
  def excluirContato(self, id: str) -> bool:
    if not self.online: raise Exception("Servidor Offline")
    novaLista = list(filter(lambda ctt: ctt['id'] != id, self._contatos))
    if len(novaLista) == len(self._contatos):
      return False

    self.contatos = novaLista
    self._copia1._contatos = novaLista
    self._copia2._contatos = novaLista

    return True

  @Pyro4.expose
  def atualizarContato(self, id: str, nome: str = None, telefone: str = None):
    if not self.online: raise Exception("Servidor Offline")
    indexContato = -1
    jaExiste = False
    novaLista = self._contatos

    for i in range(len(novaLista)):
      if novaLista[i]["id"] == id:
        indexContato = i
      elif novaLista[i]["nome"] == nome:
        jaExiste = True
    if indexContato == -1:
      return False
    if (jaExiste):
      return False
    
    novaLista[indexContato] = {
      "id": novaLista[indexContato]["id"],
      "nome": nome if nome != None else novaLista[indexContato]["nome"],
      "telefone": telefone if telefone != None else novaLista[indexContato]["telefone"],
    }

    self.contatos = novaLista
    self._copia1._contatos = novaLista
    self._copia2._contatos = novaLista

    return True
