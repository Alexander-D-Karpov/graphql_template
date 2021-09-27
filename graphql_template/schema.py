import graphene
import data.schema


class Query(data.schema.Query, graphene.ObjectType):
    pass


class Mutation(data.schema.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
