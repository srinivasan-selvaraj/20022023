from app import app
from app.views import home
from app.utils.validation import jwt_token

app.add_url_rule("/", methods=["GET"], view_func=home.index)

app.add_url_rule("/create_parent/<pk>", methods=["GET"], view_func=home.create_parent)

app.add_url_rule("/create_child/<pk>", methods=["GET"], view_func=home.create_child)

app.route('/refresh', methods=['POST'], view_func=jwt_token.refresh)

app.add_url_rule("/api/one_one_mapping", methods=["POST"], view_func=home.one_mapping)

app.add_url_rule("/api/many_related", methods=["POST"], view_func=home.many_related)

app.add_url_rule("/api/get_all_columns/<pk>", methods=["GET"], view_func=home.all_columns)

app.add_url_rule("/api/get_all_tables", methods=["GET"], view_func=home.all_tables)

