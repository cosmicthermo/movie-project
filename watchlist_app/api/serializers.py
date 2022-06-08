from rest_framework import serializers
from watchlist_app.models import Watchlist, StreamingService, Review


class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        # fields = '__all__'
        exclude = ['watchlist']

class WatchlistSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only = True)
    # lenth_name = serializers.SerializerMethodField()

    class Meta:
        model = Watchlist
        # fields = '__all__'
        exclude = ['avg_rating']


class StreamingServiceSerializer(serializers.ModelSerializer):
    watchlist = WatchlistSerializer(many=True, read_only=True)
    # # watchlist = serializers.StringRelatedField(many=True, read_only=True)
    # watchlist = serializers.HyperlinkedRelatedField(
    #     many=True,
    #     read_only=True,
    #     view_name='movie_detail'
    # )

    class Meta:
        model = StreamingService
        fields = '__all__'
        # exclude = ['active']


# class WatchList(serializers.ModelSerializer):
#     watchlist = WatchlistSerializer(many=True, read_only=True)
#     # # watchlist = serializers.StringRelatedField(many=True, read_only=True)
#     # watchlist = serializers.HyperlinkedRelatedField(
#     #     many=True,
#     #     read_only=True,
#     #     view_name='movie_detail'
#     # )

#     class Meta:
#         model = StreamingService
#         fields = '__all__'

    

# def lenth_name(name):
#     if len(name) < 2:
#             raise serializers.ValidationError("The title is too short.")
#     else:
#         return name


# class WatchlistSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(validators=[lenth_name])
#     description = serializers.CharField()
#     active = serializers.BooleanField()

#     def create(self, validated_data):
#         return Watchlist.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         # instance.id = validated_data.get('id', instance.id)
#         instance.name = validated_data.get('name', instance.name)
#         instance.description = validated_data.get('description', instance.description)
#         instance.active = validated_data.get('active', instance.active)
#         instance.save()
#         return instance

#     def validate_name(self, name):
#         if len(name) < 2:
#             raise serializers.ValidationError("The title is too short.")
#         else:
#             return name

#     def validate(self, data):
#         if data['name'] == data['description']:
#             raise serializers.ValidationError("Title and description should not be the same.")
#         return data