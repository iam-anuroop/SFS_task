from .models import File
from users.models import User
from .serializers import FileSerializer
from users.utils import generate_token,verify_token
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .permissions import IsopsUser
from rest_framework.permissions import IsAuthenticated


class FileuploadView(APIView):
    permission_classes = [IsAuthenticated,IsopsUser]

    def post(self,request):
        if request.user.role != 'ops':
            return Response({'message': 'Only Ops users can upload files'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        
        file = request.FILES.get('file')
        if not file:
            return Response({'message': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

        valid_extensions = ['pptx', 'docx', 'xlsx']
        if not file.name.split('.')[-1] in valid_extensions:
            return Response(
                {'message': 'Invalid file type. Only pptx, docx, and xlsx files are allowed.'}, 
                status=status.HTTP_400_BAD_REQUEST
                )
        
        serializer = FileSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(user = request.user)
            return Response({'message': 'File uploaded successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class ListFilesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        files = File.objects.all()
        serializer = FileSerializer(files, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DownloadFileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, file_id):
        try:
            file = File.objects.get(id=file_id)
        except:
            return Response({'msg':'file not available'},status=status.HTTP_400_BAD_REQUEST)
        if file:
            token = generate_token(request.user)
            if request.user.role == 'client':
                download_url = request.build_absolute_uri(f'/filesapp/download-file/{token}/{file.id}/')
                return Response({'download_link': download_url}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Unauthorized access'}, status=status.HTTP_403_FORBIDDEN)
        return Response({'message': 'File not found'}, status=status.HTTP_404_NOT_FOUND)


class DownloadWithTokenView(APIView):

    # def get(self, request, token, file_id):
    #     try:
    #         user = verify_token(token)
    #         if user.role == 'client':
    #             file = File.objects.get(id=file_id)
    #             response = Response(file.data, content_type='application/octet-stream')
    #             print(response)
    #             response['Content-Disposition'] = f'attachment; filename={file.filename}'
    #             return response
    #         return Response({'message': 'Unauthorized access'}, status=status.HTTP_403_FORBIDDEN)
    #     except :
    #         return Response({'message': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)


    def get(self, request, token, file_id):
        try:
            user = verify_token(token)
            if user.role == 'client':
                # Retrieve the file or return 404 if not found
                file = File.objects.get(id=file_id)

                # Ensure file.data contains the actual file content
                if file.file:
                    response = Response(file.file, content_type='application/octet-stream')
                    response['Content-Disposition'] = f'attachment; filename={file.filename}'
                    return response
                else:
                    return Response({'message': 'File content not available'}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({'message': 'Unauthorized access'}, status=status.HTTP_403_FORBIDDEN)

        except File.DoesNotExist:
            return Response({'message': 'File not found'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)