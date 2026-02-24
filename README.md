# Projeto Backend - Fase 1

## Estrutura de Pastas

```bash
Backend - Fase 1/
├── app/
│   ├── __init__.py
│   ├── main.py              # Ponto de entrada FastAPI
│   ├── config.py            # Configurações (DATABASE_URL, SECRET_KEY) — não commitar
│   ├── database.py          # Conexão SQLAlchemy/SQLModel
│   ├── exceptions.py        # Exceções customizadas
│   ├── models/              # Modelos SQLModel (tabelas do banco)
│   │   ├── __init__.py
│   │   ├── model_users.py
│   │   └── model_tasks.py
│   ├── schemas/             # Schemas Pydantic (validação/serialização)
│   │   ├── __init__.py
│   │   ├── user_schemas.py
│   │   ├── task_schemas.py
│   │   └── auth_schemas.py
│   ├── routers/             # Rotas da API (Controllers)
│   │   ├── __init__.py
│   │   ├── users.py
│   │   ├── tasks.py
│   │   ├── admin.py
│   │   └── auth.py
│   ├── interfaces/          # Interfaces/contratos das camadas (ABC)
│   │   ├── __init__.py
│   │   ├── i_user_repository.py
│   │   └── i_task_repository.py
│   ├── repositories/        # Camada de acesso a dados (Repository)
│   │   ├── __init__.py
│   │   ├── user_repository.py
│   │   └── task_repository.py
│   ├── services/            # Camada de negócio (Services)
│   │   ├── __init__.py
│   │   ├── user_services.py
│   │   └── task_services.py
│   ├── auth/                # Lógica de autenticação JWT + bcrypt
│   │   ├── __init__.py
│   │   └── auth.py
│   └── dependencies/        # Dependências FastAPI (guards de autenticação)
│       ├── __init__.py
│       └── auth.py
├── alembic/                 # Migrações de banco
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
├── test/                    # Testes automatizados
│   └── app/
│       └── routers/
│           ├── test_users_router.py
│           ├── test_tasks_router.py
│           └── test_admin_router.py
├── alembic.ini
├── requirements.txt
└── env/                     # Ambiente virtual Python
```

## Rotas disponíveis

| Método | Rota | Descrição | Auth |
|--------|------|-----------|------|
| POST | `/auth/register` | Cadastrar usuário | ❌ |
| POST | `/auth/login` | Login (retorna JWT) | ❌ |
| GET | `/users/{id}` | Buscar usuário por ID | ❌ |
| GET | `/users/by-email/` | Buscar usuário por email | ❌ |
| GET | `/users/{id}/tasks` | Listar tasks do usuário | ❌ |
| POST | `/users/{id}/tasks` | Criar task para usuário | ✅ (Bearer — owner) |
| PUT | `/users/update-user/{id}` | Atualizar usuário | ✅ (Bearer — owner) |
| DELETE | `/users/delete-user/{id}` | Deletar usuário | ✅ (Bearer — owner) |
| GET | `/tasks/{id}` | Buscar task por ID | ❌ |
| GET | `/tasks/by-title/` | Buscar task por título | ❌ |
| PUT | `/tasks/update-task/{id}` | Atualizar task | ✅ (Bearer — owner) |
| DELETE | `/tasks/delete-task/{id}` | Deletar task | ✅ (Bearer — owner) |
| GET | `/admin/users` | Listar todos os usuários | ✅ Admin |
| GET | `/admin/tasks` | Listar todas as tasks | ✅ Admin |
| POST | `/admin/create-user` | Criar usuário (admin) | ✅ Admin |
| POST | `/admin/users/{id}/task` | Criar task para qualquer usuário (admin) | ✅ Admin |
| PUT | `/admin/update-user/{id}` | Atualizar usuário (admin) | ✅ Admin |
| PUT | `/admin/update-task/{id}` | Atualizar task (admin) | ✅ Admin |
| DELETE | `/admin/users/{id}` | Deletar usuário (admin) | ✅ Admin |
| DELETE | `/admin/delete-task/{id}` | Deletar task (admin) | ✅ Admin |

## Como rodar

```bash
# Ativar ambiente virtual
source env/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Rodar migrations
alembic upgrade head

# Criar usuário admin (necessário para rotas /admin)
python create_admin.py

# Iniciar servidor
uvicorn app.main:app --reload
```

## Testes

```bash
pytest test/ -v
```
