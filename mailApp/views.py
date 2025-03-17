from django.shortcuts import render
from .serializers import SubscribersSerializer,subscribedCategorySerializer
from rest_framework import viewsets,generics
from .models import Subscribers,SubscribedCategory,VerificationToken
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from rest_framework.views import APIView
from .service import SendConfirmEmail
from django.db import transaction
# Create your views here.
class SubscriberViewSet(viewsets.ModelViewSet):
    queryset= Subscribers.objects.all()
    serializer_class = SubscribersSerializer
    
    def create(self, request, *args, **kwargs):
        email = request.data.get('email')
        category_data = request.data.get('category')

        if not email or not category_data:
            return Response({
                "detail": "Email and categories are required."
            }, status=status.HTTP_400_BAD_REQUEST)

        # Check if the email already exists in the database
        if Subscribers.objects.filter(email=email).exists():
            return Response({
                "detail": "Subscriber with this email already exists."
            }, status=status.HTTP_400_BAD_REQUEST)

        # Validate if categories exist
        categories = []
        for category_item in category_data:
            category_name = category_item.get('name')
            try:
                category = SubscribedCategory.objects.get(name=category_name)
                categories.append(category)
            except SubscribedCategory.DoesNotExist:
                raise ValidationError(f"Category '{category_name}' does not exist.")
        #VERIFY USER FIRST
        # verifyUser()
        with transaction.atomic():
            
            token = VerificationToken.objects.create(email=email)

            # Generate the verification link
            verification_url = request.build_absolute_uri(reverse('verify-email', args=[str(token.token)]))
            if not SendConfirmEmail(verification_url,email):
                token.objects.filter(email=email).first().delete()
                return Response({
                    "detail": "Something went Off .Sorry Resubscribe "
                }, status=status.HTTP_400_BAD_REQUEST)
        subscriber = Subscribers.objects.create(email=email)
        subscriber.category.set(categories)
        subscriber.save()
        return Response({
            "detail": "A verification email has been sent. Please check your inbox to confirm your subscription."
        }, status=status.HTTP_200_OK)
        
    # Update subscriber categories with PATCH /subscribers/update
    @action(detail=False, methods=['patch'], url_path="update")
    def update_categories(self, request):
        email = request.data.get('email')
        categories_data = request.data.get('category')

        if not email or not categories_data:
            return Response({
                "detail": "Email and categories are required."
            }, status=400)

        # Validate that category names exist
        category_names = [category.get('name') for category in categories_data]
        if not category_names:
            return Response({
                "detail": "At least one category name is required."
            }, status=400)

        try:
            subscriber = Subscribers.objects.get(email=email)
        except Subscribers.DoesNotExist:
            return Response({
                "detail": "Subscriber not found."
            }, status=404)

        # Validate categories
        categories = []
        for category_data in categories_data:
            category_name = category_data.get('name')
            if category_name:
                try:
                    category = SubscribedCategory.objects.get(name=category_name)
                    categories.append(category)
                except SubscribedCategory.DoesNotExist:
                    return Response({
                        "detail": f"Category '{category_name}' does not exist."
                    }, status=404)
        
        # Update subscriber categories
        subscriber.category.set(categories)
        subscriber.save()

        # Return updated subscriber data
        return Response(SubscribersSerializer(subscriber).data, status=200)

        
        # PATCH subscibers/unsubscribe
    @action(detail=False,methods=['patch'],url_path="unsubscribe")
    def unsubscribe(self,request):
            email = request.data.get("email")
            print(email)
            try:
                subscriber = Subscribers.objects.get(email=email) 
            except Subscribers.DoesNotExist:
                return Response({
                    "detail":"Subscriber not Found."
                },status=404)
            subscriber.SuscribeStatus=False
            subscriber.save()
            return Response({
                
                "detail":"Subscriber Unsubscribed."
            },status=200) 

class   SubscribedCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SubscribedCategory.objects.all()
    serializer_class= subscribedCategorySerializer
    
    
class VerifyEmailView(APIView):
    def get(self, request, token, *args, **kwargs):
        try:
            verification_token = VerificationToken.objects.get(token=token)

            if verification_token.verified:
                return Response({
                    "detail": "This email is already verified."
                }, status=status.HTTP_400_BAD_REQUEST)

            # Mark the token as verified
            verification_token.verified = True
            verification_token.save()

            # Create the subscriber instance
            email = verification_token.email
            subscriber = Subscribers.objects.filter(email=email).first()
            subscriber.verified=True
            subscriber.save()

            return Response({
                "detail": "Your email has been verified, and your subscription is now active."
            }, status=status.HTTP_200_OK)

        except VerificationToken.DoesNotExist:
            return Response({
                "detail": "Invalid verification token."
            }, status=status.HTTP_400_BAD_REQUEST)
            
