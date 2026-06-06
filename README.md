# 🏨 Hotel da Serra - Sistema de Gestão (ERP)

Um sistema de gerenciamento de reservas e hotelaria desenvolvido em Python, com foco prático em **Programação Orientada a Objetos (POO)** e na aplicação de **Princípios SOLID**. 

Este projeto simula o fluxo completo de um hotel, desde o check-in até o check-out do hóspede, aplicando padrões arquiteturais de mercado para garantir que o código seja escalável, modular e de fácil manutenção.

## 📌 Funcionalidades

* **Check-in Dinâmico:** Cadastro de hóspedes e seleção de quartos com regras de negócios e diárias independentes.
* **Consumo e Serviços Extras:** Adição de serviços avulsos (como Frigobar, Spa, Lavanderia) à ficha do cliente de forma extensível, respeitando o Princípio do Aberto/Fechado (OCP).
* **Check-out e Extrato:** Cálculo automático de totais e geração de extratos detalhados com o fechamento da conta.
* **Persistência em Memória:** Simulação de um banco de dados utilizando injeção de dependência (DIP) e repositórios.
* **Interface ANSI no Terminal:** Interface de usuário limpa, colorida e estruturada para navegação amigável via CLI.

## 🛠️ Tecnologias e Arquitetura

O sistema não utiliza bibliotecas externas, dependendo exclusivamente dos recursos nativos do Python. A estrutura do código foi dividida utilizando o padrão de **Arquitetura em Camadas (Layered Architecture)**:

* `main.py`: Interface do usuário (CLI) e injeção das dependências.
* `negocio/`: Modelos de domínio (Quartos, Serviços, Reserva) e a regra de negócio (Gerenciador).
* `dados/`: Implementação do repositório em memória para armazenamento das reservas ativas.

### Princípios SOLID Aplicados
* **SRP (Princípio da Responsabilidade Única):** Separação clara entre quem guarda os dados (`Reserva`) e quem manipula os processos (`GerenciadorDeReservas`).
* **OCP (Princípio do Aberto/Fechado):** Acomodações e serviços extras são implementados via herança de interfaces (Classes Abstratas), permitindo a criação de novos quartos ou serviços sem alterar o núcleo do sistema.
* **DIP (Princípio da Inversão de Dependência):** O Gerenciador recebe instâncias prontas de `Notificador` e `Repositorio` através de injeção, sem depender de classes concretas.

## 🚀 Como Instalar e Executar

O projeto não exige instalação de pacotes via `pip` (não há `requirements.txt`). Para rodar no terminal do Ubuntu (ou qualquer outra distribuição Linux/MacOS/Windows), basta seguir os passos:

1. Clone o repositório ou baixe os arquivos do projeto.
2. Navegue até a pasta raiz do sistema (onde o arquivo `main.py` está localizado):
   ```bash
   cd caminho/para/a/pasta/hotel_sistema

    Execute o arquivo principal com o Python 3:
    Bash

    python3 main.py

👨‍💻 Autores

Desenvolvido por Éveli Lima e Otavio Crancio.
Projeto acadêmico para a disciplina de Laboratório de Programação Orientada a Objetos - Curso de Análise e Desenvolvimento de Sistemas (ADS) da Universidade Vassouras.


