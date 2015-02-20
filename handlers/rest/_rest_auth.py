from model.oauth2 import Token, Client
from google.appengine.api import memcache
from model import User
import json
from handlers import APP_JSON
from util import clock

RATE_REMAINING = 'RateLimit-Remaining'
RATE_RESET = 'RateLimit-ResetTime'
QUOTA_TYPE_APP = 'A'
QUOTA_TYPE_USER = 'U'

LIMITS = {QUOTA_TYPE_APP: 500, QUOTA_TYPE_USER: 500}
RATE_DURATION = 15 #minutes
RATE_SLOTS = RATE_DURATION - 1
CACHE_TIMEOUT = 60 * (RATE_DURATION + 1)
INVALID_TOKEN = 'Invalid token'
RATE_EXCEEDED = 'Rate limit exceeded'

def token_required(handler_method):
    def validate_token(self, *args, **kwargs):
        token = self['token']
        if not token:
            return self.write(json.dumps({'errors' : [INVALID_TOKEN]}), 401, APP_JSON)
        email = memcache.get(token)
        if not email:
            token_obj = Token.get_by_key_name(token)
            if not token_obj:
                return self.write(json.dumps({'errors' : [INVALID_TOKEN]}), 401, APP_JSON)
            memcache.set(token, token_obj.user.email)
            self.user = token_obj.user
        else:
            self.user = User.get_by_email(email)
        if not self.user:
            return self.write(json.dumps({'errors' : [INVALID_TOKEN]}), 401, APP_JSON)
        if not check_ratelimit(self, token):
            return self.write(json.dumps({'errors' : [RATE_EXCEEDED]}),
                              503, APP_JSON)
        return handler_method(self, *args, **kwargs)
    return validate_token

    
def client_credentials_required(handler_method):
    def validate_creds(self, *args, **kwargs):
        client = Client.validate_and_get(self['client_id'],
                                         self['client_secret'])
        if not client:
            return self.write(json.dumps({'errors' : ['Invalid credentials']}),
                              401, APP_JSON)
        if not check_ratelimit(self, client.id, QUOTA_TYPE_APP):
            return self.write(json.dumps({'errors' : [RATE_EXCEEDED]}),
                              503, APP_JSON)
        self.client = client
        return handler_method(self, *args, **kwargs)
    return validate_creds

def make_key(token, token_type, suffix):
    return "%s%s%s" % (token, token_type, suffix)
    
def ratelimit_key(token, token_type = QUOTA_TYPE_USER):
    return make_key(token, token_type, "rl")
    

'''
The RATE_DURATION is a rolling period with RATE_DURATION number of time slot.
slots.pop(0) gets rid of the earliest time slot.
'''
def check_ratelimit(handler, token, token_type=QUOTA_TYPE_USER):
    memcache_client = memcache.Client()
    rl_key = ratelimit_key(token, token_type)
    limit = LIMITS[token_type]
    response = handler.response
    while True: #Keep trying till you succeed. Mutiple tries in a highly concurrent sitution
        val = memcache_client.gets(rl_key)
        this_minute = clock.this_minute()
        if not val:
            if not memcache_client.add(rl_key, (this_minute, 1, 0, []),
                                       time = CACHE_TIMEOUT):
                continue
            response.headers[RATE_REMAINING] = str(limit - 1)
            return True #assume limit is atleast 1
        time, ncnt, n_1cnt, slots = val
        if time == this_minute:
            remaining = limit - (ncnt + n_1cnt)
            if remaining > 0:
                if not memcache_client.cas(rl_key,
                                           (this_minute, ncnt + 1,
                                            n_1cnt, slots),
                                           time = CACHE_TIMEOUT):
                    continue
                response.headers[RATE_REMAINING] = str(remaining - 1)
                return True
            response.headers[RATE_REMAINING] = '0'
            handler.response.headers[RATE_RESET] = find_reset_time(
                slots)
            return False

        diff_in_mins = int((this_minute - time).total_seconds() // 60)
        if diff_in_mins >= RATE_DURATION:
            slots = []
        else:
            slots.append(ncnt)
            for i in range(diff_in_mins - 1):
                slots.append(0)
            slots = slots[max(0, len(slots) - RATE_SLOTS): len(slots)]
            
        assert len(slots) <= RATE_SLOTS
        n_1_total = sum(slots)
        remaining = limit - (n_1_total + 1)
        if not memcache_client.cas(rl_key,(this_minute, 1, n_1_total, slots),
                                   time = CACHE_TIMEOUT):
            continue
        if remaining > 0:
            handler.response.headers[RATE_REMAINING] = str(remaining)
            return True
        handler.response.headers[RATE_REMAINING] = '0'
        handler.response.headers[RATE_RESET] = find_reset_time(slots)

        return False
        
def find_reset_time(slots):
    for i, e in enumerate(slots):
        if e > 0:
            return str(i + 1)
    return str(RATE_DURATION)
        
