# Agente Formatador
## Esta solução interativa permite auxiliar o processo de formatação/validação dos dados

## Como rodar
### 1. Clone este repositório
__1.1 Com o terminal aberto, execute para clonar o repositório:__
    
    git clone https://github.com/DadosComCafe/agente_formatador.git

__1.2 Navegue até a raíz do projeto:__

    cd agente_formatador

### 2.Configure o ambiente
__2.1 Para este projeto, usaremos o gerenciador de dependências python uv. Portanto, na raiz do projeto execute:__

    uv sync

Com isso, um diretório chamado .venv será criado na raiz do projeto. Este diretório contem o ambiente python isolado.

### 3. Rode o servidor que irá levantar o agente:

    uv run streamlit run convert_types.py

### 4. Extra -> __Docker:__
__4.1 Build da imagem:__ Com um terminal aberto na raíz do projeto, rodar:

    docker build -t agente_formatador .

__4.2 Subir o container:__ Após o build terminar, rodar:

    docker run -p 8501:8501 agente_formatador

Para esta imagem docker, foi utilizada uma imagem base do python reduzido, o que garante uma melhor performance e menor tamanho da imagem, por não possuir pacotes e bibliotecas não necessárias para a aplicação.

## Utilizando o agente

__1. Acessando a página home:__
![home](imgs/home.png)
 
__2.1 Enviando uma planilha:__ 
![planilha](imgs/enviando_planilha.png)
_________________________________________________________________
![planilha](imgs/planilha.png)

__2.2 Enviando um zip de planilhas:__
![zip_de_planilha](imgs/enviando_zip_planilhas.png)

_________________________________________________________________
![zip_de_planilha](imgs/zip_planilha1.png)

_________________________________________________________________
![zip_de_planilha](imgs/zip_planilha2.png)

__3.0 Formatando as planilhas:__

![formatando_planilha](imgs/formatando_planilha1.png)
_________________________________________________________________
![formatando_planilha](imgs/formatando_planilha2.png)

__4.0 Acessando arquivos formatados:__

![acessando_arquivos](imgs/arquivos_formatados1.png)

_________________________________________________________________
![acessando_arquivos](imgs/arquivos_formatados2.png)

__4.1 Abrindo os arquivos formatados:__

![abrindo arquivos formatados](imgs/abrindo_arquivo_formatado.png)

## Ainda em construção!
