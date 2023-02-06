# install_twisted_rector must be called before importing and using the reactor
from kivy.support import install_twisted_reactor
install_twisted_reactor()

from webserver import webapp
from twisted.web.server import Site
from twisted.internet import reactor, endpoints

from kivy.app import App
from kivy.uix.label import Label

class TwistedServerApp(App):
    label = None

    def build(self):
        endpoint = endpoints.serverFromString(reactor, "tcp:8080")
        endpoint.listen(Site(webapp.resource()))
        self.label = Label(text="server started at http://localhost:8080/\n")
        return self.label

    def handle_message(self, msg):
        self.label.text = "requests handled:  {}\n".format(msg)
        return "some response" 

if __name__ == '__main__':
    TwistedServerApp().run()
