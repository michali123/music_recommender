//setting up express.js server
const express = require("express");
const bodyParser = require("body-parser");

const app = express();
const port = 3000;
app.use(bodyParser.urlencoded({extended: true}));

app.get('/', function(res,req){
  res.sendFile(__dirname + "/index.html"); // sending to home route our html file
      //console.log(request);

window.addEventListener("DOMContentLoaded", (event) => {
    setInterval(() => {
        const heartRate = mockHeartRate();
        const songs = mockSongList();

        handleHeartRate(heartRate);
        handleSongList(songs);

    }, 2000);
});

const handleHeartRate = (heartRate) => {
    console.log("HR:", heartRate)
    const heartRateElement = document.getElementById("heart-rate");
    heartRateElement.innerHTML = heartRate;
}

const handleSongList = (playList) => {
    console.log("Songs:", playList)
    const playListElement = document.getElementById("playList");
    playListElement.innerHTML = playList.join(", ");
}

// This function will be replaced by a function 'getSongList'
const mockSongList = () => {
    const playList = ["Song 1", "Song 2", "Song 3"];

    return playList
}

// This function will be replaced by a function 'getHeartRate'
const mockHeartRate = () => {
    const heartRate = Math.floor(60 + 20 * Math.random());

    return heartRate
}

app.listen(port, function(){
  console.log("server stared on port 3000");
});
