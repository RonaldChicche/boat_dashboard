import serial
from flask import Flask, render_template
from flask_socketio import SocketIO, emit


app = Flask(__name__, static_url_path='/static', template_folder='templates')
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.context_processor
def inject_globals():
    return {
        'static': '/static',
        'socketio': socketio
    }

@app.route('/')
def index():
    return render_template('index.html')

def read_serial():
    try:
        ser = serial.Serial('/dev/ttyUSB0', 9600) # Cambia el puerto y la velocidad de acuerdo a tus necesidades
        while True:
            data = ser.readline().decode().strip()
            socketio.emit('data', data)
    except serial.SerialException:
        socketio.emit('error', 'No se pudo conectar al puerto serial')

@socketio.on('connect')
def connect():
    socketio.start_background_task(target=read_serial)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)