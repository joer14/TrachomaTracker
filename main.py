#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import urllib
import webapp2
import datetime
import cgi
from google.appengine.ext import db
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext.webapp import template, logging

class Patient(db.Model):
    join_date = db.DateProperty()
    email = db.StringProperty()
    # userObject = db.UserProperty()
    join_date = db.DateProperty()
    firstName = db.StringProperty(required=False)
    middleName = db.StringProperty(required=False)
    lastName = db.StringProperty(required=False)
    age = db.StringProperty()
    leftEyeRating = db.StringProperty()
    leftEyePhoto = blobstore.BlobReferenceProperty(blobstore.BlobKey, required=False)
    leftEyePhotoURL = db.StringProperty()
    rightEyeRating = db.StringProperty()   
    rightEyePhoto = blobstore.BlobReferenceProperty(blobstore.BlobKey, required=False)
    rightEyePhotoURL = db.StringProperty()
    sex = db.StringProperty()
    leftEyeNote = db.StringProperty()
    rightEyeNote = db.StringProperty()
    clinicNumber = db.IntegerProperty()
    otherNotes = db.StringProperty()
    


class MainHandler(webapp2.RequestHandler):
  def get(self):
    upload_url = blobstore.create_upload_url('/upload')
    self.response.out.write('<html><body>')
    self.response.out.write('<form action="%s" method="POST" enctype="multipart/form-data">' % upload_url)
    self.response.out.write("""Upload File: <input type="file" name="file"><br> <input type="submit"
        name="submit" value="Submit"> </form></body></html>""")

class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
  def post(self):
    upload_files = self.get_uploads('inputLeftEye')  # 'file' is file upload field in the form
    blob_info = upload_files[0]
    upload_files2 = self.get_uploads('inputRightEye')
    blob_info2 = upload_files2[0]
    # user = users.get_current_user()
    # userQuery = User.gql("WHERE name='{}'".format(user.nickname())).get()
    patient = Patient()
    patient.firstName = cgi.escape(self.request.get('firstName'))
    patient.lastName = cgi.escape(self.request.get('lastName'))
    patient.middleName = cgi.escape(self.request.get('middleName'))
    patient.age = cgi.escape(self.request.get('age'))
    patient.leftEyeRating = cgi.escape(self.request.get('leftEyeRating'))
    patient.leftEyePhoto = upload_files[0].key()
    patient.leftEyePhotoURL = str(blob_info.key())
    patient.rightEyePhotoURL = str(blob_info2.key())
    patient.rightEyeRating = cgi.escape(self.request.get('rightEyeRating'))
    patient.rightEyePhoto = upload_files2[0].key()
    patient.note = cgi.escape(self.request.get('note'))
    patient.join_date=datetime.datetime.now().date()
    patient.sex = cgi.escape(self.request.get('sex'))
    patient.leftEyeNote = cgi.escape(self.request.get('leftEyeNote'))
    patient.rightEyeNote = cgi.escape(self.request.get('rightEyeNote'))
    patient.clinicNumber = 1
    patient.otherNotes = cgi.escape(self.request.get('otherNotes'))
    patient.put()

    self.redirect('/serve/%s' % blob_info.key())

class ServeHandler(blobstore_handlers.BlobstoreDownloadHandler):
  def get(self, resource):
    resource = str(urllib.unquote(resource))
    blob_info = blobstore.BlobInfo.get(resource)
    self.send_blob(blob_info)

class Android(webapp2.RequestHandler):
    def get(self):
        # upload_url = blobstore.create_upload_url('/upload')
        # fileURL = upload_url
        # fileurl = "joeee"
        output = {
            'fileURL': 'fileURL',
            'joe': 'hiiii'     
            }

        path = os.path.join(os.path.dirname(__file__), 'templates/formAndroid.html')
        self.response.write(template.render(path, output))

class Homepage(webapp2.RequestHandler):
    def get(self):
    	upload_url = blobstore.create_upload_url('/upload')
    	fileURL = upload_url
    	# fileurl = "joeee"
        output = {
            'fileURL': fileURL,
            'joe': 'hiiii'     
            }

        path = os.path.join(os.path.dirname(__file__), 'templates/home.html')
        self.response.write(template.render(path, output))

class Form(webapp2.RequestHandler):
    def get(self):
        upload_url = blobstore.create_upload_url('/upload')
        fileURL = upload_url
        # fileurl = "joeee"
        output = {
            'fileURL': fileURL,
            'joe': 'hiiii'     
            }

        path = os.path.join(os.path.dirname(__file__), 'templates/form.html')
        self.response.write(template.render(path, output))


class Results(webapp2.RequestHandler):
    def get(self):
    	# upload_url = blobstore.create_upload_url('/upload')
    	# fileURL = upload_url
    	# fileurl = "joeee"
        output = {
            'fileURL': 'fileURL',
            'joe': 'hiiii'     
            }

        path = os.path.join(os.path.dirname(__file__), 'templates/results.html')
        self.response.write(template.render(path, output))

class Dataset(webapp2.RequestHandler):
    def get(self):
        # upload_url = blobstore.create_upload_url('/upload')
        # fileURL = upload_url
        # fileurl = "joeee"
        patients = Patient.all()

        output = {
            'patients': patients,
            'joe': 'hiiii'     
            }

        path = os.path.join(os.path.dirname(__file__), 'templates/chart2.html')
        self.response.write(template.render(path, output))



app = webapp2.WSGIApplication([('/', Homepage),
                               ('/form2', Form),
                               ('/formandroid', Android),
							   ('/results', Results),
                               ('/form', Form),
                               ('/dataset', Dataset),
							   ('/a', MainHandler),
                               ('/upload', UploadHandler),
                               ('/serve/([^/]+)?', ServeHandler)],
                              debug=True)
