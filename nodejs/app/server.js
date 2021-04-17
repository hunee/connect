/**
 * 
 * 
 */
var cluster = require('cluster');
var os = require('os');

 /**
 * health
 */
exports.__defineGetter__('health', function () {
  return {
    pid: process.pid,
    memory: process.memoryUsage(),
    uptime: process.uptime()
  };
});

/**
 *
 */

// Keep track of http requests
var numReqs = 0;

//setInterval(function () {
//console.log("numReqs =", numReqs);
//}, 1000);

// Count requestes
function messageHandler (msg) {
	if (msg.cmd && msg.cmd == 'notifyRequest') {
		numReqs += 1;
	}
}


/**
 *
 *
 */
 function getplatformname() {
	var platformname;
	var arch;

	switch (process.platform) {
		case 'linux':
			platformname = 'Linux';
			break;

		case 'win32':
			platformname = 'Windows';
			break;
		case 'freebsd':
			platformname = 'FreeBSD';
			break;

		case 'darwin':
			platformname = 'Macintosh';
			break;

		case 'sunos':
			platformname = 'Solaris';
			break;
	}

	return platformname + ' ' + process.arch;
}

/**
 *
 *
 */
 function showInfo() {
	console.log('/**\n * Node.js ' + process.version);
	console.log(' *\t- ' + getplatformname());

	var cpus = os.cpus();
	console.log(' * \n *\tProcessor: ' + cpus[0].model + ' x ' + cpus.length);
	console.log(' *\t   Memory: ' + (os.freemem() / (1024*1024)).toFixed(0) + 'MB/' + (os.totalmem() / (1024*1024)).toFixed(0) + 'MB');
	//console.log(' *\t       IP: ' + gethostname());
	//console.log(' *\t       IP: ' + config.app.host + ':' + config.app.port);
	console.log(' */');
}

/**
 *
 */
exports.runLoop = function (_exec) {
	/**
	 *
	 */
	if (_exec !== undefined) {
		cluster.setupMaster({
			exec: _exec
		});
	}


	/**
	 *
	 */
	if (cluster.isMaster) {
		/**
		 *
		 */
		showInfo();

		/**
		 *
		 */
		//if (process.argv.length < 2) {
		//process.exit(1);
		//}


		/**
		 *
		 */
		var numCPUs = os.cpus().length;
		for (var i = 0; i < numCPUs; i++) {
			cluster.fork();
		}


		/**
		 *
		 */
		cluster.on('exit', function(worker, code, signal) {
			var exitCode = worker.process.exitCode;
			console.log('worker ' + worker.process.pid + ' died (' + exitCode + '). restarting...');

			cluster.fork();
		})

		cluster.on('fork', function(worker) {
			//console.log('[create fork] pid : ' + worker.process.pid + ' id ' + worker.id);
		});


		/**
		 *
		 */
		Object.keys(cluster.workers).forEach(function (id) {
			cluster.workers[id].on('message', messageHandler);
		})
	}
}



/**
 * workerid
 */
global.__defineGetter__('workerid', function () {
	var id = '0';//(ID:' + cluster.worker.id + ' PID:' + cluster.worker.process.pid + ')';
	return id;
});


