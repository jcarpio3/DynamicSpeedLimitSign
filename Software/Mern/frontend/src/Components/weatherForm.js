import { useState } from "react"

const WeatherForm = () => {
    const [temp, setTemp] = useState("")
    const [humidity, setHumidity] = useState("")
    const [dFPoint, setDFPoint] = useState("")
    const [rainVal, setRainVal] = useState("")
    const [avgSpeed, setAvgSpeed] = useState("")
    const [error, setError] = useState(null)

    const handleSubmit = async (e) => {
        e.preventDefault()

        const weather = {temp, humidity, dFPoint, rainVal, avgSpeed}

        const response = await fetch("/api/weather", {
            method: "POST",
            body: JSON.stringify(weather),
            headers: {
                "Content-Type": "application/json"

            }

        })

        const json = await response.json()

        if (!response.ok){
            setError(json.error)

        }

        if (response.ok){
            setTemp("")
            setHumidity("")
            setDFPoint("")
            setRainVal("")
            setAvgSpeed("")
            setError(null)
            console.log("new entry added", json)

        }

    }

    return (
        <form className="create" onSubmit={handleSubmit}>
            <h3 className="formLabel">Add a new entry</h3>

            <label className="tempLabel">Temperature</label>
            <input 
                type="text"
                onChange={(e) => setTemp(e.target.value)}
                value={temp}
                className="tempInput"

            />
            <br />

            <label className="humLabel">Humidity</label>
            <input 
                type="text"
                onChange={(e) => setHumidity(e.target.value)}
                value={humidity}
                className="humInput"

            />
            <br />

            <label className="dewLabel">Dew Point</label>
            <input 
                type="number"
                onChange={(e) => setDFPoint(e.target.value)}
                value={dFPoint}
                className="dewInput"

            />
            <br />

            <label className="rainLabel">Precipitation</label>
            <input 
                type="text"
                onChange={(e) => setRainVal(e.target.value)}
                value={rainVal}
                className="rainInput"

            />
            <br />

            <label className="speedLabel">Median Speed</label>
            <input 
                type="number"
                onChange={(e) => setAvgSpeed(e.target.value)}
                value={avgSpeed}
                className="speedInput"

            />
            <br />

            <button className="addEntryBtn">Add entry</button>
            {error && <div className="error">{error}</div>}

        </form>

    )

}

export default WeatherForm