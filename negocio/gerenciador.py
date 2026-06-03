from abc import ABC, abstractmethod
from negocio.modelos import Reserva
from dados.repositorio import RepositorioReservas

class Notificador(ABC):
    @abstractmethod
    def enviar(self, mensagem: str):
        pass

class NotificadorEmail(Notificador):
    def enviar(self, mensagem: str):
        print(f"[EMAIL ENVIADO]: {mensagem}")

class GerenciadorDeReservas:
    def __init__(self, repositorio: RepositorioReservas, notificador: Notificador):
        self.repositorio = repositorio
        self.notificador = notificador
        self.contador_id = 1000  # Gerador simples de códigos

    def gerar_extrato(self, reserva: Reserva) -> str:
        """Cria o texto formatado detalhando os custos da reserva."""
        linhas = []
        linhas.append(f"--- EXTRATO DETALHADO ---")
        
        valor_diarias = reserva.quarto.calcular_diaria() * reserva.dias
        linhas.append(f"Diárias ({reserva.dias}x R$ {reserva.quarto.calcular_diaria():.2f}): R$ {valor_diarias:.2f}")
        
        if reserva.servicos:
            linhas.append("Serviços Consumidos:")
            for servico in reserva.servicos:
                # O macete abaixo pega o nome exato da classe (ex: 'Spa' ou 'Frigobar')
                nome_servico = servico.__class__.__name__ 
                valor_servico = servico.calcular_servico()
                linhas.append(f"  - {nome_servico}: R$ {valor_servico:.2f}")
        
        total = self.calcular_total(reserva)
        linhas.append(f"-------------------------")
        linhas.append(f"TOTAL GERAL: R$ {total:.2f}")
        
        return "\n".join(linhas)

    def realizar_checkin(self, reserva: Reserva) -> str:
        codigo = f"RES-{self.contador_id}"
        self.contador_id += 1
        
        self.repositorio.salvar(codigo, reserva)

        extrato = self.gerar_extrato(reserva)

        self.notificador.enviar(f"Olá {reserva.hospede}, sua reserva {codigo} foi confirmada!\n{extrato}")
        return codigo

    def registrar_consumo(self, codigo: str, servico) -> bool:
        reserva = self.repositorio.buscar(codigo)
        if reserva:
            reserva.adicionar_servico(servico)
            self.repositorio.salvar(codigo, reserva)
            return True
        return False

    def calcular_total(self, reserva: Reserva) -> float:
        total = reserva.quarto.calcular_diaria() * reserva.dias
        for servico in reserva.servicos:
            total += servico.calcular_servico()
        return total

    def realizar_checkout(self, codigo: str) -> dict:
        reserva = self.repositorio.buscar(codigo)
        if not reserva:
            return None
        
        extrato = self.gerar_extrato(reserva)
        self.repositorio.remover(codigo)
        
        self.notificador.enviar(f"Obrigado por se hospedar, {reserva.hospede}! Volte sempre.\n{extrato}")
        
        return extrato