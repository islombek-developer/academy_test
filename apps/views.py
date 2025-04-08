from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Category, Test, Question, Answer, UserTestResult, UserSubscription
from .serializers import (
    CategorySerializer, TestListSerializer, TestDetailSerializer,
    UserTestResultSerializer, UserSubscriptionSerializer
)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TestViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TestDetailSerializer
        return TestListSerializer
    
    def get_queryset(self):
        queryset = Test.objects.all()
        
        category_id = self.request.query_params.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
            
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(is_free=True)
        else:
            try:
                subscription = self.request.user.subscription
                if not subscription.is_premium:
                    queryset = queryset.filter(is_free=True)
            except UserSubscription.DoesNotExist:
                queryset = queryset.filter(is_free=True)
                
        return queryset
    
    @action(detail=True, methods=['post'])
    def submit_answers(self, request, pk=None):
        test = self.get_object()
        answers = request.data.get('answers', [])
        
        if not answers:
            return Response({'error': 'No answers provided'}, status=status.HTTP_400_BAD_REQUEST)
    
        correct_count = 0
        total_questions = test.questions.count()
        
        for answer_data in answers:
            question_id = answer_data.get('question_id')
            answer_id = answer_data.get('answer_id')
            
            try:
                answer = Answer.objects.get(id=answer_id, question_id=question_id, is_correct=True)
                correct_count += 1
            except Answer.DoesNotExist:
                pass
        
        score = int((correct_count / total_questions) * 100) if total_questions > 0 else 0

        result, created = UserTestResult.objects.update_or_create(
            user=request.user,
            test=test,
            defaults={'score': score}
        )
        
        return Response({
            'score': score,
            'correct_answers': correct_count,
            'total_questions': total_questions
        })


class UserTestResultViewSet(viewsets.ModelViewSet):
    serializer_class = UserTestResultSerializer
    
    def get_queryset(self):
        return UserTestResult.objects.filter(user=self.request.user)


class UserSubscriptionViewSet(viewsets.ModelViewSet):
    serializer_class = UserSubscriptionSerializer
    
    def get_queryset(self):
        return UserSubscription.objects.filter(user=self.request.user)

