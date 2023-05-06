from faker import Faker

from app.core.database import Base


class Seeder:
    db: Base
    fake: Faker

    @classmethod
    def run(cls):
        print("Seeding complete")
