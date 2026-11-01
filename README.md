# ✨ Que número é esse AI?

API desenvolvida com FastAPI para **classificar dígitos manuscritos**. O projeto foi desenvolvido no **Módulo 2 do curso de Desenvolvimento de IA para Análise Preditiva do Programa SCTEC**. O modelo foi treinado usando o dataset **MNIST** e o algoritmo **Random Forest**.

## 🧬 Origem do modelo

A aplicação reaproveita o mini-projeto de classificação MNIST do Módulo 2 do Programa SCTEC, usando o modelo que foi mais performático, o Random Forest, o qual é disponibilizado por uma API FastAPI modular.


## 📌 Objetivo

O projeto tem como objetivo construir uma API de classificação de imagens, que consiga classificar imagens de números manuscritos e disponibilizar a predição do modelo em  HTTP, com validação estrita e tratamento de erros.

## 📁 Estrutura do projeto

```text
.
├── treina_modelo.ipynb            # Treinamento e avaliação do modelo
├── requirements.txt               # Dependências do projeto
├── README.md                      # Documentação
├── models/
│   └── best_model_rf.pkl          # Modelo salvo
├── images/                        # Imagens
|   ├── numero0.png
|   ├── numero1.png
|   ├── numero2.png
|   └── ...
└── app/
    ├── __init__.py                # Identifica que é um pacote python
    ├── main.py                    # Arquivo principal da aplicação
    ├── routers.py                 # Módulo de rotas usando APIRouter
    ├── schemas.py                 # Módulo de definição de schemas usando Pydantic
    └── services.py                # Módulo que carrega modelo, faz pré-processamento e inferência
```


## 🤖 Modelo usado

**Random Forest**

Foram avaliados:

- `n_estimators`: `50`, `100`, `200` e `400`;
- `max_depth`: `5`, `10` e `20`.

Melhor configuração na validação:

```text
n_estimators = 200
max_depth = 20
Accuracy = 0.96671
F1 = 0.96651
```

### Métricas obtidas com o melhor modelo

| Métrica | Valor |
|----------|----------:|
| Acurácia | 96,54% |
| Precisão (Macro) | 96,54% |
| Recall (Macro) | 96,54% |
| F1-Score (Macro) | 96,53% |
| ROC-AUC (OvR) | 99,90% |



## 📦 Dependências

O projeto utiliza as seguintes bibliotecas:

- NumPy — `2.5.4`
- Pandas — `3.0.6`
- Matplotlib — `3.11.2`
- Seaborn — `0.13.2`
- OpenCV  — `5.0.0.93`
- Joblib — `1.6.0`
- Scikit-learn — `1.9.1`
- FastAPI — `0.162.0`
- Uvicorn — `0.54.0`
- Pydantic — `2.14.1`

Elas podem ser instaladas com o comando:

```bash
pip install -r requirements.txt
```


## ▶️ Como executar


### 1. Clone o repositório

```bash
git clone https://github.com/CherylHenkels/sctec-projeto2.git
```

### 2. Acesse a pasta

```bash
cd sctec-projeto2
```

### 3. Crie um ambiente virtual

```bash
python -m venv .venv
```

### 4. Ative o ambiente virtual

Linux/macOS

```bash
source .venv/bin/activate
```

Windows

```bash
.venv\Scripts\activate
```

### 5. Instale as dependências

```bash
pip install -r requirements.txt
```

### 6. Confirme que o arquivo do modelo está disponível.

Não é necessário executar novamente o treinamento para iniciar a API com o modelo salvo. O modelo já está treinado em `models/best_model_rf.joblib`. 

Caso você queira retreiná-lo basta rodar todas as células do notebook `treina_modelo.ipynb`

### 7. Inicie o servidor

Abra um terminal na raiz do projeto, e execute o uvicorn com o seguinte comando:

```bash
python -m uvicorn app.main:app --reload
```

O servidor ficará disponível em **http://127.0.0.1:8000**.

### 7. Acesse os endpoints

Para testar os endpoints basta acessar no navegador **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**

Isso vai permitir que você acesse o swagger e teste os endpoints do modelo


## ⚙️ Inicialização e processamento

Quando a API é executada com o uvicorn, o modelo é carregado. Isso acontece uma única vez por processo, na inicialização, usando `@asynccontextmanager` e o `lifespan` do FastAPI. As requisições de predição reutilizam o modelo salvo na memória RAM; o arquivo `.joblib` não é recarregado a cada chamada.

