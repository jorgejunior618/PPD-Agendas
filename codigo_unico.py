# models/i_agenda.py
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

# models/agenda.py
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

# cli/cli.py

agendasCli: dict[str, IAgenda] = {}
for i in range(3):
  nomeAgenda = f"agenda{i+1}"
  uri = f"PYRONAME:{nomeAgenda}"
  agendasCli[nomeAgenda] = Pyro4.Proxy(uri)

# gui/gui_agenda.py

from tkinter import Tk, BooleanVar, Checkbutton
from tkinter.font import Font
from tkinter.ttk import Style, Label
from typing import Callable

TELA_AGENDA = "370x90"

class GuiAgenda:
  def __init__(
    self,
    desconectarAgenda1: Callable,
    conectarAgenda1: Callable,
    desconectarAgenda2: Callable,
    conectarAgenda2: Callable,
    desconectarAgenda3: Callable,
    conectarAgenda3: Callable
  ):
    self.desconectarAgenda1 = desconectarAgenda1
    self.conectarAgenda1 = conectarAgenda1
    self.desconectarAgenda2 = desconectarAgenda2
    self.conectarAgenda2 = conectarAgenda2
    self.desconectarAgenda3 = desconectarAgenda3
    self.conectarAgenda3 = conectarAgenda3

  def criaComponenteJanela(self):
    self.janela = Tk()
    self.janela.title(f"Minha Agenda ☏")
    self.janela.geometry(TELA_AGENDA)
    self.janela.resizable(False, False)

  def isntanciarEstilos(self):
    self.fonteGeral = Font(size=12, family="Trebuchet MS")
    self.fonteLeitura = Font(size=9, family="Trebuchet MS")

    style = Style()
    style.configure("Err.Label", font=self.fonteGeral, foreground="#F02424")
    style.configure("Info.Label", font=self.fonteGeral, foreground="#24F024")

  def criaComponentesOnline(self):
    self.varOnline1 = BooleanVar(value=True)
    self.varOnline2 = BooleanVar(value=True)
    self.varOnline3 = BooleanVar(value=True)

    def toggleCheckbox(agenda: int):
      def func():
        if agenda == 1:
          online = self.varOnline1.get()
          if not online:
            self.desconectarAgenda1()
            self.lblStatus1.configure(text="Agenda 1 offline", style="Err.Label")
          else:
            self.conectarAgenda1()
            self.lblStatus1.configure(text="Agenda Agenda 1 está online", style="Info.Label")
        elif agenda == 2:
          online = self.varOnline2.get()
          if not online:
            self.desconectarAgenda2()
            self.lblStatus2.configure(text="Agenda 2 offline", style="Err.Label")
          else:
            self.conectarAgenda2()
            self.lblStatus2.configure(text="Agenda Agenda 2 está online", style="Info.Label")
        elif agenda == 3:
          online = self.varOnline3.get()
          if not online:
            self.desconectarAgenda3()
            self.lblStatus3.configure(text="Agenda 3 offline", style="Err.Label")
          else:
            self.conectarAgenda3()
            self.lblStatus3.configure(text="Agenda Agenda 3 está online", style="Info.Label")

      return func

    self.lblStatus1 = Label(self.janela,text=f"Agenda Agenda 1 está online",style="Info.Label")
    self.chkbtnOnline1 = Checkbutton(
      self.janela,
      text="Online",
      variable=self.varOnline1,
      onvalue=True,
      offvalue=False,
      command=toggleCheckbox(1)
    )
    self.lblStatus2 = Label(self.janela,text=f"Agenda Agenda 2 está online",style="Info.Label")
    self.chkbtnOnline2 = Checkbutton(
      self.janela,
      text="Online",
      variable=self.varOnline2,
      onvalue=True,
      offvalue=False,
      command=toggleCheckbox(2)
    )
    self.lblStatus3 = Label(self.janela,text=f"Agenda Agenda 3 está online",style="Info.Label")
    self.chkbtnOnline3 = Checkbutton(
      self.janela,
      text="Online",
      variable=self.varOnline3,
      onvalue=True,
      offvalue=False,
      command=toggleCheckbox(3)
    )

    self.chkbtnOnline1.place(x=30, y=5)
    self.lblStatus1.place(x=110, y=5)
    self.chkbtnOnline2.place(x=30, y=35)
    self.lblStatus2.place(x=110, y=35)
    self.chkbtnOnline3.place(x=30, y=65)
    self.lblStatus3.place(x=110, y=65)

  def iniciaAplicacao(self):
    self.criaComponenteJanela()
    self.isntanciarEstilos()
    self.criaComponentesOnline()

    self.janela.mainloop()

