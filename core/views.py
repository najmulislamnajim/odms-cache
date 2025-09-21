import json, redis
from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import sql

# Connect Redis
try:
    redis_pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
    redis = redis.Redis(connection_pool=redis_pool)
except Exception as e:
    print(e)

# Create your views here.
class CustomerView(APIView):
    def get(self, request):
        with connection.cursor() as cursor:
            cursor.execute(sql.CUSTOMER_SQL)
            rows = cursor.fetchall()
        
        for row in rows:
            data = {
                "partner": row[0],
                "name": " ".join([row[1], row[2]]),
                "contact_person": row[3] or "",
                "address": " ".join(row[4:11]),
                "mobile_no": row[11],
                "email": row[12],
                "drug_reg_no": row[13],
                "customer_group": row[14],
                "trans_p_zone": row[15],
            }
            key = f"customer-{row[0]}"
            json_data = json.dumps(data)
            redis.set(key, json_data)
        return Response(
            {"success": True, "message": f"{len(rows)} Data cached successfully."},
            status=status.HTTP_200_OK
        )
        
class MaterialView(APIView):
    def get(self, request):
        with connection.cursor() as cursor:
            cursor.execute(sql.MATERIAL_SQL)
            rows = cursor.fetchall()
        
        for row in rows:
            data = {
                "id": row[0],
                "mtnr": row[1],
                "plant": row[2],
                "sales_org": row[3],
                "dis_channel": row[4],
                "material_name": row[5],
                "producer_company": row[6],
                "team1": row[7],
                "pack_size": row[8],
                "unit_tp": float(row[9]),
                "unit_vat": float(row[10]),
                "mrp": float(row[11]),
                "brand_name": row[12],
                "brand_description": row[13],
                "active": row[14]
            }
            key = f"material-{row[1]}"
            json_data = json.dumps(data)
            redis.set(key, json_data)
        return Response(
            {"success": True, "message": f"{len(rows)} Data cached successfully."},
            status=status.HTTP_200_OK
        )
        
class UsersListView(APIView):
    def get(self, request):
        with connection.cursor() as cursor:
            cursor.execute(sql.USERS_SQL)
            rows = cursor.fetchall()
            
        for row in rows:
            data = {
                "da_code": row[0],
                "full_name": row[1],
                "mobile_number": row[2],
                "user_type": row[3],
                "status": row[7],
                "id": row[8]
            }
            key = f"user-{row[0]}"
            json_data = json.dumps(data)
            redis.set(key, json_data)
        return Response(
            {"success": True, "message": f"{len(rows)} Data cached successfully."},
            status=status.HTTP_200_OK
        )
            