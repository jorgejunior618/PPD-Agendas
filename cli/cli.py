import Pyro4
from models.i_agenda import IAgenda

agendasCli: dict[str, IAgenda] = {}
for i in range(3):
  nomeAgenda = f"agenda{i+1}"
  uri = f"PYRONAME:{nomeAgenda}"
  agendasCli[nomeAgenda] = Pyro4.Proxy(uri)
  