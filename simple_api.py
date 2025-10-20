"""
Simple working API that connects to SQLite database
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import json

app = FastAPI()

# Enable CORS
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

@app.get("/")
async def root():
    return {"message": "FineGuard API", "status": "running"}

@app.get("/api/users")
async def get_users():
    conn = get_db()
    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    return [dict(row) for row in users]

@app.post("/api/users")
async def create_user(user: dict):
    conn = get_db()
    c = conn.cursor()
    c.execute('INSERT INTO users (name, email, role, status, created) VALUES (?, ?, ?, ?, ?)',
              (user['name'], user['email'], user['role'], user['status'], user['created']))
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

@app.get("/api/companies")
async def get_companies():
    conn = get_db()
    companies = conn.execute('SELECT * FROM companies').fetchall()
    conn.close()
    return [dict(row) for row in companies]

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
              (agent['name'], agent['status'], agent['tasks'], agent['accuracy'], agent['enabled']))
    conn.commit()
    agent_id = c.lastrowid
    conn.close()
    return {"id": agent_id, **agent}

@app.put("/api/agents/{agent_id}")
async def update_agent(agent_id: int, agent: dict):
    conn = get_db()
    conn.execute('UPDATE agents SET name=?, status=?, tasks=?, accuracy=?, enabled=? WHERE id=?',
                 (agent['name'], agent['status'], agent['tasks'], agent['accuracy'], agent['enabled'], agent_id))
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

