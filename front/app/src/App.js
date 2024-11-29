import react, {useState} from 'react';
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
import ScrollToTop from './Components/ScrollToTop';
import { TokenProvider } from './TokenContext';

function App() {
  const [token, setToken] = useState("");
  return (
    
    <Router>
      <TokenProvider>
    <ScrollToTop />
      <Routes>
        <Route path="/" element={<Main/>} /> 
        <Route path="/register" element={<Register/>} />
        <Route path="/login" element={<Login/>} />
        <Route path="/externallib" element={<ExternalLibrary/>} />
        <Route path="/programs" element={<Programs/>} />
        <Route path="/BookDetail/:id" element={<BookDetail/>} />
        <Route path="/ExternalBookDetail/:id" element={<ExternalBookDetail/>} />
        <Route path="/Skmap" element={<Skmap/>} />
        <Route path="/Mypage" element ={<Mypage />} />
      </Routes>
      </TokenProvider>
    </Router>
  );
}

export default App;
