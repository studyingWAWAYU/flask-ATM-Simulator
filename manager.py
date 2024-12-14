from ATMflask import app

if __name__=='__main__':
    app.run(host='127.0.0.1', port=5001)
    # host是监听主机名，port默认值为5000,因为5000端口被占用，所以换成5001