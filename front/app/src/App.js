import react from 'react';
import {BrowserRouter as Router, Routes, Route} from "react-router-dom";
import Main from './Page/Main';
import Login from './Page/Login';
import Register from './Page/Register';
import ExternalLibrary from './Page/ExternalLibrary';
import Programs from './Page/Programs';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Main/>} /> 
        <Route path="/register" element={<Register/>} />
        <Route path="/login" element={<Login/>} />
        <Route path="/externallib" element={<ExternalLibrary/>} />
        <Route path="/programs" element={<Programs/>} />
      </Routes>
    </Router>
  );
}

export default App;
