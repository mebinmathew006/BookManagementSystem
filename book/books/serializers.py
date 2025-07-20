from rest_framework import serializers
from .models import Books,ReadingItem
import re 

class BookSerializer(serializers.ModelSerializer):
    # description = serializers.CharField(required=False, allow_blank=True)
    class Meta:
        model = Books
        fields =['id','title','book','genre','description']
        
        
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
    
    
class ReadingItemSerializer(serializers.ModelSerializer):
    book_details  = BookSerializer(source='book',required=False)
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