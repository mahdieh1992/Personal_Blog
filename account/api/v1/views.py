from rest_framework.generics import CreateAPIView,GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .serializers import RegisterSerializer,ResendVerifyEmailSerializer
from ...models import CustomUser
from rest_framework.response import Response
from rest_framework import status
from mail_templated  import EmailMessage
from rest_framework_simplejwt.tokens import RefreshToken 
from django.shortcuts import get_object_or_404
from .utily import ThreadEmail
import jwt
from Core import settings

class RegisterUserView(CreateAPIView):
    """
        register user with send email contain token(jwt)  
        and thread placement for send email
    """
    serializer_class=RegisterSerializer
    queryset=CustomUser.objects.all()

    def post(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email=serializer.validated_data['email']
            serializer.save()
            user=get_object_or_404(CustomUser,email=email)
            create_token=get_token_for_user(user=user)
            email=EmailMessage('email/send_email_register.tp1', {'token': create_token['access']}, 'mohamadimahdieh70@gmail.com', [user.email])
            send_email=ThreadEmail(email)
            send_email.start()
            return Response({'detail':'dear user we sended email contain a token'},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)    
    

class VerifyRegisterEmailView(GenericAPIView):
    """
        verify register with token i asset token didn't expire 
        and user existed and token valid
    """
    def get(self, request, token:str, *args, **kwargs):
        if token is not None:
            try:
                decode=jwt.decode(token,settings.SECRET_KEY,algorithms=['HS256'])
                user_id=decode['user_id']
                user=get_object_or_404(CustomUser,id=user_id)
                user.is_confirm=1
                user.save()
                return Response({'user':'Dear user email verified'},status=status.HTTP_200_OK)
            except jwt.DecodeError:
                return Response({'detail':'Invalid token'})    
            except jwt.ExpiredSignatureError:
                return Response({'detail':'Token expired'})    
            except user.DoesNotExist:
                return Response({'user':'User does not exists'},status=status.HTTP_400_BAD_REQUEST) 
        return Response(status=status.HTTP_400_BAD_REQUEST)    


class ResendVerifyEmailRegister(GenericAPIView):
    """
        send again token to user's email 
        if token expired and user's account isn't verify
    """
    serializer_class=ResendVerifyEmailSerializer
    def post(self,request):
        serializer=self.get_serializer(data=request.data)
        if serializer.is_valid():
            user=serializer.validated_data['user']
            create_token=get_token_for_user(user=user) 
            email=EmailMessage('email/send_email_register.tp1', {'token': create_token['access']}, 'mohamadimahdieh70@gmail.com', [user.email])
            send_email=ThreadEmail(email)
            send_email.start()
            return Response({'detail':'dear user we  again sended email contain a token'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class SendEmail(APIView):
      """
        test for send email its format is contain path a template  ,from email , to email
      """
      def get(self,request):
        email=EmailMessage('email/send_email_register.tp1', {'token': 'sssss'}, 'mohamadimahdieh70@gmail.com', ['test@gamil.com'])
        
        return Response({'detail':'Email sended'})
      


def get_token_for_user(user):
    """
     function create toke for users 
    """
    refresh=RefreshToken.for_user(user=user)
    return{
        'refresh':str(refresh),
        'access':str(refresh.access_token)
    }