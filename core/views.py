from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest,\
                        HttpResponseForbidden, HttpResponseNotFound,\
                        FileResponse
from django.views.decorators.http import require_http_methods

from core.models import *
import time
import json
import core.proto_models.api_models_pb2 as api_proto
from datetime import datetime
from core.utils import *


ZERO_USER_ID = 0


def add_measure(request):
    try:
        add_req = api_proto.AddMeasureRequest()
        add_req = add_req.FromString(request.body)
        m_time = datetime.fromtimestamp(add_req.Time)
        user = CustomUser.objects.get(user_id=add_req.UserId)
        operator = Operator.objects.get(name=add_req.OperatorName)
        measure = Measure(user_id=user,
                          latitude=add_req.Latitude,
                          longitude=add_req.Longitude,
                          operator_id=operator,
                          signal=add_req.Signal,
                          time=m_time
                          )
        measure.save()
        if (measure.user_id.user_id != ZERO_USER_ID):
            new_score = compute_score_for_measure(measure)
            score = Scores.objects.get(user_id=measure.user_id)
            score.score += score
            score.save()
        return HttpResponse()
    except KeyError:
        return HttpResponseBadRequest()


def get_score(request):
    try:
        proto_req = api_proto.ScoreRequest()
        proto_req = proto_req.FromString(request.body)
        user = CustomUser.objects.get(user_id=proto_req.UserId)
        score = Scores.objects.get(user_id=user)
        res = api_proto.ScoreResponse()
        res.Score = score.score
        return HttpResponse(res.SerializeToString())
    except KeyError:
        return HttpResponseBadRequest()


def signal_map(request):
    return HttpResponseNotFound()
    
