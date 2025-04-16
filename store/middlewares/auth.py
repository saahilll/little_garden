from django.shortcuts import redirect

def auth_middleware(get_response):
    def middleware(request):
        if not request.sesson.get('customer'):
            return redirect('lofin')
        response = get_response(request)
        return response
    return middleware