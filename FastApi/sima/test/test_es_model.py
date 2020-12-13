from src.utils.es_model import EsModel

data = {
    "setting_es_host": "192.168.98.131",
    "setting_es_port": 9200,
    "super_user": {
        "username": "1",
        "email": "admin@admin.com",
        "full_name": "string",
        "disabled": False,
        "is_superuser": True,
        "hashed_password": "string"
    }
}
es = EsModel(
    **data
)

print(es.pk_no)
print(es.save())
print(es.load())
print(es.json())
