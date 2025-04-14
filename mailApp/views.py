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
from datetime import timedelta
from django.utils import timezone
# Create your views here.
class SubscriberViewSet(viewsets.ModelViewSet):
    
    queryset= Subscribers.objects.all()
    serializer_class = SubscribersSerializer
    
    def create(self, request, *args, **kwargs):
        email = request.data.get('email')
        category_data = request.data.get('category')

        if not email or not category_data:
            return Response({
            "success": False,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Email and categories are required."
        }
            }, status=status.HTTP_400_BAD_REQUEST)

        # Check if the email already exists in the database
        if Subscribers.objects.filter(email=email).exists():
            subscriber=Subscribers.objects.filter(email=email).first()
            if subscriber.SuscribeStatus==True:
                return Response({
                "success": False,
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": f"Email Already Subscribed."
                }
                },status=status.HTTP_400_BAD_REQUEST)
            if subscriber.SuscribeStatus==False:
                subscriber.delete()
        #     return Response({
        #     "success": False,
        #     "error": {
        #         "code": "VALIDATION_ERROR",
        #         "message": "Subscriber with This email Already Exists."
        # }
        # }, status=status.HTTP_400_BAD_REQUEST)
        # Validate if categories exist
        categories = []
        for category_item in category_data:
            category_name = category_item.get('name')
            try:
                category = SubscribedCategory.objects.get(name=category_name)
                categories.append(category)
            except SubscribedCategory.DoesNotExist:
                return Response({
                "success": False,
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": f"Category '{category_name}' does not exist."
                }
                },status=status.HTTP_400_BAD_REQUEST)
                
        #VERIFY USER FIRST
        # verifyUser()
        with transaction.atomic():
            try:
                token = VerificationToken.objects.create(email=email)
            except:
                return Response({
                "success": False,
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": f"Check Your Email Address.We have  Already send Verification Link."
                }
                },status=status.HTTP_400_BAD_REQUEST)

            # Generate the verification link
            verification_url = request.build_absolute_uri(reverse('verify-email', args=[str(token.token)]))
            if not SendConfirmEmail(verification_url,email,action="subscribe"):
                # token.objects.filter(email=email).delete()
                return Response({
                "success": False,
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "Something went Off .Sorry Resubscribe."
                }
                },status=status.HTTP_400_BAD_REQUEST)
            subscriber = Subscribers.objects.create(email=email)
            subscriber.category.set(categories)
            subscriber.save()
            return Response({
                "success": True,
                "message":"A verification email has been sent. Please check your inbox to confirm your subscription.",
                "data" :{}
                },status=status.HTTP_200_OK)

        
    # Update subscriber categories with PATCH /subscribers/update
    @action(detail=False, methods=['patch'], url_path="update")
    def update_categories(self, request):
        email = request.data.get('email')
        categories_data = request.data.get('category')

        if not email or not categories_data:
            return Response({
                "success": False,
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "Email and categories are required."
                }
                },status=status.HTTP_400_BAD_REQUEST)
           

        # Validate that category names exist
        category_names = [category.get('name') for category in categories_data]
        if not category_names:
            return Response({
                "success": False,
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "At least one category name is required."
                }
                },status=status.HTTP_400_BAD_REQUEST)
           

        try:
            subscriber = Subscribers.objects.get(email=email)
            print("here")
            
        except Subscribers.DoesNotExist:
            return  Response({
                "success": False,
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "Subscriber Not Found."
                }
                },status=status.HTTP_400_BAD_REQUEST)

        # Validate categories
        categories = []
        for category_data in categories_data:
            category_name = category_data.get('name')
            if category_name:
                try:
                    category = SubscribedCategory.objects.get(name=category_name)
                    categories.append(category)
                except SubscribedCategory.DoesNotExist:
                    return  Response({
                "success": False,
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": f"Category '{category_name}' does not exist."
                }
                },status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            try:
                print("verify")
                print(categories_data)
                # create a list from categorydata by taking only name
                # categories_data = [category.get('name') for category in categories_data]
                # print(categories_data)
                # print(categories_data)
                token = VerificationToken.objects.create(email=email,action="update",data=categories_data)
                print(token.token)
                print("token created ")
                token.save()
            except:
                print("token not created")
                return Response({
                "success": False,
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": f"Check Your Email Address.We have  Already send Verification Link."
                }
                },status=status.HTTP_400_BAD_REQUEST)

            # Generate the verification link
            verification_url = request.build_absolute_uri(reverse('verify-email', args=[str(token.token)]))
            if not SendConfirmEmail(verification_url,email,action="update"):
                # token.objects.filter(email=email).delete()
                print("not send mail")
                return Response({
                "success": False,
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "Something went Off .Sorry Retry."
                }
                },status=status.HTTP_400_BAD_REQUEST)
            return Response({
                "success": True,
                "message":"A verification email has been sent. Please check your inbox to confirm your subscription.",
                "data" :{}
                },status=status.HTTP_200_OK)

        # Update subscriber categories
        # subscriber.category.set(categories)
        # subscriber.save()

        # # Return updated subscriber data
        # return Response(SubscribersSerializer(subscriber).data, status=200)

        
        # PATCH subscibers/unsubscribe
    @action(detail=False,methods=['patch'],url_path="unsubscribe")
    def unsubscribe(self,request):
            email = request.data.get("email")
            print(email)
            try:
                subscriber = Subscribers.objects.get(email=email) 
            except Subscribers.DoesNotExist:
                return  Response({
                "success": False,
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "Subscriber Not Found."
                }
                },status=status.HTTP_400_BAD_REQUEST)
                
                #Let send a verification email to the user to confirm unsubscription 
            with transaction.atomic():
            
                try:
                    token = VerificationToken.objects.filter(email=email).first()
                    if token:
                        token.delete()
                    # Create a new verification token for unsubscription
                    token = VerificationToken.objects.create(email=email,action="unsubscribe")
                    # Generate the verification link
                    verification_url = request.build_absolute_uri(reverse('verify-email', args=[str(token.token)]))
                    if not SendConfirmEmail(verification_url,email,action="unsubscribe"):
                        token.objects.filter(email=email).first().delete()
                        return Response({
                        "success": False,
                        "error": {
                            "code": "VALIDATION_ERROR",
                            "message": "Something went Off .Sorry ReUnsubscribe."
                        }
                        },status=status.HTTP_400_BAD_REQUEST)
                    return Response({
                        "success": True,
                        "message":"A verification email has been sent. Please check your inbox to confirm your unsubscription.",
                        "data" :{}
                        },status=status.HTTP_200_OK)
                except:
                    return Response({
                "success": False,
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": f"Check Your Email Address.We have  Already send Verification Link."
                }
                },status=status.HTTP_400_BAD_REQUEST)
            # subscriber.SuscribeStatus=False
            # subscriber.save()
            # return Response({
            #     "success": True,
            #     "message":"Sucessfully Unsubscribed",
            #     "data" :{}
            #     },status=status.HTTP_200_OK)



