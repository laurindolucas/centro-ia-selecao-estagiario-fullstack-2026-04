# DOCS.md

## Nome da solução

### UniCarona

---

## Problema escolhido

Muitos estudantes enfrentam ônibus lotados, pagam passagens caras e precisam lidar com riscos principalmente em horários noturnos.

Além do custo e da insegurança, muitas vezes existem outras pessoas fazendo trajetos muito parecidos, estudando na mesma instituição e saindo em horários próximos, mas sem uma forma fácil de se conectarem para dividir uma carona.

---

## Objetivo da aplicação

A aplicação tem como objetivo conectar estudantes com rotas semelhantes para facilitar a organização de caronas.

O sistema permite cadastrar usuários, registrar rotas e encontrar possíveis matches com base em:

* proximidade entre origem e destino;
* compatibilidade de horários;
* classificação inteligente de compatibilidade.

---

## Descrição do caso de uso

1. O usuário cria uma conta.
2. O usuário cadastra uma rota informando origem, destino e horário.
3. O sistema normaliza os endereços e obtém suas coordenadas.
4. O backend compara a rota cadastrada com outras rotas existentes.
5. O sistema calcula distância entre origem, destino e diferença de horário.
6. A IA classifica a compatibilidade entre as rotas.
7. O frontend exibe uma lista de possíveis caronas.
8. O usuário pode clicar em “Solicitar carona”.

---

## Tecnologias utilizadas

### Front-end

* React
* React Router DOM
* CSS
* Axios

### Back-end

* Python
* FastAPI
* SQLAlchemy
* SQLite
* Uvicorn
* Geopy
* Passlib
* bcrypt
* python-dotenv

### IA

* Groq API
* OpenAI SDK
* Modelo: llama-3.1-8b-instant

---

## Arquitetura geral da solução

A aplicação foi dividida em front-end e back-end.

### Front-end

Responsável pela interface do usuário.

Possui telas para:

* cadastro de usuário;
* cadastro de rota;
* visualização de matches;
* solicitação de carona.

### Back-end

Responsável pelas regras de negócio.

Possui serviços para:

* cadastro e autenticação de usuários;
* cadastro de rotas;
* cálculo de distâncias;
* normalização de endereços;
* cálculo de compatibilidade;
* integração com IA.

### Banco de dados

Foi utilizado SQLite para armazenar:

* usuários;
* rotas;
* matches.

---

## Instruções de instalação e execução

### Back-end

1. Criar ambiente virtual:

```bash
python -m venv .venv
```

2. Ativar ambiente virtual:

Windows:

```bash
.venv\Scripts\activate
```

3. Instalar dependências:

```bash
pip install -r requirements.txt
```

4. Criar arquivo `.env`:

```env
GROQ_API_KEY=sua_chave_aqui
```

5. Executar servidor:

```bash
uvicorn app.main:app --reload
```

### Front-end

1. Instalar dependências:

```bash
npm install
```

2. Executar aplicação:

```bash
npm run dev
```

---

## Explicação de como a IA foi integrada

A IA foi utilizada em dois pontos principais:

### 1. Normalização de endereços

Quando o usuário informa um local como “UNICAP”, a IA tenta converter para um endereço mais completo e padronizado.

Exemplo:

* Entrada: UNICAP
* Saída: Rua do Príncipe, 526, Boa Vista, Recife, Pernambuco

Isso melhora a qualidade do geocoding.

### 2. Classificação de compatibilidade

A IA recebe:

* distância entre origens;
* distância entre destinos;
* diferença de horário.

Com base nisso, retorna:

* classificação;
* score de compatibilidade;
* explicação textual.

Exemplo de retorno:

```json
{
  "classificacao": "alta",
  "score": 85,
  "explicacao": "Origens próximas e horários muito compatíveis"
}
```

Além da IA, foi implementado um fallback local para garantir que o sistema continue funcionando mesmo sem resposta da API.

---

## Exemplos de uso da aplicação

### Exemplo 1

Usuário A:

* Origem: Torreão
* Destino: UNICAP
* Horário: 07:00

Usuário B:

* Origem: Casa Amarela
* Destino: Boa Vista
* Horário: 07:15

Resultado:

* score alto;
* boa compatibilidade;
* sugestão de carona exibida.

### Exemplo 2

Usuário A:

* Origem: Recife
* Destino: Olinda
* Horário: 08:00

Usuário B:

* Origem: Jaboatão
* Destino: Paulista
* Horário: 10:00

Resultado:

* score baixo;
* baixa compatibilidade.

---

## Limitações atuais do MVP

* Não possui autenticação completa com login e token.
* Não possui chat entre usuários.
* Não existe confirmação real de solicitação de carona.
* O banco de dados é local.
* A IA depende de uma chave de API externa.
* Não há suporte para mapas em tempo real.
* Não existe histórico de caronas.

---

## Possíveis evoluções futuras

* Implementar autenticação JWT.
* Adicionar chat entre usuários.
* Criar sistema de avaliações.
* Integrar mapas com rotas em tempo real.
* Adicionar notificações.
* Permitir confirmação e cancelamento de caronas.
* Migrar banco local para PostgreSQL.
* Implementar deploy em nuvem.
* Melhorar o modelo de IA para analisar mais fatores, como preferências e frequência de uso.
* Adicionar integração com universidades e empresas.
