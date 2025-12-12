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

class CustomerType(DjangoObjectType):
class Meta:
model = Customer

class CreateCustomer(graphene.Mutation):
class Arguments:
name = graphene.String(required=True)
email = graphene.String(required=True)
phone = graphene.String(required=True)

```
customer = graphene.Field(CustomerType)

def mutate(self, info, name, email, phone):
    customer = Customer(
        name=name,
        email=email,
        phone=phone,
    )
    customer.save()
    return CreateCustomer(customer=customer)
```

class Query(graphene.ObjectType):
all_customers = DjangoFilterConnectionField(CustomerNode)
customer = relay.Node.Field(CustomerNode)

class Mutation(graphene.ObjectType):
create_customer = CreateCustomer.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
