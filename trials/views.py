from datetime import datetime, timedelta
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from .models import Trial
from .serializers import TrialSerializer
from rest_framework.status import HTTP_404_NOT_FOUND


class TrialsView(APIView):
    def get(self, request: Request) -> Response:
        """
        Get trials that updated for 7 days.
        GET /api/v1/trials/
        """

        trials = Trial.objects.filter(
            updated_at__gte=datetime.now() - timedelta(days=7)
        )
        serializer = TrialSerializer(trials, many=True)
        return Response(serializer.data)


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
