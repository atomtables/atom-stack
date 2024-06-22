from ninja import Router

from accountman.views import AuthRequiredErrorOut
from atomtables_website.schemas import SuccessData, NotFoundErrorOut, UnrecoverableError
from blogsite.models import BlogPost

api = Router()


@api.get("/list", response={200: SuccessData, 500: UnrecoverableError})
def blog_list(request):
    try:
        blogs = BlogPost.objects.all()
        data = []
        for blog in blogs:
            data.append({
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
                "likes": blog.blog_likes_count,
                "comments": {
                    "count": blog.comments_count
                }
            })
        return SuccessData(info=data)
    except Exception as e:
        print(e)
        return 500, UnrecoverableError()


@api.get("/post/{post_id}/like")
def blog_like(request, post_id: str):
    if not request.user.is_authenticated:
        return AuthRequiredErrorOut()

    try:
        blog = BlogPost.objects.get(id=post_id)
    except BlogPost.DoesNotExist:
        return 404, NotFoundErrorOut()

    if not blog:
        return 404, NotFoundErrorOut()

    if request.user not in blog.blog_likes:
        blog.blog_likes.add(request.user)
        blog.blog_likes_count += 1

    return SuccessData(info={
        "likes": blog.blog_likes_count
    })


@api.get("/post/{post_id}")
def blog_post(request, post_id: str):
    try:
        try:
            blog = BlogPost.objects.get(id=post_id)
        except BlogPost.DoesNotExist:
            return 404, NotFoundErrorOut()

        if not blog:
            return 404, NotFoundErrorOut()

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
            "likes": blog.blog_likes_count,
            "comments": {
                "count": blog.comments_count,
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
    except Exception:
        return 500, UnrecoverableError()
