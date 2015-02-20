from handlers.web import WebRequestHandler

class HomePage(WebRequestHandler):
    def get(self):
        path = 'home.html'
        template_values = {}
        self.render_template(template_name=path, template_values=template_values)