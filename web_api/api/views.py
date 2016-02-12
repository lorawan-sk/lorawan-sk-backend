from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from api.models import Rawpoint, Point, Node, Key
import csv

def index(request):
    return HttpResponse("Not much to see here mate!")

@csrf_exempt
def points_this_node(request, node_id):
    if request.method == 'GET':
        node = Node.objects.get(id = node_id)
        p_list = Point.objects.filter(node = node_id).order_by('-timestamp')[:100]
        out = {
            'dataset': [],
            'node': {
                'serial': node.id,
                'name': node.name,
                'owner': node.owner.username,
            }
        }
        for p in p_list:
            out['dataset'].append({
                'value': p.value,
                'timestamp': str(p.timestamp),
                'key_numeric': p.key.numeric,
                'key_description': p.key.key,
                'key_unit': p.key.unit,
            })
        if request.GET.get('format') == 'csv':
            response = HttpResponse(content_type='text/plain')
            writer = csv.writer(response)
            for p in p_list:
                writer.writerow([ p.timestamp, p.key.numeric, p.value ])
            return response
        else:
            return JsonResponse(out, safe=False)

def points_this_node_key(request, node_id, key_numeric):
    if request.method == 'GET':
        if not request.GET.get('limit'):
            limit = 1000
        else:
            limit = request.GET.get('limit')
        key = Key.objects.get(numeric=key_numeric)
        node = Node.objects.get(id = node_id)
        p_list = Point.objects.filter(node = node, key = key).order_by('-timestamp')[:limit]
        out = {
            'dataset': [],
            'node_serial': node.id,
            'key': key.numeric,
        }
        for point in p_list:
            out['dataset'].append({
                'value': point.value,
                'timestamp': str(point.timestamp),
                'rssi': point.rssi
            })
        if request.GET.get('format') == 'csv':
            response = HttpResponse(content_type='text/plain')
            writer = csv.writer(response)
            i = 0
            for p in p_list:
                writer.writerow([ i, p.timestamp, p.key.numeric, p.value ])
                i = i + 1
            return response
        else:
            return JsonResponse(out, safe=False)

def points_all_nodes(request):
    if request.method == 'GET':
        p_list = Point.objects.all().order_by('-timestamp')[:1000]
        out = []
        for p in p_list:
            out.append({
                'value': p.value,
                'timestamp': str(p.timestamp),
                'key': p.key.numeric,
                'node': {
                    'serial': p.node.id,
                    'owner': p.node.owner.username,
                }
            })
        return JsonResponse(out, safe=False)

def points_all_nodes_key(request, key_numeric):
    if request.method == 'GET':
        key = Key.objects.get(numeric=key_numeric)
        p_list = Point.objects.filter(key = key).order_by('-timestamp')[:1000]
        out = []
        for p in p_list:
            out.append({
                'value': p.value,
                'timestamp': str(p.timestamp),
                'key': p.key.numeric,
                'node': {
                    'serial': p.node.id,
                    'owner': p.node.owner.username,
                }
            })
        return JsonResponse(out, safe=False)

def gecko_funnel_key(request, key_numeric):
    if request.method == 'GET':
        key = Key.objects.get(numeric=key_numeric)
        out = { "item": [] }
        for node in Node.objects.all():
            point = Point.objects.filter(node=node, key = key).order_by('-timestamp').first()
            out['item'].append({
                'value': point.value,
                'label': "Node #" + str(point.node.id) + " - " + point.node.owner.first_name + " " + point.node.owner.last_name,
                }
            )
        return JsonResponse(out, safe=False)

def gecko_line_datetime_node_key(request, node_id, key_numeric):
    if request.method == 'GET':
        if not request.GET.get('limit'):
            limit = 100
        else:
            limit = request.GET.get('limit')
        key = Key.objects.get(numeric=key_numeric)
        node = Node.objects.get(id = node_id)
        p_list = Point.objects.filter(node = node, key = key).order_by('-timestamp')[:limit]
        out = {
            'x_axis': {
                'type': 'datetime' 
            },
            'series': [{
                'name': key.key + " for node #" + str(node.id),
                'data': []
            }],
        }
        for point in p_list:
            out['series'][0]['data'].append([
                str(point.timestamp.isoformat()),
                point.value
            ])
        return JsonResponse(out, safe=False)

def gecko_meter_node_key(request, node_id, key_numeric):
    if request.method == 'GET':
        key = Key.objects.get(numeric=key_numeric)
        node = Node.objects.get(id = node_id)
        point = Point.objects.filter(node = node, key = key).last()
        out = {
            'item': point.value,
            'min': {
                'value': 629
            },
            'max': {
                'value': 850
            } 
        }
        return JsonResponse(out, safe=False)

def node_info(request, node_id):
    if request.method == 'GET':
        n = Node.objects.filter(id = node_id)[0]
        out = {
            'serial': n.id,
            'name': n.name,
            'location': n.location,
            'description': n.description,
            'owner': n.owner.username,
        }
        return JsonResponse(out, safe=False)

def rawpoints(request):
    if request.method == 'GET':
        p_list = Rawpoint.objects.all().order_by('-timestamp')[:1000]
        if request.GET.get('format') == 'csv':
            response = HttpResponse(content_type='text/plain')
            writer = csv.writer(response)
            for p in p_list:
                writer.writerow([ p.gw.description, p.timestamp, p.payload, p.rssi ])
            return response
        else:
            out = { 'dataset': [] }
            for p in p_list:
                out['dataset'].append({
                    'payload': p.payload,
                    'timestamp': p.timestamp,
                    'gw': p.gw.description,
                })
            return JsonResponse(out, safe=False)

@csrf_exempt
def save_point(request):
    if request.method == 'POST':
        out = {
            'request': request.body,
        }
        return JsonResponse(out, safe=False)