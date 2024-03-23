from ninja import Router

from atomtables_website.schemas import SuccessData
from blogsite.models import BlogPost

api = Router()


@api.get("/list")
def blog_list(request):
    return {
    }


@api.get("/post/{post_id}")
def blog_post(request, post_id: str):
    blog = BlogPost.objects.get(id=post_id)
    return SuccessData(info={
        "author": {
            "username": blog.author.username,
            "first_name": blog.author.first_name,
            "last_name": blog.author.last_name,
            "pfp": blog.author.profile.profile_picture.url
        },
        "title": blog.title,
        "subtitle": blog.subtitle,
        "content": blog.content,
        "titleImage": blog.title_image.url,
        "titleCaption": blog.title_image_caption,
        "blogImages": {
            "count": blog.blog_images.count(),
            "images": [image.image.url for image in blog.blog_images.order_by('blog_image_id')],
            "captions": [image.caption for image in blog.blog_images.order_by('blog_image_id')]
        },
        "comments": {
            "count": blog.comments.count(),
            "comments": [{
                "user": {
                    "username": comment.user.username,
                    "first_name": comment.user.first_name,
                    "last_name": comment.user.last_name,
                    "pfp": comment.user.profile.profile_picture.url
                },
                "content": comment.blog_content
            } for comment in blog.comments.all()]
        }
    })
