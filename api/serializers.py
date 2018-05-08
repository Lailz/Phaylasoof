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
    DownvoteAnswer
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
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password']

        def create(self, validated_data):
            new_user = User(**validated_data)
            new_user.set_password(validated_data['password'])
            new_user.save()
            return validated_data



class CategoryListSerializer(serializers.ModelSerializer):
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
        fields = ['id', 'category_title', 'category_description', 'image', 'questions', 'followers']




class QuestionListSerializer(serializers.ModelSerializer):
    upvotes = serializers.SerializerMethodField()
    downvotes = serializers.SerializerMethodField()
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
        fields = ['id', 'question_content', 'user', 'timestamp', 'image', 'category', 'answers', 'followers', 'upvotes', 'downvotes']

    def get_upvotes(self, obj):
        upvotes = obj.upvotequestion_set.all().count()
        return upvotes
    def get_downvotes(self, obj):
        downvotes = obj.downvotequestion_set.all().count()
        return downvotes

class QuestionCreateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Question
		fields = ['question_content','user','image', 'category']


class AnswerListSerializer(serializers.ModelSerializer):
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
		fields = ['follower']

class FollowUserListSerializer(serializers.ModelSerializer):
	user = UserSerializer()

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
