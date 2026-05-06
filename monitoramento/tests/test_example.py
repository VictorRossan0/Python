import unittest
import sys
import os
from datetime import timedelta
from src.utils.helpers import format_timedelta_to_string
from src.database.queries import fetch_execution_status
from src.database.connection import get_connection
from dotenv import load_dotenv

# Adiciona o diretório principal ao sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

load_dotenv()

class TestHelpers(unittest.TestCase):

    def test_format_timedelta_to_string(self):
        td = timedelta(hours=1, minutes=23, seconds=45)
        result = format_timedelta_to_string(td)
        self.assertEqual(result, "1:23:45")

        invalid_td = "not a timedelta"
        result = format_timedelta_to_string(invalid_td)
        self.assertEqual(result, "N/A")

class TestDatabaseQueries(unittest.TestCase):

    def test_fetch_execution_status(self):
        try:
            connection = get_connection()
            print("Conexão bem-sucedida!")
            connection.close()
        except Exception as e:
            print(f"Erro na conexão: {e}")
        
        data = fetch_execution_status()
        self.assertIsNotNone(data)
        self.assertGreaterEqual(len(data), 0)  # Pode ser vazio, mas não deve falhar
        self.assertIn("id", data.columns)

if __name__ == "__main__":
    unittest.main()
