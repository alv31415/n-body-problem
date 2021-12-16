import './App.css';
import React from "react";
import NBodyForm from './NBodyForm';
import IntegratorForm from "./IntegratorForm"
import OrbitPlotter from './OrbitPlotter';

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      nbodyID: 1,
      integratorID: 1
    }

    this.updateNBodyID = this.updateNBodyID.bind(this);
    this.updateIntegratorID = this.updateIntegratorID.bind(this);
  }


/*
<GetButton name = "Click me to get 2" getPk = "2"></GetButton>
<PostButton name = "Click me to post" getPk = "2" body = {this.json_body}></PostButton>
<NBodyForm onNBodyCreate = {this.updateNBodyID}/>
<NBodyForm onNBodyCreate = {this.updateNBodyID}/>
          <br/>
          <IntegratorForm onIntegratorCreate = {this.updateIntegratorID} nbodyID = {this.state.nbodyID}/>
<OrbitPlotter integratorID = {this.state.integratorID} onIntegratorUpdate = {this.updateIntegratorID}/>
*/


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
