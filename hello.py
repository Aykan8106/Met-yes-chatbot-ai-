 from flask 
 import Flask app = Flask(__name__) @app.route('/')
  def anasayfa(): return '<h1>SmartLead AI calisiyor!</h1>' 
  if __name__ == '__main__': app.run()