# gui/gui_cli.py

from tkinter import StringVar, Listbox, Scrollbar, Entry, SE
from tkinter.ttk import Button
from random import randint

TELA_GUI_CLI = "400x305"

class GuiCliente:
  def __init__(self, agendasCli: dict[str, IAgenda]):
    self.agendas = [ag for ag in agendasCli]
    self.agendaConectada = randint(0, 2)
    self.cliAgenda = agendasCli[self.agendas[self.agendaConectada]]
    self.contatoAtual = -1
    self.contatos = []
    self.agendasCli = agendasCli
  
  def criaComponenteJanela(self):
    self.janela = Tk()
    self.janela.title(f"Minha Agenda ☏")
    self.janela.geometry(TELA_GUI_CLI)
    self.janela.resizable(False, False)

  def instanciarEstilos(self):
    self.fonteGeral = Font(size=12, family="Trebuchet MS")
    self.fonteLeitura = Font(size=9, family="Trebuchet MS")

    style = Style()
    style.configure("Gen.Label", font=self.fonteGeral, foreground="#000000")
    style.configure("Err.Label", font=self.fonteLeitura, foreground="#F02424")
    style.configure("Info.Label", font=self.fonteLeitura, foreground="#000000")
    style.configure("Agenda.Label", font=self.fonteLeitura, foreground="#2424F0")
    style.configure("Btn.TButton", width=8, font=self.fonteGeral)
    style.configure("Add.TButton", width=10, font=self.fonteGeral)
    style.configure("Save.TButton", width=15, font=self.fonteGeral)
    style.configure("Del.TButton", width=15, font=self.fonteGeral, background="#F02424")

  def criaComponentesContatos(self):
    self.varContatos = StringVar(value=[f"{ctt["nome"]} - {ctt["telefone"]}" for ctt in self.contatos])
    self.varIDContato = StringVar(value="")
    self.varNomeContato = StringVar(value="")
    self.varTelefoneContato = StringVar(value="")

    yscrollbar = Scrollbar(self.janela)
    self.lblContatos = Label(self.janela,text="Seus contatos",style="Gen.Label")
    self.lblErroSave = Label(self.janela,text="",style="Err.Label")
    self.lblInfoAgenda = Label(self.janela,text=f"Conectado: Agenda {self.agendaConectada + 1}",style="Agenda.Label")
    self.lblNomeContato = Label(self.janela,text="Nome",style="Info.Label")
    self.lblTelefoneContato = Label(self.janela,text="Telefone",style="Info.Label")
    self.lbxContatos = Listbox(
      self.janela,
      selectmode="multiple",
      width=34,
      height=11,
      font=self.fonteLeitura,
      yscrollcommand=yscrollbar.set,
      listvariable=self.varContatos, 
    )
    self.btnAtualizarContatos = Button(self.janela, text="Atualizar", command=lambda : self.atualizarContatos(), style="Btn.TButton")
    self.btnNovoContato = Button(self.janela, text="Adicionar", command=lambda : self.iniciarCriacao(), style="Add.TButton")
    self.btnSalvarContato = Button(self.janela, state="disabled", text="Salvar", command=lambda : self.criarContato(), style="Save.TButton")
    self.btnExcluirContato = Button(self.janela, state="disabled", text="Excluir", command=lambda : self.excluirContato(), style="Del.TButton")
    self.inputNome = Entry(self.janela, state="readonly", textvariable=self.varNomeContato, width=16, font=self.fonteGeral)
    self.inputTelefone = Entry(self.janela, state="readonly", textvariable=self.varTelefoneContato, width=16, font=self.fonteGeral)

    self.lblContatos.place(x=30, y=10)
    self.lbxContatos.place(x=30, y=45)
    self.btnAtualizarContatos.place(x=163, y=5)
    self.btnNovoContato.place(x=30, y=265)
    self.lblInfoAgenda.place(x=390, y=300, anchor=SE)

    self.lblErroSave.place(x=250, y=20)
    self.lblNomeContato.place(x=250, y=45)
    self.inputNome.place(x=250, y=62)
    self.lblTelefoneContato.place(x=250, y=95)
    self.inputTelefone.place(x=250, y=112)
    self.btnSalvarContato.place(x=250, y=145)
    self.btnExcluirContato.place(x=250, y=180)

    self.lbxContatos.bind('<<ListboxSelect>>', lambda _: self.onselectContato())

  def iniciarCriacao(self):
    self.varIDContato.set(value="")
    self.varNomeContato.set(value="")
    self.varTelefoneContato.set(value="")
    self.inputNome.configure(state="normal")
    self.inputTelefone.configure(state="normal")
    self.lbxContatos.selection_clear(0, len(self.contatos) - 1)
    self.btnSalvarContato.configure(state="normal")
    self.btnExcluirContato.configure(state="disabled")

  def onselectContato(self):
    try:
      selecionados: list[int] = list(self.lbxContatos.curselection())
      if len(selecionados) == 0: self.contatoAtual = -1
      elif len(selecionados) == 1: self.contatoAtual = selecionados[0]
      else:
        selecionados.remove(self.contatoAtual)
        self.lbxContatos.selection_clear(self.contatoAtual, self.contatoAtual)
        self.lbxContatos.selection_set(selecionados[0], selecionados[0])
        self.contatoAtual = selecionados[0]

      if self.contatoAtual == -1:
        self.varIDContato.set(value="")
        self.varNomeContato.set(value="")
        self.varTelefoneContato.set(value="")
        self.inputNome.configure(state="readonly")
        self.inputTelefone.configure(state="readonly")
        self.btnSalvarContato.configure(state="disabled")
        self.btnExcluirContato.configure(state="disabled")
      else:
        self.varIDContato.set(value=self.contatos[self.contatoAtual]["id"])
        self.varNomeContato.set(value=self.contatos[self.contatoAtual]["nome"])
        self.varTelefoneContato.set(value=self.contatos[self.contatoAtual]["telefone"])
        self.inputNome.configure(state="normal")
        self.inputTelefone.configure(state="normal")
        self.btnSalvarContato.configure(state="normal")
        self.btnExcluirContato.configure(state="normal")

    except Exception as e:
      print(f"ERRO onselect: {e}")
      return False

  def conectaNovaAgenda(self):
    self.lblInfoAgenda.configure(text="Tentando reconectar")
    novaConexao = randint(0, 2)
    while novaConexao == self.agendaConectada:
      novaConexao = randint(0, 2)

    try:
      self.agendasCli[self.agendas[novaConexao]].contatos
    except:
      novaConexao = 3 - (novaConexao + self.agendaConectada)
    
    self.cliAgenda = self.agendasCli[self.agendas[novaConexao]]
    self.agendaConectada = 0 + novaConexao # evitando erros de ponteiro

    self.lblInfoAgenda.configure(text=f"Conectado: Agenda {self.agendaConectada + 1}")

  def atualizarContatos(self):
    try:
      self.contatos = self.cliAgenda.contatos
    except:
      self.conectaNovaAgenda()
      self.contatos = self.cliAgenda.contatos
    self.varContatos.set(value=[f"{ctt["nome"]} - {ctt["telefone"]}" for ctt in self.contatos])

  def criarContato(self):
    idContato = self.varIDContato.get()
    nomeContato = self.varNomeContato.get()
    telefoneContato = self.varTelefoneContato.get()

    if len(nomeContato) < 2:
      self.lblErroSave.configure(text="Nome inválido")
      return
    if len(telefoneContato) > 11 or len(telefoneContato) < 8 or not telefoneContato.isnumeric():
      self.lblErroSave.configure(text="Telefone inválido")
      return

    try:
      ok = False
      if len(idContato) > 0:
        ok = self.cliAgenda.atualizarContato(idContato, nomeContato, telefoneContato)
      else:
        ok = self.cliAgenda.adicionarContato(nomeContato, telefoneContato)
      
      if not ok:
        self.lblErroSave.configure(text="Nome ja utilizado")
        return

    except:
      self.conectaNovaAgenda()
      ok = False
      if len(idContato) > 0:
        ok = self.cliAgenda.atualizarContato(idContato, nomeContato, telefoneContato)
      else:
        ok = self.cliAgenda.adicionarContato(nomeContato, telefoneContato)

      if not ok:
        self.lblErroSave.configure(text="Nome ja utilizado")
        return

    self.atualizarContatos()
    self.lbxContatos.selection_clear(0, len(self.contatos) - 1)

    idContato = self.varIDContato.set(value="")
    nomeContato = self.varNomeContato.set(value="")
    telefoneContato = self.varTelefoneContato.set(value="")

    self.btnSalvarContato.configure(state="disabled")
    self.btnExcluirContato.configure(state="disabled")

    self.inputNome.configure(state="readonly")
    self.inputTelefone.configure(state="readonly")
    self.lblErroSave.configure(text="")

  def excluirContato(self):
    idContato = self.varIDContato.get()

    try:
      self.cliAgenda.excluirContato(idContato)

    except:
      self.conectaNovaAgenda()
      self.cliAgenda.excluirContato(idContato)

    self.atualizarContatos()
    self.lbxContatos.selection_clear(0, len(self.contatos) - 1)

    idContato = self.varIDContato.set(value="")
    nomeContato = self.varNomeContato.set(value="")
    telefoneContato = self.varTelefoneContato.set(value="")

    self.btnSalvarContato.configure(state="disabled")
    self.btnExcluirContato.configure(state="disabled")

    self.inputNome.configure(state="readonly")
    self.inputTelefone.configure(state="readonly")
    self.lblErroSave.configure(text="")

  def iniciaAplicacao(self):
    self.criaComponenteJanela()
    self.instanciarEstilos()
    self.criaComponentesContatos()
    self.atualizarContatos()

    self.janela.mainloop()

