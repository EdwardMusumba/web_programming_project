var app =require('express')()
var http=require('http').createServer(app)
var io=require('socket.io')(http)
app.get('/chat',(req,res) => {
      res.sendFile(__dirname+ '/chat.html');
})
io.on('connection',(socket)=> {
      console.log("user online");
      socket.on("codeboard-message",(msg)=>{
            consolelog("Message Received :"+msg);
            socket.broadcast.emit("codeboard-message-broadcasted",msg);
      })
})


var server_port =process.env.PORT || 3000
http.listen(server_port)