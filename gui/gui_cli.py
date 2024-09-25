import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from tkinter import Tk, StringVar, Listbox, Scrollbar, Entry, SE
from tkinter.font import Font
from tkinter.ttk import Style, Label, Button
from random import randint

from models.i_agenda import IAgenda

TELA_NORMAL = "400x305"

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
    self.janela.geometry(TELA_NORMAL)
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
