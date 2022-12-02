from datetime import datetime, timedelta
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.status import HTTP_404_NOT_FOUND
from .models import Trial
from .serializers import TrialSerializer

# Get default page size from settings
DEFAULT_PAGE_SIZE = settings.REST_FRAMEWORK["PAGE_SIZE"]


class TrialsView(APIView):
    def get(self, request: Request) -> Response:
        """
        Get trials that updated for 7 days.
        GET /api/v1/trials/?limit=<limit:5>&offset=<offset:0>
        GET /api/v1/trials/?page=<page:1>&page_size=<page_size:5>
        """

        trials = Trial.objects.filter(
            updated_at__gte=datetime.now() - timedelta(days=7)
        )
        params = request.query_params
        # pagination
        if params.get("page"):
            # If page is given, use PageNumberPagination
            paginator = PageNumberPagination()
            paginator.page_size = params.get("page_size", DEFAULT_PAGE_SIZE)
            paginator.default_page = 1
        else:
            # Default, use LimitOffsetPagination
            paginator = LimitOffsetPagination()
            paginator.default_offset = 0
        page = paginator.paginate_queryset(trials, request)
        serializer = TrialSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)


class TrialView(APIView):
    def get(self, request: Request, pk: str) -> Response:
        """
        Get a trial by number.
        GET /api/v1/trials/{number}
        """

        try:
            trial = Trial.objects.get(number=pk)
        except Trial.DoesNotExist:
            return Response({"message": "Not found"}, status=HTTP_404_NOT_FOUND)
        serializer = TrialSerializer(trial)
        return Response(serializer.data)
