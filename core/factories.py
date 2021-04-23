from django.contrib.auth import get_user_model
import factory
from .models import Article

User = get_user_model()

class ArticleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Article

    title = factory.Sequence(lambda n: f"My awesome test article number {n}")


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    
    username = factory.Sequence(lambda n: f'testuser{n}') # testuser
    password = factory.PostGenerationMethodCall('set_password', 'test1234')