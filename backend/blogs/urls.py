from django.urls import path
from .views import BlogListCreateView, BlogRetrieveUpdateDeleteView, BlogListView, LikeUnlikeBlogView, BlogCommentView, BlockCommentView, CommentListView, CommentUpdateView

urlpatterns = [
    path('blogs/', BlogListCreateView.as_view(), name='blog-list-create'),  # List and create blogs
    path('blogs/<int:pk>/', BlogRetrieveUpdateDeleteView.as_view(), name='blog-detail'),  # Retrieve, update, delete
    path('blogslist/', BlogListView.as_view(), name='blog-list'),
    path('blogs/<int:blog_id>/like/', LikeUnlikeBlogView.as_view(), name='like-unlike-blog'),
    path('blogs/<int:blog_id>/comment/', BlogCommentView.as_view(), name='comment-blog'),  # Comment on blog
    
    # New routes for comment listing and admin operations
    path('comments/', CommentListView.as_view(), name='comment-list'),  # List and create comments (admin only)
    path('comments/<int:pk>/', CommentUpdateView.as_view(), name='comment-update'),  # Update comment (admin only)
    path('comments/block/<int:comment_id>/', BlockCommentView.as_view(), name='block_comment'),
]
