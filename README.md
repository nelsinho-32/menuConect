# 🍽️ Menu Connect

**Menu Connect** é uma plataforma web inovadora, construída com Vue.js 3, que visa revolucionar a interação entre clientes e restaurantes. A aplicação oferece uma experiência rica e inteligente, desde a descoberta de novos locais até à gestão completa de mesas e pedidos pelo restaurante.

![LogoMarcaMenu](https://raw.githubusercontent.com/nelsinho-32/menuconect/main/src/assets/images/LogoMarcaMenu.png)

---

## 🚀 Visão Geral do Projeto

O Menu Connect foi projetado com dois fluxos de utilizador em mente: o **Cliente** e a **Empresa**.

* **Para o Cliente:** Uma interface intuitiva para descobrir restaurantes, explorar cardápios interativos, fazer reservas, planear encontros (manualmente ou com sugestões de IA) e gerir os seus pedidos e pratos favoritos.
* **Para a Empresa:** Um painel de gestão poderoso que permite ao restaurante personalizar completamente a sua presença na plataforma. Isto inclui adicionar e editar o cardápio, gerir um mapa de mesas interativo, visualizar o estado do salão em tempo real e muito mais.

## ✨ Funcionalidades Principais

A aplicação está repleta de funcionalidades modernas, com foco na personalização e na experiência do utilizador.

#### Para Clientes:
* **Navegação e Descoberta:** Filtre restaurantes por tipo de cozinha e explore cardápios categorizados.
* **Reservas e Fila de Espera:** Sistema de reserva de mesas com confirmação e gestão de filas de espera.
* **Notificações via WhatsApp:** Receba um lembrete da sua reserva no seu telemóvel, com opção de confirmar a presença.
* **Carrinho Inteligente:** Adicione pratos de múltiplos restaurantes, com cálculo de taxa de entrega por estabelecimento.
* **Personalização de Pedidos:** Remova ingredientes e adicione notas aos seus pratos.
* **Planeador de Encontros:**
    * **Sugestão por IA:** Receba 3 sugestões de encontros temáticos gerados pela API da Gemini.
    * **Planeamento Manual:** Monte um encontro passo a passo, escolhendo a mesa, data, hora, convidados e o menu completo para cada um.
* **Histórico de Pedidos:** Reveja todos os seus pedidos anteriores, incluindo as personalizações feitas.
* **Favoritos:** Salve os seus restaurantes e pratos preferidos para acesso rápido.

#### Para Empresas (Gestão):
* **CRUD de Restaurantes e Pratos:** Adicione novos restaurantes e itens ao cardápio com formulários intuitivos que permitem o upload de imagens locais.
* **Editor de Mapa de Mesas:**
    * **Drag & Drop:** Arraste e posicione mesas, bares, cozinhas, WCs e outros elementos.
    * **Rotação de Peças:** Gire os elementos para criar um layout realista.
    * **Personalização do Chão:** Altere a textura do chão do mapa.
* **Gestão de Mesas em Tempo Real:** Uma tela dedicada para visualizar o estado de cada mesa (Disponível, Ocupada, A Limpar) e ver detalhes como o perfil do cliente que reservou e o seu consumo.
* **Configuração de Mesas:** Edite o número de cada mesa e adicione imagens específicas para ela, que podem ser visualizadas pelos clientes.

## 🛠️ Tecnologias Utilizadas

Este projeto foi construído com um ecossistema moderno de front-end:

* **[Vue.js 3](https://vuejs.org/) (Composition API):** O coração da aplicação, permitindo a criação de componentes reativos e bem estruturados.
* **[Vite](https://vitejs.dev/):** Ferramenta de build extremamente rápida que oferece uma experiência de desenvolvimento superior.
* **[Pinia](https://pinia.vuejs.org/):** Para uma gestão de estado centralizada, limpa e escalável (utilizador, restaurantes, etc.).
* **[Tailwind CSS](https://tailwindcss.com/):** Framework CSS utility-first para a criação de uma interface moderna e responsiva.
* **Persistência de Dados:** Uso intensivo do `localStorage` do navegador para guardar o layout dos mapas, listas de restaurantes e pratos, favoritos e histórico de pedidos, simulando uma experiência de utilizador "logado".
* **(Opcional) [Gemini AI](https://ai.google.dev/gemini-api):** Integração com a API da Google para funcionalidades de inteligência artificial.

## 🚀 Como Executar o Projeto

Para executar o projeto localmente, siga estes passos:

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/nelsinho-32/menuconect.git](https://github.com/nelsinho-32/menuconect.git)
    cd menuconect
    ```

2.  **Instale as dependências:**
    (Certifique-se de que tem o [Node.js](https://nodejs.org/) instalado)
    ```bash
    npm install
    ```

3.  **(Opcional) Adicione a sua Chave da API do Gemini:**
    * Abra o ficheiro `src/services/geminiService.js`.
    * Substitua o placeholder da `apiKey` pela sua chave real para ativar as funcionalidades de IA.

4.  **Execute o servidor de desenvolvimento:**
    ```bash
    npm run dev
    ```

5.  **Acesse no navegador:**
    * Abra o endereço [http://localhost:5173](http://localhost:5173).

---

Este `README.md` está agora muito mais completo e reflete o estado atual e impressionante da sua aplicação!