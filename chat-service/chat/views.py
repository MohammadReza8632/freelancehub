from rest_framework import generics
from . serializers import MessageSerializer
from . models import Message
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

class MessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id_1 = self.kwargs['user_id_1']
        user_id_2 = self.kwargs['user_id_2']

        ids = sorted([int(user_id_1), int(user_id_2)])
        if int(self.request.user.id) != ids[0] and int(self.request.user.id) != ids[1]:
            raise PermissionDenied('someone trying to view a conversation that is not theirs')

        room_name = f'chat_{ids[0]}_{ids[1]}'
        return Message.objects.filter(room_name=room_name)
