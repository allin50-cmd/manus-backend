"""
Extended API with all endpoints for all 52 pages
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
from datetime import datetime
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = '/home/ubuntu/fineguard-backend/fineguard.db'

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_extended_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Create all tables
    tables = [
        '''CREATE TABLE IF NOT EXISTS obligations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_id INTEGER,
            title TEXT NOT NULL,
            description TEXT,
            due_date TEXT,
            status TEXT,
            priority TEXT
        )''',
        '''CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT,
            size INTEGER,
            uploaded TEXT,
            company_id INTEGER
        )''',
        '''CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT,
            created TEXT,
            status TEXT
        )''',
        '''CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            due_date TEXT,
            status TEXT,
            assigned_to INTEGER
        )''',
        '''CREATE TABLE IF NOT EXISTS invoices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            number TEXT NOT NULL,
            client_id INTEGER,
            amount REAL,
            status TEXT,
            due_date TEXT
        )''',
        '''CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            status TEXT
        )''',
        '''CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            client_id INTEGER,
            status TEXT,
            budget REAL,
            start_date TEXT
        )''',
        '''CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            service TEXT NOT NULL,
            client_name TEXT,
            date TEXT,
            status TEXT
        )''',
        '''CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT,
            source TEXT,
            status TEXT,
            score INTEGER
        )'''
    ]
    
    for table_sql in tables:
        c.execute(table_sql)
    
    conn.commit()
    conn.close()

# Initialize extended database
init_extended_db()

# Root
@app.get("/")
async def root():
    return {"message": "FineGuard Extended API", "status": "running", "endpoints": 50}

# Users (from simple_api.py)
@app.get("/api/users")
async def get_users():
    conn = get_db()
    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    return [dict(row) for row in users]

@app.get("/api/users/{user_id}")
async def get_user(user_id: int):
    conn = get_db()
    user = conn.execute('SELECT * FROM users WHERE id=?', (user_id,)).fetchone()
    conn.close()
    if user:
        return dict(user)
    from fastapi import HTTPException
    raise HTTPException(status_code=404, detail="User not found")

@app.post("/api/users")
async def create_user(user: dict):
    conn = get_db()
    c = conn.cursor()
    c.execute('INSERT INTO users (name, email, role, status, created) VALUES (?, ?, ?, ?, ?)',
              (user['name'], user['email'], user['role'], user['status'], user.get('created', datetime.now().strftime('%Y-%m-%d'))))
    conn.commit()
    user_id = c.lastrowid
    conn.close()
    return {"id": user_id, **user}

@app.put("/api/users/{user_id}")
async def update_user(user_id: int, user: dict):
    conn = get_db()
    conn.execute('UPDATE users SET name=?, email=?, role=?, status=? WHERE id=?',
                 (user['name'], user['email'], user['role'], user['status'], user_id))
    conn.commit()
    conn.close()
    return {"id": user_id, **user}

@app.delete("/api/users/{user_id}")
async def delete_user(user_id: int):
    conn = get_db()
    conn.execute('DELETE FROM users WHERE id=?', (user_id,))
    conn.commit()
    conn.close()
    return {"message": "User deleted"}

# Companies
@app.get("/api/companies")
async def get_companies():
    conn = get_db()
    companies = conn.execute('SELECT * FROM companies').fetchall()
    conn.close()
    return [dict(row) for row in companies]

@app.get("/api/companies/{company_id}")
async def get_company(company_id: int):
    conn = get_db()
    company = conn.execute('SELECT * FROM companies WHERE id=?', (company_id,)).fetchone()
    conn.close()
    if company:
        return dict(company)
    from fastapi import HTTPException
    raise HTTPException(status_code=404, detail="Company not found")

@app.post("/api/companies")
async def create_company(company: dict):
    conn = get_db()
    c = conn.cursor()
    c.execute('INSERT INTO companies (name, number, status, compliance, risk) VALUES (?, ?, ?, ?, ?)',
              (company['name'], company['number'], company['status'], company['compliance'], company['risk']))
    conn.commit()
    company_id = c.lastrowid
    conn.close()
    return {"id": company_id, **company}

@app.put("/api/companies/{company_id}")
async def update_company(company_id: int, company: dict):
    conn = get_db()
    conn.execute('UPDATE companies SET name=?, number=?, status=?, compliance=?, risk=? WHERE id=?',
                 (company['name'], company['number'], company['status'], company['compliance'], company['risk'], company_id))
    conn.commit()
    conn.close()
    return {"id": company_id, **company}

@app.delete("/api/companies/{company_id}")
async def delete_company(company_id: int):
    conn = get_db()
    conn.execute('DELETE FROM companies WHERE id=?', (company_id,))
    conn.commit()
    conn.close()
    return {"message": "Company deleted"}

# Agents
@app.get("/api/agents")
async def get_agents():
    conn = get_db()
    agents = conn.execute('SELECT * FROM agents').fetchall()
    conn.close()
    return [dict(row) for row in agents]

@app.post("/api/agents")
async def create_agent(agent: dict):
    conn = get_db()
    c = conn.cursor()
    c.execute('INSERT INTO agents (name, status, tasks, accuracy, enabled) VALUES (?, ?, ?, ?, ?)',
              (agent['name'], agent['status'], agent.get('tasks', 0), agent.get('accuracy', 0), agent.get('enabled', 0)))
    conn.commit()
    agent_id = c.lastrowid
    conn.close()
    return {"id": agent_id, **agent}

@app.put("/api/agents/{agent_id}")
async def update_agent(agent_id: int, agent: dict):
    conn = get_db()
    conn.execute('UPDATE agents SET name=?, status=?, enabled=? WHERE id=?',
                 (agent['name'], agent['status'], agent.get('enabled', 0), agent_id))
    conn.commit()
    conn.close()
    return {"id": agent_id, **agent}

@app.delete("/api/agents/{agent_id}")
async def delete_agent(agent_id: int):
    conn = get_db()
    conn.execute('DELETE FROM agents WHERE id=?', (agent_id,))
    conn.commit()
    conn.close()
    return {"message": "Agent deleted"}

# Generic CRUD for all other entities
for entity in ['obligations', 'documents', 'reports', 'tasks', 'invoices', 'clients', 'projects', 'bookings', 'leads']:
    
    @app.get(f"/api/{entity}")
    async def get_items(table=entity):
        conn = get_db()
        items = conn.execute(f'SELECT * FROM {table}').fetchall()
        conn.close()
        return [dict(row) for row in items]
    
    @app.get(f"/api/{entity}/{{item_id}}")
    async def get_item(item_id: int, table=entity):
        conn = get_db()
        item = conn.execute(f'SELECT * FROM {table} WHERE id=?', (item_id,)).fetchone()
        conn.close()
        return dict(item) if item else {"error": "Not found"}
    
    @app.delete(f"/api/{entity}/{{item_id}}")
    async def delete_item(item_id: int, table=entity):
        conn = get_db()
        conn.execute(f'DELETE FROM {table} WHERE id=?', (item_id,))
        conn.commit()
        conn.close()
        return {"message": f"{table} deleted"}

# Dashboard stats
@app.get("/api/dashboard/stats")
async def get_dashboard_stats():
    conn = get_db()
    return {
        "total_companies": conn.execute('SELECT COUNT(*) as c FROM companies').fetchone()['c'],
        "total_users": conn.execute('SELECT COUNT(*) as c FROM users').fetchone()['c'],
        "active_agents": conn.execute("SELECT COUNT(*) as c FROM agents WHERE status='running'").fetchone()['c'],
        "total_obligations": conn.execute('SELECT COUNT(*) as c FROM obligations').fetchone()['c']
    }

# Settings
@app.get("/api/settings")
async def get_settings():
    return {
        "siteName": "FineGuard",
        "adminEmail": "admin@fineguard.com",
        "enableNotifications": True,
        "enableAI": True,
        "maintenanceMode": False
    }

@app.put("/api/settings")
async def update_settings(settings: dict):
    return settings

# CRM Leads
@app.get("/api/crm/leads")
async def get_leads():
    conn = get_db()
    leads = conn.execute('SELECT * FROM leads').fetchall()
    conn.close()
    return [dict(lead) for lead in leads]

@app.post("/api/crm/leads")
async def create_lead(lead: dict):
    conn = get_db()
    c = conn.cursor()
    c.execute('''INSERT INTO leads (name, email, source, status, score)
                 VALUES (?, ?, ?, ?, ?)''',
              (lead.get('name'), lead.get('email'), lead.get('source', 'website'),
               lead.get('status', 'new'), lead.get('score', 0)))
    conn.commit()
    lead_id = c.lastrowid
    conn.close()
    return {"id": lead_id, **lead}

# Analytics
@app.get("/api/analytics")
async def get_analytics():
    conn = get_db()
    
    # Get counts
    users_count = conn.execute('SELECT COUNT(*) as count FROM users').fetchone()['count']
    companies_count = conn.execute('SELECT COUNT(*) as count FROM companies').fetchone()['count']
    documents_count = conn.execute('SELECT COUNT(*) as count FROM documents').fetchone()['count']
    tasks_count = conn.execute('SELECT COUNT(*) as count FROM tasks').fetchone()['count']
    
    conn.close()
    
    return {
        "totalUsers": users_count,
        "totalCompanies": companies_count,
        "totalDocuments": documents_count,
        "totalTasks": tasks_count,
        "activeProjects": 5,
        "revenue": 125000,
        "growth": 23.5
    }

# Notifications
@app.get("/api/notifications")
async def get_notifications():
    return [
        {
            "id": 1,
            "title": "New compliance alert",
            "message": "Company ABC has an overdue obligation",
            "type": "warning",
            "read": False,
            "created": "2024-10-16T10:30:00"
        },
        {
            "id": 2,
            "title": "Document uploaded",
            "message": "Financial report has been uploaded",
            "type": "info",
            "read": False,
            "created": "2024-10-16T09:15:00"
        },
        {
            "id": 3,
            "title": "Task completed",
            "message": "Review Q3 financials task has been completed",
            "type": "success",
            "read": True,
            "created": "2024-10-15T16:45:00"
        }
    ]

@app.post("/api/notifications")
async def create_notification(notification: dict):
    return {"id": 4, **notification}

# Accounting Services
@app.get("/api/accounting/service-categories")
async def get_accounting_service_categories():
    return [
        {"id": 1, "name": "Tax Services", "icon": "calculator", "description": "Comprehensive tax services", "services": ["Tax Planning", "Tax Returns", "Tax Compliance", "VAT Services"]},
        {"id": 2, "name": "Bookkeeping", "icon": "book", "description": "Professional bookkeeping services", "services": ["Daily Bookkeeping", "Financial Reporting", "Reconciliation", "Accounts Management"]},
        {"id": 3, "name": "Payroll", "icon": "users", "description": "Complete payroll management", "services": ["Payroll Processing", "PAYE Management", "Pension Administration", "Payslip Generation"]},
        {"id": 4, "name": "Advisory", "icon": "briefcase", "description": "Strategic business advisory", "services": ["Business Planning", "Financial Strategy", "Growth Advisory", "Risk Management"]}
    ]

@app.get("/api/accounting/packages")
async def get_accounting_packages():
    return [
        {"id": 1, "name": "Starter", "price": 99, "features": ["Basic bookkeeping", "Monthly reports"]},
        {"id": 2, "name": "Professional", "price": 299, "features": ["Full bookkeeping", "Tax filing", "Payroll"]},
        {"id": 3, "name": "Enterprise", "price": 599, "features": ["Everything", "Dedicated accountant", "CFO services"]}
    ]

@app.get("/api/accounting/add-on-services")
async def get_accounting_addon_services():
    return [
        {"id": 1, "name": "VAT Returns", "price": 50},
        {"id": 2, "name": "Year-end Accounts", "price": 200},
        {"id": 3, "name": "Tax Planning", "price": 150}
    ]

@app.get("/api/accounting/testimonials")
async def get_accounting_testimonials():
    return [
        {"id": 1, "name": "John Smith", "company": "ABC Ltd", "rating": 5, "text": "Excellent service!"},
        {"id": 2, "name": "Sarah Jones", "company": "XYZ Corp", "rating": 5, "text": "Very professional"}
    ]

# Analytics
@app.get("/api/analytics/stats")
async def get_analytics_stats():
    return {
        "revenue": 125000,
        "expenses": 85000,
        "profit": 40000,
        "growth": 23.5,
        "customers": 156
    }

# Subscription
@app.get("/api/subscription-tiers")
async def get_subscription_tiers():
    return {
        "free": {"name": "Free", "price": 0, "features": ["Basic features"]},
        "pro": {"name": "Pro", "price": 29, "features": ["All features", "Priority support"]},
        "enterprise": {"name": "Enterprise", "price": 99, "features": ["Everything", "Dedicated support"]}
    }

# Team
@app.get("/api/team/members")
async def get_team_members():
    return [
        {"id": 1, "name": "Alice Johnson", "role": "Admin", "email": "alice@example.com"},
        {"id": 2, "name": "Bob Smith", "role": "User", "email": "bob@example.com"}
    ]

@app.get("/api/team/roles")
async def get_team_roles():
    return [
        {"id": 1, "name": "Admin", "permissions": ["all"]},
        {"id": 2, "name": "User", "permissions": ["read", "write"]},
        {"id": 3, "name": "Viewer", "permissions": ["read"]}
    ]

# Payroll
@app.get("/api/payroll")
async def get_payroll():
    return [
        {"id": 1, "employee": "John Doe", "amount": 3500, "date": "2024-10-01", "status": "paid"},
        {"id": 2, "employee": "Jane Smith", "amount": 4200, "date": "2024-10-01", "status": "paid"}
    ]

# Sales
@app.get("/api/sales")
async def get_sales():
    return [
        {"id": 1, "product": "Service A", "amount": 1500, "date": "2024-10-15", "customer": "ABC Ltd"},
        {"id": 2, "product": "Service B", "amount": 2300, "date": "2024-10-14", "customer": "XYZ Corp"}
    ]

# Marketing
@app.get("/api/marketing")
async def get_marketing():
    return [
        {"id": 1, "campaign": "Email Campaign Q4", "status": "active", "leads": 234, "conversions": 45},
        {"id": 2, "campaign": "Social Media Ads", "status": "active", "leads": 567, "conversions": 89}
    ]

# Opportunities
@app.get("/api/opportunities")
async def get_opportunities():
    return [
        {"id": 1, "name": "Deal with ABC Ltd", "value": 50000, "stage": "negotiation", "probability": 75},
        {"id": 2, "name": "XYZ Corp Contract", "value": 75000, "stage": "proposal", "probability": 50}
    ]

# CRM Services
@app.get("/services")
async def get_services():
    return [
        {"id": 1, "name": "Tax Planning", "status": "active", "clients": 45},
        {"id": 2, "name": "Bookkeeping", "status": "active", "clients": 67},
        {"id": 3, "name": "Payroll Services", "status": "active", "clients": 34}
    ]

@app.get("/agents")
async def get_agents_crm():
    return [
        {"id": 1, "name": "AI Lead Scoring Agent", "status": "active", "tasks": 156},
        {"id": 2, "name": "Churn Prediction Agent", "status": "active", "tasks": 89},
        {"id": 3, "name": "Compliance Monitoring Agent", "status": "active", "tasks": 234}
    ]

@app.get("/automations")
async def get_automations():
    return [
        {"id": 1, "name": "Email Follow-up", "status": "active", "triggers": 45},
        {"id": 2, "name": "Lead Scoring", "status": "active", "triggers": 123}
    ]

@app.get("/clients")
async def get_clients():
    return [
        {"id": 1, "name": "ABC Ltd", "status": "active", "revenue": 50000},
        {"id": 2, "name": "XYZ Corp", "status": "active", "revenue": 75000},
        {"id": 3, "name": "Tech Startup Ltd", "status": "active", "revenue": 35000}
    ]

# Documents
@app.get("/api/folders")
async def get_folders():
    return [
        {"id": 1, "name": "Tax Returns", "count": 45},
        {"id": 2, "name": "Invoices", "count": 123},
        {"id": 3, "name": "Contracts", "count": 67}
    ]

# Reports
@app.get("/report-types")
async def get_report_types():
    return [
        {"id": 1, "name": "Financial Report", "category": "finance"},
        {"id": 2, "name": "Compliance Report", "category": "compliance"},
        {"id": 3, "name": "Tax Report", "category": "tax"}
    ]

@app.get("/reports")
async def get_reports():
    return [
        {"id": 1, "title": "Q3 Financial Report", "type": "financial", "date": "2024-10-01", "status": "completed"},
        {"id": 2, "title": "Annual Compliance Report", "type": "compliance", "date": "2024-09-15", "status": "completed"}
    ]

# Analytics
@app.get("/api/analytics/companyPerformance")
async def get_company_performance():
    return [
        {"company": "ABC Ltd", "revenue": 50000, "growth": 15},
        {"company": "XYZ Corp", "revenue": 75000, "growth": 23},
        {"company": "Tech Startup Ltd", "revenue": 35000, "growth": 45}
    ]

@app.get("/api/analytics/monthlyData")
async def get_monthly_data():
    return [
        {"month": "Jan", "revenue": 45000, "expenses": 30000},
        {"month": "Feb", "revenue": 52000, "expenses": 32000},
        {"month": "Mar", "revenue": 48000, "expenses": 31000},
        {"month": "Apr", "revenue": 55000, "expenses": 33000},
        {"month": "May", "revenue": 58000, "expenses": 34000},
        {"month": "Jun", "revenue": 62000, "expenses": 35000}
    ]

@app.get("/api/analytics/upcomingDeadlines")
async def get_upcoming_deadlines():
    return [
        {"id": 1, "title": "VAT Return", "date": "2024-11-01", "company": "ABC Ltd"},
        {"id": 2, "title": "Annual Accounts", "date": "2024-11-15", "company": "XYZ Corp"},
        {"id": 3, "title": "Tax Return", "date": "2024-12-01", "company": "Tech Startup Ltd"}
    ]

# Settings
@app.get("/api/v1/api-keys")
async def get_api_keys():
    return [
        {"id": 1, "name": "Production Key", "key": "pk_live_***************", "created": "2024-01-15"},
        {"id": 2, "name": "Development Key", "key": "pk_test_***************", "created": "2024-02-20"}
    ]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
