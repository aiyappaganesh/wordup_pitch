from handlers.web import WebRequestHandler

class HomePage(WebRequestHandler):
    def get(self):
        path = 'home.html'
        template_values = {}
        template_values['phone_outline_white'] = '/assets/img/iphone_skin.png'
        template_values['section2'] = {}
        template_values['section2']['carousel'] = {}
        template_values['section2']['carousel']['slides'] = []
        template_values['section2']['carousel']['slides'].append({'img':'/assets/img/screen_1.png','copy':'Share your audio music message'})
        template_values['section2']['carousel']['slides'].append({'img':'/assets/img/screen_2.png','copy':'Simply type what <br> you want to see'})
        template_values['section2']['carousel']['slides'].append({'img':'/assets/img/screen_3.png','copy':'Select the song that<br>matches your words best'})
        template_values['section2']['carousel']['slides'].append({'img':'/assets/img/screen_4.png','copy':'Pick the exact lyrics<br>to convey your message'})
        template_values['section2']['carousel']['slides'].append({'img':'/assets/img/screen_5.png','copy':'Pick the exact lyrics<br>to convey your message'})
        template_values['section2']['carousel']['slides'].append({'img':'/assets/img/screen_6.png','copy':'Add photos<br>(optional)'})
        template_values['section2']['carousel']['slides'].append({'img':'/assets/img/screen_7.png','copy':'Add photos<br>(optional)'})
        template_values['section5'] = {}
        template_values['section5']['targets'] = []
        template_values['section5']['targets'].append({'img':'/assets/img/phone_black.png','copy':'1.75B Smartphone users'})
        template_values['section5']['targets'].append({'img':'/assets/img/messaging.png','copy':'1 Trillion+ daily messages'})
        template_values['section5']['targets'].append({'img':'/assets/img/photo_sharing.png','copy':'Music, Photo and Social platforms'})
        template_values['section5']['targets'].append({'img':'/assets/img/brand.png','copy':'Consumer brands'})
        template_values['section5']['targets'].append({'img':'/assets/img/music_record.png','copy':'Record labels and artists'})
        self.render_template(template_name=path, template_values=template_values)