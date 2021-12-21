import './styles.css';
import React from "react";
import NBodyForm from './NBodyForm';
import IntegratorForm from "./IntegratorForm"
import OrbitPlotter from './OrbitPlotter';


class Simulation extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      nbodyIDs: [],
      integratorIDs: []
    }

    this.updateNBodyIDs = this.updateNBodyIDs.bind(this);
    this.updateIntegratorIDs = this.updateIntegratorIDs.bind(this);
  }


  async getIntegratorIDs() {
    const getUrl = "https://nbody-api.herokuapp.com/api/integrator-list-ids/"

    try {
        const response = await fetch(getUrl, {method: "GET"});
        const data = await response.json();
        data.sort();
        
        if (response.ok) {
            this.setState({...this.state, integratorIDs: data});
        }
    } 
    catch (e) {
        console.error("Error occurred during GET request", e)
    }     
}

async getNBodyIDs() {
  const getUrl = "https://nbody-api.herokuapp.com/api/nbody-list-ids/"

  try {
      const response = await fetch(getUrl, {method: "GET"});
      const data = await response.json();
      data.sort();
      
      if (response.ok) {
          this.setState({...this.state, nbodyIDs: data});
      }
  } 
  catch (e) {
      console.error("Error occurred during GET request", e)
  }     
}

componentDidMount() {
  this.getNBodyIDs();
  this.getIntegratorIDs();
}

updateNBodyIDs() {
  this.getNBodyIDs();
}

updateIntegratorIDs() {
  this.getIntegratorIDs();
}

render() {

  return (
        <div>
            <div className = "row-forms">
                <NBodyForm className = "bg-form" onNBodyCreate = {this.updateNBodyIDs}/>
                <IntegratorForm className = "bg-form" onIntegratorCreate = {this.updateIntegratorIDs} nbodyIDs = {this.state.nbodyIDs}/>
            </div>
            <br/>
            <OrbitPlotter integratorIDs = {this.state.integratorIDs} onIntegratorUpdate = {this.updateIntegratorIDs}/>
        </div>
        );
    };
};

export default Simulation;
