import uuid
import random
from faker import Faker

fake = Faker()

def create_dummy_transaction():
    """Creates a dummy transaction using Faker."""
    transaction = {
        "transaction_id": str(uuid.uuid4()),
        "date_time": fake.date_time_between(start_date='-1y', end_date='now').strftime("%Y-%m-%d %H:%M:%S"),
        "currency": random.choice(['USD', 'EUR', 'GBP', 'JPY', 'INR']),
        "sender": fake.name(),
        "receiver": fake.name(),
        "transaction_type": random.choice(['purchase', 'sale', 'refund', 'transfer']),
    }
    return transaction
