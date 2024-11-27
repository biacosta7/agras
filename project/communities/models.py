from django.db import models
from users.models import User
from seedbeds.models import Seedbed
from django.utils import timezone

class Community(models.Model):
    name = models.CharField(max_length=255, unique=True, null=False, blank=False)
    description = models.TextField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_communities')
    members = models.ManyToManyField(User, related_name='communities_members')
    admins = models.ManyToManyField(User, related_name='admin_communities', blank=True)
    seedbeds = models.ManyToManyField(Seedbed, related_name='communities')

    def __str__(self):
        return self.name

class MembershipRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='membership_requests', null=False)
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='membership_requests')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    request_date = models.DateTimeField(default=timezone.now)
    decision_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"O usuário {self.user} pediu para entrar na comunidade {self.community}"

class SendCommunityInvite(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    requested_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_community_invites')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_community_invites')
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='community_invites')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    invite_date = models.DateTimeField(default=timezone.now)
    decision_date = models.DateTimeField(null=True, blank=True)
