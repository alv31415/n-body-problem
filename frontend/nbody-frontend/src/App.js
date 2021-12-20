import './styles.css';

import Simulation from './Simulation';
import About from './About';
import Math from './Math';
import NavBar from './NavBar';
import SocialLinks from './SocialLinks';


function App() {

  return (
    <div className="App">
      <header className="App-header">
        <h1>N Body Problem Simulation</h1>
        <SocialLinks/>
      </header>
      <Simulation/>
      <hr></hr>
      <About/>
      <Math/>
      </div>
  );
}

export default App;
