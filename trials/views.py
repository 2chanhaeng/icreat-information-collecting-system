from datetime import datetime, timedelta
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.pagination import (
    LimitOffsetPagination,
    PageNumberPagination,
    CursorPagination,
)
from rest_framework.status import HTTP_404_NOT_FOUND
from .models import Trial
from .serializers import TrialSerializer

# Get default page size from settings
DEFAULT_PAGE_SIZE = settings.REST_FRAMEWORK["PAGE_SIZE"]
DEFAULT_ORDERING = "-updated_at"


class TrialsView(APIView):
    def set_paginator(self, params):
        """
        Set pagination by value of pagination of params.
        Use PageNumberPagination where pagination is page.
        Use CursorPagination where pagination is cursor.
        Use LimitOffsetPagination as default.
        """
        match params.get("pagination", "limit"):
            case "page":
                # Page pagination
                # If page is given, use PageNumberPagination
                self.paginator = PageNumberPagination()
                self.paginator.page_size = params.get("page_size", DEFAULT_PAGE_SIZE)
            case "cursor":
                # Cursor pagination
                self.paginator = CursorPagination()
                self.paginator.ordering = params.get("order", DEFAULT_ORDERING)
                page_size = int(params.get("page_size", DEFAULT_PAGE_SIZE))
                self.paginator.page_size = page_size
                # If using cursor pagination
                # and self.paginator.page_size = params.get("page_size"),
                # then get TypeError: unsupported operand type(s) for +: 'int' and 'str'
                # So, convert page_size to int.
            case _:
                # Limit-offset pagination
                self.paginator = LimitOffsetPagination()
                self.paginator.default_offset = 0

    def get(self, request: Request) -> Response:
        """
        Get trials that updated for 7 days.
        GET /api/v1/trials/?page=<page:1>&page_size=<page_size:5>
        GET /api/v1/trials/?cursor=<cursor>&page_size=<page_size:5>
        GET /api/v1/trials/?limit=<limit:5>&offset=<offset:0>
        """

        trials = Trial.objects.filter(
            updated_at__gte=datetime.now() - timedelta(days=7),
        )
        self.set_paginator(request.query_params)
        page = self.paginator.paginate_queryset(trials, request)
        serializer = TrialSerializer(page, many=True)
        return self.paginator.get_paginated_response(serializer.data)


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
