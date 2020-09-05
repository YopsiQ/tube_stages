import os
import mimetypes
from wsgiref.util import FileWrapper

from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.http.response import HttpResponse
from django.template import loader
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, CreateView

from .forms import UploadFileForm
from .models import Video, Tag, VideoTag


class VideoView(LoginRequiredMixin, FormView):
    login_url = reverse_lazy('login')
    template_name = 'tube/upload_file.html'
    form_class = UploadFileForm

    def form_valid(self, form):
        kwargs = self.get_form_kwargs()
        tags_str = kwargs['data'].get('tags')
        tags = [x.strip('#') for x in tags_str.split()]
        existed_tags = {tag.name: tag.id for tag
                        in Tag.objects.filter(name__in=tags)}
        tags_to_create = [tag for tag in tags if tag not in existed_tags]
        tags_ids = list(existed_tags.values())
        for tag in tags_to_create:
            created_tag = Tag.objects.create(name=tag)
            tags_ids.append(created_tag.id)

        video = Video(
            file=kwargs.get('files')['video'],
            title=kwargs['data'].get('title'),
        )
        video.save()
        video_id = video.id

        for tags_id in tags_ids:
            VideoTag.objects.create(tag_id=tags_id, video_id=video_id)

        return HttpResponseRedirect(reverse('main'))


def uploaded_stream_detail(request, name):
    path = os.path.join(settings.MEDIA_ROOT, name)
    size = os.path.getsize(path)
    content_type, encoding = mimetypes.guess_type(path)
    content_type = content_type or 'application/octet-stream'
    response = HttpResponse(FileWrapper(open(path, 'rb')),
                            content_type=content_type)
    response['Content-Length'] = str(size)
    response['Accept-Ranges'] = 'bytes'
    return response


def watch(request, video_id):
    video = Video.objects.filter(id=video_id).first()
    name = video.file.name if video else None
    tags = [tag.name for tag
            in Tag.objects.filter(videotag__video__id=video_id)]

    template = loader.get_template('tube/video_detail.html')

    context = {
        'url': f'/tube/{name}',
        'tags': tags,
        'title': video.title,
    }
    return HttpResponse(template.render(context, request))


def main(request):
    q = request.GET.get('q', '')
    tag = request.GET.get('tag', '')
    if tag:
        videos = Video.objects.filter(videotag__tag__name= tag.strip('#'))
    else:
        videos = Video.objects.all()

    if q:
        videos = videos.filter(title__icontains=q)

    template = loader.get_template('tube/main.html')

    context = {
        'q': q,
        'tag': tag,
        'videos': videos,
        'video_count': videos.count()
    }
    return HttpResponse(template.render(context, request))


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('main'))


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'tube/signup.html'
