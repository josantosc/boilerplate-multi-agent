### Este projeto é baseado no template [full-stack-fastapi-template](https://github.com/fastapi/full-stack-fastapi-template), que fornece uma base eficiente para construir aplicações Web modernas utilizando FastAPI. Esta implementação é ajustada para criar multi-agentes.

# Borlaiplate Multi Agent Rag
Borlaiplate Multi Agent Rag é um projeto desenvolvido para a criação de múltiplos agentes, utilizando diversas tecnologias modernas para garantir eficiência e escalabilidade.

## Tecnologias Utilizadas
- **[Langchain](https://www.langchain.com/):** Uma estrutura de desenvolvimento para criar aplicativos baseados em grandes modelos de linguagem (LLMs), facilitando a integração e interação entre diferentes modelos de linguagem.

- **[Langgraph](https://www.langchain.com/langgraph):** Uma ferramenta ou biblioteca que pode ser utilizada para representar ou visualizar relações semânticas entre conceitos, embora não seja amplamente conhecida como outras listadas; pode referir-se a uma aplicação ou extensão específica no contexto de linguagens ou processamento de linguagem natural.

- **[Python](https://www.python.org/):** Uma linguagem de programação de alto nível conhecida por sua simplicidade e legibilidade, amplamente usada em desenvolvimento web, cientistas de dados, inteligência artificial, entre outras áreas.

- **[Docker](https://www.docker.com/):** Uma plataforma que permite criar, implantar e gerenciar aplicativos em contêineres, que são ambientes isolados que garantem a consistência de aplicativos entre diferentes sistemas e etapas do ciclo de vida de desenvolvimento.

- **[ChromaDB](https://www.trychroma.com/):** Um sistema de banco de dados especializado para lidar com dados contextuais e relacionais, possivelmente utilizado para armazenamento eficiente em aplicações que precisam processar grandes volumes de dados inter-relacionais.

- **[FastAPI](https://fastapi.tiangolo.com/):** Um moderno framework web para Python que permite criar APIs com rapidez e alto desempenho, utilizando tipagem de dados para gerar documentação automática e validação.

- **[Uvicorn](https://www.uvicorn.org/):** Um servidor ASGI (Asynchronous Server Gateway Interface) para Python, projetado para ser rápido e leve, ideal para executar aplicações desenvolvidas com frameworks como FastAPI e Starlette.

## Instruções de Instalação

### Pré-requisitos
- Certifique-se de ter o Docker e o Python instalados na sua máquina.


### Configuração das Variáveis de Ambiente

Antes de iniciar o projeto, é essencial configurar as variáveis de ambiente. Use o arquivo `env.example` como referência:

1. **Crie um arquivo `.env` na raiz do projeto.**
2. **Copie o conteúdo do arquivo `.env.example` para o arquivo `.env`** e personalize os valores de acordo com suas necessidades específicas.

Exemplo de conteúdo do arquivo `.env`:

```plaintext
# Configurações gerais do projeto
PROJECT_NAME="SERVER"
FIRST_SUPERUSER=admin@gmail.com
FIRST_SUPERUSER_PASSWORD=mudar123
FIRST_FULL_NAME=admin

# Configurações do banco de dados PostgreSQL
POSTGRES_SERVER=localhost
POSTGRES_DB=postgres
POSTGRES_PORT=5432
POSTGRES_USER=admin
POSTGRES_PASSWORD=admin

# Configurações de CORS
BACKEND_CORS_ORIGINS="http://localhost,http://localhost:5173,https://localhost,https://localhost:5173"

# Chave secreta para o aplicativo
SECRET_KEY=mudar123

# Configurações para integração com WhatsApp
BASE_URL_WHATSAPP=https://graph.facebook.com/v20.0
WHATSAPP_TOKEN=
WHATSAPP_PHONE_NUMBER_ID=

# Configurações do Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# Outros tokens e chaves
VERYFY_TOKEN=12345
OPENAI_API_KEY=

# Configurações do stack e domínio
STACK_NAME=teste
DOMAIN=localhost
ENVIRONMENT=local

# Configuração do tempo de expiração de thread
EXPIRATION_TIME=24
```
### Passos para Instalação
1. **Clone o repositório**:
   ```bash
   git clone https://github.com/seu-usuario/borlaiplate-multi-agent-rag.git
   cd borlaiplate-multi-agent-rag
   ```

2. **Crie um ambiente virtual (opcional, mas recomendado)**:
   ```bash
   python -m venv env
   source env/bin/activate  # No Windows use `env\Scripts\activate`
   ```

3. **Instale as dependências do Python**:
   ```bash
   pip install -r requirements.txt
   ```
   
4. **Construa e inicie os containers Docker**:
   ```bash
   docker-compose up --build
   ```

5. **Acessar a API do Chromadb:**
   Depois de iniciar os contêineres Docker, siga as instruções abaixo para acessar o aplicativo e a API do Chromadb:
   Abra seu navegador e acesse o endereço:
   ```
     http://172.30.0.2:8000/docs#/
   ```
   
5. **Acessar a API da aplicação:**
   Depois de iniciar os contêineres Docker, siga as instruções abaixo para acessar o aplicativo e a API do Chromadb:
   Abra seu navegador e acesse o endereço:
   ```
     http://172.30.0.5:8001/docs#/
   ```

6. **Parar os serviços:**
   Para parar a execução dos contêineres, utilize o seguinte comando:
   ```bash
   docker-compose down
   ```
## Instalação sem Docker

### Para executar a aplicação sem Docker, siga os passos abaixo:

1. Configure as variáveis de ambiente necessárias.
2. Navegue até a raiz do projeto.
3. Execute os seguintes scripts na ordem indicada:
   - `./load_env.sh`
   - `./start.sh`
4. Certifique-se de que os serviços de banco de dados estejam em execução.

## Integração
Este projeto integra-se com a API oficial do WhatsApp, que faz parte dos produtos da Meta. 
Ele foi desenvolvido para facilitar o envio e recebimento de mensagens entre agentes e usuários, proporcionando uma comunicação eficiente e automatizada.

####  Pré-requisitos
- Conta de desenvolvedor na Meta
- Conta no WhatsApp Business

#### Configuração
Para configurar corretamente a aplicação com a API do WhatsApp da Meta, siga as etapas abaixo:

1. **Conta de Desenvolvedor e Configuração de Aplicativo**:
   - **Crie uma conta de desenvolvedor na Meta**: Acesse [Meta for Developers](https://developers.facebook.com/) e siga as instruções para criar sua conta.
   - **Configure seu aplicativo na Meta**: Após criar a conta, crie um novo aplicativo no painel de desenvolvedor e configure a API do WhatsApp.

2. **Habilite e Configure o Webhook da Meta**:
   - No painel do seu aplicativo na Meta, navegue até a seção de Webhooks.
   - **Adicione a URL do seu aplicativo**: Insira a URL onde sua aplicação está hospedada para receber eventos de webhook (garanta que a URL esteja acessível publicamente).
   - **Configure o Webhook** com os campos necessários para o seu caso de uso.

3. **Defina as Variáveis de Ambiente**:
   - Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:
     ```env
     WHATSAPP_TOKEN=sua_chave_de_acesso
     BASE_URL_WHATSAPP=https://graph.facebook.com/v13.0/
     WHATSAPP_PHONE_NUMBER_ID=seu_numero_de_telefone_id
     VERIFY_TOKEN=seu_token_de_verificação
     ```

   - **WHATSAPP_TOKEN**: Obtido ao configurar sua conta do WhatsApp Business.
   - **BASE_URL_WHATSAPP**: URL base para as chamadas à API do WhatsApp.
   - **WHATSAPP_PHONE_NUMBER_ID**: ID do número de telefone associado à sua conta do WhatsApp Business.
   - **VERIFY_TOKEN**: Token de verificação usado na configuração do webhook.

4. **Mais Informações**:
   - Para detalhes adicionais e configurações avançadas, consulte a documentação oficial da Meta [aqui](https://developers.facebook.com/docs/whatsapp).

### Utilização

  ```bash
  python main.py --agente exemplo
  ```
## Caso de Uso
**Agent Med:** Um sistema multiagente que responde a consultas médicas usando o [MedQuad-MedicalQnADataset](https://huggingface.co/datasets/keivalya/MedQuad-MedicalQnADatasetOs) com [RAG](https://medium.com/blog-do-zouza/rag-retrieval-augmented-generation-8238a20e381d).

### Descrição

Este sistema foi desenvolvido para fornecer respostas a perguntas relacionadas a doenças e tratamentos médicos. Utilizando o dataset [MedQuad-MedicalQnADataset](https://huggingface.co/datasets/keivalya/MedQuad-MedicalQnADatasetOs), o sistema aplica a técnica de [RAG](https://medium.com/blog-do-zouza/rag-retrieval-augmented-generation-8238a20e381d), que enriquece o contexto do modelo de linguagem [LLM](https://www.datacamp.com/pt/blog/what-is-an-llm-a-guide-on-large-language-models) ao combinar a recuperação de informações relevantes com a geração de respostas.

O [MedQuad-MedicalQnADataset](https://huggingface.co/datasets/keivalya/MedQuad-MedicalQnADatasetOs) contém um amplo conjunto de perguntas e respostas médicas extraídas de fontes confiáveis, como o [National Institutes of Health](https://www.nih.gov/). A junção desses dados com as capacidades do [LLM](https://www.datacamp.com/pt/blog/what-is-an-llm-a-guide-on-large-language-models) podem garantir que as respostas sejam tanto precisas quanto contextualizadas.

Além disso, o sistema armazena informações consideradas relevantes pelo sistema na base vetorial [ChromaDB](https://docs.trychroma.com/), um banco de dados projetado para lidar com dados contextuais e vectoriais. Esse armazenamento contínuo e atualizado permite que o multiagente disponha de um banco de dados cada vez mais enriquecido, proporcionando um contexto mais robusto para o agente. Essa abordagem assegura que o agente esteja em contínuo aperfeiçoamento, melhorando suas respostas conforme novas informações são integradas e armazenadas, ao mesmo tempo em que garante que informações falsas não sejam retidas.

Este mecanismo de atualização constante transforma o sistema em uma ferramenta dinâmica e evolutiva para responder com precisão a consultas médicas, mantendo sua base de conhecimento atualizada.

### Workflow do Agent
![Fluxo de Trabalho](https://raw.githubusercontent.com/josantosc/boilerplate-multi-agent/refs/heads/master/medias/imagens/workflow.png)
### Como Usar

1. **Via Endpoint**: Uma vez que a API esteja configurada, você pode acessar [api/v1/use_case/medical_agent] para interagir com a aplicação.
2. **Utilização via API do WhatsApp**: Para utilizar a aplicação através da API, é essencial seguir atentamente as etapas de configuração descritas na seção de integração.

### Imagem da utilização via API.

![API](https://raw.githubusercontent.com/josantosc/boilerplate-multi-agent/refs/heads/master/medias/imagens/api_agent.jpeg)
### Vídeo demostrativo da aplicação funcionando.
- Utilização via Whatsapp

[![Assista ao Vídeo Explicativo](https://img.youtube.com/vi/glqW2wKfoUI/maxresdefault.jpg)](https://www.youtube.com/watch?v=glqW2wKfoUI)

### Trabalhos futuros
- Reconhecimento e armazenamento de preferências do usuário, como a preferência por um tom mais formal nas respostas. Quando essa preferência é confirmada, o sistema atualiza a base de conhecimento, registrando a pergunta e a resposta no estilo desejado.
- Confirmação do usuário sobre a precisão da reposta do Agent e atualização da base de conhecimento.
- Utilizar o modelo [BioBERTpt](https://github.com/HAILab-PUCPR/BioBERTpt), desenvolvido pela PUCPR e treinado especificamente no contexto médico brasileiro, como embeddings para a técnica de RAG, aproveitando um dataset de dados médicos brasileiros para otimizar a relevância e precisão das respostas no domínio médico.


## Contribuindo
Estamos abertos a contribuições! Sinta-se à vontade para abrir uma issue ou enviar um pull request. Para contribuições significativas, por favor, entre em contato conosco para discutir o que você gostaria de mudar.

## Licença
Este projeto é licenciado sob a [MIT license](https://opensource.org/license/mit).

## Contribuidores
- [Joeckson](https://github.com/josantosc)

## Autor
- [Joeckson](https://github.com/josantosc)
