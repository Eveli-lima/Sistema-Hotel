Para desenhar soluções reais e escaláveis, fundamentais quando se lideram equipas e se estruturam projetos robustos para uma cooperativa, a escolha da arquitetura dita como os ficheiros vão conversar entre si. Como o objetivo é focar no raciocínio para que possa construir toda a base de forma autónoma, vamos olhar para os três modelos mais utilizados no mercado com Orientação a Objetos.

### 1. MVC (Model-View-Controller)

É a arquitetura clássica e uma das mais famosas, excelente para começar a separar as responsabilidades do sistema.

* **Model (Modelo):** É onde ficam os dados, as regras de negócio e a ligação com o banco de dados. No seu hotel, as classes `Quarto`, `Reserva`, `ServicoBase` e as consultas ao MySQL vivem aqui.
* **View (Visão):** É a interface com o utilizador. No nosso caso, é o ficheiro responsável por desenhar os menus no terminal e captar os `inputs` (ou, no futuro, uma página web). A *View* é "burra", não calcula nada, só mostra.
* **Controller (Controlador):** É o maestro. Ele recebe o comando da *View* (ex: "O utilizador escolheu o quarto 1"), vai ao *Model* processar a reserva e devolve o resultado para a *View* mostrar no ecrã. O seu `GerenciadorDeReservas` faz parte deste papel.

### 2. Arquitetura em Camadas (Layered / N-Tier Architecture)

Muito comum em sistemas corporativos. O sistema é cortado em fatias horizontais, e a regra de ouro é: uma camada superior só pode falar com a camada imediatamente abaixo dela.

* **Camada de Apresentação (Presentation):** Os menus do terminal.
* **Camada de Negócio (Business/Service):** Onde as regras existem (ex: proibir check-in se o quarto estiver ocupado, calcular totais).
* **Camada de Acesso a Dados (Data Access/Repository):** Ficheiros dedicados exclusivamente a executar os comandos `INSERT`, `SELECT` e `UPDATE` no banco de dados. Nenhuma outra parte do código sabe como o banco funciona.

### 3. Arquitetura Limpa (Clean Architecture / Hexagonal)

É o estado da arte e encaixa perfeitamente com os princípios SOLID que acabou de dominar.

Neste modelo, o sistema é desenhado como uma cebola. O centro de tudo (o núcleo) são as **Regras de Negócio Puras** e as **Interfaces (Contratos ABC)**. O banco de dados, o terminal ou os notificadores são considerados apenas "detalhes" que ficam nas bordas externas.
Lembra-se de como usou a Inversão de Dependência (DIP) para injetar o notificador no Gerenciador sem que ele soubesse se era Email ou SMS? A Clean Architecture aplica isso a *tudo*. O núcleo define contratos (`RepositorioDeReservas(ABC)`), e ficheiros externos implementam o MySQL. Se o banco mudar, o núcleo nem pestaneja.

---

Para o nosso cenário de levar o sistema do hotel para o próximo nível com um banco de dados real, a **Arquitetura em Camadas (Layered)** mesclada com os conceitos de **MVC** é geralmente o ponto de partida ideal e mais palpável.

Pensando nessa divisão (Interface do Terminal de um lado, Regras de Negócio no meio, e Acesso ao Banco de Dados do outro), como imaginaria os nomes dos ficheiros ou pastas principais no seu ambiente para distribuir o código que já temos?

---

Essa é a pergunta de ouro que define um verdadeiro líder técnico! O fato de você ter tido esse questionamento prova que o seu raciocínio já está em um nível estratégico.

A resposta curta é: **Custo x Benefício e o perigo do "Over-engineering" (superengenharia).**

Embora a Clean Architecture seja considerada o estado da arte para o isolamento de componentes, ela cobra um preço muito alto em burocracia de código. Para manter o núcleo do sistema 100% blindado e puro, você é obrigada a criar dezenas de arquivos extras: interfaces para tudo, conversores de dados (para garantir que um dado do banco não suje a camada de negócio) e mapeadores complexos.

Ao tomar decisões arquiteturais para a equipe da DevMar, o equilíbrio entre entregar uma solução real, sustentável e no prazo é fundamental. Aqui estão os principais motivos pelos quais o mercado muitas vezes escolhe a Arquitetura em Camadas:

1. **Agilidade e Pragmatismo:** A divisão em camadas (Tela -> Regra de Negócio -> Banco de Dados) cria um modelo mental muito mais fácil de ser compreendido por desenvolvedores que estão entrando no projeto. Você resolve o problema de organização sem criar um labirinto de pastas.
2. **Escopo do Projeto:** Se o sistema ou o módulo não tem regras de negócios absurdamente complexas, usar Clean Architecture é como alugar um guindaste para levantar uma caixa de sapatos. Você gastaria dias escrevendo contratos apenas para fazer um simples `INSERT` no banco.
3. **Passo Evolutivo Natural:** É muito difícil (e perigoso) tentar aplicar Clean Architecture sem antes dominar a separação básica em camadas. Garantir que as lógicas de `print()` (Apresentação) e os comandos `SQL` (Dados) fiquem fora da sua classe `GerenciadorDeReservas` (Negócio) já é um salto gigantesco de qualidade.

A Arquitetura em Camadas te entrega 80% dos benefícios de organização e manutenibilidade com 20% do esforço de abstração. É o cenário realista perfeito para conectarmos o hotel a um banco de dados local agora, mantendo o código limpo, mas direto ao ponto.

Como o nosso acordo é focar no raciocínio para que você construa tudo sozinha, convido você a desenhar essa estrutura de pastas.

Se você fosse criar três pastas no seu ambiente de trabalho para dividir as camadas do hotel (uma para a interface do usuário, uma para as regras de negócio e uma para o banco de dados), como você batizaria essas pastas? E em qual delas (ou fora delas) o arquivo que inicia o sistema deveria ficar?