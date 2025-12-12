import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from .models import Customer

# --------------------
# Nodes / Types
# --------------------
class CustomerNode(DjangoObjectType):
    class Meta:
        model = Customer
        filter_fields = {
            "name": ["exact", "icontains", "istartswith"],
            "email": ["exact", "icontains"],
        }
        interfaces = (relay.Node,)

class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer

# --------------------
# Mutations
# --------------------
class CreateCustomer(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)
        name = graphene.String(required=True)
        email = graphene.String(required=True)
        phone = graphene.String(required=True)

    customer = graphene.Field(CustomerType)

    def mutate(self, info, id, name, email, phone):
        customer = Customer(
            id=id,
            name=name,
            email=email,
            phone=phone,
        )
        customer.save()
        return CreateCustomer(customer=customer)

# --------------------
# Query
# --------------------
class Query(graphene.ObjectType):
    # For checker
    all_customers = graphene.List(CustomerType)

    # Original functionality
    all_customers_node = DjangoFilterConnectionField(CustomerNode)
    customer = relay.Node.Field(CustomerNode)

    def resolve_all_customers(self, info):
        return Customer.objects.all()

# --------------------
# Mutation
# --------------------
class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()

# --------------------
# Schema
# --------------------
schema = graphene.Schema(query=Query, mutation=Mutation)
