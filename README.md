<h1 align="center"> 🌱AGRAS </h1>

## Bem vindo(a) ao **AGRAS**
Bem-vindo ao Agras! Este projeto foi desenvolvido para auxiliar famílias que praticam agricultura familiar no acompanhamento das suas plantações e no planejamento das atividades agrícolas.

## 🧑‍🌾 Sobre o Projeto  
### A aplicação permite que os usuários/agricultores:

- Realizem o cadastro das plantas cultivadas.
- Acompanhem o ciclo de produção (desde o plantio até a colheita).
- Organizem atividades diárias como irrigação e fertilização.
- Gerenciem o estoque de insumos agrícolas.
- Gerem relatórios sobre a produção e o desempenho das culturas.


## 🌍 Visão Geral
A agricultura familiar é essencial para o sustento de muitas famílias ao redor do mundo, e ter uma ferramenta para gerenciar esse processo de forma organizada pode fazer toda a diferença. Este sistema foi criado para otimizar o controle de plantações, organizar atividades diárias, e monitorar o desempenho da produção, proporcionando um apoio digital para agricultores familiares.

## 🛠️ Funcionalidades
- **🌾 Cadastro de Plantas:** Adicionar e gerenciar informações sobre as culturas plantadas.  
- **📅 Ciclo de Produção:** Acompanhar o ciclo de vida das plantas, desde o plantio até a colheita.  
- **📋 Agenda de Atividades:** Registrar e organizar as atividades agrícolas como irrigação, adubação e colheita.  
- **📊 Estoque e Produção:** Gerenciar o estoque de insumos e monitorar a produção agrícola.  
- **📦 Relatórios:** Gerar relatórios detalhados sobre o desempenho das culturas e o histórico de produção.  

## 🧷 Links
<a href="https://sites.google.com/cesar.school/agras">
    <img src="https://img.shields.io/badge/GOOGLE SITES-8abf17?style=for-the-badge&logo=google&logoColor=white" height="30px"/></a>
    
<a href="https://www.figma.com/design/wqEwDyRuQGX0MaPecGGU4n/Untitled?node-id=0-1&t=wYhB3IAeSWCCwKws-1">
  <img src="https://img.shields.io/badge/FIGMA-183219?style=for-the-badge&logo=figma&logoColor=white" height="30px"/></a>
  
<a href="https://app.clickup.com/9013393286/v/o/s/90131619724">
  <img src="https://img.shields.io/badge/ClickUp-8abf17?style=for-the-badge&logo=clickup&logoColor=white" height="30px"/></a>
  
<a href="URL DO YOUTUBE">
  <img src="https://img.shields.io/badge/YOUTUBE-183219?style=for-the-badge&logo=youtube&logoColor=white" height="30px"/></a>
  
<a href="https://agras.azurewebsites.net/">
  <img src="https://img.shields.io/badge/SITE DO PROJETO-8abf17?style=for-the-badge&logo=google&logoColor=white" height="30px"/></a>
  
<a href="https://agras.atlassian.net/jira/software/projects/KAN/boards/1">
  <img src="https://img.shields.io/badge/JIRA-183219?style=for-the-badge&logo=jira&logoColor=white" height="30px"/></a>

# 🚚 Status Report 1

## [🎬 Screencast Protótipo](https://www.youtube.com/watch?v=i34DN3N1n_Y)

<a href="https://www.youtube.com/watch?v=i34DN3N1n_Y" target="_blank">
    <img src="https://github.com/user-attachments/assets/8604c9da-aa65-42a5-97c1-ef5479af12bd" alt="Clique para assistir o vídeo (abrirá em uma nova aba)">
</a>


## 🐛🔍 [Issue/Bug Tracker](https://github.com/biacosta7/agras/issues?q=is%3Aissue+is%3Aclosed)

