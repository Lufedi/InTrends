from app import ma

class TermSchema(ma.Schema):
    class Meta:
        fields = ("id", "term")

class JobsSchema(ma.Schema):
    class Meta:
        fields = ("id", "location", "total", "created_at", "term_id")
        