# UniCarona — Mobilidade Acadêmica com IA

O UniCarona é uma plataforma FullStack desenvolvida para otimizar o transporte universitário através de conexões inteligentes. O sistema vai além de um simples mural de caronas, utilizando Inteligência Artificial e dados geoespaciais para calcular a compatibilidade real entre trajetos, promovendo uma mobilidade urbana mais eficiente, econômica e sustentável para a comunidade acadêmica.

---

## Sumário

1. [Problema Escolhido](#1-problema-escolhido)
2. [Objetivo da Aplicação](#2-objetivo-da-aplicação)
3. [Descrição do Caso de Uso](#3-descrição-do-caso-de-uso)
4. [Tecnologias Utilizadas](#4-tecnologias-utilizadas)
5. [Arquitetura Geral da Solução](#5-arquitetura-geral-da-solução)
6. [Integração com Inteligência Artificial](#6-integração-com-inteligência-artificial)
7. [Instruções de Instalação e Execução](#7-instruções-de-instalação-e-execução)
8. [Exemplos de Uso da Aplicação](#8-exemplos-de-uso-da-aplicação)
9. [Limitações Atuais do MVP](#9-limitações-atuais-do-mvp)
10. [Possíveis Evoluções Futuras](#10-possíveis-evoluções-futuras)

---

## 1. Problema Escolhido

Estudantes enfrentam diariamente a precarização do transporte público e os altos custos de deslocamento individual. Soluções existentes como grupos de WhatsApp ou murais físicos são descentralizadas, ineficientes e não consideram a compatibilidade real entre trajetos — resultando em combinações que exigem grandes desvios de rota ou diferenças de horário incompatíveis.

O UniCarona resolve isso ao identificar padrões de deslocamento e sugerir conexões que minimizam desvios para motoristas e maximizam o conforto para passageiros, utilizando cálculo geodésico e análise qualitativa por IA.

---

## 2. Objetivo da Aplicação

Criar uma plataforma de caronas universitárias que, diferente de um simples mural, calcule a **compatibilidade real entre rotas** de dois usuários — considerando distância geográfica entre origens, distância entre destinos e janela temporal — e apresente ao usuário uma explicação gerada por IA sobre a viabilidade do match.

---

## 3. Descrição do Caso de Uso

O fluxo principal da aplicação percorre as seguintes etapas:

**1. Cadastro do usuário**
O usuário acessa a aplicação e preenche nome, e-mail, senha, uma breve descrição e seleciona seu perfil: motorista ou passageiro. O cadastro é feito via `POST /users` e o `id` retornado é armazenado no `localStorage` do navegador para uso nas etapas seguintes.

**2. Onboarding**
Após o cadastro, o usuário é direcionado à tela de Story, que explica o funcionamento da plataforma em quatro passos: criar rota, encontrar matches, escolher a carona e combinar o trajeto.

**3. Criação de rota**
O usuário informa o endereço de origem, o endereço de destino e o horário desejado. O frontend envia esses dados via `POST /rotas`. O backend, ao receber a requisição, aciona o `location_service.py` que primeiro normaliza os endereços via IA e em seguida obtém as coordenadas geográficas (latitude e longitude) via Geopy. As coordenadas são persistidas junto à rota no banco de dados.

**4. Busca de matches**
Com o `id` da rota recém-criada, o frontend redireciona o usuário para a tela de matches e executa `GET /matches/{rota_id}`. O backend percorre todas as rotas cadastradas por outros usuários e, para cada uma, calcula a distância entre origens, entre destinos e a diferença de horário. Rotas com desvio superior a 5 km em qualquer ponto são descartadas automaticamente.

**5. Análise por IA e exibição de resultados**
Para cada rota que passa pelo filtro de distância, o `ai_service.py` é acionado. A IA recebe os dados numéricos e retorna um objeto JSON com classificação (`alta`, `média` ou `baixa`), score de 0 a 100 e uma explicação textual personalizada. Os resultados são ordenados pelo score e os cinco melhores são retornados ao frontend.

**6. Solicitação de carona**
O usuário visualiza os matches com todos os detalhes (nome do usuário, rota, horário, distâncias e análise da IA) e pode clicar em "Solicitar carona", que exibe uma confirmação modal informando que a conexão foi estabelecida.

---

## 4. Tecnologias Utilizadas

### Backend

**Python 3.10+ / FastAPI:** Escolhido pela alta performance e suporte nativo a operações assíncronas.

**Geopy (Nominatim):** Biblioteca utilizada para geocodificação. Transforma endereços em texto livre em coordenadas de latitude e longitude, permitindo o cálculo matemático de distância entre rotas.

**SQLAlchemy + SQLite:** Persistência de dados com mapeamento objeto-relacional (ORM), garantindo integridade referencial entre as entidades `Usuario` e `Rota`.

**Pydantic:** Validação de dados de entrada através dos schemas `UserCreate` e `RideCreate`.

**Passlib (bcrypt):** Hash de senhas dos usuários com truncamento seguro em 72 caracteres.

**python-dotenv:** Carregamento de variáveis de ambiente, incluindo a `GROQ_API_KEY`.

### Frontend

**React 19 + Vite 8:** SPA moderna com carregamento instantâneo e React Compiler habilitado para otimizações automáticas.

**React Router DOM v7:** Gerenciamento de rotas com as páginas `Splash`, `Cadastro`, `Story`, `CriarRota` e `Matches`.

**React Icons:** Ícones de interface (BiCar, BiUser) utilizados na seleção de perfil.

**CSS Modular por página:** Cada página possui seu próprio arquivo `.css` com variáveis de design consistentes (tema escuro com cor de destaque `#6c63ff`).

### Inteligência Artificial

**Groq Cloud API (Llama 3.1-8B — `llama-3.1-8b-instant`):** Utilizado em duas frentes: normalização semântica de endereços e análise qualitativa de compatibilidade de rotas. Acessado via cliente OpenAI-compatible apontando para `https://api.groq.com/openai/v1`.

---

## 5. Arquitetura Geral da Solução

### Estrutura de pastas

```
uniCarona/
├── backend/
│   ├── app/
│   │   └── main.py              # Entrada da aplicação FastAPI, CORS e registro de rotas
│   ├── database/
│   │   └── connection.py        # Engine SQLAlchemy, SessionLocal e Base
│   ├── models/
│   │   └── models.py            # Entidades: Usuario e Rota
│   ├── schemas/
│   │   └── schemas.py           # Contratos de entrada: UserCreate e RideCreate
│   ├── services/
│   │   ├── ai_service.py        # Análise de compatibilidade via Groq + fallback local
│   │   ├── location_service.py  # Normalização de endereços via IA + geocodificação Geopy
│   │   ├── match_service.py     # Regras de negócio do match e orquestração do pipeline
│   │   ├── ride_service.py      # CRUD de rotas com geocodificação automática
│   │   └── user_service.py      # CRUD de usuários com hash de senha
│   └── routes/
│       ├── user_routes.py       # POST /users, GET/PUT/DELETE /users/{id}
│       ├── ride_routes.py       # POST /rotas, GET/PUT/DELETE /rotas e /rotas/{id}
│       └── match_routes.py      # GET /matches/{rota_id}
│
└── frontend/
    └── src/
        ├── App.jsx              # Definição de rotas com React Router
        ├── main.jsx             # Ponto de entrada React
        ├── services/
        │   └── api.js           # Funções de acesso à API: criarUsuario, criarRota, buscarMatches
        └── page/
            ├── Splash.jsx       # Tela de carregamento com redirecionamento automático (2s)
            ├── Cadastro.jsx     # Formulário de cadastro com seleção de perfil
            ├── Story.jsx        # Onboarding explicando o fluxo da plataforma
            ├── CriarRota.jsx    # Formulário de origem, destino e horário
            └── Matches.jsx      # Exibição dos matches com análise da IA e modal de solicitação
```

### Endpoints da API

| Método | Endpoint | Descrição |
|---|---|---|
| `POST` | `/users` | Cria um novo usuário com hash de senha |
| `GET` | `/users/{id}` | Retorna dados de um usuário |
| `PUT` | `/users/{id}` | Atualiza dados de um usuário |
| `DELETE` | `/users/{id}` | Remove um usuário |
| `POST` | `/rotas` | Cria uma rota geocodificando automaticamente os endereços |
| `GET` | `/rotas` | Lista todas as rotas cadastradas |
| `GET` | `/rotas/{id}` | Retorna uma rota específica |
| `PUT` | `/rotas/{id}` | Atualiza uma rota com nova geocodificação |
| `DELETE` | `/rotas/{id}` | Remove uma rota |
| `GET` | `/matches/{rota_id}` | Retorna os 5 melhores matches com análise de IA |

### Princípios de Engenharia (SOLID)

**S (Single Responsibility):** Cada serviço possui responsabilidade única e isolada. `ai_service.py` cuida exclusivamente da análise de compatibilidade, `location_service.py` da normalização e geocodificação, e `match_service.py` da orquestração das regras de negócio.

**D (Dependency Inversion):** O uso de `SessionLocal` injetado em cada operação de banco de dados permite que as sessões sejam abertas e fechadas de forma controlada, desacoplando a lógica de negócio da camada de persistência.

**Arquitetura em Camadas:** A separação clara entre Models, Schemas, Services e Routes evita acoplamento indevido e melhora a legibilidade para novos desenvolvedores.

---

## 6. Integração com Inteligência Artificial

A IA é utilizada em duas etapas distintas do pipeline, ambas via Groq Cloud API com o modelo `llama-3.1-8b-instant`.

### Etapa 1 — Normalização Semântica de Endereços (`location_service.py`)

Antes de qualquer cálculo, o sistema trata a entrada do usuário, que frequentemente é informal ou incompleta.

**Como funciona:** O `location_service.py` envia o endereço digitado para o modelo com um prompt que instrui a IA a retornar apenas o endereço oficial estruturado, sem explicações ou saudações. A temperatura é configurada em `0.1` para máxima precisão.

```
Entrada:  "UNICAP"
Saída IA: "Rua do Príncipe, 526, Boa Vista, Recife - PE"
```

**Mecanismo de fallback:** A resposta da IA é validada contra uma lista de palavras negativas (`"infelizmente"`, `"desculpe"`, `"não posso"`) e contra um limite de tamanho (150 caracteres). Se a validação falhar, o sistema ignora a normalização e usa o texto original. Se o endereço normalizado também não retornar coordenadas, o sistema tenta o texto original uma segunda vez.

### Etapa 2 — Análise Cognitiva de Compatibilidade (`ai_service.py`)

Após calcular as distâncias geodésicas e a diferença de horário, o sistema aciona novamente a IA para um julgamento qualitativo.

**Entrada da IA:** Desvio na origem (km), desvio no destino (km) e diferença de horário (minutos).

**Configuração do prompt:** A IA recebe o papel de especialista em logística urbana, com regras de negócio explícitas (priorizar convergência de trajeto, janela temporal ideal abaixo de 30 minutos) e instrução obrigatória de que a explicação deve começar com o prefixo `[IA] Sugestão:`. A temperatura é `0.3` para respostas consistentes mas com variação natural no texto.

**Resposta esperada (JSON):**

```json
{
  "classificacao": "alta",
  "score": 85,
  "explicacao": "[IA] Sugestão: A convergência de trajeto entre as origens é excelente, com apenas 0.4 km de desvio, e a janela temporal de 12 minutos está bem dentro do ideal para uma carona confortável."
}
```

**Cache de resultados:** O `ai_service.py` implementa um cache em memória (`cache_resultados`) com chave composta por `dist_origem`, `dist_destino` e `diferenca_horario` arredondados. Chamadas idênticas não acionam a API novamente.

**Fallback local:** Caso a API do Groq esteja indisponível ou retorne dado inválido, o `ai_service.py` possui uma função `calcular_compatibilidade_local` que replica a lógica de scoring puramente em Python, sem dependência externa, garantindo que o sistema nunca deixe de retornar um resultado.

---

## 7. Instruções de Instalação e Execução

### Pré-requisitos

- Python 3.10 ou superior
- Node.js 20.19.0 ou superior (exigido pelo Vite 8)
- Chave de API do Groq Cloud (`GROQ_API_KEY`)

### Backend

```bash
# 1. Acesse o diretório do backend
cd uniCarona/backend

# 2. Crie e ative o ambiente virtual
python -m venv venv

# Linux / macOS
source venv/bin/activate

# Windows
venv\Scripts\activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure a variável de ambiente
# Crie um arquivo .env na raiz do backend com o seguinte conteúdo:
# GROQ_API_KEY=sua_chave_aqui

# 5. Execute o servidor
uvicorn app.main:app --reload
```

O backend estará disponível em `http://127.0.0.1:8000`.
A documentação interativa da API (Swagger) estará em `http://127.0.0.1:8000/docs`.

Para verificar se a integração com o Groq está funcionando antes de subir o servidor:

```bash
python teste_groq.py
# Saída esperada: funcionando
```

### Frontend

```bash
# 1. Acesse o diretório do frontend
cd uniCarona/frontend

# 2. Instale os pacotes
npm install

# 3. Inicie o servidor de desenvolvimento
npm run dev
```

O frontend estará disponível em `http://localhost:5173`.

> O frontend consome a API no endereço `http://127.0.0.1:8000`. Certifique-se de que o backend está em execução antes de utilizar a interface.

---

## 8. Exemplos de Uso da Aplicação

### Exemplo 1 — Cadastro de usuário via API

**Requisição:**

```http
POST /users
Content-Type: application/json

{
  "nome": "Ana Lima",
  "email": "ana.lima@unicap.br",
  "descricao": "Estudante de Direito, saio de Casa Amarela todos os dias",
  "senha": "minhasenha123",
  "tipo": "passageiro"
}
```

**Resposta:**

```json
{
  "id": 1,
  "nome": "Ana Lima",
  "email": "ana.lima@unicap.br",
  "descricao": "Estudante de Direito, saio de Casa Amarela todos os dias",
  "tipo": "passageiro"
}
```

---

### Exemplo 2 — Criação de rota com geocodificação automática

**Requisição:**

```http
POST /rotas
Content-Type: application/json

{
  "usuario_id": 1,
  "origem": "Casa Amarela, Recife",
  "destino": "UNICAP",
  "horario": "07:30"
}
```

O backend normaliza `"UNICAP"` para `"Rua do Príncipe, 526, Boa Vista, Recife - PE"` via IA, obtém as coordenadas e persiste a rota.

**Resposta:**

```json
{
  "id": 3,
  "usuario_id": 1,
  "origem": "Casa Amarela, Recife",
  "destino": "UNICAP",
  "horario": "07:30",
  "lat_origem": -8.0272,
  "lon_origem": -34.9181,
  "lat_destino": -8.0564,
  "lon_destino": -34.9193
}
```

---

### Exemplo 3 — Busca de matches com análise de IA

**Requisição:**

```http
GET /matches/3
```

**Resposta (fragmento do primeiro resultado):**

```json
[
  {
    "rota_id": 7,
    "usuario_id": 2,
    "nome_usuario": "Carlos Mendes",
    "origem": "Dois Irmãos, Recife",
    "destino": "UNICAP",
    "horario": "07:45",
    "dist_origem_km": 0.83,
    "dist_destino_km": 0.21,
    "diferenca_horario_min": 15,
    "score_backend": 100,
    "score_ia": 92,
    "classificacao": "alta",
    "explicacao": "[IA] Sugestão: A convergência de trajeto é excelente — origens separadas por menos de 1 km e destinos praticamente idênticos. A janela temporal de 15 minutos está dentro do ideal, tornando esta uma das combinações mais eficientes possíveis."
  }
]
```

---

### Exemplo 4 — Fluxo completo pela interface

1. Ao acessar a aplicação, a tela de Splash exibe o logo por 2 segundos e redireciona para o cadastro.
2. O usuário preenche o formulário e seleciona seu perfil (motorista ou passageiro) clicando nos cartões de seleção.
3. Após o cadastro, é exibida a tela de onboarding (Story) com os quatro passos do fluxo.
4. Na tela de criação de rota, o usuário informa origem (`"Casa Amarela"`), destino (`"UNICAP"`) e horário (`07:30`).
5. Ao clicar em "Buscar caronas", a aplicação cria a rota e redireciona para `/matches/3`.
6. Os cards de match são exibidos com nome do usuário, distância em metros, diferença de horário, score percentual com indicação visual de cor (verde para alta, amarelo para média, vermelho para baixa) e a explicação da IA.
7. Ao clicar em "Solicitar carona", um modal confirma que a solicitação foi enviada.

---

## 9. Limitações Atuais do MVP

**Geolocalização Estática:** A análise é baseada nos pontos de origem e destino e não no trajeto completo da via (ruas e avenidas). Dois usuários podem ter origens próximas, mas caminhos naturais muito divergentes.

**Persistência Simples:** Uso de SQLite, ideal para desenvolvimento e testes, mas que precisaria ser substituído por PostgreSQL em um cenário de alta escala ou múltiplos acessos simultâneos.

**Autenticação Simplificada:** O sistema possui hash de senha com bcrypt, mas não implementa autenticação por token (JWT). O `user_id` é armazenado no `localStorage` do navegador sem proteção de sessão.

**Sem Verificação de Vínculo Universitário:** Qualquer pessoa pode se cadastrar. Não há validação de e-mail institucional ou integração com sistemas da universidade.

**Dependência de APIs Externas:** A precisão do match depende da disponibilidade da API do Groq e do serviço de geocodificação Nominatim. Ambos possuem limites de requisição que podem impactar o desempenho em uso intensivo.

**Comunicação entre Usuários:** O botão "Solicitar carona" exibe apenas um modal de confirmação. Não existe um canal de comunicação real entre os usuários dentro da plataforma.

---

## 10. Possíveis Evoluções Futuras

**Integração Nativa com Maps:** Implementação de uma interface de mapa interativo (Google Maps ou Leaflet) para que o usuário visualize onde o motorista passará e confirme o ponto de encontro.

**Chatbot Comunitário:** Um agente de IA focado em resolver conflitos, sugerir pontos de encontro seguros e responder dúvidas sobre as regras da comunidade.

**Histórico e Gamificação:** Dashboard com histórico de viagens, economia de combustível acumulada e um sistema de medalhas para bons motoristas.

**Interação em Tempo Real:** Uso de WebSockets para que o passageiro receba notificação instantânea assim que um match for encontrado pela IA.

**Segurança Reforçada:** Autenticação via JWT, integração com APIs de verificação estudantil (e-mail `.edu`) e proteção de rotas privadas no frontend.

**Cálculo de Trajeto Real:** Substituição do cálculo geodésico simples por integração com APIs de rotas (Google Directions ou OSRM) para considerar o percurso real pelas vias.

---

Desenvolvido por: Caio Laurindo
Desafio Técnico: Seleção de Estágio Dev FullStack (04/2026)
