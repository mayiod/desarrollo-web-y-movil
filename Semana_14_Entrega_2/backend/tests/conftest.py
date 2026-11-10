import os
import tempfile

# Las variables deben existir ANTES de importar los módulos de la app
os.environ["INTERNAL_GATEWAY_SECRET"] = "test-backend-secret"
os.environ["AUTH_INTROSPECTION_SECRET"] = "test-auth-secret"
os.environ["VAULT_TOKEN"] = "test-vault-token"
os.environ["BACKEND_URL"] = "http://backend.test"
os.environ["AUTH_URL"] = "http://auth.test"
os.environ["DB_PATH"] = os.path.join(tempfile.mkdtemp(), "test.db")

import pytest  # noqa: E402

import database  # noqa: E402


@pytest.fixture(autouse=True)
def fresh_db():
    database.reset_db()
