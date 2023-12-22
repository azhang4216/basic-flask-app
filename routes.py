from flask import Flask, render_template
import elasticapm
import logging
from logging.handlers import RotatingFileHandler
import ecs_logging
from elasticapm.contrib.flask import ElasticAPM
import os
from dotenv import load_dotenv

# # Set logger to write to "/logs/ecs_logs.ndjson" for Filebeat to ship
# logging.basicConfig(filename="logs/ecs_logs.ndjson", 
# 					filemode='w')

# # Get the Logger
# logger = logging.getLogger("app")
# logger.setLevel(logging.DEBUG)

# # Add an ECS formatter to the Handler
# handler = logging.StreamHandler()
# handler.setFormatter(ecs_logging.StdlibFormatter())
# logger.addHandler(handler)

# app = Flask(__name__)

# Initialize Flask app
app = Flask(__name__)

# Configure Elastic APM
apm = ElasticAPM(app)

# Set logger to write to "logs/ecs_logs.ndjson" for Filebeat to ship
log_file_path = "logs/ecs_logs.ndjson"

# Get the Logger
logger = logging.getLogger("app")
logger.setLevel(logging.DEBUG)

# Create a FileHandler for the log file
file_handler = RotatingFileHandler(log_file_path, maxBytes=1024 * 1024, backupCount=5)

# Add an ECS formatter to the FileHandler
file_handler.setFormatter(ecs_logging.StdlibFormatter())

# Add the FileHandler to the logger
logger.addHandler(file_handler)

# Add an ECS formatter to the StreamHandler (for stdout)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(ecs_logging.StdlibFormatter())
logger.addHandler(stream_handler)

# Set up connection to elastic APM
load_dotenv()
app.config['ELASTIC_APM'] = {
  'SERVICE_NAME': os.getenv('SERVICE_NAME'),
  'SECRET_TOKEN': os.getenv('SECRET_TOKEN'),
  'SERVER_URL': os.getenv('SERVER_URL'),
  'ENVIRONMENT': os.getenv('ENVIRONMENT'),
}
apm = ElasticAPM(app)

# two decorators, same function
@app.route('/')
@app.route('/index.html')
@elasticapm.capture_span()
def index():
    logger.debug("Tiger home page", extra={"http.request.method": "get"})
    return render_template('index.html', the_title='Tiger Home Page')

@app.route('/symbol.html')
@elasticapm.capture_span()
def symbol():
    logger.debug("Tiger as a symbol", extra={"http.request.method": "get"})
    return render_template('symbol.html', the_title='Tiger As Symbol')

@app.route('/myth.html')
@elasticapm.capture_span()
def myth():
    logger.debug("Tiger in myth and legend", extra={"http.request.method": "get"})
    return render_template('myth.html', the_title='Tiger in Myth and Legend')

if __name__ == '__main__':
    app.run(debug=True)
