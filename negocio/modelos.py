from abc import ABC, abstractmethod

# --- ACOMODAÇÕES (OCP) ---
class QuartoBase(ABC):
    @abstractmethod
    def calcular_diaria(self) -> float:
        pass
    @abstractmethod
    def exibir_detalhes(self) -> str:
        pass

class QuartoStandard(QuartoBase):
    def calcular_diaria(self) -> float: return 150.00
    def exibir_detalhes(self): return "Quarto Standard: Cama casal, wi-fi e TV"

class QuartoVIP(QuartoBase):
    def calcular_diaria(self) -> float: return 200.00
    def exibir_detalhes(self): return "Quarto VIP: Cama King, banheira, piscina aquecida."

class QuartoPresidencial(QuartoBase):
    def calcular_diaria(self) -> float: return 300.00
    def exibir_detalhes(self): return "Quarto Presidencial: Cobertura, frigobar livre, vista."

# --- SERVIÇOS ADICIONAIS (OCP) ---
class ServicoBase(ABC):
    @abstractmethod
    def calcular_servico(self) -> float:
        pass

class Frigobar(ServicoBase):
    def calcular_servico(self) -> float: return 50.00

class Spa(ServicoBase):
    def calcular_servico(self) -> float: return 150.00

class Lavanderia(ServicoBase):
    def calcular_servico(self) -> float: return 80.00

# --- ENTIDADE PRINCIPAL ---
class Reserva:
    def __init__(self, hospede: str, quarto: QuartoBase, dias: int):
        self.hospede = hospede
        self.quarto = quarto
        self.dias = dias
        self.servicos = []

    def adicionar_servico(self, servico: ServicoBase):
        self.servicos.append(servico)