from gui.gui_cli import GuiCliente
from cli.cli import agendasCli

def inicializaCliente():
  cliente = GuiCliente(agendasCli)
  cliente.iniciaAplicacao()

if __name__ == "__main__":
  inicializaCliente()