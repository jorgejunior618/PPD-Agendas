import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from tkinter import Tk, BooleanVar, Checkbutton
from tkinter.font import Font
from tkinter.ttk import Style, Label
from typing import Callable

TELA_NORMAL = "370x90"

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
    self.janela.geometry(TELA_NORMAL)
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
