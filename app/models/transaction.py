from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.database import Base


class TransactionType(str, enum.Enum):
    """Type of financial transaction."""
    INCOME = "income"
    EXPENSE = "expense"


class TransactionCategory(str, enum.Enum):
    """Categories for financial transactions."""
    # Income categories
    SALARY = "salary"
    FREELANCE = "freelance"
    INVESTMENT = "investment"
    BUSINESS = "business"
    OTHER_INCOME = "other_income"

    # Expense categories
    FOOD = "food"
    TRANSPORT = "transport"
    HOUSING = "housing"
    HEALTHCARE = "healthcare"
    EDUCATION = "education"
    ENTERTAINMENT = "entertainment"
    SHOPPING = "shopping"
    UTILITIES = "utilities"
    OTHER_EXPENSE = "other_expense"


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    type = Column(Enum(TransactionType), nullable=False)
    category = Column(Enum(TransactionCategory), nullable=False)
    description = Column(Text, nullable=True)
    date = Column(DateTime, default=datetime.utcnow, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Foreign key linking to user
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationship back to user
    owner = relationship("User", back_populates="transactions")

    def __repr__(self):
        return f"<Transaction {self.type} | {self.amount} | {self.category}>"