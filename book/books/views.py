import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Books,ReadingList,ReadingItem
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from django.http import Http404
from django.db import transaction
from .serializers import (
    BookSerializer,
    ReadingItemSerializer,
    ReadingItemCreateSerializer,
    ReadingListSerializer,
)
from django.db import IntegrityError

logger = logging.getLogger(__name__)


class Pagination(PageNumberPagination):
    page_size = 10  # Default items per page
    page_size_query_param = 'page_size'  # Optional override via query param
    max_page_size = 100

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
    
    def get(self, request):
        """Get paginated reading lists of the logged-in user"""
        readinglists = ReadingList.objects.filter(user=request.user)

        paginator = Pagination()
        paginated_qs = paginator.paginate_queryset(readinglists, request)
        serializer = ReadingListSerializer(paginated_qs, many=True)

        return paginator.get_paginated_response({
            'status': 'success',
            'reading_lists': serializer.data
        })
        
    def post(self, request):
        """Create a new reading list"""
        serializer = ReadingListSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'status': 'error', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, list_id):
        """Update an existing reading list"""
        readinglist = get_object_or_404(ReadingList, pk=list_id, user=request.user)
        serializer = ReadingListSerializer(
            readinglist, 
            data=request.data, 
            partial=True, 
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response({'status': 'error', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, list_id):
        """Delete a reading list"""
        readinglist = get_object_or_404(ReadingList, pk=list_id, user=request.user)
        readinglist.delete()
        return Response(
            {
                'status': 'success',
                'message': 'Reading list deleted.'
            },
            status=status.HTTP_204_NO_CONTENT
        )
class UserReadingListItem(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, list_id):
        try:
            readinglist = get_object_or_404(ReadingList, id=list_id, user=request.user)

            serializer = ReadingItemCreateSerializer(
                data=request.data,
                context={'request': request, 'readinglist': readinglist}
            )

            if not serializer.is_valid():
                return Response(
                    {'status': 'error',
                     'errors': serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                    )

            serializer.save()
            return Response(
                {'status': 'success',
                 'message': 'Book added successfully'},
                status=status.HTTP_201_CREATED
                )
        except Http404:
            return Response({'status': 'error', 'message': 'Reading list not found.'},
                        status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.critical(f"POST error: {str(e)}")
            return Response({'status': 'error', 'message': 'Unexpected error occurred.'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, list_id):
        try:
            readinglist = get_object_or_404(
                ReadingList.objects.prefetch_related('readingitems__book'), 
                id=list_id, 
                user=request.user
            )

            reading_items = readinglist.readingitems.all()  
            paginator = Pagination()
            paginated_qs = paginator.paginate_queryset(reading_items, request)  
            serializer = ReadingItemSerializer(paginated_qs, many=True)

            return paginator.get_paginated_response({
                'status': 'success',
                'list_id': readinglist.id,
                'name': readinglist.name,
                'created_at': readinglist.created_at,
                'items': serializer.data
            })

        except Http404:
            return Response({'status': 'error', 'message': 'Reading list not found.'},
                            status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.critical(f"GET error: {str(e)}")
            return Response({'status': 'error', 'message': 'Unexpected error occurred.'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def patch(self, request, list_id):
        try:
            old_order = int(request.data.get('old_order'))
            new_order = int(request.data.get('new_order'))

            readinglist = get_object_or_404(ReadingList, id=list_id, user=request.user)
            items = readinglist.readingitems.all()

            if old_order == new_order:
                return Response(
                    {'status': 'success',
                     'message': 'No changes made.'},
                    status=status.HTTP_200_OK
                    )

            if old_order < 1 or new_order < 1 or old_order > items.count() or new_order > items.count():
                return Response({'status': 'error',
                                 'message': 'Invalid order positions.'},
                                status=status.HTTP_400_BAD_REQUEST)

            item1 = items.get(order=old_order)
            item2 = items.get(order=new_order)

            with transaction.atomic():
                temp_order = items.count() + 1
                item1.order = temp_order
                item1.save()
                item2.order = old_order
                item2.save()
                item1.order = new_order
                item1.save()

            return Response({'status': 'success', 'message': 'Items reordered.'}, status=status.HTTP_200_OK)
        except Http404:
            return Response({'status': 'error', 'message': 'Reading list not found.'},
                        status=status.HTTP_404_NOT_FOUND)
        except ReadingItem.DoesNotExist:
            return Response({'status': 'error', 'message': 'Item not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.critical(f"PATCH error: {str(e)}")
            return Response({'status': 'error', 'message': 'Unexpected error occurred.'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def delete(self, request, list_id):
        try:
            item_id = request.data.get('item_id')
            if not item_id:
                return Response({'status': 'error', 'message': 'item_id is required.'}, status=status.HTTP_400_BAD_REQUEST)

            with transaction.atomic():  
                item = get_object_or_404(
                    ReadingItem,
                    id=item_id,
                    readinglist__id=list_id,
                    readinglist__user=request.user
                )

                readinglist = item.readinglist
                item.delete()

                
                remaining_items = readinglist.readingitems.order_by('order')
                for index, item in enumerate(remaining_items, start=1):
                    item.order = index
                ReadingItem.objects.bulk_update(remaining_items, ['order'])

            return Response({'status': 'success', 'message': 'Item deleted and order updated.'},
                            status=status.HTTP_204_NO_CONTENT)

        except Http404:
            return Response({'status': 'error', 'message': 'Reading list not found.'},
                            status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.critical(f"DELETE error: {str(e)}")
            return Response({'status': 'error', 'message': 'Unexpected error occurred.'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
