from core.models import *
import random
from datetime import datetime
x1 = 50
y1 = 30
x2  = 60
y2 = 45

n = 10
user = CustomUser.objects.get(user_id=0)
operator = Operator.objects.get(name="BEELINE")
network = Operator.objects.get(network_name='LTE')

for i in range(x1, x2):
    for j in range(y1, y2):
        for k in range(n):
            x = i + random.random()
            y = j + random.random()
            m = Measure(user_id=user, operator_id=operator, network_id=network, latitude=x, longitude=y,time=datetime.now(), signal=(x+y)/(x2+y2))
            m.save()
            
    
