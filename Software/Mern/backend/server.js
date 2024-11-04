require("dotenv").config()

const express = require("express")
const mongoose = require("mongoose")
const weatherRoutes = require("./Routes/weather")

//Express app
const app = express()

//Middleware
app.use(express.json())

app.use((req, res, next) => {
    console.log(req.path, req.method)
    next()

})

//Routes
app.use("/api/weather", weatherRoutes)

//Connect to db
mongoose.connect(process.env.MONGO_URI)
    .then(() => {
        //Listen for request
        app.listen(process.env.PORT, () => {
            console.log("connected to db & istening on port 4000")

        })

    })
    .catch((error) => {
        console.log(error)

    })



