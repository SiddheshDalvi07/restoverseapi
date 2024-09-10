from django.shortcuts import render

# Create your views here.
import requests
from django.http import JsonResponse
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework import status
from google.auth.credentials import Credentials
from googleapiclient.discovery import build
from rest_framework.decorators import api_view
from django.http import JsonResponse

from google.auth.credentials import Credentials
from googleapiclient.discovery import build
from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Review, Reply
from .serializers import ReviewSerializer, ReplySerializer

@api_view(['GET', 'POST'])
def review_list(request):
    if request.method == 'GET':
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)  # Log the serializer errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def add_reply(request, pk):
    try:
        review = Review.objects.get(pk=pk)  # Fetch review by ID
    except Review.DoesNotExist:
        return Response({"error": "Review not found"}, status=status.HTTP_404_NOT_FOUND)

    reply_serializer = ReplySerializer(data=request.data)
    if reply_serializer.is_valid():
        reply_serializer.save(review=review)  # Save reply with the review reference
        return Response(reply_serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(reply_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def fetch_reviews(request):
    # Retrieve access token from the Authorization header
    auth_header = request.META.get('HTTP_AUTHORIZATION')
    if not auth_header:
        return JsonResponse({'error': 'Authorization header not provided'}, status=400)

    # Extract the token from the Bearer format
    try:
        access_token = auth_header.split(' ')[1]
    except IndexError:
        return JsonResponse({'error': 'Invalid Authorization header format'}, status=400)

    if not access_token:
        return JsonResponse({'error': 'Access token not found'}, status=400)

    credentials = Credentials(token=access_token)

    try:
        # Initialize the My Business Account Management API client
        service = build('mybusinessaccountmanagement', 'v1', credentials=credentials)
        
        # Get the list of accounts
        accounts = service.accounts().list().execute()

        # Check if any accounts are available
        if not accounts.get('accounts'):
            return JsonResponse({'error': 'No accounts found'}, status=404)

        account_id = accounts['accounts'][0]['name']  # Ensure you have at least one account
        
        # Initialize the My Business Business Information API client
        business_service = build('mybusinessbusinessinformation', 'v1', credentials=credentials)
        
        # Get the list of locations for the account
        locations = business_service.accounts().locations().list(parent=account_id).execute()
        
        # Check if any locations are available
        if not locations.get('locations'):
            return JsonResponse({'error': 'No locations found'}, status=404)
        
        location_id = locations['locations'][0]['name']  # Ensure you have at least one location

        # Fetch reviews for the location
        location_details = business_service.accounts().locations().get(name=location_id).execute()
        
        # Extract reviews from location details (if available)
        reviews = location_details.get('reviews', [])
        
        return JsonResponse({
            'reviews': reviews,
            'averageRating': location_details.get('averageRating'),
            'totalReviewCount': location_details.get('totalReviewCount'),
            'nextPageToken': location_details.get('nextPageToken')
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)




@api_view(['POST'])
def google_login(request):
    code = request.data.get('code')
    
    if not code:
        return JsonResponse({'error': 'Authorization code is required.'}, status=status.HTTP_400_BAD_REQUEST)

    # Exchange authorization code for access token
    token_url = "https://oauth2.googleapis.com/token"
    
    data = {
        'code': code,
        'client_id': settings.GOOGLE_CLIENT_ID,
        'client_secret': settings.GOOGLE_CLIENT_SECRET,
        'redirect_uri': 'postmessage',  # For mobile/JS-based apps
        'grant_type': 'authorization_code',
    }

    try:
        response = requests.post(token_url, data=data)
        token_data = response.json()

        if 'error' in token_data:
            return JsonResponse({'error': token_data['error_description']}, status=status.HTTP_400_BAD_REQUEST)
        
        # Get user info using the access token
        access_token = token_data.get('access_token')
        request.session['access_token'] = access_token
        
       
        user_info_url = "https://www.googleapis.com/oauth2/v2/userinfo"
        headers = {'Authorization': f'Bearer {access_token}'}
        user_info_response = requests.get(user_info_url, headers=headers)
        user_info = user_info_response.json()

        # Use user_info to create or login the user in your app
        # Example response: {"id": "12345", "email": "test@example.com", "name": "John Doe", etc.}
        
        # Check if the user exists in your database, and if not, create a new user
        # Example: 
        # user = User.objects.filter(email=user_info['email']).first()
        # if not user:
        #     user = User.objects.create(email=user_info['email'], username=user_info['name'])
        #     # Further setup like generating tokens, etc.

        return JsonResponse({'user_info': user_info, 'access_token': access_token})

    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': 'Something went wrong while communicating with Google.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# views.py
from googleapiclient.discovery import build
from google.oauth2 import service_account
from django.conf import settings






# from django.contrib.auth.decorators import login_required
# from google.oauth2.credentials import Credentials
# from googleapiclient.discovery import build
# from django.http import JsonResponse

# SCOPES = ['https://www.googleapis.com/auth/business.manage']

# # @login_required
# # def fetch_reviews(request):
# #     if not request.user.socialaccount_set.exists():
# #         return JsonResponse({'error': 'Google account not linked'}, status=400)

# #     social_account = request.user.socialaccount_set.get(provider='google')
# #     token = social_account.socialtoken_set.first()

# #     credentials = Credentials(
# #         token.token,
# #         refresh_token=token.token_secret,
# #         token_uri='https://oauth2.googleapis.com/token',
# #         client_id='154250790058-t7d20mqf4ipgju60d5spg4jr785vshnm.apps.googleusercontent.com',
# #         client_secret='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'
# #     )

# #     try:
# #         service = build('mybusiness', 'v4', credentials=credentials)

# #         accounts = service.accounts().list().execute()
# #         account_id = accounts['accounts'][0]['name']
# #         locations = service.accounts().locations().list(parent=account_id).execute()
# #         location_id = locations['locations'][0]['name']
# #         reviews = service.accounts().locations().reviews().list(parent=location_id).execute()

# #         return JsonResponse({
# #             'accountId': account_id,
# #             'locationId': location_id,
# #             'reviews': reviews.get('reviews', [])
# #         })

# #     except Exception as e:
# #         return JsonResponse({'error': str(e)}, status=500)
# import os
# from django.http import JsonResponse
# from googleapiclient.discovery import build
# from google.oauth2.credentials import Credentials

# # def fetch_reviews(request):
# #     # Retrieve access token from user's session
# #     access_token = request.session.get('access_token')

# #     if not access_token:
# #         # Handle case where access token is not available
# #         return JsonResponse({'error': 'Access token not found'}, status=400)

# #     credentials = Credentials(
# #         token=access_token,
# #         # Other credential fields as needed
# #     )

# #     try:
# #         service = build('mybusiness', 'v4', credentials=credentials)

# #         # Get account and location information
# #         accounts = service.accounts().list().execute()
# #         account_id = accounts['accounts'][0]['name']
# #         locations = service.accounts().locations().list(parent=account_id).execute()
# #         location_id = locations['locations'][0]['name']

# #         # Fetch reviews
# #         reviews = service.accounts().locations().reviews().list(parent=location_id).execute()

# #         return JsonResponse({
# #             'accountId': account_id,
# #             'locationId': location_id,
# #             'reviews': reviews.get('reviews', [])
# #         })

# #     except Exception as e:
# #         return JsonResponse({'error': str(e)}, status=500)
# @api_view(['GET'])
# def fetch_reviews(request):
#     # Retrieve access token from the Authorization header
#     auth_header = request.headers.get('Authorization')
#     print(auth_header)

#     if not auth_header:
#         return JsonResponse({'error': 'Authorization header not provided'}, status=400)

#     # Extract the token from the Bearer format
#     access_token = auth_header.split(' ')[1]
#     print(access_token)

#     if not access_token:
#         return JsonResponse({'error': 'Access token not found'}, status=400)

#     credentials = Credentials(token=access_token)

#     try:
#         service = build('mybusiness', 'v4', credentials=credentials)

#         # Get account and location information
#         accounts = service.accounts().list().execute()
#         account_id = accounts['accounts'][0]['name']
#         locations = service.accounts().locations().list(parent=account_id).execute()
#         location_id = locations['locations'][0]['name']

#         # Fetch reviews
#         reviews = service.accounts().locations().reviews().list(parent=location_id).execute()

#         return JsonResponse({
#             'accountId': account_id,
#             'locationId': location_id,
#             'reviews': reviews.get('reviews', [])
#         })

#     except Exception as e:
#         return JsonResponse({'error': str(e)}, status=500)

# def fetch_reviews(request):
#     if request.method == 'GET':
#         # Retrieve access token from the Authorization header
#         auth_header = request.headers.get('Authorization')
#         print(f'Authorization Header: {auth_header}')

#         if not auth_header or not auth_header.startswith('Bearer '):
#             return JsonResponse({'error': 'Authorization header not provided or invalid'}, status=400)

#         # Extract the token from the Bearer format
#         access_token = auth_header.split(' ')[1] if ' ' in auth_header else None
#         print(f'Access Token: {access_token}')

#         if not access_token:
#             return JsonResponse({'error': 'Access token not found'}, status=400)

#         credentials = Credentials(token=access_token)
#         try:
#         # Initialize the Google Business Profile Performance API client
#             service = build('businessprofileperformance', 'v1', credentials=credentials)

#         # Example code to fetch reviews - adjust based on actual API methods
#         # For demonstration, assuming you need to list reviews directly:
#         reviews = service.reviews().list().execute()

#         return JsonResponse({
#             'reviews': reviews.get('reviews', [])
#         })

#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)

    #     try:
    #         service = build('businessprofileperformance', 'v1', credentials=credentials)

    #         # Get account and location information
    #         accounts = service.accounts().list().execute()
    #         account_id = accounts['accounts'][0]['name']
    #         locations = service.accounts().locations().list(parent=account_id).execute()
    #         location_id = locations['locations'][0]['name']

    #         # Fetch reviews
    #         reviews = service.accounts().locations().reviews().list(parent=location_id).execute()

    #         return JsonResponse({
    #             'accountId': account_id,
    #             'locationId': location_id,
    #             'reviews': reviews.get('reviews', [])
    #         })

    #     except Exception as e:
    #         print(f'Exception: {e}')  # Log the exception message
    #         return JsonResponse({'error': str(e)}, status=500)
    # else:
    #     return JsonResponse({'error': 'Invalid request method'}, status=405)








import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Set environment variable for Google OAuth
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# Path to client_secret.json, replace with your actual path
CLIENT_SECRETS_FILE = "client_secret_154250790058-t7d20mqf4ipgju60d5spg4jr785vshnm.apps.googleusercontent.com.json"

# Scopes required for Google My Business API
SCOPES = ['https://www.googleapis.com/auth/business.manage']

# Set redirect URI (Ensure it matches the one you registered in Google Cloud Console)
REDIRECT_URI = "http://localhost:8000/accounts/google/login/callback/"

# Function to exchange authorization code for an access token
# @csrf_exempt
# def google_login(request):
#     if request.method == 'POST':
#         try:
#             # Get the authorization code from the request
#             data = json.loads(request.body)
#             auth_code = data.get('code')
            
#             if not auth_code:
#                 return JsonResponse({'error': 'Authorization code not provided'}, status=400)
            
#             # Create flow object
#             flow = Flow.from_client_secrets_file(
#                 CLIENT_SECRETS_FILE,
#                 scopes=SCOPES,
#                 redirect_uri=REDIRECT_URI
#             )
            
#             # Fetch the token using the authorization code
#             flow.fetch_token(code=auth_code)
#             credentials = flow.credentials
            
#             # Get user information
#             user_info = get_user_info(credentials)
            
#             # Return token and user info to the frontend
#             return JsonResponse({
#                 'access_token': credentials.token,
#                 'user_info': user_info
#             })
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=400)
#     else:
#         return JsonResponse({'error': 'Invalid request method'}, status=405)

def get_user_info(credentials):
    try:
        service = build('oauth2', 'v2', credentials=credentials)
        user_info = service.userinfo().get().execute()
        return user_info
    except Exception as e:
        return {'error': str(e)}

# Fetch reviews from Google My Business
# @csrf_exempt
# def fetch_reviews(request):
#     if request.method == 'GET':
#         try:
#             # Retrieve access token from the Authorization header
#             auth_header = request.headers.get('Authorization')
#             if not auth_header:
#                 return JsonResponse({'error': 'Authorization header not provided'}, status=400)

#             # Extract the token from the Bearer format
#             access_token = auth_header.split(' ')[1]

#             if not access_token:
#                 return JsonResponse({'error': 'Access token not found'}, status=400)

#             # Use the access token to fetch Google My Business data
#             credentials = Credentials(token=access_token)
#             service = build('mybusiness', 'v4', credentials=credentials)

#             # Get account and location information
#             accounts = service.accounts().list().execute()
#             account_id = accounts['accounts'][0]['name']
#             locations = service.accounts().locations().list(parent=account_id).execute()
#             location_id = locations['locations'][0]['name']

#             # Fetch reviews
#             reviews = service.accounts().locations().reviews().list(parent=location_id).execute()

#             return JsonResponse({
#                 'accountId': account_id,
#                 'locationId': location_id,
#                 'reviews': reviews.get('reviews', [])
#             })
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)
