window.addEventListener("DOMContentLoaded", (event) => {
    setInterval(() => {
        const data = mockData();
        handleData(data);
    }, 2000);
});

const handleData = (data) => {
    console.log(data)
    const heartRateElement = document.getElementById("heart-rate");
    heartRateElement.innerHTML = data.heartRate;

    const playList = document.getElementById("playList");
    playList.innerHTML = data.playList.join(", ");
}

// This function will be replaced by a function 'getData'
const mockData = () => {
    const playList = ["Song 1", "Song 2", "Song 3"];
    const heartRate = Math.floor(60 + 20*Math.random());

    return {
        playList, heartRate
    }
}
