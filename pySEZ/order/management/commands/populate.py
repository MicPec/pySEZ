from random import randrange, uniform

import factory
from client.models import Client
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from faker import Faker
from order.models import Order, OrderItem
from product.models import Product, Unit
from status.models import Status

fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.LazyAttribute(lambda x: fake.user_name())
    email = factory.LazyAttribute(lambda x: fake.email())


class StatusFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Status

    name = factory.LazyAttribute(lambda x: fake.sentence(nb_words=1)[:-1])
    color = factory.LazyAttribute(lambda x: fake.color())
    state = factory.LazyAttribute(
        lambda x: fake.random_choices(elements=Status.STATE_CHOICES, length=1)[0][0]
    )


class ClientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Client

    firstname = factory.LazyAttribute(lambda x: fake.first_name())
    lastname = factory.LazyAttribute(lambda x: fake.last_name())
    company = factory.LazyAttribute(lambda x: fake.company())
    email = factory.LazyAttribute(lambda x: fake.email())
    phone = factory.LazyAttribute(lambda x: fake.phone_number())
    website = factory.LazyAttribute(lambda x: fake.url())


class UnitFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Unit

    name = factory.LazyAttribute(
        lambda x: fake.sentence(
            ext_word_list=["kg", "m", "h", "piece", "m2"], nb_words=1
        )[:-1]
    )
    minvalue = factory.LazyAttribute(lambda x: 0)
    maxvalue = factory.LazyAttribute(lambda x: randrange(1, 100))
    step = factory.LazyAttribute(lambda x: round(uniform(0, 1), 2))


product_list = {
    "apple",
    "banana",
    "orange",
    "grape",
    "strawberry",
    "watermelon",
    "car",
    "truck",
    "bike",
    "motorcycle",
    "boat",
    "tank-top",
    "underwear",
    "bra",
    "panties",
    "backpack",
    "laptop",
    "tablet",
    "eraser",
    "ruler",
    "scissors",
    "stapler",
    "staples",
    "paperclip",
    "notebook",
    "notebook-cover",
    "binders",
    "chicken",
    "egg",
    "rocket",
    "tape",
    "glue",
    "marker",
    "highlighter",
    "pens",
    "pencils",
    "erasers",
    "phone",
    "headphones",
    "watch",
    "sunglasses",
    "hat",
    "mouse",
    "pen",
    "pencil",
    "crayons",
    "pencil-sharpener",
    "paper",
    "envelope",
    "stamps",
    "folder",
    "calculator",
    "brush",
    "shampoo",
    "conditioner",
    "soap",
    "deodorant",
    "razor",
    "shaving-cream",
    "shower-gel",
    "shower-curtain",
    "towel",
    "toilet-paper",
    "toilet-brush",
    "toilet-seat",
    "toilet",
    "toilet-bowl",
    "toilet-plunger",
    "toothbrush",
    "hairspray",
    "paint",
    "paintbrush",
    "paint-roller",
    "paint-tray",
    "paint-splatter",
    "paint-can",
    "painting",
    "painting-easel",
    "painting-palette",
    "tracker",
    "tracker-stand",
    "strap",
    "strap-clip",
    "pants",
    "shirt",
    "shoes",
    "socks",
    "t-shirt",
    "sweater",
    "sweatshirt",
    "sweatpants",
    "pool",
    "pool-table",
    "toy",
    "toy-car",
    "toy-truck",
    "toy-train",
    "robot",
    "robot-arm",
    "robot-leg",
    "robot-head",
    "robot-body",
    "robot-eye",
    "robot-hand",
    "head",
    "body",
    "eye",
    "hand",
    "foot",
    "leg",
    "arm",
    "nose",
    "ear",
    "mouth",
    "tooth",
    "hair",
    "cleaner",
    "vacuum",
    "vacuum-attachment",
    "vacuum-bag",
    "plate",
    "bowls",
    "mug",
}


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.LazyAttribute(
        lambda x: fake.sentence(ext_word_list=product_list, nb_words=randrange(2, 4))[
            :-1
        ]
    )
    unit_price = factory.LazyAttribute(lambda x: randrange(1, 100))
    unit = factory.Iterator(Unit.objects.all())


class OrderItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OrderItem

    product = factory.SubFactory(ProductFactory)
    product = factory.Iterator(Product.objects.all())
    quantity = factory.LazyAttribute(lambda x: randrange(1, 10))
    note = factory.LazyAttribute(lambda x: fake.sentence(nb_words=randrange(0, 8)))


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    user = factory.Iterator(User.objects.all())
    client = client = factory.SubFactory(ClientFactory)
    note = factory.lazy_attribute(lambda x: fake.sentence(nb_words=randrange(5, 20)))
    status = factory.lazy_attribute(
        lambda x: Status.objects.filter(state="NEW").first()
    )
    products = factory.RelatedFactoryList(OrderItemFactory, "order", size=3)


class Command(BaseCommand):
    def handle(self, *args, **options):
        users = UserFactory.create_batch(2)
        units = UnitFactory.create_batch(5)
        products = ProductFactory.create_batch(25)
        clients = ClientFactory.create_batch(15)
        statuses = StatusFactory.create_batch(5)
        orders = OrderFactory.create_batch(50)
