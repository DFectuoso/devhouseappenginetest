from google.appengine.ext import webapp, db
from google.appengine.ext.webapp import util, template
from google.appengine.api import taskqueue

import logging
import random
import string

class Helado(db.Model):
  sabor = db.StringProperty()

class MainHandler(webapp.RequestHandler):
  def get(self):
    helados = Helado.all().order("sabor").fetch(1000)
    self.response.out.write(template.render("templates/main.html", locals()))
    for i in range(1,100):
      taskqueue.add(url='/creaHelado', params={'l':20})
    
  def post(self):
    h = Helado(sabor=self.request.get("sabor"))
    h.put()
    self.redirect("/")

class HeladoHandler(webapp.RequestHandler):
  def get(self):
    char_set = string.ascii_uppercase + string.digits
    longitud = self.request.get("l")
    if not longitud:
      longitud = 25
    else:
      
    helado = ''.join(random.sample(char_set,int(self.request.get("l"))))
    h = Helado(sabor=helado)
    h.put()
  
  def post(self):
    self.get() 

def main():
  application = webapp.WSGIApplication([
    ('/', MainHandler),
    ('/creaHelado', HeladoHandler),
  ], debug=True)
  util.run_wsgi_app(application)


if __name__ == '__main__':
  main()
