from rest_framework import status,generics, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import *
# Create your views here.

class SignUp(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self,request):
        user_data = request.data
        serializer = UserSerializer(data=user_data)
        if serializer.is_valid(raise_exception=True):
            patron = serializer.save()
            patron.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST) 

class LoginView(generics.GenericAPIView):
    serializer_class =  LoginSerializer

    def post(self,request):
        serializer = LoginSerializer(data=request.data,context={'request':request})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class LogoutView(generics.GenericAPIView):
     permission_classes = [IsAuthenticated]
     def post(self, request):
          
          try:
               refresh_token = request.data["refresh_token"]
               token = RefreshToken(refresh_token)
               token.blacklist()
               content = {'message': 'Successfully logged out'}
               return Response(status=status.HTTP_205_RESET_CONTENT)
          except Exception as e:
               content = {'message': 'refresh token invalid'}
               return Response(content,status=status.HTTP_400_BAD_REQUEST)

class NoteViewSet(viewsets.ModelViewSet):
    permission_class = [IsAuthenticated]
    serializer_class = NoteSerializers
    queryset = Note.objects.all()

    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    
    
