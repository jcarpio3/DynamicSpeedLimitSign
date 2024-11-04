const mongoose = require("mongoose")

const Schema = mongoose.Schema

const weatherSchema = new Schema({
    temp: {
        type: String,
        required: true

    },
    humidity: {
        type: String,
        required: true

    },
    avgSpeed: {
        type: Number,
        required: true

    },
    rainVal: {
        type: String,
        required: true

    },
    dFPoint: {
        type: Number,
        required: true
        
    }

}, {timestamps: true})

module.exports = mongoose.model("Weather", weatherSchema)