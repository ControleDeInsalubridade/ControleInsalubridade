# Controle de pessoas

## Introdução

Este projeto possui o objetivo principal de verificar e auxiliar no gerenciamento do controle de acesso de colaboradores que atuam em funções operacionais as quais apresentam insalubridade controlada em um período específico.

Buscando atender a necessidade principal de segurança dos colaboradores e de manutenção das ações gerenciais da empresa contratante, foi pensado em um sistema que possa facilitar este processo. Considerando um cenário constituído de quatro bancadas de abatedouro de frango com utilização individual de colaborador, conforme demonstrado na Figura 1, faz-se necessário a identificação e armazenamento dos dados relativos ao período de permanência do colaborador em cada bancada.

![Simulação de cenário](/images/diagrama.png)

As ferramentas utilizadas para o desenvolvimento do projeto visam baixo custo, logo esta característica define uma etapa inicial de pesquisa de viabilidade financeira e adaptabilidade para o desenvolvimento. Assim sendo, as etapas principais para o desenvolvimento deste projeto constituem levantamento de requisitos, modelagem e implementação do banco de dados, implementação da interface, implementação java e demonstração dos dados através de consultas no banco.

## Análise técnica

### Descrição do ambiente técnico

O sistema é composto por um banco de dados relacional e uma interface web, com o propósito de oferecer para empresas que trabalhem com abatedouro de animais o controle e informação do acesso de funcionários a locais específicos. Assim, assegurando a empresa em questões legais. Possuirá acesso via interface web e irá armazenar em um banco de dados as informações resultantes dos requisitos estabelecidos por este documento. Para o desenvolvimento do módulo de verificação de presença será utilizado um componente detector de IR, possibilitando a detecção do funcionário.

As ferramentas utilizadas para o desenvolvimento incluem *Python 3.6* que é um interpretador orientado a objetos, para programação de alto nível, *PyCharm* que atua como ambiente de desenvolvimento integrado (IDE), *Mysql Workbench* atuando como sistema gerenciador de banco de dados relacional e *WampServer* atuando como ambiente de desenvolvimento web do Windows.

### Levantamento de requisitos  
Os requisitos foram demonstrados pelo professor Roberto de Matos, na disciplina de Sistemas embarcados e pelo professor Emerson de Mello da disciplina de Banco de dados.

### Requisitos Funcionais
Respeitando a proposta, o sistema deverá atender os seguintes requisitos:

* **RF1** - Cadastro de diversos funcionários.
* **RF2** - Permitir que o funcionário esteja presente em diferentes bancadas durante o período de trabalho.
* **RF3** - Identificar a presença do funcionário em cada bancada.
* **RF4** - Verificar a localização do funcionário considerando data e hora.
* **RF5** - Verificar entrada em sala específica.
* **RF6** - Informar funcionário que passaram o tempo trabalho.
* **RF7** - Permitir inserir novas bancadas em uma sala.
* **RF8** - Permitir inserir novas salas.
* **RF9** - Informar funcionário que passaram o tempo trabalho.
* **RF10** - Informar funcionário que já foram demitidos.
* **RF11** - Informar funcionário que trabalham atualmente.
* **RF12** - Informar dados de funcionário específico.

## Requisitos Não-Funcionais

* **RNF1** - Permitir o cadastro de novos funcionários somente pelo administrado do sistema.
* **RNF2** - O sistema será desenvolvido em ambiente web.
* **RNF3** - Analisar a eficiência do sistema em um cenário real.

## Regras de Negócio

1. **RGN1** - *Tempo de uso da bancada*

Um aviso deverá ser enviado para o administrador quando o tempo de 4 horas for ultrapassado por qualquer um dos funcionários.   

2. **RGN2** - *Uso da bancada*

O funcionário poderá trocar de bancada durante o período de uso determinado pela regra de negócio RGN1.

3. **RGN3** - *Login no sistema*

O administrador irá acessar o sistema com seu CPF e uma senha.

4. **RGN4** - *Acesso a salas e bancadas*

Todo funcionário que estiver em uma bancada estará em uma sala, mas nem todo funcionário que estiver em uma sala estará em uma bancada.

## Casos de Uso

1. **UC1** - *Primeiro login no sistema*

Ao entrar no sistema pela primeira vez o administrador deverá acessá-lo com os dados padrão, e criar seu login.
```
CPF: 000.000.000-00
senha: admin
```

***Visão do sistema***