class   SubscribedCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SubscribedCategory.objects.all()
    serializer_class= subscribedCategorySerializer
    
class VerifyEmailView(APIView):
    def get(self, request, token, *args, **kwargs):
        try:
            verification_token = VerificationToken.objects.get(token=token)
            if timezone.now() > verification_token.created_at + timedelta(minutes=5):
                verification_token.delete()  # delete expired token
                return Response({
                    "success": False,
                    "error": {
                        "code": "VALIDATION_ERROR",
                        "message": f"Verification Token Expired."
                    }
                    },status=status.HTTP_400_BAD_REQUEST)
            if verification_token.action == "unsubscribe":
                try:
                    subscriber = Subscribers.objects.get(email=verification_token.email)
                    subscriber.SuscribeStatus=False
                    verification_token.delete()
                    subscriber.save()
                except Subscribers.DoesNotExist:
                    return Response({
                        "success": False,
                        "error": {
                            "code": "VALIDATION_ERROR",
                            "message": f"Subscriber Not Found."
                        }
                        },status=status.HTTP_400_BAD_REQUEST)
                return Response({
                    "success": True,
                    "message":"You have successfully unsubscribed from our newsletter.",
                    "data" :{}
                    },status=status.HTTP_200_OK)
            if verification_token.action == "subscribe":
                try:
                    if verification_token.verified:
                        return Response({
                        "success": False,
                        "error": {
                            "code": "VALIDATION_ERROR",
                            "message": f"Email Already Verified"
                        }
                        },status=status.HTTP_400_BAD_REQUEST)

                    verification_token.delete()

                    # Create the subscriber instance
                    email = verification_token.email
                    subscriber = Subscribers.objects.filter(email=email).first()
                    subscriber.verified=True
                    subscriber.SuscribeStatus=True
                    subscriber.save()
                    
                    return Response({
                        "success": True,
                        "message":"Your email has been verified, and your subscription is now active.",
                        "data" :{}
                        },status=status.HTTP_200_OK)

                except VerificationToken.DoesNotExist:
                    return Response({
                        "success": False,
                        "error": {
                            "code": "VALIDATION_ERROR",
                            "message": f"Invalid Verification Token."
                        }
                        },status=status.HTTP_400_BAD_REQUEST)
            if verification_token.action == "update":
                subscriber = Subscribers.objects.get(email=verification_token.email)
                categories = verification_token.data
                categories = [SubscribedCategory.objects.get(name=category['name']) for category in categories]
                # Update subscriber categories
                subscriber.category.set(categories)
                subscriber.save()
                verification_token.delete()
                # Send a success response
                return Response({
                    "success": True,
                    "message":"Your categories have been updated successfully.",
                    "data" :{}
                    },status=status.HTTP_200_OK)

                


        except VerificationToken.DoesNotExist:
            return Response({
                "success": False,
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": f"Invalid Verification Token."
                }
                },status=status.HTTP_400_BAD_REQUEST)
                
      