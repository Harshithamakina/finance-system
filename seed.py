from app.database import SessionLocal, init_db
from app.models.user import UserRole
from app.models.transaction import TransactionType, TransactionCategory
from app.services.auth_service import register_user
from app.services.transaction_service import create_transaction
from app.schemas.user import UserCreate
from app.schemas.transaction import TransactionCreate
from datetime import datetime, timedelta


def seed():
    """Seed the database with sample data."""
    init_db()
    db = SessionLocal()

    print("🌱 Seeding database...")

    # Create users
    users_data = [
        UserCreate(
            full_name="Admin User",
            email="admin@finance.com",
            password="admin123",
            role=UserRole.ADMIN
        ),
        UserCreate(
            full_name="Analyst User",
            email="analyst@finance.com",
            password="analyst123",
            role=UserRole.ANALYST
        ),
        UserCreate(
            full_name="Viewer User",
            email="viewer@finance.com",
            password="viewer123",
            role=UserRole.VIEWER
        ),
    ]

    created_users = []
    for user_data in users_data:
        try:
            user = register_user(db, user_data)
            created_users.append(user)
            print(f"✅ Created user: {user.email} | Role: {user.role}")
        except Exception as e:
            print(f"⚠️ User already exists: {user_data.email}")

    if not created_users:
        print("⚠️ All users already exist. Skipping transactions.")
        db.close()
        return

    # Create sample transactions for admin user
    admin_user = created_users[0]
    transactions_data = [
        TransactionCreate(
            amount=5000,
            type=TransactionType.INCOME,
            category=TransactionCategory.SALARY,
            description="Monthly salary",
            date=datetime.utcnow() - timedelta(days=30)
        ),
        TransactionCreate(
            amount=1200,
            type=TransactionType.EXPENSE,
            category=TransactionCategory.HOUSING,
            description="Monthly rent",
            date=datetime.utcnow() - timedelta(days=28)
        ),
        TransactionCreate(
            amount=300,
            type=TransactionType.EXPENSE,
            category=TransactionCategory.FOOD,
            description="Groceries",
            date=datetime.utcnow() - timedelta(days=20)
        ),
        TransactionCreate(
            amount=150,
            type=TransactionType.EXPENSE,
            category=TransactionCategory.TRANSPORT,
            description="Monthly transport pass",
            date=datetime.utcnow() - timedelta(days=15)
        ),
        TransactionCreate(
            amount=1000,
            type=TransactionType.INCOME,
            category=TransactionCategory.FREELANCE,
            description="Freelance project payment",
            date=datetime.utcnow() - timedelta(days=10)
        ),
        TransactionCreate(
            amount=200,
            type=TransactionType.EXPENSE,
            category=TransactionCategory.ENTERTAINMENT,
            description="Netflix and dining out",
            date=datetime.utcnow() - timedelta(days=5)
        ),
    ]

    for t_data in transactions_data:
        create_transaction(db, t_data, admin_user.id)
        print(f"✅ Created transaction: {t_data.type} | {t_data.amount}")

    print("\n🎉 Database seeded successfully!")
    print("\n📋 Test Credentials:")
    print("Admin    → admin@finance.com    | password: admin123")
    print("Analyst  → analyst@finance.com  | password: analyst123")
    print("Viewer   → viewer@finance.com   | password: viewer123")

    db.close()


if __name__ == "__main__":
    seed()