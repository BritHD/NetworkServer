from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

import networkx as nx
import pandas as pd
import json
import random
# Create your views here.
class getRandomCsv(APIView):
    def get(self, request, *args, **kwargs):
        names = ["Alfred", "Chloe", "Morgan", "Hilda", "Felix", "Ingrid", "Lissa", "Selena", "Roy", "Est"]
        genders = ["M", "F", "V"]
        nations = ['Sky', "Land", "Ocean"]

        attr = {name: {'gender': random.choice(genders), 'nation': random.choice(nations)} for name in names}
        combos = [(a, b) for idx, a in enumerate(names) for b in names[idx + 1:]]
        list = []

        for a, b in combos:
            list.append({'source': a, 'target': b, 'source_gender': attr[a]['gender'], 'weight': random.randint(1,100),
            'target_gender': attr[b]['gender'], 'source_nation': attr[a]['nation'], 'target_nation': attr[b]['nation']})

        jsonobj = json.dumps(list, ensure_ascii=False) 

        return Response(jsonobj, status=status.HTTP_200_OK)

class getNetwork(APIView):
    def get(self, request, *args, **kwargs):
        data = {
            "message": "GET request received"
        }
        return Response(data, status=status.HTTP_200_OK)
    def post(self, request, *args, **kwargs):
        # You can access the POST data from request.data
        received_data = request.data
        # Process the data as needed
        positions = getPosNetwork(received_data['data'], received_data['seed'], received_data['scale'], received_data['dis'])
        if positions == None: #bad request
            return Response({'request': 400}, status=status.HTTP_400_BAD_REQUEST)

        response_data = positions  # send back the positons

        return Response(response_data, status=status.HTTP_200_OK)
    
class getNetworkKamada(APIView):
    def get(self, request, *args, **kwargs):
        data = {
            "message": "GET request received"
        }
        return Response(data, status=status.HTTP_200_OK)
    def post(self, request, *args, **kwargs):
        # You can access the POST data from request.data
        received_data = request.data
        # Process the data as needed
        positions = getPosNetwork(received_data['data'], received_data['seed'], received_data['scale'], received_data['dis'], 'Kamada')
        if positions == None: #bad request
            return Response({'request': 400}, status=status.HTTP_400_BAD_REQUEST)

        response_data = positions  # send back the positons

        return Response(response_data, status=status.HTTP_200_OK)
    
def getPosNetwork(list, seed, scale, dis, layout = 'Spring'):
        s = []
        t = []
        w = []

        if 'source' not in list[0] or 'target' not in list[0] or 'weight' not in list[0]: #incorect csv
            return None

        for i in list:
            s.append(i['source'])
            t.append(i['target'])
            w.append(i['weight'])


        ddf = pd.DataFrame({'source': s, 'target': t, 'weight': w})

        G = nx.from_pandas_edgelist(ddf, source='source', target='target', edge_attr='weight')
        if layout == 'Spring':
            if (dis == 0):
                pos = nx.spring_layout(G, seed = seed, scale = scale)  # positions for all nodes - seed for set layout
            else:
                pos = nx.spring_layout(G, seed = seed, scale = scale, k = dis) #distance between nodes
        else: #Kamada
            pos = nx.kamada_kawai_layout(G, scale = scale)  #this layout doesn't take seeds, and i haven't figured out distance...

        newdict = {}
        for i in pos:
            newdict[i] = {'x': pos[i][0], 'y': pos[i][1]}
        jsonobj = json.dumps(newdict, ensure_ascii=False) 
        
        return jsonobj