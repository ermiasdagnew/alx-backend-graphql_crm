import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from .models import Customer

class CustomerNode(DjangoObjectType):
class Meta:
model = Customer
filter_fields = {
"name": ["exact", "icontains", "istartswith"],
"email": ["exact", "icontains"],
}
interfaces = (relay.Node,)

class Query(graphene.ObjectType):
all_customers = DjangoFilterConnectionField(CustomerNode)
customer = relay.Node.Field(CustomerNode)

schema = graphene.Schema(query=Query)
