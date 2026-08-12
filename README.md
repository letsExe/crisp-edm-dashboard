# 📊 CRISP-EDM Dashboard

> **Análise longitudinal de dados acadêmicos com CRISP-EDM e dashboards interativos**

O **CRISP-EDM Dashboard** é uma aplicação web desenvolvida em Python e Streamlit para apoiar a análise de dados acadêmicos do curso de Ciência da Computação da **Universidade Estadual do Oeste do Paraná — UNIOESTE, Campus de Foz do Iguaçu**.

O projeto utiliza o **CRISP-EDM**, adaptação do processo CRISP-DM para o contexto educacional, como estrutura metodológica para organização, preparação, análise e apresentação dos dados.

A aplicação reúne diferentes relatórios acadêmicos em **um único dashboard**, permitindo a exploração de indicadores relacionados ao fluxo discente, desempenho acadêmico, perfil dos estudantes e formas de ingresso.

---

## ✨ Objetivos

O projeto busca transformar dados acadêmicos institucionais em informações organizadas, compreensíveis e úteis para apoio à gestão acadêmica.

Entre seus principais objetivos estão:

- 📈 acompanhar a evolução histórica de indicadores acadêmicos;
- 🎓 analisar situações acadêmicas dos estudantes;
- 📚 identificar padrões de aprovação e reprovação por disciplina;
- 👥 caracterizar o perfil discente;
- 🚪 analisar as diferentes formas de ingresso;
- 🔎 facilitar a identificação de tendências e possíveis pontos de atenção;
- ♻️ tornar o processo de análise mais reprodutível;
- 🖥️ disponibilizar os resultados por meio de dashboards interativos.

---

## 🧭 Relatórios analisados

A aplicação é organizada a partir de quatro relatórios acadêmicos.

### GR13 — Situação Acadêmica

Permite acompanhar a evolução das diferentes situações acadêmicas ao longo do tempo.

Entre as análises previstas estão:

- quantidade de estudantes por situação;
- distribuição percentual;
- evolução temporal;
- estatísticas descritivas;
- identificação de picos e vales;
- comparação entre diferentes períodos.

---

### GR14 — Aprovação e Reprovação

Voltado à análise do desempenho acadêmico por disciplina e série.

Entre as análises previstas estão:

- número de estudantes matriculados;
- quantidade e percentual de aprovados;
- quantidade e percentual de reprovados;
- evolução histórica por disciplina;
- disciplinas com maiores taxas de reprovação;
- comparação entre séries do curso.

---

### GR16 — Perfil Discente

Permite caracterizar o perfil dos estudantes matriculados no curso.

Entre as dimensões analisadas estão:

- idade;
- faixa etária;
- sexo;
- cor/raça;
- série do curso;
- composição do corpo discente ao longo dos anos.

---

### GR38 — Perfil dos Ingressantes

Voltado à análise das características dos estudantes no momento do ingresso.

Entre as análises previstas estão:

- quantidade anual de ingressantes;
- formas de ingresso;
- distribuição por sexo;
- perfil etário;
- comparação da idade entre modalidades de ingresso;
- evolução das formas de ingresso ao longo do tempo.

---

## Metodologia

O desenvolvimento é organizado segundo o **CRISP-EDM**, que adapta o CRISP-DM para aplicações em dados educacionais.

De forma geral, o projeto segue o seguinte fluxo:

```text
Entendimento do domínio
        ↓
Entendimento dos dados
        ↓
Preparação dos dados
        ↓
Análise e modelagem
        ↓
Avaliação dos resultados
        ↓
Disponibilização dos dashboards
```

Neste projeto, a etapa de modelagem é direcionada principalmente para **análises descritivas e diagnósticas**, incluindo:

- séries históricas;
- distribuições;
- taxas e proporções;
- comparações temporais;
- segmentações;
- rankings;
- estatísticas descritivas.

O objetivo não é realizar predição individual do comportamento dos estudantes, mas construir um diagnóstico histórico e transparente dos indicadores acadêmicos.

---

## 🏗️ Arquitetura do projeto

O projeto utiliza uma arquitetura modular para separar:

- dados originais;
- preparação dos dados;
- cálculos;
- tabelas;
- gráficos;
- interface web;
- resultados exportados.

```text
crisp-edm-dashboard/
│
├── app.py
├── pyproject.toml
├── poetry.lock
├── README.md
├── LICENSE
│
├── data/
│   ├── raw/
│   │   ├── gr13/
│   │   ├── gr14/
│   │   ├── gr16/
│   │   └── gr38/
│   │
│   ├── interim/
│   │   └── gr14/
│   │
│   └── processed/
│
├── outputs/
│   ├── tables/
│   │   ├── gr13/
│   │   ├── gr14/
│   │   ├── gr16/
│   │   └── gr38/
│   │
│   └── figures/
│       ├── gr13/
│       ├── gr14/
│       ├── gr16/
│       └── gr38/
│
├── scripts/
│   └── process_all.py
│
├── src/
│   └── crisp_edm_dashboard/
│       ├── config.py
│       │
│       ├── loaders/
│       ├── processing/
│       ├── analysis/
│       ├── tables/
│       ├── charts/
│       ├── views/
│       └── utils/
│
└── tests/
```

