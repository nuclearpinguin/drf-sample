from datetime import datetime, timedelta
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from movies.models import Movie, Comment
from movies.serializers import MovieSerializer, CommentSerializer, CommentsForMovieSerializer
from movies.helpers import top_counter


# MOVIES

class MoviesList(APIView):
    @staticmethod
    def get(request):
        movies = Movie.objects.all()

        # Simple filtering by metascore
        metascore_limit = request.query_params.get('metascore', None)
        if metascore_limit:
            movies = movies.filter(metascore__gte=metascore_limit)

        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)

    @staticmethod
    def post(request):
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class MovieDetails(APIView):
    @staticmethod
    def get_object(pk):
        try:
            return Movie.objects.get(pk=pk)
        except Movie.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        movie = self.get_object(pk)
        serializer = MovieSerializer(movie)
        return Response(serializer.data)

    def delete(self, request, pk):
        movie = self.get_object(pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# COMMENTS

class CommentsList(APIView):
    @staticmethod
    def get(request):
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    @staticmethod
    def post(request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class CommentsForMovie(APIView):
    @staticmethod
    def get_object(pk):
        try:
            return Movie.objects.get(pk=pk)
        except Movie.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        movie = self.get_object(pk)
        serializer = CommentsForMovieSerializer(movie)
        return Response(serializer.data.get('comments', []))


# TOP

class TopList(APIView):
    @staticmethod
    def get(request):
        now = datetime.now()
        default_from = now - timedelta(days=7)

        date_from = request.data.get('date_from', default_from.strftime("%Y-%m-%d"))
        date_to = request.data.get('date_to', (now+timedelta(days=1)).strftime("%Y-%m-%d"))
        data = top_counter(date_from, date_to)

        return Response(data)
