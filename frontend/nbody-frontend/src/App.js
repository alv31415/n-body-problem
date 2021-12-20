import './styles.css';

import React from 'react';
import Simulation from './Simulation';
import About from './About';
import Math from './Math';
import SocialLinks from './SocialLinks';
import AboutSimulation from './AboutSimulation';
import AboutRunSimulation from './AboutRunSimulation';
import ScrollButton from './ScrollTop';


function App() {

  return (
    <>
    <div className="App">
      <header className="App-header">
        <h1>N Body Problem Simulation</h1>
        <SocialLinks/>
      </header>
      <Simulation/>
      <About/>
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