Para cada imagem, o serviço realiza:

1. Leitura em escala de cinza.
2. Aplicação de blur gaussiano e threshold invertido.
3. Recorte da região do dígito com margem.
4. Redimensionamento para 20 × 20 e posicionamento em uma imagem preta de 28 × 28.
5. Normalização dos pixels por 255 e organização em um vetor de 784 características.
6. Classificação pelo Random Forest.

As imagens de entrada devem conter um único dígito escuro sobre fundo branco, conforme o pré-processamento implementado.

## 🔌 Uso da API

Com o servidor em execução, você pode acessar a documentação interativa Swagger através da url:

**[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**

Nela, você consegue testar os endpoints. Para isso, escolha um endpoint, clique em **Try it out**, e depois preencha a requisição no formato JSON conforme o exemplo mostrado no swagger. Por fim clique em **Execute** e veja o resultado.

### `GET /health`

Verifica se o serviço responde e informa se o modelo está carregado em memória. Por ser uma requisição `GET` não recebe corpo JSON.

Resposta normal — **200 OK**:

```json
{
  "status": "ok",
  "model_loaded": true
}
```

Isso indica que o serviço está ativo e que o modelo foi carregado corretamente na memória RAM 


### `POST /predict`

Recebe um JSON com o caminho de uma imagem e devolve o dígito previsto.

**ENTRADA:**

```json
{
  "image_path": "images/numero2.png"
}
```

**EXEMPLO DE SAÍDA:**

**200 OK**

```json
{
  "digit": 2
}
```

O resultado depende da imagem e do modelo. O campo `digit` é um inteiro entre 0 e 9.

**Importante:** esta versão da api recebe um caminho de arquivo, não faz upload da imagem. O arquivo deve existir no computador que executa a API. O caminho passado deve ser relativo a raiz do projeto. 


#### Validação e tratamento de erros

| Status HTTP | Situação |
|---|---|
| **200 OK** | Consulta de saúde ou predição bem-sucedida |
| **400 Bad Request** | Imagem não pode ser lida ou nenhum dígito é encontrado |
| **422** | Corpo inválido, campo obrigatório ausente, tipo incorreto, caminho vazio ou campo extra |
| **500 Internal Server Error** | Falha inesperada na inferência ou construção da resposta |


Agora vamos mostrar todos os erros que podem aparecer na api

- Exemplo erro **400**

Caso o arquivo não exista:

```json
{
  "image_path": "images/inexistente.png"
}
```

Resposta:

```json
{
  "detail": "Não foi possível ler a imagem."
}
```

Caso o arquivo não contenha uma imagem:

```json
{
  "image_path": "images/branco.png"
}
```

Resposta:

```json
{
  "detail": "Nenhum dígito foi encontrado na imagem."
}
```

- Exemplo erro **422** 

Campo necessário:

```json
{}
```
Input deve ser uma string

```json
{
  "image_path": 123
}
```
Caminho precisa ter no mínimo 1 caractere
```json
{
  "image_path": ""
}
```

As respostas para essas validações são retornadas automaticamente pelo FastAPI/Pydantic. Erros internos são registrados no log e retornam uma mensagem genérica ao cliente.

- Exemplo erro **500**

Erro 500 é um erro de servidor, ele ocorre por algum problema interno do sistema. Para testar basta descomentar a linha 23 de `routers.py`

```
raise RuntimeError("Falha simulada para teste")
```
Mesmo após falhas de requisição, o serviço deve continuar atendendo. Então é só comentar a linha que a api volta a funcionar normalmente


## Possíveis Melhorias Futuras

* Criar um front para a utilização da API

* Usar um banco de dados para subir as imagens na api e, assim, preencher automaticamente o caminho na requisição `\predict`

* Melhorar a acurácia do modelo testando imagens de fora do banco de dados do MNIST


## 🎥 Video de demonstração

[link do video](https://drive.google.com/file/d/1eo-pvm5E4Hkoucgq5i_JyoRRM2ENj82U/view?usp=sharing)

---

## 👩‍💻 Autores

Projeto desenvolvido por 
* **Cheryl Henkels** - [GitHub](https://github.com/CherylHenkels)

