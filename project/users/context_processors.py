from .models import FileUpload

def images(request):
    if request.user.is_authenticated:
        # Imagem de perfil
        profile_image = FileUpload.objects.filter(user=request.user, image_type="profile").last()
        image_profile_url = profile_image.image.url if profile_image else None
        
        # Imagem da comunidade
        community_image = FileUpload.objects.filter(user=request.user, image_type="community").last()
        image_community_url = community_image.image.url if community_image else None

        # Imagem do seedbed
        seedbed_image = FileUpload.objects.filter(user=request.user, image_type="seedbed").last()
        image_seedbed_url = seedbed_image.image.url if seedbed_image else None
    else:
        image_profile_url = None
        image_community_url = None
        image_seedbed_url = None

    return {
        'image_profile_url': image_profile_url,
        'image_community_url': image_community_url,
        'image_seedbed_url': image_seedbed_url,
    }
