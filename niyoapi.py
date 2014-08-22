import webapp2
import json
import urllib2
import logging
import pprint
import time

from google.appengine.ext import ndb

DIRECTIONS_API_KEY = "AIzaSyDBdaxeZln_ubb2yrqM8Wg6H0INz_GZ"


class UserEntry(ndb.Model):
    user_id = ndb.StringProperty()
    reg_id = ndb.StringProperty()
    user_email = ndb.StringProperty()

def user_entry_key(user_email='DEFAULT_EMAIL'):
    """Constructs a datastore key for a UserEntry entity with user_email."""
    return ndb.Key('UserEntry', user_email)


class MainPage(webapp2.RequestHandler):

    def get(self):
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write({'Hello': 'fuck!'})

class Ping(webapp2.RequestHandler):

    def get(self):

        logging.error('Ping started')

    	reg_id = self.request.get('regId')

    	json_data = {"collapse_key" : "niyo-push","data" : {"Category" : "radar","Type": "ping", "user":"yifat.ferber@gmail.com", "latitude":"some_lie", "longitude":"another_lie"},"registration_ids": [reg_id]}
    	apiKey = "AIzaSyDwamDrY7mp6CKS8SvWZJaerxe73i6mMqs"
    	myKey = "key=" + apiKey
    	headers = {'Content-Type': 'application/json', 'Authorization': myKey}

    	data = json.dumps(json_data)

    	url = 'https://android.googleapis.com/gcm/send'

    	req = urllib2.Request(url, data, headers)                          


        f = urllib2.urlopen(req)
        response = json.loads(f.read())
        reply = {}
        if response ['failure'] == 0:
        	reply['error'] = '0'
        else:
        	response ['error'] = '1'

		self.response.headers['Content-Type'] = 'application/json'
		self.response.write('this is a push')

class Register(webapp2.RequestHandler):
    def get(self):

        logging.error('Register started')
        reg_id = self.request.get('reg_id')
        user_id = self.request.get('user_id')
        user_email = self.request.get('user_email')

        newUserEntry = UserEntry(key=user_entry_key(user_email))
        newUserEntry.user_id = user_id
        newUserEntry.reg_id = reg_id
        newUserEntry.user_email = user_email
        newUserEntry.put()

        json_data = {"collapse_key" : "niyo-push","data" : {"Category" : "radar","Type": "ack", "user":user_email},"registration_ids": [reg_id]}
        apiKey = "AIzaSyDwamDrY7mp6CKS8SvWZJaerxe73i6mMqs"
        myKey = "key=" + apiKey
        headers = {'Content-Type': 'application/json', 'Authorization': myKey}

        data = json.dumps(json_data)

        url = 'https://android.googleapis.com/gcm/send'

        req = urllib2.Request(url, data, headers)


        f = urllib2.urlopen(req)
        response = json.loads(f.read())
        reply = {}
        if response ['failure'] == 0:
            reply['error'] = '0'
        else:
            response ['error'] = '1'

        self.response.headers['Content-Type'] = 'application/json'
        self.response.write('this is a push')

class AskForPosition(webapp2.RequestHandler):
    def get(self):

        user_asking = self.request.get('user_asking')
        user_answering = self.request.get('user_answering')
        trx_id = self.request.get('trx_id')

        logging.debug('askForPosition really started. id %s', trx_id)

        userEntryQuery = UserEntry.query(UserEntry.user_email == user_answering)
        userEntry = userEntryQuery.fetch(1)

        logging.info('after user fetch. userEntry is %s', userEntry[0])

        reg_id = userEntry[0].reg_id

        logging.info('askForPosition reg id is %s', reg_id)

        json_data = {"collapse_key" : "niyo-push","data" : {"Category" : "radar","Type": "req", "user_asking":user_asking, "trx_id": trx_id},"registration_ids": [reg_id]}
        apiKey = "AIzaSyDwamDrY7mp6CKS8SvWZJaerxe73i6mMqs"
        myKey = "key=" + apiKey
        headers = {'Content-Type': 'application/json', 'Authorization': myKey}

        data = json.dumps(json_data)

        url = 'https://android.googleapis.com/gcm/send'

        msg = 'Everything is normal'
        try:
            req = urllib2.Request(url, data, headers)
        except Exception as inst:
            logging.error('Error in calling gcm %s', inst)
            msg = 'Server raised an exception'
        

        f = urllib2.urlopen(req)
        response = json.loads(f.read())
        responseLog = json.dumps(response)
        logging.info('response is %s', responseLog)
        reply = {}
        if response ['failure'] == 0:
            reply['error'] = '0'
        else:
            msg = 'AskForPosition Call to GCM succeeded but returned an error'

        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(msg)

