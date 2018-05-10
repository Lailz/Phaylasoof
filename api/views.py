from django.shortcuts import render
from rest_framework.generics import (
	ListAPIView,
	RetrieveAPIView,
	CreateAPIView,
	DestroyAPIView,
	RetrieveUpdateAPIView
	)
from .models import Question, Category, UpvoteQuestion, DownvoteQuestion, UpvoteAnswer, DownvoteAnswer, Answer, FollowCategory, FollowUser, FollowQuestion, Profile
from .serializers import (
    CategoryListSerializer,
	QuestionListSerializer,
	AnswerListSerializer,
    UpvoteQuestionCreateSerializer,
    UpvoteQuestionListSerializer,
    DownvoteQuestionCreateSerializer,
    DownvoteQuestionListSerializer,
	UpvoteAnswerCreateSerializer,
    UpvoteAnswerListSerializer,
    DownvoteAnswerCreateSerializer,
    DownvoteAnswerListSerializer,
    RegisterUserSerializer,
    UserLoginSerializer,
	FollowCategoryCreateSerializer,
    FollowCategoryListSerializer,
	FollowUserCreateSerializer,
    FollowUserListSerializer,
	FollowQuestionCreateSerializer,
	FollowQuestionListSerializer,
	QuestionCreateSerializer,
	AnswerCreateSerializer,
	ProfileSerializer




    )
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .permissions import IsAuthorOrStaff
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
import requests
from django.urls import reverse
from django.http import JsonResponse
import json

from django.db.models import Q




class LoginAPIView(APIView):
	permission_classes = [AllowAny]
	serializer_class = UserLoginSerializer

	def post(self, request, format=None):
		my_data = request.data
		my_serializer = UserLoginSerializer(data=my_data)
		if my_serializer.is_valid(raise_exception=True):
			new_data = my_serializer.data
			return Response(new_data, status=HTTP_200_OK)
		return Response(my_serializer.errors, status=HTTP_400_BAD_REQUEST)


class UserRegisterView(CreateAPIView):
	queryset = User.objects.all()
	serializer_class = RegisterUserSerializer
	permission_classes = [AllowAny]


class ProfileView(APIView):
	permission_classes = [AllowAny,]
	def get(self, request, user_id):
		get_profile = Profile.objects.get(user__id=user_id)
		profiles = ProfileSerializer(get_profile, context={'request':request}).data
		return Response(profiles)


class CategoryListView(APIView):
	permission_classes = [AllowAny,]

	def get(self, request):
		category_list = Category.objects.all()
		query = request.GET.get("search", None)
		if query:
			categories = category_list.filter(
			Q(category_title__icontains=query)|
			Q(category_description__icontains=query)).distinct()
			categories = CategoryListSerializer(categories, many=True, context={'request':request}).data
		else:
			categories = CategoryListSerializer(category_list, many=True, context={'request':request}).data
		return Response(categories)


class QuestionListView(APIView):
	permission_classes = [AllowAny,]

	def get(self, request, category_id):
		question_list = Question.objects.filter(category__id=category_id)
		query = request.GET.get("search", None)
		if query:
			questions = question_list.filter(
			Q(question_content__icontains=query)).distinct()
			questions = QuestionListSerializer(questions, many=True, context={'request':request}).data
		else:
			questions = QuestionListSerializer(question_list, many=True, context={'request':request}).data
		return Response(questions)

class QuestionCreateView(CreateAPIView):
	queryset = Question.objects.all()
	serializer_class = QuestionCreateSerializer
	permission_classes = [IsAuthenticated,]

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)

class QuestionDeleteView(DestroyAPIView):
	queryset = Question.objects.all()
	serializer_class = QuestionListSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'question_id'
	permission_classes = [IsAuthenticated,IsAuthorOrStaff]


class AnswerListView(APIView):
	permission_classes = [AllowAny,]

	def get(self, request, question_id):
		answer_list = Answer.objects.filter(question__id=question_id)
		query = request.GET.get("search", None)
		if query:
			answers = answer_list.filter(
			Q(answer_content__icontains=query)).distinct()
			answers = AnswerListSerializer(answers, many=True, context={'request':request}).data
		else:
			answers = AnswerListSerializer(answer_list, many=True, context={'request':request}).data
		return Response(answers)

class AnswerCreateView(CreateAPIView):
	queryset = Answer.objects.all()
	serializer_class = AnswerCreateSerializer
	permission_classes = [IsAuthenticated,]

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)

class AnswerDeleteView(DestroyAPIView):
	queryset = Answer.objects.all()
	serializer_class = AnswerListSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'answer_id'
	permission_classes = [IsAuthenticated,IsAuthorOrStaff]


class UpvoteQuestionCreateView(APIView):
	def post(self, request):
		my_data = request.data
		my_serializer=UpvoteQuestionCreateSerializer(data=my_data)
		if my_serializer.is_valid(raise_exception=True):
			new_data = my_serializer.data
			question_obj=Question.objects.get(id=new_data['question'])
			upvote_question, created = UpvoteQuestion.objects.get_or_create(question=question_obj, user=request.user)
			if not created:
				upvote_question.delete()
			return Response(new_data, status=HTTP_200_OK)
		return Response(my_serializer.errors, status=HTTP_400_BAD_REQUEST)


