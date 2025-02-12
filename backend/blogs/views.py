from rest_framework import generics, permissions, status
from .serializers import BlogSerializer
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Blog, Like, Comment
from .serializers import BlogSerializer,  CommentSerializer



# List and Create View
class BlogListCreateView(generics.ListCreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [AllowAny]

# Retrieve, Update, Delete View
class BlogRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticated] # Restrict to admin users

  

class BlogListView(generics.ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticated]



class LikeUnlikeBlogView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, blog_id):
        try:
            blog = Blog.objects.get(id=blog_id)
        except Blog.DoesNotExist:
            return Response({'success': False, 'message': 'Blog not found'}, status=status.HTTP_404_NOT_FOUND)

        user = request.user
        like, created = Like.objects.get_or_create(user=user, blog=blog)

        if created:
            return Response({'success': True, 'message': 'Blog liked'}, status=status.HTTP_200_OK)
        else:
            like.delete()
            return Response({'success': True, 'message': 'Blog unliked'}, status=status.HTTP_200_OK)



class BlogCommentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, blog_id):
        try:
            blog = Blog.objects.get(id=blog_id)
            comments = Comment.objects.filter(blog=blog)
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Blog.DoesNotExist:
            return Response({"error": "Blog not found."}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, blog_id):
        try:
            # Get the blog object
            blog = Blog.objects.get(id=blog_id)

            # Initialize serializer with request data
            serializer = CommentSerializer(data=request.data)
            if serializer.is_valid():
                # Save the comment, assigning the user and blog programmatically
                serializer.save(user=request.user, blog=blog)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            # Return validation errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Blog.DoesNotExist:
            return Response({"error": "Blog not found."}, status=status.HTTP_404_NOT_FOUND)
        


class CommentListView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAdminUser]  # Only admins can list and create comments
    

class CommentUpdateView(generics.UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAdminUser]  # Only admins can update comments

    def perform_update(self, serializer):
        approved = self.request.data.get("approved", None)
        if approved is not None:
            serializer.save(approved=approved)



class BlockCommentView(APIView):
    """
    Block a comment by changing its status to "blocked".
    """

    def post(self, request, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id)
            comment.status = "blocked"  # Change status to "blocked"
            comment.save()
            return Response({"message": "Comment blocked successfully!"}, status=status.HTTP_200_OK)
        except Comment.DoesNotExist:
            return Response({"message": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)