class RoutesSummary(webapp2.RequestHandler):
    def get(self):

        userEntryQuery = UserEntry.query(UserEntry.user_email == "ori.harel@gmail.com")

        logging.info('query result is %s', userEntryQuery)

        userEntry = userEntryQuery.fetch(1)

        # logging.info('after user fetch. userEntry is %s', userEntry[0])

        reg_id = userEntry[0].reg_id
        # reg_id = "APA91bFORdnT8tygJPSCUIY3fwwAFTe5s-qY59sxg60tJA4J7LZH94ETGTOlBAaI4xqXqXy145KjdE8ah3ytA4Hk0wZS9kAqJI_yiymSozupdupQz_Td7uP7bG2HywXVM_ZAnqm6hQJItjnO-lp-HMxVh7fQqSI-AQ"

        json_data = {"collapse_key" : "niyo-push","data" : {"Category" : "radar","Type": "morningTrafficToWork", "payload": "none"},"registration_ids": [reg_id]}
        apiKey = "AIzaSyDwamDrY7mp6CKS8SvWZJaerxe73i6mMqs"
        myKey = "key=" + apiKey
        headers = {'Content-Type': 'application/json', 'Authorization': myKey}

        data = json.dumps(json_data)

        url = 'https://android.googleapis.com/gcm/send'

        msg = 'Everything is normal'

        try:
            req = urllib2.Request(url, data, headers)
        except Exception as inst:
            logging.error('Error in calling gcm %s', inst)
            msg = 'Server raised an exception'


        f = urllib2.urlopen(req)
        gcmresponse = json.loads(f.read())
        gcmresponseLog = json.dumps(gcmresponse)

        logging.info('GCM response is: %s with', gcmresponseLog)
        logging.info('reg_id is: %s with', reg_id)

        if gcmresponse ['failure'] == 0:
            msg = 'traffic report Call to GCM succeeded'
            logging.info('Calling gcm %s', msg)
        else:
            msg = 'traffic Call to GCM succeeded but returned an error'
            logging.error('Error in calling gcm %s', msg)



        # self.response.headers['Content-Type'] = 'application/json'
        self.response.write(msg)

class EveningTraffic(webapp2.RequestHandler):
    def get(self):

        userEntryQuery = UserEntry.query(UserEntry.user_email == "ori.harel@gmail.com")

        logging.info('query result is %s', userEntryQuery)

        userEntry = userEntryQuery.fetch(1)

        # logging.info('after user fetch. userEntry is %s', userEntry[0])

        reg_id = userEntry[0].reg_id
        # reg_id = "APA91bFORdnT8tygJPSCUIY3fwwAFTe5s-qY59sxg60tJA4J7LZH94ETGTOlBAaI4xqXqXy145KjdE8ah3ytA4Hk0wZS9kAqJI_yiymSozupdupQz_Td7uP7bG2HywXVM_ZAnqm6hQJItjnO-lp-HMxVh7fQqSI-AQ"

        json_data = {"collapse_key" : "niyo-push","data" : {"Category" : "radar","Type": "eveningTrafficHome", "payload": "none"},"registration_ids": [reg_id]}
        apiKey = "AIzaSyDwamDrY7mp6CKS8SvWZJaerxe73i6mMqs"
        myKey = "key=" + apiKey
        headers = {'Content-Type': 'application/json', 'Authorization': myKey}

        data = json.dumps(json_data)

        url = 'https://android.googleapis.com/gcm/send'

        msg = 'Everything is normal'

        try:
            req = urllib2.Request(url, data, headers)
        except Exception as inst:
            logging.error('Error in calling gcm %s', inst)
            msg = 'Server raised an exception'


        f = urllib2.urlopen(req)
        gcmresponse = json.loads(f.read())
        gcmresponseLog = json.dumps(gcmresponse)

        logging.info('GCM response is: %s with', gcmresponseLog)
        logging.info('reg_id is: %s with', reg_id)

        if gcmresponse ['failure'] == 0:
            msg = 'traffic report Call to GCM succeeded'
            logging.info('Calling gcm %s', msg)
        else:
            msg = 'traffic Call to GCM succeeded but returned an error'
            logging.error('Error in calling gcm %s', msg)



        # self.response.headers['Content-Type'] = 'application/json'
        self.response.write(msg)


