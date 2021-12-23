import './styles.css';
import React from "react";
import NBodyForm from './NBodyForm';
import IntegratorForm from "./IntegratorForm"
import OrbitPlotter from './OrbitPlotter';
import {GET_NBODY_IDS_URL, GET_INTEGRATOR_IDS_URL} from "./reqResources";


class Simulation extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      nbodyIDs: [],
      integratorIDs: []
    }
    this.getIntegratorIDs = this.getIntegratorIDs.bind(this);
    this.getNBodyIDs = this.getNBodyIDs.bind(this);
    this.fetchIDs = this.fetchIDs.bind(this);
  }


  async getIntegratorIDs() {

    const response = await fetch(GET_INTEGRATOR_IDS_URL, {method: "GET"});

    if (response.ok) {
      const data = await response.json();
      data.sort();

      return data;
    }
    else {
      alert(`There was a problem fetching the Integrator IDs: ${response.statusText}`)
    }   
}

async getNBodyIDs() {

  const response = await fetch(GET_NBODY_IDS_URL, {method: "GET"});

    if (response.ok) {
      const data = await response.json();
      data.sort();

      return data;
    }
    else {
      alert(`There was a problem fetching the NBody IDs: ${response.statusText}`)
    }     
}

fetchIDs() {
  Promise.all([this.getNBodyIDs(), this.getIntegratorIDs()])
    .then(([nbodyIDs, integratorIDs]) => {
          this.setState({...this.state, integratorIDs: integratorIDs, nbodyIDs: nbodyIDs});
      }
    );
}

 componentDidMount() {
   this.fetchIDs();
}

render() {

  if (this.state.nbodyIDs.length === 0 && this.state.integratorIDs.length === 0) {
    return (
      <div id = "simulation">
        <p style = {{fontSize: "12pt"}}>Start by setting initial conditions below  ⬇️</p>
        <NBodyForm className = "bg-form" onNBodyCreate = {this.fetchIDs}/>
      </div>
    );
  }
  else if (this.state.nbodyIDs.length !== 0 && this.state.integratorIDs.length === 0){
    return (
      <div id = "simulation">
          <p style = {{fontSize: "12pt", textAlign: "center"}}>Great! Now, set integrator parameters below  ⬇️</p>
          <div className = "row-forms">
              <NBodyForm className = "bg-form" onNBodyCreate = {this.fetchIDs}/>
              <IntegratorForm className = "bg-form" onIntegratorCreate = {this.fetchIDs} nbodyIDs = {this.state.nbodyIDs}/>
          </div>
      </div>
    );
  }
  else {
  return (
          <div id = "simulation">
              <div className = "row-forms">
                  <NBodyForm className = "bg-form" onNBodyCreate = {this.fetchIDs}/>
                  <IntegratorForm className = "bg-form" onIntegratorCreate = {this.fetchIDs} nbodyIDs = {this.state.nbodyIDs}/>
              </div>
              <br/>
              <OrbitPlotter onIntegratorUpdate = {this.fetchIDs} integratorIDs = {this.state.integratorIDs}/>
          </div>
          );
  };
};
};

export default Simulation;
