from starlette_admin.contrib.sqla import ModelView


class UserAdminView(ModelView):

    fields=[
        "id",
        "email",
        "password_hash",
        "first_name",
        "last_name",
        "proffesion_id",
        "bio",
        "post_count",
        "post_read_count",
        "is_active",
        "is_staff",
        "is_supperuser",
        "is_deleted",
        "deleted_email",
        "created_at",
        "updated_at"
        ]
    exclude_fields_from_list=[
        "password_hash",
        "bio",
        "post_count",
        "post_read_count",
        "is_deleted",
        "deleted_email",

    ] 
    
    exclude_fields_from_detail=[]
    exclude_fields_from_create=[
        "id",
        "created_at",
        "updated_at",
        "post_count",
        "post_read_count",
    ]
    exclude_fields_from_edit=[
        "id",
        "password_hash",
        "created_at",
        "updated_at"

    ]



class PostView(ModelView):
    fields=[
        "id",
        "title",
        "slug",
        "body",
        "category",
        "user_id",
        "views_count",
        "likes_count",
        "comments_count",
        "is_active",
        "created_at",
        "updated_at",

    ]
    exclude_fields_from_list=[
        "slug",
        "body",
        "views_count",
        "likes_count",
        "comments_count",
    ]
    exclude_fields_from_edit=[
        "id",
        "created_at",
        "updated_at"
    ]
    exclude_fields_from_create=[
        "id",
        "created_at",
        "updated_at"
    ]

class CategoryView(ModelView):
    fields=[
        "id",
        "slug",
        "name",
    ] 
    exclude_fields_from_create=[
        "id",

    ]   
    exclude_fields_from_detail=[]
    exclude_fields_from_edit=[
        "id"
    ]
    exclude_fields_from_list=[
    ]

class ProfessionView(ModelView):
    fields=[
        "id",
        "name"
    ]
    exclude_fields_from_detail=[]
    exclude_fields_from_create=["id"]
    exclude_fields_from_edit=["id"]
    exclude_fields_from_list=[]
class TagView(ModelView):
    fields=[
        "id",
        "slug",
        "name",
    ] 
    exclude_fields_from_create=[
        "id",

    ]   
    exclude_fields_from_detail=[]
    exclude_fields_from_edit=[
        "id"
    ]
    exclude_fields_from_list=[]
class PostTagView(ModelView):
    fields=["post_id",
            "tag_id"]    
class PostMediaView(ModelView):
    fields=["post_id",
            "media_id"]        

class CommentView(ModelView):
    fields=[
        "id",
        "user_id",
        "text",
        "post_id",
        "is_active",
        "created_at",
        "updated_at"
    ]   
    exclude_fields_from_create=[
        "id",
        "created_at",
        "updated_at",
    ]
    exclude_fields_from_list=[
        "updated_at",
    ]
    exclude_fields_from_edit=[
        "id",
        "created_at",
        "updated_at"
    ]
    exclude_fields_from_detail=[]
    