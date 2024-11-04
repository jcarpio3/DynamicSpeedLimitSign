const express = require("express")
const {
    createWeather,
    getWeather,
    getWeathers,
    deleteWeather,
    updateWeather

} = require("../Controllers/weatherController")

const router = express.Router()

//Find all weathers
router.get("/", getWeathers)

//Find a weather
router.get("/:id", getWeather)

//Post weather
router.post("/", createWeather)

//Delete weather
router.delete("/:id", deleteWeather)

//Update weather
router.patch("/:id", updateWeather)

module.exports = router
