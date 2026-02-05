from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, LoginSerializer ,ProfileSerilzer
from .service import refresh_function
from .models import ChatBotModel ,ProfileModel
import logging
logger=logging.getLogger(__name__)


class RegisterView(APIView):
    def post(self, request):
        print( "New UserRegistered -- username is ",request.data.get('username'), "Password is ", request.data.get('password')  )

        logger.debug("-------------------- Entered in RegisterAPIView ------------------------")
        logger.info('----------------------Post Request received------------------------------')
        
        try :
            serializer = RegisterSerializer(data=request.data)
                    
            if serializer.is_valid():
                user = serializer.save()
                refresh=refresh_function(user)
                return Response({
                    "message": "-----------------------User Registered Successfully-------------------",
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }, status=status.HTTP_201_CREATED)
            
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )    
        except ValueError as e :
            logger.error(f'Value Error Occured : ',{str(e)})
            return Response({"error": "Invalid value"},status=status.HTTP_400_BAD_REQUEST)
            
        except Exception :
            logger.exception("Unhandled Exception Post RegisterAPIView")            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )
        if user is None:
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        refresh = RefreshToken.for_user(user)       
        return Response({
            "Message ":"----------------------------Login Successfull-------------------------",
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        })
        

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]      
    
    def get(self, request):
        profile = getattr(request.user, 'profile', None)  # safely get profile
        profile_pic_url = profile.profile_pic.url if profile and profile.profile_pic else None
              
        return Response({
            "first_name":request.user.first_name,                   ### Changed here
            # "last_name":request.user.last_name,                   ### Changed here
            "username": request.user.username,
            "email": request.user.email,
            "profile_pic":profile_pic_url  
        })             
    def post(self,request):        
        profile, created = ProfileModel.objects.get_or_create(user=request.user)
        
        if "profile_pic" not in request.FILES:
              return Response({"message": "No file provided"},status=status.HTTP_400_BAD_REQUEST )
           
        serilizer=ProfileSerilzer(profile, data=request.data ,   partial=True)
        
        if serilizer.is_valid():
            serilizer.save()
            return Response({"message":"Profile Pic Uploaded successfulluy","profile_pic":serilizer.data["profile_pic"]} ,status=status.HTTP_200_OK)
        return Response(serilizer.errors ,status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    authentication_classes = []
    permission_classes = []
    
    def post(self, request):
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response(
                {"error": "Refresh token is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(
                {"message": "----------------------Logged out successfully------------------------"},
                status=status.HTTP_200_OK
            )

        except Exception:
            return Response(
                {"error": "Invalid or expired token"},
                status=status.HTTP_400_BAD_REQUEST
            )                   
                    
             
##------------------------- ChatBOT View --------------------------------------------------------------
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
load_dotenv()
            
class ChatBotAPIView(APIView) :
        def post(self ,request):
            try:
                
                prompt=request.data.get("prompt")
                llm = HuggingFaceEndpoint(
                    repo_id="openai/gpt-oss-20b",               #BEST Version
                    # repo_id="deepseek-ai/DeepSeek-V3.2",
                    # repo_id="HuggingFaceH4/zephyr-7b-beta",
                    task="text-generation",
                    
                    max_new_tokens=512,
                    temperature=0.3,
                    top_p=0.9,
                    top_k=50,
                    repetition_penalty=1.1,

                    # ⚡ Performance / stability
                    do_sample=True,
                    return_full_text=False,
                )        
                
                if not prompt:
                    return Response(
                        {"error": "prompt is required"},
                        status=status.HTTP_400_BAD_REQUEST
                    )                
                    
                model=ChatHuggingFace(llm=llm,temperature=2)
                result=model.invoke(prompt)
                
                print(result.content)
                
                ChatBotModel.objects.create(
                prompt=prompt,
                ai=result.content
                )
                return Response({"ai": result.content },status=status.HTTP_200_OK)
            except Exception as e:
                    return Response({"error": str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)        
        
        def get(self, request):
            chats = ChatBotModel.objects.all().order_by("-id")
            data = []
            for chat in chats:
                data.append({
                    "id": chat.id,
                    "prompt": chat.prompt,
                    "ai": chat.ai,
                })
            ChatBotModel.objects.all().delete()
            return Response(data, status=status.HTTP_200_OK)                    