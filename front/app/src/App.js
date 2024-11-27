import react from 'react';
import Header from './Components/Header';
import MainBanner from './Components/MainBanner';
import Search from './Components/Search';
import BookList from './Components/BookList';
import LoadButton from './Components/LoadButton';
import logo from './logo.svg';
import './App.css';

function App() {
  return (
    <div className="App">
      <Header/>
      <MainBanner/>
      <Search/>
      <BookList/>
      <LoadButton/>
    </div>
  );
}

export default App;
