from starlette_admin.contrib.sqla import Admin

from app.database import engine
from app.models import User,Post,Category,Proffesion,Tag,PostTag,PostMedia,Comments
from app.admin.views import UserAdminView,PostView,CategoryView,ProfessionView,TagView,PostTagView,PostMediaView,CommentView
from app.admin.auth import JSONAuthProvider



admin = Admin(engine=engine, title="Chesnokdek admin", base_url="/admin",auth_provider=JSONAuthProvider(login_path="/login", logout_path="/logout"))
# admin1 = Admin(engine=engine, title="Chesnokdek admin", base_url="/admin1",auth_provider=JSONAuthProvider(login_path="/login", logout_path="/logout"))

admin.add_view(UserAdminView(User, icon="fa fa-user"))
admin.add_view(PostView(Post,icon="fa fa-video"))
admin.add_view(CategoryView(Category,icon="fa fa-table"))
admin.add_view(ProfessionView(Proffesion,icon="fa fa-book"))
admin.add_view(TagView(Tag,icon="fa fa-tag"))
admin.add_view(PostTagView(PostTag,icon="fa fa-pen"))
admin.add_view(PostMediaView(PostMedia,icon="fa fa-car"))
admin.add_view(CommentView(Comments,icon="fa fa-comment"))
