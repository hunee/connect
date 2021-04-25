/**
 * worker - main
 */
var server = require('./server');

var	connect = require('connect'),
  http = require('http');

var morgan = require('morgan');
var path = require('path');

var bodyParser = require('body-parser');
var compression = require('compression');

var os = require('os'),
  fs = require('fs'),
  uuid = require('uuid')
const { config } = require('process');


/**
 * HACK http.ServerResponse.prototype
 */
 http.ServerResponse.prototype.send = function(data) {
  ///console.log('->> httpServer.send');

  var body = {};

  /**
   * header
   */
  body.header = {};
  body.header.uuid = Buffer.from(uuid.v1()).toString('base64');
  body.header.timeofday = new Date().toString();

  /**
   * data
   */
  body.data = data;

  this.writeHeader(200, { 'Content-Type': 'application/json' });
  this.write(JSON.stringify(body));
  this.end();
};


var app = connect();

// setup the logger
app.use(morgan('combined'))
 
// parse application/json
app.use(bodyParser.json())

// gzip/deflate outgoing responses
app.use(compression());

// body-parser
app.use(function (req, res) {
  //console.log(req.headers);
  console.log('remoteAddress: ' + req.socket.remoteAddress);

  //app.emit(req.body.data.pid, req, res);

  /*if (req.body.header === undefined) {
      console.log(req.body);
      res.end(JSON.stringify(server.health));
  }
  else*/ {
      app.emit('data', res, req.body);
  }

  // notify master about the request
  //process.send({ cmd: 'notifyRequest' });
  process.send ? process.send({ cmd: 'notifyRequest' }) : {};
});

app.use(function(err, req, res, next) {
  console.error(err.stack);
  res.statusCode = 500;
  res.send('');
});

/**
 *
 */
app.on('data', function (res, data) {
	console.log("$ app.on('data') " + workerid);

  res.send('');
 });

 /**
 *
 */
app.on('send', function (response, packet, data) {
	///console.log("->> server.network.on('send')");

	var body = {};

	/**
	 * for tcp - socket
	 */
	if (packet.key) {
		body.key = packet.key;
	}

	/**
	 * header
	 */
	body.header = {};
	body.header.uuid = Buffer.from(uuid.v1(), 'base64');
	body.header.timeofday = gettimeofday();

    /**
     * body
     */
    if (data !== undefined) {
        body.body = JSON.parse(data);
        body.body.uuid = response.uuid;
        //body.header.uuid = body.body.uuid;
        if (body.body.uuid != undefined)
            body.header.uuid = new Buffer(body.body.uuid).toString('base64');

        /**
         * uid, uuid 삭제
         */
        delete body.body.uid;
        delete body.body.uuid;
    }

	//response.writeHead(200, { 'Content-Type': 'application/json' });
    //response.writeHead(200, { 'Content-Type': 'application/json' });
    response.setHeader('Content-Type', 'application/json' );
	response.write(JSON.stringify(body));
//    var base64_body = new Buffer(JSON.stringify(body)).toString('base64');
//    response.write(base64_body);
	response.end();

    //server.network.emit('tdd_팀유효성체크', packet.body.uid, packet.header.timeofday);
});

/**
 *
 * # openssl genrsa 1024 > key.pem
 * # openssl req -x509 -new -key key.pem > key-cert.pem
 *
 * @type {{key: *, cert: *}}
 */

/*
 switch (process.env.NODE_ENV) {
  case 'production':
    config = conf.production;
    break;

      case 'testserver':
          global.config = conf.testserver;
          break;

  case 'development':
    default:
      global.config = conf.development;
    break;
}*/

app.port = 8000;

/*
if (config.app.https) {
  var options = {
      key:  fs.readFileSync('./key.pem'),
      cert: fs.readFileSync('./cert.pem')
  };

  https.createServer(options, app).listen(config.app.port, function() {
      console.log('worker https.server started port: ' + config.app.port);
  });
}
else*/ {
  http.createServer(app).listen(app.port, function() {
      console.log('worker http.server started port: ' + app.port);
  });
}
