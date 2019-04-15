from rest_framework import serializers
from movies.models import Movie, Comment
from movies.helpers import omdb_enrichment


class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=True, max_length=300)

    # Fields filled using omdb api
    director = serializers.CharField(max_length=500, read_only=True)
    genre = serializers.CharField(max_length=2000, read_only=True)
    metascore = serializers.IntegerField(read_only=True)

    def create(self, validated_data):
        """
        Create and return a new `Movie` instance using enrichment data
        from OMDB.
        """
        genre, director, metascore = omdb_enrichment(validated_data.get('title'))

        validated_data.update(genre=genre)
        validated_data.update(director=director)
        validated_data.update(metascore=metascore)

        return Movie.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.save()
        return instance


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'body', 'movie_id')


class CommentsForMovieSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True)

    class Meta:
        model = Movie
        fields = ('comments',)
