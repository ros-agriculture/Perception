from flask import Flask, request

app = Flask(__name__) #Initialize Flask App

#Inorder to run flask server, wrap the function
#request is used to transfer inputs from user
@app.route('/',methods=['POST'])
def add():
    #a=10
    #b=20
    #a = request.args.get("a") #this will give strings
    #b = request.args.get("b") #this will give string
    #Request has secirity issues, POST makes parameters invisible & gives secirity through forums
    a= request.form["a"]
    b= request.form["b"]
    return str(int(a)+int(b))


#print(add(2,3))

if __name__ == '__main__':
    app.run(port=7000)