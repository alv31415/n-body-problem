import styles from './styles.css';
import React, { useLayoutEffect } from "react";
import NBodyForm from './NBodyForm';
import IntegratorForm from "./IntegratorForm"
import OrbitPlotter from './OrbitPlotter';
import NavBar from './NavBar';
import NavItem from './NavItem';
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col"
import bootstrap from 'bootstrap';

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
        <div style={{ display: "flex", flexDirection: "row", gap: "100px"}}>
            <NBodyForm onNBodyCreate = {this.updateNBodyID}/>
            <IntegratorForm onIntegratorCreate = {this.updateIntegratorID} nbodyID = {this.state.nbodyID}/>
        </div>
        <br/>
        <OrbitPlotter integratorID = {this.state.integratorID} onIntegratorUpdate = {this.updateIntegratorID}/>
      </header>
    </div>
  );
};
};

export default App;
