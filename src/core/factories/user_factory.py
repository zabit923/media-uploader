import factory
from faker import Faker

from core.database.models import User

fake = Faker()


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = None

    username = factory.LazyAttribute(lambda _: fake.user_name())
