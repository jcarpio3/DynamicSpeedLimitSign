const Weather = require("../Models/weatherModel")
const mongoose = require("mongoose")

//Get all weather
const getWeathers = async (req, res) => {
    const weathers = await Weather.find({}).sort({createdAt: -1})
    res.status(200).json(weathers)

}

//Get a weather
const getWeather = async (req, res) => {
    const {id} = req.params

    if (!mongoose.Types.ObjectId.isValid(id)) {
        return res.status(404).json({error: "No such weather"})

    }

    const weather = await Weather.findById(id).sort({createdAt: -1})

    if (!weather) {
        return res.status(404).json({error: "No such weather"})

    }

    res.status(200).json(weather)

}

//Create new weather
const createWeather = async (req, res) => {
    const {temp, humidity, avgSpeed, rainVal, dFPoint} = req.body

    try {
        const weather = await Weather.create({temp, humidity, avgSpeed, rainVal, dFPoint})
        res.status(200).json(weather)

    } catch (error) {
        res.status(400).json({error: error.message})

    }

}

//Delete a weather
const deleteWeather = async (req, res) => {
    const {id} = req.params

    if (!mongoose.Types.ObjectId.isValid(id)) {
        return res.status(404).json({error: "No such weather"})

    }

    const weather = await Weather.findOneAndDelete({_id: id})

    if (!weather) {
        return res.status(400).json({error: "No such weather"})

    }

    res.status(200).json(weather)

}

//Update a weather
const updateWeather = async (req, res) => {
    const {id} = req.params

    if (!mongoose.Types.ObjectId.isValid(id)) {
        return res.status(404).json({error: "No such weather"})

    }

    const weather = await Weather.findOneAndUpdate({_id: id}, {
        ...req.body

    })

    if (!weather) {
        return res.status(400).json({error: "No such weather"})

    }

    res.status(200).json(weather)

}

module.exports = {
    getWeathers,
    getWeather,
    createWeather,
    deleteWeather,
    updateWeather

}