# inicializa_servidor.py

import Pyro4.naming
from threading import Thread

def inicializaServidor():
  daemon = Pyro4.Daemon()
  ns = Pyro4.locateNS()

  agendasServer: dict[str, Agenda] = {
    "agenda1": Agenda(),
    "agenda2": Agenda(),
    "agenda3": Agenda(),
  }
  agendasServer["agenda1"].defineCopias(agendasServer["agenda2"],agendasServer["agenda3"])
  agendasServer["agenda2"].defineCopias(agendasServer["agenda1"],agendasServer["agenda3"])
  agendasServer["agenda3"].defineCopias(agendasServer["agenda1"],agendasServer["agenda2"])
  
  uri1 = daemon.register(agendasServer["agenda1"])
  uri2 = daemon.register(agendasServer["agenda2"])
  uri3 = daemon.register(agendasServer["agenda3"])
  
  ns.register("agenda1", uri1)
  ns.register("agenda2", uri2)
  ns.register("agenda3", uri3)

  def desconectaAgenda(nome: str):
    def func():
      agendasServer[nome].online = False

    return func

  def conectaAgenda(nome: str):
    def func():
      agendasServer[nome].online = True

    return func

  guiAgendas = GuiAgenda(
    desconectarAgenda1=desconectaAgenda("agenda1"),
    conectarAgenda1=conectaAgenda("agenda1"),
    desconectarAgenda2=desconectaAgenda("agenda2"),
    conectarAgenda2=conectaAgenda("agenda2"),
    desconectarAgenda3=desconectaAgenda("agenda3"),
    conectarAgenda3=conectaAgenda("agenda3")
  )
  thread_agendas = Thread(target=guiAgendas.iniciaAplicacao, daemon=True)
  thread_agendas.start()

  print("Agenda pronta.")
  daemon.requestLoop()

# if __name__ == "__main__":
#   inicializaServidor()

# index.py

def inicializaCliente():
  cliente = GuiCliente(agendasCli)
  cliente.iniciaAplicacao()

if __name__ == "__main__":
  inicializaCliente()
