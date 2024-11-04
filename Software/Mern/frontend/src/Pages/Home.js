import {useEffect, useState} from "react"

//components
import WeatherDetails from "../Components/weatherDetails"
import WeatherForm from "../Components/weatherForm"

const Home = ()=> {
    const [weathers, setWeathers] = useState(null)

    useEffect(() => {
        const fetchWeather = async () => {
            const response = await fetch("/api/weather")
            const json = await response.json()

            if (response.ok) {
                setWeathers(json)

            }

        }

        fetchWeather()

    }, [])

    let maxTemp = 0
    let minTemp = 0
    let maxHum = 0
    let minHum = 0
    let weatherArr = []

    weathers && weathers.map((weather) => (
        weatherArr.push(weather)

    ))

    weatherArr.forEach((weather, i) => {
        if (parseFloat(weather.temp) > maxTemp){
            maxTemp = parseFloat(weather.temp)
            minTemp = maxTemp
        }
        if (parseFloat(weather.humidity) > maxHum){
            maxHum = parseFloat(weather.humidity)
            minHum = maxHum
        }

    })

    weatherArr.forEach((weather, i) => {
        if (parseFloat(weather.temp) > 0 && parseFloat(weather.temp) < minTemp){
            minTemp = parseFloat(weather.temp)
        }
        if (parseFloat(weather.humidity) > 0 && parseFloat(weather.humidity) < minHum){
            minHum = parseFloat(weather.humidity)
        }

    })

    // weathers && weathers.map((weather) => {
    //     if (parseFloat(weather.temp) > maxTemp){
    //         maxTemp = parseFloat(weather.temp)
    //         minTemp = maxTemp
    //     }
    //     if (parseFloat(weather.humidity) > maxHum){
    //         maxHum = parseFloat(weather.humidity)
    //         minHum = maxHum
    //     }

    // })

    // weathers && weathers.map((weather) => {
    //     if (parseFloat(weather.temp) > 0 && parseFloat(weather.temp) < minTemp){
    //         minTemp = parseFloat(weather.temp)
    //     }
    //     if (parseFloat(weather.humidity) > 0 && parseFloat(weather.humidity) < minHum){
    //         minHum = parseFloat(weather.humidity)
    //     }

    // })

    // function showHide() {
    //     weatherArr.map((weather) => (
    //         document.getElementById("main").appendChild(
    //             // <WeatherDetails key={weather._id} weather={weather}/>
    //             <div className="weatherInfoDiv">
    //                 <h4>{weather.time}</h4>
    //                 <p><strong>Temperature:</strong> {weather.temp}</p>
    //                 <p><strong>Humidity:</strong> {weather.humidity}</p>
    //                 <p><strong>Dew Point:</strong> {weather.dFPoint}</p>
    //                 <p><strong>Median Speed:</strong> {weather.avgSpeed}</p>
    //             </div>

    //         )

    //     ))

    // }

    function checkArr() {
        if (weatherArr.length > 0) {
            // document.getElementById("showBtn").addEventListener("click", showHide)

            return (
                <div className="weatherInfoDiv">
                    <h4>Latest Entry</h4>
                    <p><strong>Temperature:</strong> {weatherArr[0].temp}</p>
                    <p><strong>Humidity:</strong> {weatherArr[0].humidity}</p>
                    <p><strong>Dew Point:</strong> {weatherArr[0].dFPoint}C</p>
                    <p><strong>Precipitation:</strong> {weatherArr[0].rainVal}</p>
                    <p><strong>Median Speed:</strong> {weatherArr[0].avgSpeed}km/h</p>
                    <p><strong>Highest Temp:</strong> {maxTemp} <strong>Lowest Temp:</strong> {minTemp}</p>
                    <p><strong>Highest Humidity:</strong> {maxHum} <strong>Lowest Humidity:</strong> {minHum}</p>
                    {/* <br/>
                    <button id="showBtn" className="showButton" onClick={showHide}>Show all entries</button> */}
                </div>

            )

        }

    }

    return (
        <div className="home">
            <h1>Dynamic Speed Limit System</h1>
            <div className="weathers" id="main">
                {checkArr()}

                <hr />

                {/* <button id="showBtn" className="showButton" onClick={showHide}>Show all entries</button> */}

                {weatherArr.map((weather) => (
                    <WeatherDetails key={weather._id} weather={weather}/>

                ))}

                <hr />

                {/* {weathers && weathers.map((weather) => (
                    <WeatherDetails key={weather._id} weather={weather}/>

                ))} */}


            </div>
            
            <WeatherForm/>

            {/* <div className="formDiv">
                <WeatherForm/>

            </div> */}
            

        </div>

    )

}

export default Home