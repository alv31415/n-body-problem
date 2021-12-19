import './styles.css';
import React from "react";
import NBodyForm from './NBodyForm';
import IntegratorForm from "./IntegratorForm"
import OrbitPlotter from './OrbitPlotter';
import ImgLink from './ImgLink';

import { faGithub } from "@fortawesome/free-brands-svg-icons";
import { faFileAlt } from "@fortawesome/free-regular-svg-icons";


class App extends React.Component {
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
    const getUrl = "http://localhost:8000/api/integrator-list-ids/"

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
  const getUrl = "http://localhost:8000/api/nbody-list-ids/"

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
    <div className="App">
      <header className="App-header">
      <h1>N Body Problem Simulation</h1>
      <div className = "row-icons">
        <ImgLink icon = {faGithub} 
                 className = "icon github" 
                 size = "2x" 
                 link = "https://github.com/alv31415/n-body-problem/tree/website"/>
        <ImgLink icon = {faFileAlt} 
                 className = "icon file" 
                 size = "2x" 
                 link = "https://github.com/alv31415/n-body-problem/tree/website/n-body-report.pdf"/>
      </div>
      </header>
      <div className = "row-forms">
            <NBodyForm className = "bg-form" onNBodyCreate = {this.updateNBodyIDs}/>
            <IntegratorForm className = "bg-form" onIntegratorCreate = {this.updateIntegratorIDs} nbodyIDs = {this.state.nbodyIDs}/>
        </div>
        <br/>
        <OrbitPlotter integratorIDs = {this.state.integratorIDs} onIntegratorUpdate = {this.updateIntegratorIDs}/>
        <iframe src="https://github.com/alv31415/n-body-problem/tree/website/n-body-report.pdf" height="200" width="300"></iframe>
    </div>
  );
};
};

export default App;
