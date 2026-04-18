# UniCarona — Mobilidade Acadêmica Inteligente com IA

O UniCarona é uma plataforma FullStack desenvolvida para otimizar o transporte universitário através de conexões inteligentes. O sistema vai além de um simples mural de caronas, utilizando Inteligência Artificial e dados geoespaciais para calcular a compatibilidade real entre trajetos, promovendo uma mobilidade urbana mais eficiente, econômica e sustentável para a comunidade acadêmica.

---


## 1. Problema e Proposta de Valor

Estudantes e professores enfrentam diariamente a precarização do transporte público e os altos custos de deslocamento individual. O UniCarona resolve isso ao identificar padrões de deslocamento e sugerir conexões que minimizam desvios para motoristas e maximizam o conforto para passageiros.

---

## 2. Tecnologias e Ferramentas

### Backend (Engenharia e Lógica)

**Python 3.10+ / FastAPI:** Escolhido pela alta performance e suporte nativo a operações assíncronas.

**Geopy:** Biblioteca fundamental utilizada para geocodificação. Ela transforma endereços em texto livre em coordenadas de latitude e longitude, permitindo o cálculo matemático de distância entre rotas.

**SQLAlchemy + SQLite:** Persistência de dados robusta com mapeamento objeto-relacional (ORM), garantindo integridade referencial entre usuários e rotas.

**Pydantic:** Garantia de integridade de dados através de esquemas de validação rigorosos para as requisições da API.

### Frontend (Interface de Usuário)

**React + Vite:** Ecossistema moderno para uma Single Page Application (SPA) de alta velocidade e carregamento instantâneo.

**CSS Modular & Lucide Icons:** Interface limpa, responsiva e focada na usabilidade mobile.

### Inteligência Artificial

**Groq Cloud API (Llama 3.1-8B):** Processamento de linguagem natural para análise qualitativa. A IA interpreta os dados técnicos (distância e tempo) e gera um parecer humano sobre a viabilidade do match.

---

## 3. Arquitetura e Boas Práticas (SOLID)

O projeto segue padrões de engenharia de software para garantir que o MVP seja uma base sólida para um produto de produção:

**S (Single Responsibility):** Lógica de IA (`ai_service.py`), Geolocalização (`location_service.py`) e Regras de Negócio (`match_service.py`) são isoladas, facilitando a manutenção.

**D (Dependency Inversion):** O uso de injeção de dependência do FastAPI para sessões de banco de dados (`get_db`) permite que o sistema seja facilmente testável e desacoplado.

**Arquitetura em Camadas:** A separação clara entre Models, Schemas, Services e Routes evita o "código espaguete" e melhora a legibilidade para novos desenvolvedores.

---

## 4. O Motor de Inteligência e Geolocalização

A aplicação resolve o desafio de conexão entre usuários através de um pipeline inteligente que combina Modelos de Linguagem (LLM) e cálculos geodésicos. O fluxo funciona em três etapas críticas:

### A. Normalização Semântica de Endereços (IA - Camada 1)

Antes de qualquer cálculo, o sistema trata a entrada do usuário (que pode ser informal ou incompleta).

**Como funciona:** O `location_service.py` utiliza o modelo `llama-3.1-8b-instant` para converter termos como "UNICAP" ou "Rua 15 de nov, 10, SP" em endereços oficiais estruturados (ex: "Rua do Príncipe, 526, Boa Vista, Recife - PE").

**Valor Técnico:** Isso reduz drasticamente falhas de geocodificação causadas por erros de digitação ou nomes de locais populares que não constam em bases de mapas tradicionais.

**Segurança (Fallback):** Caso a IA retorne um dado inválido ou "lixo", o sistema possui uma trava de segurança que ignora a normalização e tenta usar o texto original, garantindo resiliência.

### B. Geocodificação e Cálculo de Distância (Geopy)

Com o endereço normalizado e "limpo", o sistema utiliza a biblioteca Geopy:

**Geocoding:** Transforma a string do endereço em coordenadas geográficas exatas (Latitude e Longitude).

**Cálculo Geodésico:** Utiliza a fórmula de `geodesic` para calcular a distância real em quilômetros entre a origem do motorista e a do passageiro, e o mesmo para o destino.

### C. Análise Cognitiva de Compatibilidade (IA - Camada 2)

Após obter as distâncias e a diferença de horário, o sistema aciona novamente a IA em `ai_service.py` para um julgamento qualitativo.

**Entrada de Dados:** A IA recebe o "Desvio na origem", "Desvio no destino" e a "Janela temporal".

**A Resposta da IA (JSON):** A inteligência retorna um objeto estruturado com:

- **Classificação:** `alta`, `média` ou `baixa`.
- **Score:** Um valor numérico de 0 a 100 baseado na eficiência logística.
- **Explicação Personalizada:** Um texto que começa com `[IA] Sugestão:`. Este texto utiliza terminologia técnica (ex: "convergência de trajeto") de forma didática para explicar ao usuário por que aquela carona é viável.

---

## 5. Instruções de Instalação e Execução

### Backend

```bash
cd uniCarona/backend
python -m venv venv
pip install -r requirements.txt
# Configure sua GROQ_API_KEY no arquivo .env
uvicorn app.main:app --reload
```

### Frontend

```bash
cd uniCarona/frontend
npm install
npm run dev
```

---

## 6. Limitações Atuais do MVP

Como toda solução em estágio inicial, o UniCarona possui limitações que focam no equilíbrio entre funcionalidade e prazo de entrega:

**Geolocalização Estática:** A análise é baseada nos pontos de origem/destino e não no trajeto completo da via (ruas e avenidas).

**Persistência Simples:** Uso de SQLite, que é ideal para desenvolvimento e testes, mas precisaria de um PostgreSQL para alta escala.

**Autenticação:** O sistema foca no fluxo de negócio de caronas; a implementação de segurança JWT e criptografia de senhas é simplificada para este MVP.

**Dependência de API Externa:** A precisão do match depende da disponibilidade das APIs do Groq e do serviço de geocodificação.

---

## 7. Evoluções Planejadas e Roadmap

O UniCarona possui um caminho claro para se tornar um ecossistema completo:

**Integração Nativa com Maps:** Implementação de uma interface de mapa interativo (Google Maps ou Leaflet) para que o usuário veja visualmente onde o motorista passará.

**Chatbot Comunitário:** Um agente de IA focado em resolver conflitos, sugerir pontos de encontro seguros e responder dúvidas sobre as regras da comunidade.

**Histórico e Gamificação:** Criação de um dashboard com o histórico de viagens, economia de combustível acumulada e um sistema de "medalhas" para bons motoristas.

**Interação em Tempo Real:** Uso de WebSockets para que o passageiro receba uma notificação instantânea assim que um match for encontrado pela IA.

**Segurança Reforçada:** Integração com APIs de verificação estudantil (ex: e-mail .unicap) para garantir que apenas membros da universidade utilizem o app.

---

Desenvolvido por: Caio Laurindo  
Desafio Técnico: Seleção de Estágio Dev FullStack (04/2026)
