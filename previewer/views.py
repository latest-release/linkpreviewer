from django.shortcuts import render
from django.views import View
from django.http import (
            HttpResponse, HttpResponseRedirect,
            HttpResponseServerError, JsonResponse
        )
from .lpreviewer import parse_webpage


class IndexPage(View):
    def get(self, request):
        return render(request, "index.html", {"t_title":"Link previewer"})
    
    def post(self, request):
        try:
            domain = request.POST.get('domain', '')
            
            domain = self.fix_domain_protocol(domain)
            # Get the preview
            try:
                parsed_response = parse_webpage(None, url=domain, prettify=False)
                if(parsed_response):
                    parsed_response["t_title"]="Link previewer"
                    parsed_response["domain"]=domain
                    parsed_response["details"]=True
                    return render(request, "index.html", parsed_response)
                return HttpResponse("No power")
                
            except Exception as e:
                context = {}
                context["error"]=e
                context["error_string"]="System encountered an expected error"
                return render(request, "index.html", context)
                
        except Exception as e:
            raise 
    
    def fix_domain_protocol(self, domain):
        """
        some input domains don't have https:, www.
        """
        if domain.startswith("http://"):
            return domain   
        if(domain.startswith("www")):
            domain = "https://" + domain
            return domain 
        elif domain.startswith("https:"):
            return domain
        else:
            return "https://"+domain 
        
