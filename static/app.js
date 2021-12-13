

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

$(window).scroll(function() {
    var winScrollTop = $(window).scrollTop();
    var winHeight = $(window).height();
    var floaterHeight = $('#floater').outerHeight(true);
    //true so the function takes margins into account
    var fromBottom = 20;

    var top = winScrollTop + winHeight - floaterHeight - fromBottom;
    $('#floater').css({'top': top + 'px'});
});

const redirectUri = 'http://localhost:8888/callback';