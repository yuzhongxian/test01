from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect

WHITELIST = ['/seller/login/', '/seller/register/', '/']


class LoginMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # 获取请求的路由
        path_info = request.path_info
        print(path_info)
        # 路由在白名单中 通过
        if path_info in WHITELIST:
            return
        # 路由为买家路由 通过
        if path_info.find('/buyer/') != -1:
            return
        # 已登录 通过
        if request.session.get('seller_name'):
            return
        # 否则重定向
        return redirect('/seller/login/')
