import graphene
from graphene_django import DjangoObjectType
from .models import Customer

# --------------------
# Types
# --------------------
class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer

# --------------------
# Mutations
# --------------------
class CreateCustomer(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=True)
        phone = graphene.String(required=True)

    customer = graphene.Field(CustomerType)

    def mutate(self, info, name, email, phone):
        customer = Customer(name=name, email=email, phone=phone)
        customer.save()
        return CreateCustomer(customer=customer)

# --------------------
# Query
# --------------------
class Query(graphene.ObjectType):
    all_customers = graphene.List(CustomerType)

    def resolve_all_customers(self, info):
        return Customer.objects.all()

# --------------------
# Mutation
# --------------------
class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()
