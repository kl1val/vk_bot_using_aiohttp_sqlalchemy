from aiohttp.web import HTTPForbidden
from aiohttp_apispec import request_schema, response_schema, docs
from aiohttp_session import new_session

from app.admin.schemes import AdminSchema
from app.web.mixins import AuthRequiredMixin
from app.web.app import View
from app.web.utils import json_response


class AdminLoginView(View):

    @docs(tags=["admin"], summary="Login of admin", description="Method allowing admin to login")
    @request_schema(AdminSchema)
    @response_schema(AdminSchema, 200)
    async def post(self):
        email, password = self.data["email"], self.data["password"]
        admin  = await self.store.admins.get_by_email(email)
        if not admin or not admin.is_password_valid(password):
            raise HTTPForbidden(reason="Invalid login data")
        
        admin_schema = AdminSchema().dump(admin)
        session = await new_session(request=self.request)
        session["admin"] = admin_schema

        return json_response(data=admin_schema)



class AdminCurrentView(AuthRequiredMixin, View):

    @docs(tags=["admin"], summary="Current admin", description="Return information about currently active admin")
    @response_schema(AdminSchema, 200)
    async def get(self):
        admin_schema = AdminSchema().dump(self.request.admin)
        return json_response(data=admin_schema)
