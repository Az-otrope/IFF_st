import pandas as pd
from supabase import create_client, Client

from src.settings import ApiKeys


class DataManager:
    def __init__(self) -> None:
        self.client: Client = create_client(ApiKeys.SUPABASE_URL, ApiKeys.SUPABASE_KEY)

    def create_new_user(self, email: str, psw: str) -> None:
        self.client.auth.sign_up({"email": email, "password": psw})

    def fetch_data(self, table_name: str = "samples", select: str = "*") -> pd.DataFrame:
        response = self.client.table(table_name).select(select).execute()

        return pd.DataFrame(response.data)
