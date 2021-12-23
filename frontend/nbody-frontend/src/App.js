import './styles.css';

import React from 'react';
import Simulation from './Simulation';
import About from './About';
import Math from './Math';
import SocialLinks from './SocialLinks';
import AboutSimulation from './AboutSimulation';
import AboutRunSimulation from './AboutRunSimulation';
import ScrollButton from './ScrollButton';
import NavBar from './NavBar';


function App() {

  return (
    <>
    <div className="App">
      <header className="App-header">
        <NavBar/>
        <h1>N Body Problem Simulation</h1>
        <SocialLinks/>
      </header>
      <About/>
      <Simulation/>
      <AboutSimulation/>
      <AboutRunSimulation/>
      <Math/>
      <ScrollButton/>
      <footer className = "copyright"> <small>&copy; Copyright {new Date().getFullYear()}, Antonio León Villares</small> </footer>
    </div>
    </>
  );
}

export default App;
