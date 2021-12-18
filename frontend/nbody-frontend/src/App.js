import './App.css';
import React, { useLayoutEffect } from "react";
import NBodyForm from './NBodyForm';
import IntegratorForm from "./IntegratorForm"
import OrbitPlotter from './OrbitPlotter';
import NavBar from './NavBar';
import NavItem from './NavItem';
import orbits from "./imgs/orbits.png";

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      nbodyID: null,
      integratorID: null
    }

    this.updateNBodyID = this.updateNBodyID.bind(this);
    this.updateIntegratorID = this.updateIntegratorID.bind(this);
  }

updateNBodyID(id) {
  this.setState({...this.state, nbodyID: id});
  console.log("NBODY ID", id);
}

updateIntegratorID(id) {
  this.setState({...this.state, integratorID: id});
  console.log("INTEGRATOR ID", id);
}

render() {

  return (
    <div className="App">
      <header className="App-header">
        <img src = {orbits}></img>
        <NBodyForm onNBodyCreate = {this.updateNBodyID}/>
        <br/>
        <IntegratorForm onIntegratorCreate = {this.updateIntegratorID} nbodyID = {this.state.nbodyID}/>
        <br/>
        <OrbitPlotter integratorID = {this.state.integratorID} onIntegratorUpdate = {this.updateIntegratorID}/>
      </header>
    </div>
  );
};
};

export default App;
