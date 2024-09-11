<h1 align="center"> 🌱Aegro </h1>

## Bem vindo(a) ao Agras
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
**Cadastro de Plantas:** Adicionar e gerenciar informações sobre as culturas plantadas.  
**Ciclo de Produção:** Acompanhar o ciclo de vida das plantas, desde o plantio até a colheita.  
**Agenda de Atividades:** Registrar e organizar as atividades agrícolas como irrigação, adubação e colheita.  
**Estoque e Produção:** Gerenciar o estoque de insumos e monitorar a produção agrícola.  
**Relatórios:** Gerar relatórios detalhados sobre o desempenho das culturas e o histórico de produção.  

## 🧷 Links
#### [Figma - Agras](URL FIGMA)

#### [Quadro do Jira](URL JIRA)

#### [Site do Projeto](URL GOOGLE SITES OU GITHUB)

# Entrega 01
## [Screencast (YOUTUBE)](URL DO YOUTUBE)

[![Clique para assistir o vídeo (abrirá em uma nova aba)](IMAGEM PARA ACESSAR O SCREENCAST)](URL DO YOUTUBE)

## [Quadro&BackLog (JIRA)](URL JIRA)

[![Clique para ver o quadro do jira (abrirá em uma nova aba)](IMAGEM DO QUADRO JIRA)](URL PRO QUADRO DO JIRA)
[![Clique para ver o backlog do jira (abrirá em uma nova aba)](IMAGEM BACKLOG JIRA)](URL BACKLOG JIRA)

## 💻 Tecnologias Utilizadas
- **Backend:** Django (Python) 🐍
- **Banco de Dados:** PostgreSQL 🐘
- Frontend: HTML, CSS, JavaScript 🌐
- Docker 🐳

## ⚙️ Pré-requisitos
Python 3.8+  
PostgreSQL  
Git  
Docker

## 🛠️ Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/agras.git
cd agras
```

### 2. Crie e ative um ambiente virtual

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/MacOS
ou
venv\Scripts\activate  # Windows
```
### 3. Instale as dependências

``` bash
pip install -r requirements.txt
```
### 4. Configurar o Banco de Dados

Configure o banco de dados PostgreSQL no arquivo `settings.py`
``` DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'nome_do_banco',
        'USER': 'usuario',
        'PASSWORD': 'senha',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 5. Execute as migrações

``` bash

python manage.py migrate
```
### 6. Inicie o servidor de desenvolvimento

``` bash
python manage.py runserver
``` 

## 🚀 Como Usar
- Acesso ao Painel: Navegue até `http://localhost:8000` para acessar a plataforma.
- Administração: Acesse `http://localhost:8000/admin` para gerenciar cursos e usuários.

## 🤝 Colaboradores
<table>
  <tr>
    <td align="center">
      <a href="#" title="defina o título do link">
        <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR65dbMui6whWaxsVpnyP_A1zY2IXODEzLVoA&s" width="100px;" alt="Foto do Adrian Michael"/><br>
        <sub>
          <b>Adrian Michael</b>
        </sub>
      </a>
    </td>
    <td align="center">
      <a href="#" title="defina o título do link">
        <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR65dbMui6whWaxsVpnyP_A1zY2IXODEzLVoA&s" width="100px;" alt="Foto da Beatriz Costa"/><br>
        <sub>
          <b>Beatriz Costa</b>
        </sub>
      </a>
    </td>
    <td align="center">
      <a href="#" title="defina o título do link">
        <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR65dbMui6whWaxsVpnyP_A1zY2IXODEzLVoA&s" width="100px;" alt="Foto da Aline Amancio"/><br>
        <sub>
          <b>Aline Amancio</b>
        </sub>
      </a>
    </td>
    <td align="center">
      <a href="#" title="defina o título do link">
        <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR65dbMui6whWaxsVpnyP_A1zY2IXODEzLVoA&s" width="100px;" alt="Foto do William Souza"/><br>
        <sub>
          <b>William Souza</b>
        </sub>
      </a>
    </td>
     <td align="center">
      <a href="#" title="defina o título do link">
        <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR65dbMui6whWaxsVpnyP_A1zY2IXODEzLVoA&s" width="100px;" alt="Foto do Vinicius Ventura"/><br>
        <sub>
          <b>Vinícius Ventura</b>
        </sub>
      </a>
    </td>
     <td align="center">
      <a href="#" title="defina o título do link">
        <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR65dbMui6whWaxsVpnyP_A1zY2IXODEzLVoA&s" width="100px;" alt="Foto da Nina Franca"/><br>
        <sub>
          <b>Nina França</b>
        </sub>
      </a>
    </td>
  </tr>
</table>
