from django.db import models
from django.contrib.auth import get_user_model
from cryptography.fernet import Fernet

# models.py
class ChatRoom(models.Model):
    """
    Model to represent a chat room.
    """
    name = models.CharField(max_length=255)
    participants = models.ManyToManyField(get_user_model(), related_name='chat_rooms')
    encryption_key = models.BinaryField()

    def __str__(self):
        return self.name

    def generate_key(self):
        return Fernet.generate_key()   

    def save(self, *args, **kwargs):
        if not self.encryption_key:  # Check if encryption key is not set
            self.encryption_key = self.generate_key()        
        super().save(*args, **kwargs)    
    

class Message(models.Model): 
    sender = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='sent_messages',default=None)    
    encrypted_content = models.CharField(max_length=255)   
    timestamp = models.DateTimeField(auto_now_add=True)
    thread = models.ForeignKey(ChatRoom,on_delete=models.CASCADE, default=None)

    def set_content(self, content, key):
        cipher_suite = Fernet(key)
        encrypted_content = cipher_suite.encrypt(content.encode('utf-8'))
        self.encrypted_content = encrypted_content

    def get_content(self, key):
        cipher_suite = Fernet(key)
        decrypted_content = cipher_suite.decrypt(self.encrypted_content).decode('utf-8')
        return decrypted_content

    def __str__(self):
        return f"{self.sender} - {self.thread} - {self.timestamp}"


    class Meta:
        ordering = ['-timestamp']
