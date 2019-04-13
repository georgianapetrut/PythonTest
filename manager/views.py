from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from manager.serializers import TaskSerializer, BoardSerializer
from manager.models import Task, Board
from manager.constants import TaskState


# Instead of having two views for working with Tasks, we can have only one, a
# smart one
# This view can deal with all the responsibilities of the prior two views, combined
class TaskViewSet(viewsets.ModelViewSet):

    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    @action(detail=False, methods=['GET'])
    def done_tasks(selfself, request):
        queryset = Task.objects.filter(state=TaskState.DONE)
        serializer = TaskSerializer(queryset, many=True)

        return Response(serializer.data)

    def filter_queryset(self, queryset):
        board = self.request.GET['board']
        if board:
            queryset = queryset.filter(board_id=board)

        return queryset


class BoardViewSet(viewsets.ModelViewSet):

    serializer_class = BoardSerializer
    queryset = Board.objects.all()