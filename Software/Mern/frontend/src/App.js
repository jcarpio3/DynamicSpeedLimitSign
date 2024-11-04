import {BrowserRouter, Routes, Route} from 'react-router-dom'

//Pages and components
import Home from "./Pages/Home"

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <div className="main">
          <Routes>
            <Route 
              path="/" 
              element={<Home />}
              
            />

          </Routes>

        </div>

      </BrowserRouter>

    </div>

  );
}

export default App;
