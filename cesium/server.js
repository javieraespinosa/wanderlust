
var app   = require('express')();
var http  = require('http').Server(app);
var io    = require('socket.io')(http);
var kafka = require('node-rdkafka');
var argparse = require('argparse')

// Constants 
var DEFAULT_KAFKA_HOST  = "kafka:9092";
var DEFAULT_KAFKA_TOPIC = "input.stream";
var DEFAULT_KAFKA_GROUP = "default.group";
var DEFAULT_PORT = 3334;

// Configuration argument parser
var parser = createParser();


// Get arguments
var args = parser.parseArgs();
KAFKA_HOST  = args['k']; 
KAFKA_TOPIC = args['t'];
PORT = args['p'];



// Serve static files
app.use(require('express').static('.'))

// Start web server
http.listen(PORT, function(){
    console.log('listening on *:' + PORT);
});


// Web socket connection
io.on('connection', function(socket){
    
    console.log('user connected');
    
    // Connect to Kafka using CL arguments
    var globalConfig = {
      'group.id': DEFAULT_KAFKA_GROUP,
      'metadata.broker.list': KAFKA_HOST,
    }
    
    var topics = {
        'topics': [ KAFKA_TOPIC ]
    }
    
    var stream = kafka.KafkaConsumer.createReadStream(
        globalConfig, 
        {}, 
        topics
    );

    stream.on('data', function(message) {
      var location = message.value.toString()
      console.log(location);
      socket.emit('location', location)
    });

});



function createParser() {
    
    var parser = new argparse.ArgumentParser();

    parser.addArgument( ['-t', '-topic'], {
        help: 'Kafka topic to read from',
        defaultValue: DEFAULT_KAFKA_TOPIC
    });

    parser.addArgument( ['-k', '-kafka'], {
        help: 'Kafka host URI',
        defaultValue: DEFAULT_KAFKA_HOST
    });

    parser.addArgument( ['-p', '-port'], {
        help: 'Port to listen for connections',
        defaultValue: DEFAULT_PORT
    });
    
    return parser;
}


