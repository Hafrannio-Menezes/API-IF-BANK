# if Bank API

Backend REST para um projeto bancario academico/profissional, construido com Django, Django REST Framework e PostgreSQL, com foco em organizacao modular, separacao por dominio, documentacao automatica e base pronta para evolucao.

## Sumario

- [Visao geral](#visao-geral)
- [Stack](#stack)
- [Arquitetura](#arquitetura)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Dominios e models principais](#dominios-e-models-principais)
- [Configuracao de ambiente](#configuracao-de-ambiente)
- [Instalacao](#instalacao)
- [Rodando o projeto](#rodando-o-projeto)
- [Documentacao da API](#documentacao-da-api)
- [Guia rapido para apresentar e testar](#guia-rapido-para-apresentar-e-testar)
- [Endpoints principais](#endpoints-principais)
- [Exemplos de uso](#exemplos-de-uso)
- [Testes](#testes)
- [Admin](#admin)
- [Proximos passos](#proximos-passos)

## Visao geral

O projeto cobre os seguintes dominios:

- autenticacao e perfil de usuarios
- contas bancarias
- depositos, saques, transferencias e extrato
- catalogo de investimentos, carteira, aplicacoes, resgates e simulacoes
- metas financeiras
- notificacoes do usuario

## Stack

- Python 3
- Django
- Django REST Framework
- PostgreSQL
- Django ORM
- JWT com `djangorestframework-simplejwt`
- OpenAPI/Swagger com `drf-spectacular`
- CORS com `django-cors-headers`
- variaveis de ambiente com `.env`

## Arquitetura

Fluxo macro da aplicacao:

`Frontend/App -> DRF Views -> Services -> Selectors/Validators -> Django ORM -> PostgreSQL`

Principios aplicados:

- separacao por dominio de negocio
- views enxutas
- regras criticas em services
- consultas em selectors
- validacoes especificas em validators
- permissoes por ownership
- settings separados por ambiente
- versionamento da API em `/api/v1/`

## Estrutura do projeto

```text
api_ifbank/
|-- manage.py
|-- README.md
|-- requirements.txt
|-- .env.example
|-- iniciar_if_bank.cmd
|-- iniciar_if_bank.ps1
|-- config/
|   |-- urls.py
|   |-- asgi.py
|   |-- wsgi.py
|   `-- settings/
|       |-- base.py
|       |-- dev.py
|       |-- prod.py
|       `-- test.py
|-- common/
|   |-- exceptions/
|   |-- pagination/
|   |-- permissions/
|   |-- utils/
|   |-- mixins/
|   `-- choices/
|-- data/
|   |-- demo/
|   `-- reference/
`-- apps/
    |-- users/
    |-- accounts/
    |-- transactions/
    |-- investments/
    |-- goals/
    `-- notifications/
```

Cada app foi preparado para crescer com:

- `models/`
- `serializers/`
- `views/`
- `services/`
- `selectors/`
- `permissions/`
- `validators/`
- `urls/`
- `tests/`
- `migrations/`

## Dominios e models principais

### `users`

- `User`
  - `full_name`
  - `email`
  - `cpf`
  - `phone`
  - `birth_date`
  - `created_at`
  - `updated_at`

### `accounts`

- `BankAccount`
  - `user`
  - `agency_number`
  - `account_number`
  - `account_type`
  - `balance`
  - `is_active`
  - `created_at`
  - `updated_at`

### `transactions`

- `Transaction`
  - `account`
  - `destination_account`
  - `transaction_type`
  - `amount`
  - `description`
  - `status`
  - `reference_code`
  - `balance_after`
  - `created_at`

### `investments`

- `InvestmentProduct`
- `PortfolioPosition`
- `InvestmentTransaction`

### `goals`

- `FinancialGoal`
  - `user`
  - `title`
  - `target_amount`
  - `current_amount`
  - `deadline`
  - `status`
  - `created_at`
  - `updated_at`

### `notifications`

- `Notification`
  - `user`
  - `title`
  - `message`
  - `notification_type`
  - `is_read`
  - `created_at`

## Configuracao de ambiente

Crie o arquivo `.env` a partir de `.env.example`.

Exemplo:

```env
DJANGO_ENV=development
DEBUG=True
SECRET_KEY=change-me-with-at-least-32-characters-for-jwt-signing
ALLOWED_HOSTS=127.0.0.1,localhost
CSRF_TRUSTED_ORIGINS=http://127.0.0.1:8000,http://localhost:8000

POSTGRES_DB=if_bank
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
DB_CONN_MAX_AGE=60

CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
CORS_ALLOW_ALL_ORIGINS=False

ACCESS_TOKEN_LIFETIME_MINUTES=30
REFRESH_TOKEN_LIFETIME_DAYS=1
LOG_LEVEL=INFO
```

## Instalacao

### 1. Criar ambiente virtual

```bash
python -m venv .venv
```

### 2. Ativar ambiente virtual

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Criar banco PostgreSQL

Crie um banco chamado `if_bank` ou ajuste os valores do `.env` conforme seu ambiente.

## Rodando o projeto

### Opcao 1. Subir tudo com um comando

Recomendado para demonstracao rapida:

```powershell
.\iniciar_if_bank.cmd
```

Esse script:

- cria a `.venv` se faltar
- instala dependencias
- verifica o ambiente
- roda `migrate`
- carrega o catalogo de investimentos
- carrega os dados de demonstracao
- sobe o servidor

### Opcao 2. Rodar manualmente

#### Ambiente de desenvolvimento com PostgreSQL

```bash
python manage.py migrate --settings=config.settings.dev
python manage.py sync_investment_products --settings=config.settings.dev
python manage.py load_presentation_data --settings=config.settings.dev
python manage.py runserver 127.0.0.1:8000 --settings=config.settings.dev
```

#### Ambiente de testes local com SQLite

```bash
python manage.py migrate --settings=config.settings.test
python manage.py sync_investment_products --settings=config.settings.test
python manage.py load_presentation_data --settings=config.settings.test
python manage.py runserver 127.0.0.1:8000 --settings=config.settings.test
```

### Criar superusuario

```bash
python manage.py createsuperuser --settings=config.settings.dev
```

### Checagem de deploy

```bash
python manage.py check --deploy --settings=config.settings.prod
```

## Documentacao da API

Depois de subir o servidor, use:

- Swagger UI: `GET /api/schema/swagger/`
- Schema OpenAPI: `GET /api/schema/`
- Healthcheck: `GET /health/`

Links locais:

- `http://127.0.0.1:8000/api/schema/swagger/`
- `http://127.0.0.1:8000/api/schema/`
- `http://127.0.0.1:8000/health/`

## Guia rapido para apresentar e testar

### Usuarios de demonstracao

- `alice.demo@ifbank.local` / `SenhaForte123!`
- `bruno.demo@ifbank.local` / `SenhaForte456!`

### Ordem recomendada da apresentacao

#### 1. Provar que a API esta no ar

Abrir:

- `GET /health/`

Explique:

- a API esta online
- o banco esta acessivel

#### 2. Mostrar como registrar um usuario

Abrir:

- `POST /api/v1/auth/register/`

JSON:

```json
{
  "full_name": "Usuario Apresentacao",
  "email": "usuario.apresentacao@ifbank.local",
  "password": "SenhaForte123!",
  "password_confirm": "SenhaForte123!",
  "cpf": "39053344705",
  "phone": "11999990011",
  "birth_date": "1999-01-10"
}
```

Explique:

- esse endpoint cria um novo usuario
- ele e publico porque o usuario ainda nao tem token
- existe limitacao de requisicoes para evitar abuso

#### 3. Fazer login

Abrir:

- `POST /api/v1/auth/login/`

JSON:

```json
{
  "email": "alice.demo@ifbank.local",
  "password": "SenhaForte123!"
}
```

Explique:

- o login devolve `access` e `refresh`
- o `access` sera usado nas rotas protegidas

#### 4. Autorizar no Swagger

1. Copie o token `access`
2. Clique em `Authorize`
3. Cole o token
4. Confirme

#### 5. Mostrar perfil

- `GET /api/v1/auth/profile/`
- `PATCH /api/v1/auth/profile/`

JSON de exemplo:

```json
{
  "phone": "11999990099"
}
```

#### 6. Listar contas

- `GET /api/v1/accounts/`

Explique:

- cada usuario ve apenas as proprias contas
- aqui voce pega o `account_id` para os proximos testes

#### 7. Criar conta bancaria

- `POST /api/v1/accounts/`

```json
{
  "account_type": "checking",
  "initial_balance": "500.00"
}
```

Explique:

- a conta e criada vinculada ao usuario autenticado
- agencia e numero da conta sao gerados
- o saldo inicial gera registro de auditoria

#### 8. Consultar saldo

- `GET /api/v1/accounts/{account_id}/balance/`

#### 9. Fazer deposito

- `POST /api/v1/transactions/deposit/`

```json
{
  "account_id": 1,
  "amount": "100.00",
  "description": "deposito de apresentacao"
}
```

#### 10. Fazer saque

- `POST /api/v1/transactions/withdraw/`

```json
{
  "account_id": 1,
  "amount": "50.00",
  "description": "saque de apresentacao"
}
```

#### 11. Mostrar extrato

- `GET /api/v1/transactions/statement/?account_id=1`

#### 12. Fazer transferencia

- `POST /api/v1/transactions/transfer/`

```json
{
  "source_account_id": 1,
  "destination_account_id": 2,
  "amount": "75.00",
  "description": "transferencia de apresentacao"
}
```

Explique:

- a transferencia e atomica
- origem e destino sao validados
- nao e permitido transferir para a mesma conta

#### 13. Mostrar produtos de investimento

- `GET /api/v1/investments/products/`

#### 14. Mostrar simulacao

- `POST /api/v1/investments/simulate/`

```json
{
  "initial_amount": "1000.00",
  "annual_rate": "12.00",
  "period_months": 12,
  "monthly_amount": "100.00"
}
```

#### 15. Mostrar carteira e historico

- `GET /api/v1/investments/portfolio/`
- `GET /api/v1/investments/history/`

#### 16. Aplicar investimento

- `POST /api/v1/investments/apply/`

```json
{
  "account_id": 1,
  "product_id": 1,
  "amount": "300.00"
}
```

#### 17. Explicar resgate

- `POST /api/v1/investments/redeem/`

Use mais para explicar a regra de negocio:

- o resgate nao pode passar do saldo investido
- a carencia do produto e validada

#### 18. Mostrar metas

- `GET /api/v1/goals/`
- `POST /api/v1/goals/`
- `PATCH /api/v1/goals/{goal_id}/`
- `DELETE /api/v1/goals/{goal_id}/`

JSON de criacao:

```json
{
  "title": "Notebook novo",
  "target_amount": "4500.00",
  "current_amount": "800.00",
  "deadline": "2027-12-01"
}
```

JSON de atualizacao:

```json
{
  "current_amount": "1200.00"
}
```

#### 19. Mostrar notificacoes

- `GET /api/v1/notifications/`
- `POST /api/v1/notifications/{notification_id}/read/`

### O que pode ser excluido e o que nao pode

Existe `DELETE` para:

- metas

Nao existe `DELETE` para:

- conta bancaria
- usuario

Como explicar isso:

- em contexto bancario, apagar conta ou usuario fisicamente nem sempre e desejavel
- o mais comum seria desativacao ou encerramento com trilha de auditoria

### Ordem curta se o tempo estiver apertado

1. `GET /health/`
2. `POST /api/v1/auth/login/`
3. `Authorize` no Swagger
4. `GET /api/v1/accounts/`
5. `POST /api/v1/accounts/`
6. `GET /api/v1/accounts/{account_id}/balance/`
7. `POST /api/v1/transactions/deposit/`
8. `GET /api/v1/transactions/statement/`
9. `POST /api/v1/investments/simulate/`
10. `GET /api/v1/goals/`
11. `GET /api/v1/notifications/`

### Frases curtas para explicar o projeto

- A API esta organizada por dominio.
- As views estao enxutas e a regra de negocio esta em services.
- A autenticacao principal e JWT.
- O usuario autenticado acessa apenas os proprios dados.
- A documentacao e automatica com Swagger e OpenAPI.
- O projeto esta preparado para integracao com frontend web ou mobile.

## Endpoints principais

### Autenticacao

- `POST /api/v1/auth/register/`
- `POST /api/v1/auth/login/`
- `POST /api/v1/auth/refresh/`
- `GET /api/v1/auth/profile/`
- `PATCH /api/v1/auth/profile/`

### Contas

- `GET /api/v1/accounts/`
- `POST /api/v1/accounts/`
- `GET /api/v1/accounts/{id}/`
- `GET /api/v1/accounts/{id}/balance/`

### Transacoes

- `POST /api/v1/transactions/deposit/`
- `POST /api/v1/transactions/withdraw/`
- `POST /api/v1/transactions/transfer/`
- `GET /api/v1/transactions/statement/`

### Investimentos

- `GET /api/v1/investments/products/`
- `GET /api/v1/investments/portfolio/`
- `POST /api/v1/investments/apply/`
- `POST /api/v1/investments/redeem/`
- `GET /api/v1/investments/history/`
- `POST /api/v1/investments/simulate/`

### Metas

- `GET /api/v1/goals/`
- `POST /api/v1/goals/`
- `GET /api/v1/goals/{id}/`
- `PATCH /api/v1/goals/{id}/`
- `DELETE /api/v1/goals/{id}/`

### Notificacoes

- `GET /api/v1/notifications/`
- `POST /api/v1/notifications/{id}/read/`

## Exemplos de uso

### Registro

```http
POST /api/v1/auth/register/
Content-Type: application/json

{
  "full_name": "Maria Souza",
  "email": "maria@ifbank.com",
  "password": "StrongPass123",
  "password_confirm": "StrongPass123",
  "cpf": "39053344705",
  "phone": "+55 11 99999-9999",
  "birth_date": "1998-04-10"
}
```

Resposta:

```json
{
  "id": 1,
  "full_name": "Maria Souza",
  "email": "maria@ifbank.com",
  "cpf": "39053344705",
  "phone": "+55 11 99999-9999",
  "birth_date": "1998-04-10",
  "created_at": "2026-03-19T18:00:00Z",
  "updated_at": "2026-03-19T18:00:00Z",
  "tokens": {
    "refresh": "<jwt-refresh>",
    "access": "<jwt-access>"
  }
}
```

### Criar conta

```http
POST /api/v1/accounts/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "account_type": "CHECKING",
  "initial_balance": "1000.00"
}
```

### Depositar

```http
POST /api/v1/transactions/deposit/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "account_id": 1,
  "amount": "200.00",
  "description": "Deposito inicial"
}
```

### Simular investimento

```http
POST /api/v1/investments/simulate/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "initial_amount": "1000.00",
  "annual_rate": "12.00",
  "period_months": 12,
  "monthly_contribution": "100.00"
}
```

Resposta:

```json
{
  "initial_amount": "1000.00",
  "annual_rate": "12.0000",
  "period_months": 12,
  "monthly_contribution": "100.00",
  "invested_capital": "2200.00",
  "estimated_return": "204.17",
  "final_amount": "2404.17"
}
```

## Testes

Testes iniciais implementados:

- autenticacao
- criacao de conta
- deposito
- saque
- transferencia
- criacao de meta
- simulacao de investimento
- carga do catalogo de investimentos
- carga de dados de apresentacao

Executar:

```bash
python manage.py test --settings=config.settings.test
```

Observacoes:

- o projeto usa PostgreSQL na configuracao principal
- `config.settings.test` usa SQLite apenas para testes locais e demonstracoes rapidas

## Admin

Modelos registrados no Django Admin:

- `User`
- `BankAccount`
- `Transaction`
- `InvestmentProduct`
- `PortfolioPosition`
- `InvestmentTransaction`
- `FinancialGoal`
- `Notification`

## Proximos passos

- adicionar logs estruturados e auditoria avancada
- incluir filtros por periodo no extrato
- adicionar webhooks ou filas para notificacoes assincronas
- expandir testes para cenarios de erro e permissao
- incluir CI com lint, testes e validacao do schema OpenAPI
