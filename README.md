
-----

# 🍽️ Menu Connect

**Menu Connect** é uma plataforma web inovadora, construída com Vue.js 3 e um backend em Python, que visa revolucionar a interação entre clientes e restaurantes. A aplicação oferece uma experiência rica e inteligente, desde a descoberta de novos locais até à gestão completa de mesas e pedidos pelo restaurante.

-----

## 🚀 Visão Geral do Projeto

O Menu Connect foi projetado com três fluxos de utilizador em mente: o **Cliente**, a **Empresa** e o **Administrador**.

  * **Para o Cliente:** Uma interface intuitiva para descobrir restaurantes, explorar cardápios interativos, fazer reservas, planear encontros (manualmente ou com sugestões de IA) e gerir os seus pedidos e pratos favoritos.
  * **Para a Empresa:** Um painel de gestão poderoso que permite ao restaurante personalizar completamente a sua presença na plataforma. Isto inclui adicionar e editar o cardápio, gerir um mapa de mesas interativo, visualizar o estado do salão em tempo real e muito mais.
  * **Para o Administrador:** Controlo total sobre a plataforma, incluindo a capacidade de adicionar novos restaurantes e gerir os perfis das empresas.

## ✨ Funcionalidades Principais

A aplicação está repleta de funcionalidades modernas, com foco na personalização e na experiência do utilizador.

#### Para Clientes:

  * **Autenticação Completa:** Sistema de login e cadastro seguro.
  * **Navegação e Descoberta:** Filtre restaurantes por tipo de cozinha e explore cardápios categorizados.
  * **Reservas e Fila de Espera:** Sistema de reserva de mesas com confirmação e gestão de filas de espera, tudo persistido no banco de dados.
  * **Notificações via WhatsApp:** Receba um lembrete da sua reserva no seu telemóvel.
  * **Carrinho Inteligente:** Adicione pratos de múltiplos restaurantes.
  * **Personalização de Pedidos:** Remova ingredientes e adicione notas aos seus pratos.
  * **Planeador de Encontros:**
      * **Sugestão por IA:** Receba 3 sugestões de encontros temáticos gerados pela API da Gemini.
      * **Planeamento Manual:** Monte um encontro passo a passo, escolhendo a mesa, data, hora, convidados e o menu completo para cada um, com os dados salvos no banco de dados.
  * **Favoritos:** Salve os seus restaurantes e pratos preferidos na sua conta de usuário.

#### Para Empresas e Administradores (Gestão):

  * **CRUD de Restaurantes e Pratos:** Adicione novos restaurantes (apenas admin) e itens ao cardápio (admin e empresa dona) com formulários intuitivos.
  * **Editor de Mapa de Mesas:**
      * **Drag & Drop:** Arraste e posicione mesas, bares, cozinhas, etc.
      * **Rotação de Peças:** Gire os elementos para criar um layout realista.
      * **Layout Salvo no Banco de Dados:** As alterações no mapa são guardadas permanentemente.
  * **Gestão de Mesas em Tempo Real:** Uma tela dedicada para visualizar o estado de cada mesa (Disponível, Ocupada, A Limpar) e ver detalhes como o perfil do cliente que reservou e o seu consumo.
  * **Gestão Financeira:** Um painel que exibe as vendas do dia e os pratos mais populares, com cálculos feitos no back-end.

## 🛠️ Tecnologias Utilizadas

Este projeto foi construído como uma aplicação Full-Stack moderna:

  * **Frontend:**
      * **[Vue.js 3](https://vuejs.org/) (Composition API):** O coração da aplicação, permitindo a criação de componentes reativos.
      * **[Vite](https://vitejs.dev/):** Ferramenta de build extremamente rápida.
      * **[Pinia](https://pinia.vuejs.org/):** Para uma gestão de estado centralizada e escalável.
      * **[Tailwind CSS](https://tailwindcss.com/):** Framework CSS utility-first para a interface.
  * **Backend:**
      * **[Python 3](https://www.python.org/)** com **[Flask](https://flask.palletsprojects.com/)**: Para construir uma API RESTful robusta e segura.
      * **[MySQL](https://www.mysql.com/)**: Como banco de dados relacional para persistir todos os dados da aplicação.
      * **Autenticação:** JWT (JSON Web Tokens) para sessões seguras e Bcrypt para a encriptação de senhas.
  * **APIs Externas:**
      * **(Opcional) [Gemini AI](https://ai.google.dev/gemini-api):** Integração com a API da Google para funcionalidades de inteligência artificial.

## 🚀 Como Executar o Projeto (Para a Equipa)

Para executar este projeto localmente, siga estes passos.

### Pré-requisitos

Certifique-se de que tem o seguinte software instalado:

  * [Node.js](https://nodejs.org/) (versão 18 ou superior)
  * [Python](https://www.python.org/downloads/) (versão 3.10 ou superior)
  * [link suspeito removido] (versão 8)

### 1\. Clonar o Repositório

```bash
git clone https://github.com/nelsinho-32/menuconect.git
cd menuconect
```

### 2\. Configurar o Banco de Dados

1.  Abra o seu cliente MySQL (Workbench, DBeaver, ou linha de comando).
2.  Execute o script `database_setup.sql` que está na raiz do projeto. Isto irá criar o banco de dados `menu_connect` e todas as tabelas necessárias.

### 3\. Configurar o Backend

1.  Navegue até à pasta do backend:
    ```bash
    cd backend
    ```
2.  (Recomendado) Crie e ative um ambiente virtual:
    ```bash
    python -m venv venv
    # No Windows:
    .\venv\Scripts\activate
    # No macOS/Linux:
    source venv/bin/activate
    ```
3.  Instale as dependências Python a partir do ficheiro `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```
4.  Abra o ficheiro `backend/app.py` num editor de código.
5.  Encontre a secção `db_config` e **altere a sua senha do MySQL** para a senha que você definiu ao instalar o MySQL.

### 4\. Configurar o Frontend

1.  Volte para a pasta principal do projeto.
2.  Instale as dependências do Node.js:
    ```bash
    npm install
    ```

### 5\. Executar a Aplicação

Você precisará de ter **dois terminais abertos** para executar a aplicação completa.

  * **Terminal 1 (Backend):**

    ```bash
    # (Dentro da pasta 'backend', com o ambiente virtual ativado)
    python app.py
    ```

  * **Terminal 2 (Frontend):**

    ```bash
    # (Dentro da pasta principal do projeto)
    npm run dev
    ```

A aplicação estará a funcionar em `http://localhost:5173`. Agora você pode registar um novo usuário e usar a aplicação completa\!