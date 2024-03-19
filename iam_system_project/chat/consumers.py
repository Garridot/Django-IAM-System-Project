import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import *
from .models import Message as Messages
from asgiref.sync import sync_to_async


User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        # Fetch messages for the room asynchronously
        messages_context = await self.get_messages_for_room(self.room_name)
        # Fetch messages asynchronously
        messages = await self.fetch_messages(messages_context)  

        # Send the serialized messages as JSON
        await self.send(text_data=json.dumps({
            'type': 'initial_messages',
            'messages': messages            
        }))   
                 

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data_json = json.loads(text_data)
        message = data_json['message'].strip()  # Strip leading/trailing whitespace
        user = self.scope["user"]

        if message:  # Check if message is not empty
            await self.save_message(user, message)   

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': user
            }
        )

    async def chat_message(self, event):       
        message = event['message']
        user = event['username']        
        sender = await self.get_sender_email(user.id)

        await self.send(text_data=json.dumps({
            'type': 'new_message',
            'message': message,
            'sender': sender 
        }))    
    
    @sync_to_async
    def get_messages_for_room(self,room_id):      
        thread = ChatRoom.objects.get(id=room_id)   
        messages = Messages.objects.filter(thread=thread).order_by("timestamp")
        return messages

    # Fetch messages asynchronously
    @sync_to_async
    def fetch_messages(self, messages_queryset):             
        serialized_messages = []
        for message in messages_queryset:  
            serialized_message = {
                'message': message.encrypted_content,
                'sender': message.sender.email,
                'timestamp' : message.timestamp.strftime('%Y-%m-%d %H:%M:%S %Z'),  
                'thread'   :  message.thread.id             
            }
            serialized_messages.append(serialized_message)
           
        return serialized_messages    
    

    @sync_to_async
    def save_message(self, user, message):
        thread = ChatRoom.objects.get(id=self.room_name)
        message_to_save = Messages(
            sender=user,
            encrypted_content=message,
            thread=thread
        )
        message_to_save.save()

    @sync_to_async
    def get_sender_email(self, user_id):
        try:
            sender = get_user_model().objects.get(id=user_id)
            return sender.email
        except User.DoesNotExist:
            return None



