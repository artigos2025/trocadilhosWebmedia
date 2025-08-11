# trocadilhosWebmedia

# 🎭 Gerador e Analisador de Trocadilhos em Português

Um projeto de pesquisa para geração automática e análise de trocadilhos em português brasileiro usando Modelos de Linguagem de Grande Escala (LLMs).

## 📋 Descrição

Este projeto implementa um sistema completo para:

- **Gerar trocadilhos sintéticos** usando GPT-4 e Sabiá-3.1 com diferentes estratégias de prompt
- **Analisar e classificar trocadilhos** automaticamente usando modelos de IA
- **Distinguir entre trocadilhos humanos e sintéticos** através de classificadores BERT
- **Avaliar a qualidade dos trocadilhos gerados** com múltiplas métricas

### Tipos de Trocadilhos Suportados

- **Homográficos**: Mesma grafia, múltiplos significados (ex: "O aluno nada" - verbo nadar vs. pronome nada)
- **Heterográficos**: Grafia diferente, som similar (ex: "Rinocerrote" - rinoceronte + serrote)

## 🚀 Instalação

### Pré-requisitos

- Python 3.8+
- Pipenv
- Chaves de API para OpenAI e Maritaca AI

### Configuração

1. **Clone o repositório**
```bash
git clone <url-do-repositorio>
cd trocadilhos_cursor
```

2. **Instale as dependências**
```bash
pipenv install
pipenv shell
```

3. **Configure as variáveis de ambiente**
Crie um arquivo `.env` na raiz do projeto:
```env
openai_api_key=sua_chave_da_openai
maritaca_api_key=sua_chave_da_maritaca
```

4. **Estrutura de diretórios**
Certifique-se de que a seguinte estrutura existe:
```
files/
├── prompts/
│   ├── generation/
│   │   ├── zero_shot.txt
│   │   ├── few_shot.txt
│   │   └── chain_of_thought.txt
│   └── recognition/
│       └── few_shot.txt
├── puns_real/
└── puns_sintetico/
```

## 📖 Como Usar

### 1. Geração de Trocadilhos

Execute o notebook `1_GERAÇÃO_DOS_DADOS.ipynb` ou use a classe diretamente:

```python
from functions.generation.generator import PunsGenerator
from functions.generation.prompt import load_prompt
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()
openai_api_key = os.getenv("openai_api_key")
maritaca_api_key = os.getenv("maritaca_api_key")

# Inicializa o gerador
generator = PunsGenerator(
    openai_api_key=openai_api_key,
    maritaca_api_key=maritaca_api_key,
    use_sabia_generate=False  # True para usar Sabiá-3.1, False para GPT-4
)

# Carrega prompt e executa geração
prompt_generation = load_prompt('generation/few_shot', num_puns=5)
prompt_recognition = load_prompt('recognition/few_shot')

# Executa o processo completo
generator.run_batch_process(
    prompt_generation, 
    prompt_recognition, 
    num_batches=1
)

# Salva resultados
generator.get_history().to_csv('trocadilhos_gerados.csv', index=False)
```

### 2. Análise de Trocadilhos

Execute o notebook `2_ANÁLISE_TROCADILHOS.ipynb` para:

- Carregar dados de trocadilhos reais e sintéticos
- Avaliar modelos de reconhecimento automático
- Treinar classificadores para distinguir origem (humana vs IA)
- Gerar métricas de performance e visualizações

## 📊 Estratégias de Prompt

O projeto suporta três estratégias de geração:

- **Zero-shot**: Geração direta sem exemplos
- **Few-shot**: Geração baseada em exemplos fornecidos
- **Chain-of-thought**: Geração com raciocínio passo-a-passo

## 📁 Estrutura do Projeto

```
├── functions/
│   └── generation/
│       ├── generator.py      # Classe principal PunsGenerator
│       └── prompt.py         # Carregamento de prompts
├── files/
│   ├── prompts/             # Templates de prompt
│   ├── puns_real/           # Dataset PunTuguese
│   └── puns_sintetico/      # Trocadilhos gerados
├── results/                 # Modelos treinados e checkpoints
├── 1_GERAÇÃO_DOS_DADOS.ipynb
├── 2_ANÁLISE_TROCADILHOS.ipynb
├── Pipfile                  # Dependências
└── README.md
```

## 🔧 Funcionalidades Principais

### Classe PunsGenerator

- `generate_puns(prompt)`: Gera trocadilhos usando LLM especificado
- `analyze_puns(puns, prompt, model)`: Analisa trocadilhos com Sabiá ou GPT
- `run_batch_process()`: Executa pipeline completo de geração e análise
- `get_history()`: Retorna histórico de trocadilhos gerados

### Sistema de Avaliação

- Classificação automática usando `pun-recognition-pt`
- Treinamento de modelos BERT personalizados
- Métricas de accuracy, precision, recall e F1-score
- Matrizes de confusão e análises estatísticas

## 📈 Resultados Esperados

O sistema gera arquivos CSV com:

- **Trocadilhos gerados**: Texto completo dos trocadilhos
- **Classificações**: Avaliações de humor por diferentes modelos
- **Análises**: Explicações detalhadas dos mecanismos humorísticos
- **Métricas**: Scores de qualidade e classificação

## 📄 Licença

Este projeto é distribuído sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.