class NextEventTraffic(webapp2.RequestHandler):
    def get(self):

        userEntryQuery = UserEntry.query(UserEntry.user_email == "ori.harel@gmail.com")

        logging.info('query result is %s', userEntryQuery)

        userEntry = userEntryQuery.fetch(1)

        # logging.info('after user fetch. userEntry is %s', userEntry[0])

        reg_id = userEntry[0].reg_id
        # reg_id = "APA91bFORdnT8tygJPSCUIY3fwwAFTe5s-qY59sxg60tJA4J7LZH94ETGTOlBAaI4xqXqXy145KjdE8ah3ytA4Hk0wZS9kAqJI_yiymSozupdupQz_Td7uP7bG2HywXVM_ZAnqm6hQJItjnO-lp-HMxVh7fQqSI-AQ"

        json_data = {"collapse_key" : "niyo-push","data" : {"Category" : "radar","Type": "nextEventTraffic", "payload": "none"},"registration_ids": [reg_id]}
        apiKey = "AIzaSyDwamDrY7mp6CKS8SvWZJaerxe73i6mMqs"
        myKey = "key=" + apiKey
        headers = {'Content-Type': 'application/json', 'Authorization': myKey}

        data = json.dumps(json_data)

        url = 'https://android.googleapis.com/gcm/send'

        msg = 'Everything is normal'

        try:
            req = urllib2.Request(url, data, headers)
        except Exception as inst:
            logging.error('Error in calling gcm %s', inst)
            msg = 'Server raised an exception'


        f = urllib2.urlopen(req)
        gcmresponse = json.loads(f.read())
        gcmresponseLog = json.dumps(gcmresponse)

        logging.info('GCM response is: %s with', gcmresponseLog)
        logging.info('reg_id is: %s with', reg_id)

        if gcmresponse ['failure'] == 0:
            msg = 'traffic report Call to GCM succeeded'
            logging.info('Calling gcm %s', msg)
        else:
            msg = 'traffic Call to GCM succeeded but returned an error'
            logging.error('Error in calling gcm %s', msg)



        # self.response.headers['Content-Type'] = 'application/json'
        self.response.write(msg)



class Acknowledge(webapp2.RequestHandler):
    def get(self):

        user_asking = self.request.get('user_asking')
        user_answering = self.request.get('user_answering')
        trx_id = self.request.get('trx_id')
        ring = self.request.get('ring')

        userEntryQuery = UserEntry.query(UserEntry.user_email == user_asking)
        userEntry = userEntryQuery.fetch(1)

        reg_id = userEntry[0].reg_id

        json_data = {"collapse_key" : "niyo-push","data" : {"Category" : "radar","Type": "ack", "user_asking":user_asking, "user_answering": user_answering, "trx_id": trx_id, "ring": ring},"registration_ids": [reg_id]}
        apiKey = "AIzaSyDwamDrY7mp6CKS8SvWZJaerxe73i6mMqs"
        myKey = "key=" + apiKey
        headers = {'Content-Type': 'application/json', 'Authorization': myKey}

        data = json.dumps(json_data)

        url = 'https://android.googleapis.com/gcm/send'

        msg = 'Everything is normal'
        try:
            req = urllib2.Request(url, data, headers)
        except Exception as inst:
            logging.error('Error in calling gcm %s', inst)
            msg = 'Server raised an exception'
        

        f = urllib2.urlopen(req)
        response = json.loads(f.read())
        responseLog = json.dumps(response)
        logging.info('response is %s', responseLog)
        reply = {}
        if response ['failure'] == 0:
            reply['error'] = '0'
        else:
            msg = 'Acknowledge Call to GCM succeeded but returned an error'

        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(msg)

class AnswerPosition(webapp2.RequestHandler):
    def get(self):

        logging.info('answerPosition started')
        user_asking = self.request.get('user_asking')
        user_answering = self.request.get('user_answering')
        latitude = self.request.get('latitude')
        longitude = self.request.get('longitude')
        update_time = self.request.get('update_time')
        image_url = self.request.get('image_url')
        trx_id = self.request.get('trx_id')
        ring = self.request.get('ring')

        logging.info('answerPosition really started. id is %s', trx_id)

        userEntryQuery = UserEntry.query(UserEntry.user_email == user_asking)

        logging.info('query result is %s', userEntryQuery)

        userEntry = userEntryQuery.fetch(1)

        logging.info('after user fetch. userEntry is %s', userEntry[0])

        reg_id = userEntry[0].reg_id

        json_data = {"collapse_key" : "niyo-push","data" : {"Category" : "radar","Type": "res", "user_answering": user_answering, "latitude":latitude, "longitude": longitude, "updateTime": update_time, "imageUrl": image_url, "trx_id": trx_id, "ring": ring},"registration_ids": [reg_id]}
        apiKey = "AIzaSyDwamDrY7mp6CKS8SvWZJaerxe73i6mMqs"
        myKey = "key=" + apiKey
        headers = {'Content-Type': 'application/json', 'Authorization': myKey}

        data = json.dumps(json_data)

        url = 'https://android.googleapis.com/gcm/send'

        msg = 'Everything is normal'

        try:
            req = urllib2.Request(url, data, headers)
        except Exception as inst:
            logging.error('Error in calling gcm %s', inst)
            msg = 'Server raised an exception'


        f = urllib2.urlopen(req)
        response = json.loads(f.read())
        reply = {}
        if response ['failure'] == 0:
            reply['error'] = '0'
        else:
            msg = 'AnswerPosition Call to GCM succeeded but returned an error'

        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(msg)




application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/ping', Ping),
    ('/register', Register),
    ('/askForPosition', AskForPosition),
    ('/answerPosition', AnswerPosition),
    ('/getRoutesSummary', RoutesSummary),
    ('/sendEveningTraffic', EveningTraffic),
    ('/sendNextEventTraffic', NextEventTraffic),
    ('/ack', Acknowledge)
], debug=True)