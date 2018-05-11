from rest_framework import serializers
from .models import (
    Question,
    Category,
    Answer,
    FollowCategory,
    FollowQuestion,
    FollowUser,
    UpvoteQuestion,
    DownvoteQuestion,
    UpvoteAnswer,
    DownvoteAnswer,
    Profile,
    FeedPage
)
from django.contrib.auth.models import User
from rest_framework_jwt.settings import api_settings


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type':'password'}, write_only=True)
    token = serializers.CharField(allow_blank=True, read_only=True)

    def validate(self, data):
        my_username = data.get('username')
        my_password = data.get('password')

        if my_username == '':
            raise serializers.ValidationError("A username is required to login.")

        try:
            user_obj = User.objects.get(username=my_username)
        except:
            raise serializers.ValidationError("This username does not exist")

        if not user_obj.check_password(my_password):
            raise serializers.ValidationError("Incorrect username/password combination! Noob..")


        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)

        data["token"] = token

        return data


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type':'password'}, write_only=True)
    token = serializers.CharField(allow_blank=True, read_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password', 'token']

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        email = validated_data['email']
        new_user = User(username=username, first_name=first_name, last_name=last_name, email=email)
        new_user.set_password(password)
        new_user.save()
        new_profile = Profile(user=new_user)
        new_profile.save()

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(new_user)
        token = jwt_encode_handler(payload)

        validated_data["token"] = token
        return validated_data



class ProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.SerializerMethodField()
    followers_number = serializers.SerializerMethodField()
    followings_number = serializers.SerializerMethodField()
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    followers = serializers.HyperlinkedIdentityField(
    view_name = "api-follower-user-list",
    lookup_field = "user_id",
    lookup_url_kwarg = "following_id"
    )
    followings = serializers.HyperlinkedIdentityField(
    view_name = "api-following-user-list",
    lookup_field = "user_id",
    lookup_url_kwarg = "follower_id"
    )
    class Meta:
        model = Profile
        fields = ['id', 'user_id', 'user', 'image', 'biography', 'followers', 'followings', 'followings_number', 'followers_number', 'first_name', 'last_name', 'email' ]

    def get_user_id(self, obj):
        user_id = obj.user.id
        return user_id
    def get_followers_number(self, obj):
        followers_number = obj.user.followings.all().count()
        return followers_number
    def get_followings_number(self, obj):
        followings_number = obj.user.followers.all().count()
        return followings_number
    def get_first_name(self, obj):
        first_name = obj.user.first_name
        return first_name
    def get_last_name(self, obj):
        last_name = obj.user.last_name
        return last_name
    def get_email(self, obj):
        email = obj.user.email
        return email



class CategoryListSerializer(serializers.ModelSerializer):
    followers_number = serializers.SerializerMethodField()
    questions_number = serializers.SerializerMethodField()
    questions = serializers.HyperlinkedIdentityField(
    view_name = "api-question_list",
    lookup_field = "id",
    lookup_url_kwarg = "category_id"
    )
    followers = serializers.HyperlinkedIdentityField(
    view_name = "api-follow-category-list",
    lookup_field = "id",
    lookup_url_kwarg = "category_id"
    )
    class Meta:
        model = Category
        fields = ['id', 'category_title', 'category_description', 'image', 'questions', 'followers', 'followers_number', 'questions_number']

    def get_followers_number(self, obj):
        followers_number = obj.followcategory_set.all().count()
        return followers_number

    def get_questions_number(self, obj):
        questions_number = obj.question_set.all().count()
        return questions_number





class QuestionListSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    category = CategoryListSerializer()
    upvotes = serializers.SerializerMethodField()
    downvotes = serializers.SerializerMethodField()
    followers_number = serializers.SerializerMethodField()
    answers_number = serializers.SerializerMethodField()
    answers = serializers.HyperlinkedIdentityField(
    view_name = "api-answer_list",
    lookup_field = "id",
    lookup_url_kwarg = "question_id"
    )
    followers = serializers.HyperlinkedIdentityField(
    view_name = "api-follow-question-list",
    lookup_field = "id",
    lookup_url_kwarg = "question_id"
    )
    class Meta:
        model = Question
        fields = ['id', 'question_content', 'user', 'timestamp', 'image', 'category', 'answers', 'followers', 'upvotes', 'downvotes', 'followers_number', 'answers_number']

    def get_upvotes(self, obj):
        upvotes = obj.upvotequestion_set.all().count()
        return upvotes
    def get_downvotes(self, obj):
        downvotes = obj.downvotequestion_set.all().count()
        return downvotes

    def get_followers_number(self, obj):
        followers_number = obj.followquestion_set.all().count()
        return followers_number

    def get_answers_number(self, obj):
        answers_number = obj.answer_set.all().count()
        return answers_number

class QuestionCreateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Question
		fields = ['question_content','user','image', 'category']


class AnswerListSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    question = QuestionListSerializer()
    upvotes = serializers.SerializerMethodField()
    downvotes = serializers.SerializerMethodField()
    class Meta:
        model = Answer
        fields = ['id', 'answer_content', 'user', 'timestamp', 'image', 'question', 'upvotes', 'downvotes']
    def get_upvotes(self, obj):
        upvotes = obj.upvoteanswer_set.all().count()
        return upvotes
    def get_downvotes(self, obj):
        downvotes = obj.downvoteanswer_set.all().count()
        return downvotes

class AnswerCreateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Answer
		fields = ['answer_content','user','image', 'question']


class FollowCategoryCreateSerializer(serializers.ModelSerializer):
	class Meta:
		model = FollowCategory
		fields = ['category']


class FollowCategoryListSerializer(serializers.ModelSerializer):
    follower = UserSerializer()
    class Meta:
        model = FollowCategory
        fields = ['id', 'category', 'follower']

class FollowQuestionCreateSerializer(serializers.ModelSerializer):
	class Meta:
		model = FollowQuestion
		fields = ['question']

class FollowQuestionListSerializer(serializers.ModelSerializer):
    follower = UserSerializer()

    class Meta:
        model = FollowQuestion
        fields = ['id', 'question', 'follower']

class FollowUserCreateSerializer(serializers.ModelSerializer):
	class Meta:
		model = FollowUser
		fields = ['following']

class FollowerUserListSerializer(serializers.ModelSerializer):
	follower = UserSerializer()

	class Meta:
		model = FollowUser
		fields = ['follower']

class FollowingUserListSerializer(serializers.ModelSerializer):
	following = UserSerializer()

	class Meta:
		model = FollowUser
		fields = ['following']

class UpvoteQuestionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UpvoteQuestion
        fields = ['question']

class UpvoteQuestionListSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UpvoteQuestion
        fields = ['user', 'id', 'question']

class DownvoteQuestionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DownvoteQuestion
        fields = ['question']

class DownvoteQuestionListSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = DownvoteQuestion
        fields = ['user', 'id', 'question']

class UpvoteAnswerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UpvoteAnswer
        fields = ['answer']

class UpvoteAnswerListSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UpvoteAnswer
        fields = ['user', 'id', 'answer']

class DownvoteAnswerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DownvoteAnswer
        fields = ['answer']

class DownvoteAnswerListSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = DownvoteAnswer
        fields = ['user', 'id', 'answer']

class FeedPageSerializer(serializers.ModelSerializer):

    user_id = serializers.SerializerMethodField()
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    followers = serializers.HyperlinkedIdentityField(
    view_name = "api-follower-user-list",
    lookup_field = "user_id",
    lookup_url_kwarg = "following_id"
    )
    followings = serializers.HyperlinkedIdentityField(
    view_name = "api-following-user-list",
    lookup_field = "user_id",
    lookup_url_kwarg = "follower_id"
    )
    class Meta:
        model = FeedPage
        fields = [
            'id',
            'user_id',
            'user',
            'followers',
            'followings',
            'first_name',
            'last_name',
            'email',
            'followed_categories',
            'followed_questions',
            'followed_users',

        ]

    def get_user_id(self, obj):
        user_id = obj.user.id
        return user_id
    def get_first_name(self, obj):
        first_name = obj.user.first_name
        return first_name
    def get_last_name(self, obj):
        last_name = obj.user.last_name
        return last_name
    def get_email(self, obj):
        email = obj.user.email
        return email
