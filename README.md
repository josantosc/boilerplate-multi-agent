Este projeto é baseado no template [full-stack-fastapi-template](https://github.com/fastapi/full-stack-fastapi-template), que fornece uma base eficiente para construir aplicações Web modernas utilizando FastAPI. Esta implementação é ajustada para criar multi-agentes.

# Borlaiplate Multi Agent Rag
Borlaiplate Multi Agent Rag é um projeto desenvolvido para a criação de múltiplos agentes, utilizando diversas tecnologias modernas para garantir eficiência e escalabilidade.

## Tecnologias Utilizadas
- **Langchain**: 
- **Langgraph**: 
- **Python**: 
- **Docker**: 
- **Chromadb**: 
- **FastAPI**: 
- **Uvicorn**: 

## Instruções de Instalação

### Pré-requisitos
- Certifique-se de ter o Docker e o Python instalados na sua máquina.

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

## Docker
1. **Construir e iniciar os serviços:**
   No diretório raiz do projeto, execute o comando abaixo para construir a imagem e iniciar o contêiner:
   ```bash
   docker-compose up --build
   ```
   Isso irá construir a imagem e iniciar o serviço, tornando o aplicativo acessível na porta 8005.

3. **Acessar o aplicativo:**
   Abra seu navegador e acesse `http://localhost:8005` para visualizar o aplicativo em execução.

4. **Parar os serviços:**
   Para parar a execução dos contêineres, utilize o seguinte comando:
   ```bash
   docker-compose down
   ```


## Exemplos de Uso
Aqui estão alguns exemplos de como usar o Borlaiplate Multi Agent Rag:

- **Exemplo 1**: Descreva como iniciar um agente básico.
  ```bash
  python main.py --agente exemplo
  ```

- **Exemplo 2**: Um cenário mais complexo.
  ```bash
  python main.py --agente avancado --config config.json
  ```

## Contribuindo
Estamos abertos a contribuições! Sinta-se à vontade para abrir uma issue ou enviar um pull request. Para contribuições significativas, por favor, entre em contato conosco para discutir o que você gostaria de mudar.

## Licença
Este projeto é licenciado sob a [MIT license] - veja o arquivo `LICENSE` para mais detalhes.

## Contribuidores
- [Nome do Contribuidor 1](link para o perfil do GitHub)
- [Nome do Contribuidor 2](link para o perfil do GitHub)

