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
│   ├── crud/                # Operações de banco (Repository)
│   │   ├── __init__.py
│   │   ├── crud_users.py
│   │   └── crud_tasks.py
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
| POST | `/users/{id}/tasks` | Criar task para usuário | ❌ |
| PUT | `/users/update-user/{id}` | Atualizar usuário | ❌ |
| DELETE | `/users/delete-user/{id}` | Deletar usuário | ❌ |
| GET | `/tasks/{id}` | Buscar task por ID | ❌ |
| GET | `/tasks/by-title/` | Buscar task por título | ❌ |
| PUT | `/tasks/update-task/{id}` | Atualizar task | ❌ |
| DELETE | `/tasks/delete-task/{id}` | Deletar task | ❌ |
| GET | `/admin/users` | Listar todos os usuários | ✅ Admin |
| GET | `/admin/tasks` | Listar todas as tasks | ✅ Admin |
| POST | `/admin/create-user` | Criar usuário (admin) | ✅ Admin |
| POST | `/admin/users/{id}/task` | Criar task (admin) | ✅ Admin |
| DELETE | `/admin/users/{id}` | Deletar usuário (admin) | ✅ Admin |

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
