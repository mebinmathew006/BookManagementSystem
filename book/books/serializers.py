from rest_framework import serializers
from .models import Books,ReadingItem,ReadingList
import re 


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields =['id', 'title', 'book', 'genre', 'description']
        
    def validate_book(self, value):
        if not value.name.lower().endswith('.pdf'):
            raise serializers.ValidationError("Only PDF files are allowed.")
        if value.content_type != 'application/pdf':
            raise serializers.ValidationError("Uploaded file must be a PDF.")
        return value
    
    def validate_title(self,value):
        if bool(re.match(r'^[A-Za-z\s]+$',value)):
            return value
        raise serializers.ValidationError("Only alphabetic titles are allowed.")
    
    def validate_genre(self,value):
        if bool(re.match(r'^[A-Za-z\s]+$',value)):
            return value
        raise serializers.ValidationError("Only alphabetic generes are allowed.")


class ReadingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadingList
        fields = ['id', 'name', 'created_at']
        read_only_fields = ['created_at']
    
    def validate_name(self, value):
        user = self.context['request'].user
        qs = ReadingList.objects.filter(user=user, name=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)  
        if qs.exists():
            raise serializers.ValidationError("You already have a reading list with this name.")
        return value

    
class ReadingItemCreateSerializer(serializers.Serializer):
    book = serializers.PrimaryKeyRelatedField(queryset=Books.objects.all())

    def validate(self, data):
        readinglist = self.context.get('readinglist')
        book = data.get('book')
        if ReadingItem.objects.filter(readinglist=readinglist, book=book).exists():
            raise serializers.ValidationError({
                'book': 'This book is already in your reading list.'
            })
        return data

    def create(self, validated_data):
        readinglist = self.context.get('readinglist')
        book = validated_data['book']
        order = readinglist.readingitems.count() + 1
        print(order,readinglist.readingitems.count())
        return ReadingItem.objects.create(
            readinglist=readinglist,
            book=book,
            order=order
        )

    
class ReadingItemSerializer(serializers.ModelSerializer):
    book_details = BookSerializer(source='book', required=False)
    class Meta:
        model = ReadingItem
        fields = ['id', 'book', 'readinglist', 'order', 'book_details']
        read_only_fields = ['readinglist', 'order']

    def validate(self, data):
        readinglist = self.context.get('readinglist')
        book = data.get('book')

        if ReadingItem.objects.filter(readinglist=readinglist, book=book).exists():
            raise serializers.ValidationError({
                'book': 'This book is already in your reading list.'
            })
        return data
