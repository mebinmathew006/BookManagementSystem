import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import BookSerializer,ReadingItemSerializer
from .models import Books,ReadingList,ReadingItem
from django.db import transaction

logger = logging.getLogger(__name__)


class UserUploadBook(APIView):
    
    permission_classes = [IsAuthenticated]
    def post (self,request):
        try:
            serializer = BookSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    {
                        'status':'error',
                        "message":"Validation Error",
                        "errors":serializer.errors
                    },
                    status= status.HTTP_400_BAD_REQUEST
                )
            # Save book with the current authenticated user as author
            serializer.save(author=request.user)
            return Response(
                {
                    'status':'success',
                    "message":"Book added successfully",
                },
                status= status.HTTP_201_CREATED
            )
                
        except Exception as e:
            logger.critical(f"Something Happened,{str(e)}")
            return Response(
                {
                    'status': 'error',
                    'message': 'An unexpected error occurred.',
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
    def delete(self, request, book_id=None):
        try:
            if book_id is None:
                return Response(
                    {
                     'status': 'error',
                     'message':  "Book ID is required"
                     }, 
                    status=status.HTTP_400_BAD_REQUEST)

            book = Books.objects.get(pk=book_id, author=request.user)
            book.delete()
            return Response(
                {
                    'status':'success',
                    "message": "Book deleted successfully"
                    }, 
                status=status.HTTP_204_NO_CONTENT)
        except Books.DoesNotExist:
            return Response(
                {
                    'status': 'error',
                    'message':  "Book not found"
                    }, 
                status=status.HTTP_404_NOT_FOUND
                )
        except Exception as e :
            logger.critical(f"An unexpected error happend {str(e)}")
            return Response(
                {
                    'status': 'error',
                    'message': 'An unexpected error occurred.',
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
    def get(self, request):
        try:
            books = Books.objects.all()
            serialized_books = BookSerializer(books, many=True)
            return Response(
                    {
                        'status':'success',
                        "Books":serialized_books.data
                    },
                    status= status.HTTP_400_BAD_REQUEST
                )
        except Exception as e :
            logger.critical(f"An unexpected error happend {str(e)}")
            return Response(
                {
                    'status': 'error',
                    'message': 'An unexpected error occurred.',
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
            
class UserReadingList(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def post (self, request):
        try:
            readinglist , created  = ReadingList.objects.get_or_create(user=request.user)
            next_order = readinglist.readingitems.count() + 1 or 1
            
            serializer = ReadingItemSerializer(data=request.data,context={
                'readinglist': readinglist,
                'order': next_order
            }
        )
            if not serializer.is_valid():
                return Response(
                    {
                        'status': 'error',
                        'message': 'Validation Error',
                        'errors': serializer.errors
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            serializer.save(readinglist=readinglist, order=next_order)
            return Response(
                {
                    'status':'success',
                    "message":"Book added successfully",
                },
                status= status.HTTP_201_CREATED
            )
        except Exception as e :
            logger.critical(f"An unexpected error happend {str(e)}")
            return Response(
                {
                    'status': 'error',
                    'message': 'An unexpected error occurred.',
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
    def get(self, request):
        try:
            readinglist, created = ReadingList.objects.get_or_create(user=request.user)
            reading_items = readinglist.readingitems.all()
            serializer = ReadingItemSerializer(reading_items, many=True)
            return Response({
                'status': 'success',
                'reading_items': serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.critical(f"An unexpected error happened: {str(e)}")
            return Response({
                'status': 'error',
                'message': 'An unexpected error occurred.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            
    def patch(self, request):
        try:
            old_order = int(request.data.get('old_order'))
            new_order = int(request.data.get('new_order'))

            if old_order == new_order:
                return Response({
                    'status': 'success',
                    'message': 'No changes made. Same position.'
                }, status=status.HTTP_200_OK)

            readinglist = ReadingList.objects.get(user=request.user)
            items = readinglist.readingitems.all()

            if old_order < 1 or new_order < 1 or old_order > items.count() or new_order > items.count():
                return Response({
                    'status': 'error',
                    'message': 'Invalid order positions.'
                }, status=status.HTTP_400_BAD_REQUEST)

            item1 = items.get(order=old_order)
            item2 = items.get(order=new_order)
            temp_order = items.count() + 1
            with transaction.atomic():  # Optional, ensures changes are rolled back on failure

                item1.order = temp_order
                item1.save()

                item2.order = old_order
                item2.save()

                item1.order = new_order
                item1.save()

            return Response({
                'status': 'success',
                'message': f'Item at position {old_order} swapped with item at {new_order}.'
            }, status=status.HTTP_200_OK)

        except ReadingList.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Reading list not found.'
            }, status=status.HTTP_404_NOT_FOUND)

        except ReadingItem.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Item with the specified order not found.'
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.critical(f"An unexpected error happened: {str(e)}")
            return Response({
                'status': 'error',
                'message': 'An unexpected error occurred.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, list_id=None):
        try:
            if list_id is None:
                return Response(
                    {
                     'status': 'error',
                     'message':  "Id is required"
                     }, 
                    status=status.HTTP_400_BAD_REQUEST)

            readinglist = ReadingItem.objects.get(id=list_id)
            readinglist.delete()
            return Response(
                {
                    'status':'success',
                    "message": "Reading list item deleted successfully"
                    }, 
                status=status.HTTP_204_NO_CONTENT)
        except ReadingItem.DoesNotExist:
            return Response(
                {
                    'status': 'error',
                    'message':  "Item not found"
                    }, 
                status=status.HTTP_404_NOT_FOUND
                )
        except Exception as e :
            logger.critical(f"An unexpected error happend {str(e)}")
            return Response(
                {
                    'status': 'error',
                    'message': 'An unexpected error occurred.',
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )