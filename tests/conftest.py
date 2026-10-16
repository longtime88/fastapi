import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from passlib.hash import sha256_crypt

from api.main import app
from api.database import Base
from api.deps import get_db
from api.models import User
import api.deps as deps_module

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function", autouse=True)
def patch_bcrypt():
    deps_module.bcrypt_context.hash = sha256_crypt.hash
    deps_module.bcrypt_context.verify = sha256_crypt.verify
    yield


@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(db):
    user = User(username="testuser", hashed_password=sha256_crypt.hash("test"))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def auth_client(client: TestClient, test_user):
    response = client.post("/auth/token", data={"username": "testuser", "password": "test"})
    token = response.json()["access_token"]
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client