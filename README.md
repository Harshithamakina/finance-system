# Finance System API

A professional **Python-based Finance Tracking System** backend built with **FastAPI**. This system allows users to manage financial records, analyze spending patterns, and get intelligent financial health insights — all through a clean, role-based REST API.

---

## 🚀 Live API Documentation

After running the server, visit:
- **Swagger UI:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc

---

## ✨ Features

### Core Features
- 💰 **Financial Records Management** — Create, read, update, delete income and expense records
- 📊 **Financial Health Score** — Unique scoring system (A+ to F) based on savings rate
- 📈 **Smart Analytics** — Category breakdown, monthly summaries, recent activity
- 👥 **Role Based Access Control** — Admin, Analyst, and Viewer roles with different permissions
- 🔐 **JWT Authentication** — Secure login with token based authentication
- ✅ **Input Validation** — Strict validation on all endpoints using Pydantic
- 🚨 **Smart Spending Alerts** — Automatic alerts when expenses exceed 80% of income

### Unique Features
- **Financial Health Score** — A score out of 100 with grade (A+, A, B, C, D, F) that tells users how healthy their finances are
- **Savings Rate Calculator** — Shows what percentage of income is being saved
- **Spending Alert System** — Warns users when spending is dangerously high
- **Role Scoped Data** — Admins see all data, others see only their own

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| **FastAPI** | Modern, fast Python web framework |
| **SQLAlchemy** | Database ORM |
| **SQLite** | Lightweight database |
| **Pydantic** | Data validation and serialization |
| **JWT (python-jose)** | Authentication tokens |
| **Passlib + Bcrypt** | Password hashing |
| **Uvicorn** | ASGI server |

---

## 📁 Project Structure
```
finance-system/
├── app/
│   ├── main.py              
│   ├── database.py          
│   ├── core/
│   │   ├── config.py        
│   │   ├── security.py      
│   │   └── dependencies.py  
│   ├── models/
│   │   ├── user.py          
│   │   └── transaction.py   
│   ├── schemas/
│   │   ├── user.py          
│   │   └── transaction.py   
│   ├── services/
│   │   ├── auth_service.py          
│   │   ├── transaction_service.py   
│   │   └── analytics_service.py     
│   └── routers/
│       ├── auth.py          
│       ├── users.py         
│       ├── transactions.py  
│       └── analytics.py     
├── seed.py                  
├── requirements.txt         
└── README.md               
```

## ⚙️ Setup Instructions

### Step 1 — Clone The Repository
```bash
git clone https://github.com/Harshithamakina/finance-system.git
cd finance-system
```

### Step 2 — Create Virtual Environment
```bash
python -m venv venv
```

### Step 3 — Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

### Step 4 — Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 5 — Seed Sample Data
```bash
python seed.py
```

### Step 6 — Run The Server
```bash
python -m uvicorn app.main:app --reload
```

### Step 7 — Open API Documentation
http://127.0.0.1:8000/docs

---

## 👥 User Roles

| Role | Permissions |
|---|---|
| **Admin** | Full access — manage all users and transactions |
| **Analyst** | View transactions, access detailed analytics |
| **Viewer** | View own transactions and basic summary only |

---

## 🔑 Test Credentials

| Role | Email | Password |
|---|---|---|
| Admin | admin@finance.com | admin123 |
| Analyst | analyst@finance.com | analyst123 |
| Viewer | viewer@finance.com | viewer123 |

---

## 📡 API Endpoints

### Authentication
| Method | Endpoint | Description | Access |
|---|---|---|---|
| POST | `/api/auth/register` | Register new user | Public |
| POST | `/api/auth/login` | Login and get JWT token | Public |

### Users
| Method | Endpoint | Description | Access |
|---|---|---|---|
| GET | `/api/users/me` | Get current user profile | All users |
| GET | `/api/users/` | Get all users | Admin only |
| PATCH | `/api/users/{id}/deactivate` | Deactivate user | Admin only |

### Transactions
| Method | Endpoint | Description | Access |
|---|---|---|---|
| POST | `/api/transactions/` | Create transaction | All users |
| GET | `/api/transactions/` | List with filters | All users |
| GET | `/api/transactions/{id}` | Get single transaction | All users |
| PUT | `/api/transactions/{id}` | Update transaction | All users |
| DELETE | `/api/transactions/{id}` | Delete transaction | All users |

### Analytics
| Method | Endpoint | Description | Access |
|---|---|---|---|
| GET | `/api/analytics/summary` | Summary + health score | All users |
| GET | `/api/analytics/category-breakdown` | Spending by category | Analyst + Admin |
| GET | `/api/analytics/monthly` | Monthly totals | Analyst + Admin |
| GET | `/api/analytics/recent-activity` | Recent transactions | All users |

---

## 📊 Financial Health Score

| Score | Grade | Savings Rate | Meaning |
|---|---|---|---|
| 100 | A+ | 50%+ | Excellent financial health |
| 85 | A | 30–50% | Great financial health |
| 70 | B | 20–30% | Good financial health |
| 50 | C | 10–20% | Fair — needs improvement |
| 30 | D | 0–10% | Warning — barely saving |
| 10 | F | Negative | Critical — expenses exceed income |

---

## 🔍 Filtering Transactions
GET /api/transactions/?type=expense&category=food&start_date=2026-01-01&end_date=2026-12-31

Available filters:
- `type` — income or expense
- `category` — food, transport, salary, etc.
- `start_date` — filter from date
- `end_date` — filter to date
- `min_amount` — minimum amount
- `max_amount` — maximum amount
- `skip` — pagination offset
- `limit` — results per page (max 100)

---

## 💡 Assumptions Made

- SQLite is used for simplicity — can be switched to PostgreSQL by changing `DATABASE_URL` in `config.py`
- JWT tokens expire after 30 minutes by default
- Passwords must be minimum 6 characters
- Transaction amounts must be positive numbers
- Admin users can view and manage all transactions across all users
- Analyst and Viewer users can only see their own transactions
- Categories are predefined to ensure clean and consistent data

---

## 🧪 How To Test

1. Run server and open `http://127.0.0.1:8000/docs`
2. Use test credentials from the table above
3. Click **Authorize** and login
4. Test any endpoint using **Try it out** → **Execute**
5. Try different roles to see access control in action

---

## 📦 Dependencies
fastapi
uvicorn
sqlalchemy
pydantic
pydantic-settings
passlib==1.7.4
python-jose
bcrypt==4.0.1
email-validator
python-multipart

---

## 👨‍💻 Author

Built as part of a Python Developer Internship assignment.
Demonstrates clean architecture, role based access control,
JWT authentication, and smart financial analytics.