class UpvoteQuestionListView(APIView):
	permission_classes = [AllowAny,]

	def get(self, request, question_id):
		user_list = UpvoteQuestion.objects.filter(question__id=question_id)
		users = UpvoteQuestionListSerializer(user_list, many=True, context={'request':request}).data
		return Response(users)

class DownvoteQuestionCreateView(APIView):
	def post(self, request):
		my_data = request.data
		my_serializer=DownvoteQuestionCreateSerializer(data=my_data)
		if my_serializer.is_valid(raise_exception=True):
			new_data = my_serializer.data
			question_obj=Question.objects.get(id=new_data['question'])
			downvote_question, created = DownvoteQuestion.objects.get_or_create(question=question_obj, user=request.user)
			if not created:
				downvote_question.delete()
			return Response(new_data, status=HTTP_200_OK)
		return Response(my_serializer.errors, status=HTTP_400_BAD_REQUEST)

class DownvoteQuestionListView(APIView):
	permission_classes = [AllowAny,]

	def get(self, request, question_id):
		user_list = DownvoteQuestion.objects.filter(question__id=question_id)
		users = DownvoteQuestionListSerializer(user_list, many=True, context={'request':request}).data
		return Response(users)

class UpvoteAnswerCreateView(APIView):
	def post(self, request):
		my_data = request.data
		my_serializer=UpvoteAnswerCreateSerializer(data=my_data)
		if my_serializer.is_valid(raise_exception=True):
			new_data = my_serializer.data
			answer_obj=Answer.objects.get(id=new_data['answer'])
			upvote_answer, created = UpvoteAnswer.objects.get_or_create(answer=answer_obj, user=request.user)
			if not created:
				upvote_answer.delete()
			return Response(new_data, status=HTTP_200_OK)
		return Response(my_serializer.errors, status=HTTP_400_BAD_REQUEST)


class UpvoteAnswerListView(APIView):
	permission_classes = [AllowAny,]

	def get(self, request, answer_id):
		user_list = UpvoteAnswer.objects.filter(answer__id=answer_id)
		users = UpvoteAnswerListSerializer(user_list, many=True, context={'request':request}).data
		return Response(users)

class DownvoteAnswerCreateView(APIView):
	def post(self, request):
		my_data = request.data
		my_serializer=DownvoteAnswerCreateSerializer(data=my_data)
		if my_serializer.is_valid(raise_exception=True):
			new_data = my_serializer.data
			answer_obj=Answer.objects.get(id=new_data['answer'])
			downvote_answer, created = DownvoteAnswer.objects.get_or_create(answer=answer_obj, user=request.user)
			if not created:
				downvote_answer.delete()
			return Response(new_data, status=HTTP_200_OK)
		return Response(my_serializer.errors, status=HTTP_400_BAD_REQUEST)

class DownvoteAnswerListView(APIView):
	permission_classes = [AllowAny,]

	def get(self, request, answer_id):
		user_list = DownvoteAnswer.objects.filter(answer__id=answer_id)
		users = DownvoteAnswerListSerializer(user_list, many=True, context={'request':request}).data
		return Response(users)



class FollowCategoryCreateView(APIView):
	def post(self, request):
		my_data = request.data
		my_serializer=FollowCategoryCreateSerializer(data=my_data)
		if my_serializer.is_valid(raise_exception=True):
			new_data = my_serializer.data
			category_obj=Category.objects.get(id=new_data['category'])
			category_follow, created = FollowCategory.objects.get_or_create(category=category_obj, follower=request.user)
			if not created:
				category_follow.delete()
			return Response(new_data, status=HTTP_200_OK)
		return Response(my_serializer.errors, status=HTTP_400_BAD_REQUEST)


class FollowCategoryListView(APIView):
	permission_classes = [AllowAny,]

	def get(self, request, category_id):
		follower_list = FollowCategory.objects.filter(category__id=category_id)
		followers = FollowCategoryListSerializer(follower_list, many=True, context={'request':request}).data
		return Response(followers)


class FollowQuestionCreateView(APIView):
	def post(self, request):
		my_data = request.data
		my_serializer=FollowQuestionCreateSerializer(data=my_data)
		if my_serializer.is_valid(raise_exception=True):
			new_data = my_serializer.data
			question_obj=Question.objects.get(id=new_data['question'])
			question_follow, created = FollowQuestion.objects.get_or_create(question=question_obj, follower=request.user)
			if not created:
				question_follow.delete()
			return Response(new_data, status=HTTP_200_OK)
		return Response(my_serializer.errors, status=HTTP_400_BAD_REQUEST)

class FollowQuestionListView(APIView):
	permission_classes = [AllowAny,]

	def get(self, request, question_id):
		follower_list = FollowQuestion.objects.filter(question__id=question_id)
		followers = FollowQuestionListSerializer(follower_list, many=True, context={'request':request}).data
		return Response(followers)

class FollowUserCreateView(CreateAPIView):
	queryset = FollowUser.objects.all()
	serializer_class = FollowUserCreateSerializer
	permission_classes = [IsAuthenticated,]

	def perform_create(self,serializer):
		serializer.save(following=self.request.user)

class FollowUserListView(APIView):
	permission_classes = [AllowAny,]

	def get(self, request, follower_id):
		follower_list = FollowUser.objects.filter(follower__id=follower_id)
		followers = FollowUserListSerializer(follower_list, many=True, context={'request':request}).data
		print(follower_list)
		print(follower_id)

		return Response(followers)
