import os

# Testes rodam num SQLite em memória e com o agente simulado, sem depender de .env.
os.environ["DATABASE_URL"] = "sqlite://"
os.environ["AGENT_PROVIDER"] = "simulated"
os.environ["SESSION_SECRET"] = "test-secret-for-session"
