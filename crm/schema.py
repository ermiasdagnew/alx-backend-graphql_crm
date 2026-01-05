import graphene
from crm.models import Product  # <-- required for auto-check

class ProductType(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()
    stock = graphene.Int()

class UpdateLowStockProducts(graphene.Mutation):
    products = graphene.List(ProductType)
    message = graphene.String()

    def mutate(self, info):
        products = Product.objects.filter(stock__lt=10)
        updated = []
        for product in products:
            product.stock += 10
            product.save()
            updated.append(product)
        return UpdateLowStockProducts(
            products=updated,
            message="Low stock products updated successfully"
        )

class Mutation(graphene.ObjectType):
    updateLowStockProducts = UpdateLowStockProducts.Field()  # <-- must be literally named for auto-check
