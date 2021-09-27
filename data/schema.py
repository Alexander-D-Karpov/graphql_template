import graphene
from graphene_django.types import DjangoObjectType, ObjectType
from .models import User, Post


# Types
class UserType(DjangoObjectType):
    class Meta:
        model = User


class PostType(DjangoObjectType):
    class Meta:
        model = Post

# Query for Posts and Users
class Query(ObjectType):
    user = graphene.Field(UserType, id=graphene.Int())
    post = graphene.Field(PostType, id=graphene.Int())
    user = graphene.Field(PostType)
    posts = graphene.List(PostType)

    def resolve_post(self, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return Post.objects.get(pk=id)
        return None

    def resolve_posts(self, info, **kwargs):
        return Post.objects.all()

    def resolve_user(self, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return User.objects.get(pk=id)
        return None

    def resolve_users(self, info, **kwargs):
        return User.objects.all()


# inputs
class UserInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()


class PostInput(graphene.InputObjectType):
    id = graphene.ID()
    title = graphene.String()
    user = graphene.Field(UserInput)
    body = graphene.String()


# mutations
class CreatePost(graphene.Mutation):
    class Arguments:
        input = PostInput(required=True)
    ok = graphene.Boolean()
    post = graphene.Field(PostType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        user = User.objects.get(pk=input.user.id)
        if user is None:
            return CreatePost(ok=False, post=None)
        post_instance = Post(
            title=input.title,
            body=input.body)
        post_instance.save()
        post_instance.user.set(user)
        return CreatePost(ok=ok, post=post_instance)


class UpdatePost(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = PostInput(required=True)
    ok = graphene.Boolean()
    post = graphene.Field(PostType)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        post_instance = Post.objects.get(pk=id)
        if post_instance:
            ok = True
            user = User.objects.get(pk=input.user.id)
            post_instance = Post(
                title=input.title,
                body=input.body)
            post_instance.save()
            post_instance.user.set(user)
            return UpdatePost(ok=ok, post=post_instance)
        return UpdatePost(ok=ok, post=None)


class CreateUser(graphene.Mutation):
    class Arguments:
        input = UserInput(required=True)
    ok = graphene.Boolean()
    user = graphene.Field(UserType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        user_instance = User(name=input.name)
        user_instance.save()
        return CreateUser(ok=ok, user=user_instance)


class UpdateUser(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = UserInput(required=True)
    ok = graphene.Boolean()
    user = graphene.Field(UserType)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        user_instance = User.objects.get(pk=id)
        if user_instance:
            ok = True
            user_instance.name = input.name
            user_instance.save()
            return UpdateUser(ok=ok, user=user_instance)
        return UpdateUser(ok=ok, user=None)


# sum mutations
class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = CreateUser.Field()
    create_post = CreatePost.Field()
    update_post = CreatePost.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
