import Pyro4
import Pyro4.naming
from models.agenda import Agenda
from gui.gui_agenda import GuiAgenda
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

if __name__ == "__main__":
  inicializaServidor()