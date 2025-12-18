#from django.shortcuts import render
#from django.utils.deprecation import MiddlewareMixin

#class LoadingMiddleware(MiddlewareMixin):
    #def process_view(self, request, view_func, view_args, view_kwargs):
        # Skip the loading screen for:
        # 1. The home page ("/").
        # 2. The loading page itself.
        # 3. Static files (CSS, JS, images).
       # if request.path == "/" or request.path.startswith("/loading/") or request.path.startswith("/static/"):
       #     return None

        # Render the loading screen for all other pages
       # return render(request, "loading.html", {"next_url": request.get_full_path()})
