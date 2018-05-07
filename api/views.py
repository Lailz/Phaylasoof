from django.shortcuts import render
from rest_framework.generics import (
	ListAPIView,
	RetrieveAPIView,
	CreateAPIView,
	DestroyAPIView,
	RetrieveUpdateAPIView
	)
from .models import Question, Category, Upvote, Downvote, Answer, FollowCategory, FollowUser, FollowQuestion
from .serializers import (
    CategoryListSerializer,
	QuestionListSerializer,
	AnswerListSerializer,
    UpvoteCreateSerializer,
    UpvoteListSerializer,
    DownvoteCreateSerializer,
    DownvoteListSerializer,
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

from rest_framework.filters import SearchFilter, OrderingFilter

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


class CategoryListView(APIView):
	permission_classes = [AllowAny,]

	def get(self, request):
		category_list = Category.objects.all()
		categories = CategoryListSerializer(category_list, many=True, context={'request':request}).data
		return Response(categories)


class QuestionListView(APIView):
	permission_classes = [AllowAny,]

	def get(self, request, category_id):
		question_list = Question.objects.filter(category__id=category_id)
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
		answers = AnswerListSerializer(answer_list, many=True).data
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



class UpvoteCreateView(CreateAPIView):
	queryset = Upvote.objects.all()
	serializer_class = UpvoteCreateSerializer
	permission_classes = [IsAuthenticated,]

	def perform_create(self,serializer):
		serializer.save(user=self.request.user)


class DownvoteCreateView(CreateAPIView):
	queryset = Downvote.objects.all()
	serializer_class = DownvoteCreateSerializer
	permission_classes = [IsAuthenticated,]

	def perform_create(self,serializer):
		serializer.save(user=self.request.user)


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
