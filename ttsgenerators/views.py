from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class TextToSpeechAPIView(APIView):

    permission_classes = (AllowAny,)
    
    def post(self, request, *args, **kwargs):
        text = request.data.get('text', '')
        return Response({'audio_url': f'http://example.com/tts/{text}.mp3'})