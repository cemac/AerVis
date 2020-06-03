from flask import Flask,request,jsonify,render_template
import os,sys

# get calling program dir
PATH = os.path.dirname(sys.argv[0])+''

def streamed_response():
    @stream_with_context
    def generate():
        for i in range(100):
            yield '!'+i
    return Response(generate())
    
    
routing = {
    '/test':lambda:'This is a Test!',
    '/':streamed_response,

}

class server:
    '''
    A server for Flask
    Initiate with 
    '''
    def __init__(self,name='miniflask',host='127.0.0.1',port=5000,routing=routing,static_url=False):
        self.__name__ =  name
        
        #location settings
        if not static_url: static_url=PATH
        self.host = host
        self.port = port
        print(PATH,host,port)
        
        #app setup
        self.app  = Flask(__name__,static_url_path=static_url,template_folder=static_url)
        
        #set up routing functions
        if not routing: routing=routing
        for ext in routing:
            self.app.route(ext)(routing[ext])#lets not use the decorator

    def run(self,debug=True,open=True):
        # if open:
        #     os.system('open http://%s:%s/'%(self.host,self.port))
        self.app.run(debug=debug,host=self.host,port=self.port)


s = server()
s.run()

#a.to_dataset().to_dask_dataframe().compute().to_hdf('test.h5','time') 