### Fluxo dos dados

```text
Planilhas originais
       │
       ▼
data/raw/
       │
       ▼
Preparação e padronização
       │
       ▼
data/processed/
       │
       ├──────────────┐
       ▼              ▼
   Análises        Tabelas
       │              │
       ├──────┬───────┘
       ▼      ▼
   Gráficos  Indicadores
       │      │
       └──┬───┘
          ▼
      Streamlit
          │
          ▼
   Dashboard Web
```

Essa separação permite que os mesmos cálculos utilizados no dashboard também sejam utilizados na geração das tabelas e figuras destinadas à documentação e às publicações científicas.

---

## 🛠️ Tecnologias

O projeto utiliza principalmente:

- **Python** — linguagem principal;
- **pandas** — manipulação e análise de dados tabulares;
- **Streamlit** — desenvolvimento da aplicação web;
- **Matplotlib** — geração de gráficos;
- **openpyxl** — leitura de arquivos Excel;
- **PyArrow** — armazenamento de dados processados em formato Parquet;
- **Poetry** — gerenciamento de dependências e ambiente virtual;
- **pytest** — testes automatizados;

---

## 📦 Gerenciamento de dependências

O projeto utiliza o [Poetry](https://python-poetry.org/) para gerenciamento do ambiente Python e das dependências.

### Requisitos

- Python `>= 3.11`
- Poetry

Confira as versões instaladas:

```bash
python --version
poetry --version
```

---

## 🚀 Instalação

Clone o repositório:

```bash
git clone <URL-DO-REPOSITORIO>
```

Entre na pasta:

```bash
cd crisp-edm-dashboard
```

Instale as dependências:

```bash
poetry install
```

O Poetry criará e configurará automaticamente o ambiente virtual do projeto.

Para verificar o ambiente:

```bash
poetry env info
```

---

## ⚙️ Processamento dos dados

Antes de iniciar o dashboard, os dados brutos precisam ser preparados.

Execute:

```bash
poetry run python scripts/process_all.py
```

Os arquivos tratados serão armazenados em:

```text
data/processed/
```

---

## ▶️ Executando o dashboard

Depois de processar os dados:

```bash
poetry run streamlit run app.py
```

O Streamlit iniciará um servidor local e apresentará um endereço semelhante a:

```text
http://localhost:8501
```

Acesse esse endereço pelo navegador.

---

## 🖥️ Organização da interface

A aplicação reúne todos os relatórios em uma única interface.

```text
🏠 Visão Geral

📊 GR13
   Situação Acadêmica

📚 GR14
   Aprovação e Reprovação

👥 GR16
   Perfil Discente

🚪 GR38
   Perfil dos Ingressantes

🧠 Metodologia
```

A ideia é evitar aplicações independentes para cada relatório e proporcionar uma navegação única e consistente.

---

## 📂 Dados

Os dados utilizados neste projeto têm origem em relatórios acadêmicos institucionais.

### ⚠️ Importante

Os dados institucionais reais **não são distribuídos neste repositório público**.

Por essa razão, os diretórios:

```text
data/raw/
data/interim/
data/processed/
```

não devem ser versionados no Git.

O arquivo `.gitignore` impede sua inclusão acidental no repositório.

No futuro, o projeto poderá disponibilizar um conjunto de **dados sintéticos ou anonimizados de demonstração**, permitindo executar a aplicação sem acesso aos dados institucionais.

---

## 🔐 Privacidade

O projeto foi concebido para trabalhar com dados acadêmicos agregados e evitar a utilização de identificadores pessoais dos estudantes.

O código-fonte pode ser disponibilizado publicamente sem que isso implique a publicação das bases institucionais utilizadas na análise.

---

## 📤 Resultados exportados

Além da visualização interativa, o projeto permite organizar resultados em:

```text
outputs/
├── tables/
└── figures/
```

### Tabelas

Exemplos:

```text
outputs/tables/gr13/
outputs/tables/gr14/
outputs/tables/gr16/
outputs/tables/gr38/
```

Esses arquivos poderão ser utilizados para:

- artigos científicos;
- relatórios;
- apresentações;
- análises institucionais.

### Figuras

Os gráficos também poderão ser exportados de forma independente:

```text
outputs/figures/
```

Isso evita a necessidade de capturar imagens manualmente diretamente do dashboard.

---

## 🧪 Testes

Os testes automatizados ficam disponíveis em:

```text
tests/
```

Para executá-los:

```bash
poetry run pytest
```

Os testes serão utilizados principalmente para verificar:

- cálculos de taxas;
- agregações;
- tratamento de valores ausentes;
- padronização das categorias;
- consistência dos totais;
- regras utilizadas na preparação dos dados.

---


## 👩‍💻 Autoria

**Leticia Zanellatto de Oliveira**

Projeto desenvolvido inicialmente no contexto de Iniciação Científica na **Universidade Estadual do Oeste do Paraná — UNIOESTE, Campus de Foz do Iguaçu**.

**Orientação:** Prof. Claudio Roberto Marquetto Mauricio

---


## 📄 Licença

A licença de software livre do projeto será definida antes da publicação da primeira versão estável.

---

<p align="center">
  Desenvolvido com Python, Streamlit e software livre. 🐧
</p>