![image](https://github.com/user-attachments/assets/9516bcc5-283c-434e-b518-353196774b0b)
![image](https://github.com/user-attachments/assets/a9a6dcaf-e122-4736-ac7e-cb0f0ff22347)


## 🤝 Relatos de Pair Programming

Nas últimas três semanas, a equipe aplicou intensivamente o Pair Programming como uma prática central no desenvolvimento do projeto. Essa abordagem envolve dois programadores trabalhando juntos em uma única tarefa, onde um atua como "driver", escrevendo o código, e o outro como "navigator", revisando e sugerindo melhorias em tempo real. Essa dinâmica permite uma maior troca de ideias e colaboração, com foco na qualidade do código e na detecção rápida de erros. Durante o projeto, a equipe promoveu um rodízio frequente de papéis, garantindo que todos pudessem tanto programar quanto revisar, ampliando o conhecimento coletivo e a familiaridade com o código.

Essa metodologia foi fundamental para a aceleração do desenvolvimento e a melhoria contínua do código, permitindo que os membros da equipe colaborassem de forma mais eficiente. Além de otimizar o tempo e a qualidade das entregas, o Pair Programming também serviu como uma ferramenta de aprendizado colaborativo, onde todos os envolvidos puderam trocar experiências, discutir soluções e aplicar as melhores práticas de programação, tanto no back-end quanto no front-end. Colocar essa metodologia em prática contribuiu para uma maior coesão do grupo e para a entrega de um produto com código mais sólido e bem estruturado.


## 🔄 Diagrama de atividades do sistema

![image](https://github.com/user-attachments/assets/553302b0-f5e2-4945-aec9-cb561c4cf5e5)

## 📝 Histórias do usuário (JIRA)

![image](https://github.com/user-attachments/assets/064f223a-c9b8-449d-9f1d-9e9fecfa284a)


## 💻 Tecnologias Utilizadas
- **Backend:** Django (Python) 🐍
- **Banco de Dados:** PostgreSQL 🐘
- **Frontend:** HTML, Tailwind CSS, JavaScript 🌐

## ⚙️ Pré-requisitos
Python 3.12+  
PostgreSQL  
Git

## 🛠️ Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/biacosta7/agras.git
cd agras
```

### 2. Crie e ative um ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/MacOS
ou
venv\Scripts\activate  # Windows
```
### 3. Instale as dependências

``` bash
pip install -r requirements.txt
```

### 4. Execute as migrações

``` bash

python manage.py migrate
```
### 5. Inicie o servidor de desenvolvimento

``` bash
python manage.py runserver
``` 

## 🚀 Como Usar
- Acesso ao Painel: Navegue até `http://localhost:8000` para acessar a plataforma.

## 🤝 Colaboradores
<table>
  <tr>
    <td align="center">
      <a href="https://github.com/AdrianMichael5" title="defina o título do link">
        <img src="https://avatars.githubusercontent.com/u/144910632?v=4" width="100px;" alt="Foto do Adrian Michael"/><br>
        <sub>
          <b>Adrian Michael</b>
        </sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/biacosta7" title="defina o título do link">
        <img src="https://avatars.githubusercontent.com/u/113059480?v=4" width="100px;" alt="Foto da Beatriz Costa"/><br>
        <sub>
          <b>Beatriz Costa</b>
        </sub>
      </a>
    </td>
    <td align="center">
      <a href="#" title="defina o título do link">
        <img src="https://avatars.githubusercontent.com/u/168862762?v=4" width="100px;" alt="Foto da Aline Amancio"/><br>
        <sub>
          <b>Aline Amancio</b>
        </sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/william-mjsouza" title="defina o título do link">
        <img src="https://avatars.githubusercontent.com/u/66651052?v=4" width="100px;" alt="Foto do William Souza"/><br>
        <sub>
          <b>William Souza</b>
        </sub>
      </a>
    </td>
     <td align="center">
      <a href="https://github.com/vinivent" title="defina o título do link">
        <img src="https://avatars.githubusercontent.com/u/99739118?v=4" width="100px;" alt="Foto do Vinicius Ventura"/><br>
        <sub>
          <b>Vinícius Ventura</b>
        </sub>
      </a>
    </td>
     <td align="center">
      <a href="https://github.com/ninahffbs" title="defina o título do link">
        <img src="https://avatars.githubusercontent.com/u/168862762?v=4" width="100px;" alt="Foto da Nina Franca"/><br>
        <sub>
          <b>Nina França</b>
        </sub>
      </a>
    </td>
  </tr>
</table>

___

![Alt](https://repobeats.axiom.co/api/embed/61eaafb2cc575131259cf8ec9139855670acc63a.svg "Repobeats analytics image")
