### Estrutura das pastas

<!-- Backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # Ponto de entrada FastAPI
│   ├── config.py            # Configurações (DATABASE_URL, etc.)
│   ├── database.py          # Conexão SQLAlchemy
│   ├── models/              # Modelos SQLAlchemy
│   │   ├── __init__.py
│   │   └── user.py          # Exemplo de modelo
│   ├── schemas/             # Schemas Pydantic
│   │   ├── __init__.py
│   │   └── user.py
│   ├── routers/             # Rotas da API
│   │   ├── __init__.py
│   │   └── user.py
│   ├── crud/                # Operações de banco (Create, Read, Update, Delete)
│   │   ├── __init__.py
│   │   └── user.py
│   └── dependencies/        # Dependências FastAPI
│       └── __init__.py
├── alembic/                 # Migrações (criado via `alembic init alembic`)
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
├── alembic.ini
├── requirements.txt
└── env/ -->