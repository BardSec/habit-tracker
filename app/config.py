import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "postgresql://habit_tracker:habit_tracker@db:5432/habit_tracker"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_TYPE = "sqlalchemy"
    WTF_CSRF_ENABLED = True

    # Admin emails — first matching user gets admin role
    ADMIN_EMAILS = [
        e.strip()
        for e in os.environ.get("ADMIN_EMAILS", "").split(",")
        if e.strip()
    ]

    # SSO — Microsoft Entra ID
    AZURE_CLIENT_ID = os.environ.get("AZURE_CLIENT_ID")
    AZURE_CLIENT_SECRET = os.environ.get("AZURE_CLIENT_SECRET")
    AZURE_TENANT_ID = os.environ.get("AZURE_TENANT_ID")

    # SSO — Google Workspace
    GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")

    @property
    def sso_enabled(self):
        azure = all([self.AZURE_CLIENT_ID, self.AZURE_CLIENT_SECRET, self.AZURE_TENANT_ID])
        google = all([self.GOOGLE_CLIENT_ID, self.GOOGLE_CLIENT_SECRET])
        return azure or google
