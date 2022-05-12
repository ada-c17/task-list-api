from flask import request

class Handler():
    @classmethod
    def sort(cls):
        from app.routes import error_message
        sort_map = {
            "title": {
                "asc": cls.query.order_by(cls.title).all(),
                "desc": cls.query.order_by(cls.title.desc()).all()
            },
            "id": {
                "asc": cls.query.order_by(cls.id).all(),
                "desc": cls.query.order_by(cls.id.desc()).all()
            }
        }

        sort_query = request.args.get("sort")
        sort_by = request.args.get("sort_by")
        if sort_by == None:
            sort_by = "title"
        if sort_query == None:
            sort_query = "asc"

        if sort_by not in sort_map:
            error_message("Invalid query parameter value for sort-by", 400)
        if sort_query not in sort_map[sort_by]:
            error_message("Invalid query parameter value for sort", 400)

        sorted = sort_map[sort_by][sort_query]

        return sorted

    @classmethod
    def validate(cls, id):
        from app.routes import error_message

        try:
            id = int(id)
        except:
            error_message(f"{cls.__name__.lower()} {id} invalid", 400)
        
        valid = cls.query.get(id)
        if not valid:
            error_message(f"{cls.__name__.lower()} {id} not found", 404)

        return valid