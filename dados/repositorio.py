from abc import ABC, abstractmethod

class RepositorioReservas(ABC):
    @abstractmethod
    def salvar(self, codigo: str, reserva):
        pass

    @abstractmethod
    def buscar(self, codigo: str):
        pass

    @abstractmethod
    def remover(self, codigo: str):
        pass

class BancoEmMemoria(RepositorioReservas):
    def __init__(self):
        self.tabela_reservas = {}

    def salvar(self, codigo: str, reserva):
        self.tabela_reservas[codigo] = reserva

    def buscar(self, codigo: str):
        return self.tabela_reservas.get(codigo)

    def remover(self, codigo: str):
        if codigo in self.tabela_reservas:
            del self.tabela_reservas[codigo]