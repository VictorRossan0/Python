import logging
import redis.asyncio as redis  # Importação do redis-py para operações assíncronas

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("banking_api")

# Criação de uma conexão assíncrona com o Redis
redis_client = redis.from_url("redis://localhost")
