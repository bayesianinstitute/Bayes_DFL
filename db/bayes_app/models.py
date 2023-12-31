from django.db import models
from django.utils import timezone

class TrainingInformation(models.Model):
    model_name_choices = [
        ('CNN', 'Convolutional Neural Network'),
    ]

    dataset_name_choices = [
        ('Mnist', 'MNIST'),
    ]

    optimizer_choices = [
        ('Adam', 'Adam'),
        ('Sgd', 'Stochastic Gradient Descent'),
    ]
    model_name = models.CharField(max_length=50, choices=model_name_choices)
    dataset_name = models.CharField(max_length=50, choices=dataset_name_choices)
    optimizer = models.CharField(max_length=50, choices=optimizer_choices)
    training_name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return f"{self.training_name} -{self.model_name} -{self.dataset_name} -{self.optimizer}"

    class Meta:
        verbose_name_plural="Training Information"
    
class TrainingResult(models.Model):
    training_info = models.ForeignKey(TrainingInformation, on_delete=models.CASCADE, related_name='training_results',null=True, blank=True)
    accuracy = models.FloatField()
    loss = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.timestamp = timezone.now()
        super().save(*args, **kwargs)    
    def __str__(self):
        return f"{self.training_info.model_name} - {self.training_info.dataset_name} - {self.training_info.optimizer} - {self.timestamp}"

    class Meta:
        verbose_name_plural="User Training Result"
    
class TrainingResultAdmin(models.Model):
    training_info = models.ForeignKey(
        TrainingInformation,
        on_delete=models.CASCADE,
        related_name='admin_training_results',  # Provide a unique related_name
        null=True,
        blank=True
    )
    node_id = models.CharField(max_length=100)
    accuracy = models.FloatField()
    loss = models.FloatField()
  
    timestamp = models.DateTimeField(auto_now_add=True)
    def save(self, *args, **kwargs):
        self.timestamp = timezone.now()
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.training_info.model_name} - {self.training_info.dataset_name} - {self.training_info.optimizer} - {self.timestamp}"
    
    class Meta:
        verbose_name_plural = "Admin Training Result"

    
class Logs(models.Model):
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.timestamp = timezone.now()
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.timestamp}"
    class Meta:
        verbose_name_plural="Logs"
        
class Admin(models.Model):

    NETWORK_STATUS_CHOICES = [
        ('connected', 'Connected'),
        ('disconnected', 'Disconnected'),
       
    ]
    ROLE_CHOICES = [
        ('User', 'User'),
        ('Admin', 'Admin'),
        ('BackupAdmin', 'BackupAdmin'),
    ]
    OPERATION_CHOICES = [
        ('idle', 'Idle'),
        ('resume', 'resume'),
        ('pause', 'pause'),
        ('terminate', 'terminate'),
    ]
    operation_status = models.CharField(
        max_length=20,
        choices=OPERATION_CHOICES,
        default='idle'
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='User'
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    node_id = models.CharField(max_length=100)
    model_hash = models.CharField(max_length=255, blank=True, null=True) 
    network_status = models.CharField(
        max_length=15,
        choices=NETWORK_STATUS_CHOICES,
        default='disconnected'
    )
    def save(self, *args, **kwargs):
        self.timestamp = timezone.now()
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.role}-{self.node_id}-{self.operation_status} - {self.model_hash}"
    
    
    class Meta:
        verbose_name_plural="AdminNodes"
    
class NodeStatusManager(models.Manager):
    def get_or_create_single_instance(self):
        instance, created = self.get_or_create(pk=1)
        return instance
    
class NodeStatus(models.Model):
    NETWORK_STATUS_CHOICES = [
        ('connected', 'Connected'),
        ('disconnected', 'Disconnected'),
    ]
    OPERATION_CHOICES = [
        ('idle', 'idle'),
        ('resume', 'resume'),
        ('pause', 'pause'),
        ('terminate', 'terminate'),
    ]
    operation_status = models.CharField(
        max_length=20,
        choices=OPERATION_CHOICES,
        default='idle'
    )
    network_status = models.CharField(
        max_length=15,
        choices=NETWORK_STATUS_CHOICES,
        default='disconnected'
    )    
    model_hash = models.CharField(max_length=255, blank=True, null=True) 
    objects = NodeStatusManager()
    def __str__(self):
        return f"{self.operation_status} - {self.network_status}"
   
    class Meta:
        verbose_name_plural="User Node Status"
    
class GlobalModelHash(models.Model):
    global_model_hash = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True) 
    def save(self, *args, **kwargs):
        self.timestamp = timezone.now()
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name_plural="GlobalModelHash"
 
class TrackManager(models.Manager):
    def get_or_create_single_instance(self):
        instance, created = self.get_or_create(pk=1)
        return instance
       
class Track(models.Model):
    ROLE_CHOICES = [
        ('User', 'User'),
        ('Admin', 'Admin'),
        ('BackupAdmin', 'BackupAdmin'),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='User'
    )
    objects = TrackManager()
    def __str__(self):
        return f"{self.role}"
   
    class Meta:
        verbose_name_plural="Track"
        