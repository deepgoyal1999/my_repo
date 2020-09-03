from django.shortcuts import render,get_object_or_404
from blog.models import Post,comments
from blog.forms import commentform
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from taggit.models import Tag 
# Create your views here.

def Post_view(request,tag_slug=None):
    post_data=Post.objects.all()
    tag=None
    if tag_slug:
        tag=get_object_or_404(Tag,slug=tag_slug)
        post_data=post_data.filter(tags__in=[tag])

    paginator=Paginator(post_data,2)
    page_number=request.GET.get('page')
    try:
        post_data=paginator.page(page_number)
    except PageNotAnInteger:
        post_data=paginator.page(1)
    except EmptyPage:
        post_data=paginator.page(paginator.num_pages)
    return render(request,'blog/home.html',{'post_data':post_data,'tag':tag})

def Post_detail_view(request,year,month,day,post):
    post=get_object_or_404(Post,slug=post,status="published",
                                          publish__year=year,
                                          publish__month=month,
                                          publish__day=day)

    comments=post.comments.filter(active=True)
    submit=False
    if request.method=="POST":
        form=commentform(request.POST)
        if form.is_valid():
            new_comment=form.save(default=False)
            new_comment.post=post
            new_comment=form.save()
            submit=True
    else:
        form=commentform()
    return render(request,'blog/post_detail.html',{'post':post,'form':form,'submit':submit,'comments':comments})


from django.core.mail import send_mail
from blog.forms import sendmailform

def mail_view(request,id):
    post=get_object_or_404(Post,id=id,status='published')
    sent=False
    if request.method=="POST":
        form=sendmailform(request.POST)
        if form.is_valid():
            d=form.cleaned_data
            post_url=request.build_absolute_uri(post.get_absolute_url())
            message='Read post {} \n By:{} \n Comments:{}'.format(post_url,d['name'],d['comments'])
            subject='{} ({})recomends you to read {}'.format(d['name'],d['email'],post.title)
            send_mail(subject,message,'upto@blog.com',[d['to']])
            sent=True
    else:
        form=sendmailform()



    return render(request,'blog/sendmail.html',{'post':post,'form':form,'sent':sent})
