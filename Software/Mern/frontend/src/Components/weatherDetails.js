const WeatherDetails = ({weather}) => {
    var stringOfTime = `${weather.createdAt}`
    var formattedTime = stringOfTime.substring(0, 19)
    formattedTime = formattedTime.replace("T", ", ")

    // document.getElementById("showBtn").addEventListener("click", () => {
    //     document.getElementsByClassName("weatherInfoDiv").style.display = "none";

    // })

    return (
        <div className="weatherInfoDiv">
            <h4>{formattedTime}</h4>
            <p><strong>Temperature:</strong> {weather.temp}</p>
            <p><strong>Humidity:</strong> {weather.humidity}</p>
            <p><strong>Dew Point:</strong> {weather.dFPoint}C</p>
            <p><strong>Precipitation:</strong> {weather.rainVal}</p>
            <p><strong>Median Speed:</strong> {weather.avgSpeed}km/h</p>
        </div>

    )

}

export default WeatherDetails