O sistema mostrará uma tela com dois campos, um campo de CPF e um campo senha, na primeira vez que o administrador do sistema entrar, deverá utilizar o CPF e senha padrão. Após o primeiro login, entrará com seu CPF e sua senha e uma tela será mostrada com as opções do sistema : *Funcionário*,*Tempo de trabalho*,*Sala*,*Bancada*.

2. **UC2** - *Bancada identifica funcionário*

A bancada identificará o funcionário através de um sistema de controle com sensor IR e Raspberry Pi. Em um cenário real, a inclusão dos dados de identificação serão realizados no sistema embarcado, o qual certificará que o funcionário não poderá ser identificado em mais de uma bancada ao mesmo tempo e que estará registrado apenas em uma bancada onde esteja em trabalho atual, podendo estar presente em uma sala sem ser identificado em alguma bancada. Para demonstração da funcionalidade uma página será criada para a atualização dos dados da bancada.

***Visão do sistema***

O sistema mostrará as informações relacionadas a bancada, ao funcionário e sala. Como administrador será possível acessar um botão ( *Uso de bancada* ) na tela principal que possibilitará inserir informações de utilização de bancada para simular seu uso.


3. **UC3** - *Funcionário acessa sala*

A identificação de entrada do funcionário será realizada através de um sistema de controle com sensor IR e Raspberry Pi. Em um cenário real, a inclusão dos dados de identificação serão realizados no sistema embarcado. Para demonstração da funcionalidade uma página será criada para a atualização dos dados de acesso da sala.

***Visão do sistema***

O sistema mostrará as informações relacionadas a sala, ao funcionário e bancada. Como administrador será possível acessar um botão ( *Uso de sala* ) na tela principal que possibilitará inserir informações de utilização de sala para simular seu uso.

5. **UC4** - *Novo funcionário admitido*

O administrador deverá inserir um novo funcionário na plataforma, inserindo todas as informações requisitadas na interface web.

***Visão do sistema***

Ao acessar o sistema o administrador deverá clicar em *Funcionário*, uma nova tela será demonstrada com as opções: *Funcionário admitido*, *Funcionário demitido*, *Verificar Bancada* e *Verificar Sala*. Ao acessar a opção *Funcionário admitido* uma nova tela demonstrará a opção de inserir as informações de funcionário e o administrador irá preencher os dados e clicar no botão *Cadastrar*.

6. **UC5** - *Funcionário demitido*

O administrador deverá inserir a data de demissão do funcionário na plataforma, onde os dados continuarão mantidos para consultas futuras.

***Visão do sistema***

Ao acessar o sistema o administrador deverá clicar em *Funcionário*, uma nova tela será demonstrada com as opções: *Funcionário admitido*, *Funcionário demitido*, *Verificar Bancada* e *Verificar Sala*. Ao acessar a opção *Funcionário demitido* uma nova tela demonstrará a opção de inserir as informações de funcionário e o administrador irá preencher o campo *Data de demissão* e clicar no botão *Registrar*.

7. **UC6** - *Funcionários ultrapassaram o tempo de uso*

O administrador poderá consultar quais foram os funcionários que ultrapassaram o tempo de trabalho, e em um sistema futuro será possível informar ao líder quando um funcionário ultrapassar o limite de tempo.

***Visão do sistema***

Ao acessar o sistema o administrador deverá clicar em *Bancada*, uma nova lista será demonstrada com as opções: *Tempo de uso - Funcionário* e *Tempo de uso ultrapassado*. Ao acessar a opção *Tempo de uso ultrapassado* demonstrará as informações de funcionários que ultrapassaram o tempo de uso estabelecido na *RN1*.

8. **UC7** - *Funcionário muda de bancada varias vezes em um dia*

O sistema possibilitará que o funcionário mude de bancada ao longo do período de trabalho, mantendo as premissas da *RGN1*.

***Visão do sistema***

Ao acessar o sistema o administrador deverá clicar em *Sala*, uma nova lista será demonstrada com as opções: *Uso de bancadas* e *Bancadas*. Ao acessar a opção *Uso de bancadas* demonstrará as informações de funcionários que se movimentaram entre várias bancadas ao longo do dia.

# Implementação técnica

## Diagrama de casos de Uso
![Diagrama de casos de Uso](/images/Usecase.png)

## Diagrama UML
![Diagrama UML](/images/)

## Diagrama ER de banco de dados
![Diagrama ER de banco de dados](/images/db_pf.png)
