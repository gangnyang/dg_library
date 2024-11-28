import react from 'react';
import {BrowserRouter as Router, Routes, Route} from "react-router-dom";
import Main from './Page/Main';
import Login from './Page/Login';
import Register from './Page/Register';
import ExternalLibrary from './Page/ExternalLibrary';
import Programs from './Page/Programs';
import BookDetail from './Page/BookDetail';
import ExternalBookDetail from './Page/ExternalBookDetail';
import Skmap from './Page/Skmap';
import Mypage from './Page/Mypage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Main/>} /> 
        <Route path="/register" element={<Register/>} />
        <Route path="/login" element={<Login/>} />
        <Route path="/externallib" element={<ExternalLibrary/>} />
        <Route path="/programs" element={<Programs/>} />
        <Route path="/BookDetail" element={<BookDetail/>} />
        <Route path="/ExternalBookDetail" element={<ExternalBookDetail/>} />
        <Route path="/Skmap" element={<Skmap/>} />
        <Route path="/Mypage" element ={<Mypage />} />
      </Routes>
    </Router>
  );
}

export default App;
