"""
Script para criar um usuário admin no banco de dados.
Uso: python create_admin.py
"""
from sqlmodel import Session, select
from app.database import engine
from app.models.model_users import User
from app.auth.auth import hash_password

# ── Edite aqui os dados do admin ──────────────────────────────
ADMIN_NAME = "Admin"
ADMIN_EMAIL = "admin@example.com"
ADMIN_PASSWORD = "admin123"
# ─────────────────────────────────────────────────────────────

def create_admin():
    with Session(engine) as session:
        existing = session.exec(select(User).where(User.email == ADMIN_EMAIL)).first()
        if existing:
            if not existing.is_admin:
                existing.is_admin = True
                session.commit()
                print(f"Usuário '{ADMIN_EMAIL}' promovido a admin.")
            else:
                print(f"Admin '{ADMIN_EMAIL}' já existe.")
            return

        admin = User(
            name=ADMIN_NAME,
            email=ADMIN_EMAIL,
            password_hash=hash_password(ADMIN_PASSWORD),
            is_admin=True,
        )
        session.add(admin)
        session.commit()
        session.refresh(admin)
        print(f"Admin criado com sucesso! ID: {admin.id}")
        print(f"  Email: {ADMIN_EMAIL}")
        print(f"  Senha: {ADMIN_PASSWORD}")

if __name__ == "__main__":
    create_admin()
