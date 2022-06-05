import React from "react";
import FormBlock from "./FormBlock";
import {getCookie, POST_INTEGRATOR_CREATE_URL} from "./reqResources";

class IntegratorForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            nbody_id: this.props.nbodyIDs[0],
            name: "Leapfrog3",
            steps: "",
            delta: "",
            tolerance: "",
            adaptive: false,
            adaptive_constant: "0.1",
            delta_lim: "0.00001"
        };
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleChange = this.handleChange.bind(this);
    }

    async handleSubmit(e) {

        e.preventDefault()

        if (!this.canSubmit()) {
            alert("Fill in all inputs to create an Integrator!");
            return null;
        }

        var csrfToken = getCookie("csrftoken");

        const reqBody = {
            method: "POST",
            headers: {
                "Content-Type" : "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify(this.state)
        };

        const response = await fetch(POST_INTEGRATOR_CREATE_URL, reqBody);

        if (response.ok) {
            const data = await response.json();
            this.props.onIntegratorCreate();
            alert(`Integrator with ID ${data.id} succesfully created!`)
        }
        else {
            alert(`There was a problem setting the integrator: ${response.statusText}`);
        }
   
    }

    handleChange(e) {

        const newIntegrator = {...this.state};
        if (e.target.name === "adaptive") {
            newIntegrator[e.target.name] = !this.state.adaptive;
        }
        else {
            newIntegrator[e.target.name] = e.target.value;
        }
        
        this.setState(newIntegrator);
    }

    canSubmit() {

        return !(this.state.steps === ""
                || this.state.delta === ""
                || this.state.tolerance === ""
                || this.state.adaptive_constant === ""
                || this.state.delta_lim === "");
    }

    render() {

        let buttonClass = "button" + (this.canSubmit() ? "" : " disabled");
        
        return (
            <div className = {this.props.className}>
                <h2>Integrator Properties</h2>
                <form type = "submit" onSubmit = {this.handleSubmit}>
                    <FormBlock hoverLabel = "The number of integration steps to make. If integration is adaptive, this is used to define the simulation time via steps * time steps."
                               labelName = "Integration Steps" 
                               name = "steps" 
                               type = "number" 
                               step = "1" 
                               placeholder = "1000" 
                               value = {this.state.steps} 
                               onChange = {this.handleChange}/>
                    <FormBlock hoverLabel = "The size of an integration step, h. If integration is adaptive, this is used to define the simulation time via steps * time steps."
                               labelName = "Time Step" 
                               name = "delta" 
                               type = "number" 
                               step = "any" 
                               placeholder = "0.1" 
                               value = {this.state.delta} 
                               onChange = {this.handleChange}/>
                    <FormBlock hoverLabel = "The error tolerance when computing quantities like energy or angular momentum."
                               labelName = "Tolerance" 
                               name = "tolerance" 
                               type = "number" 
                               step = "any" 
                               placeholder = "0.01" 
                               value = {this.state.tolerance} 
                               onChange = {this.handleChange}/>
                    <FormBlock hoverLabel = "Whether an adaptive time step should be used to integrate."
                               labelName = "Adaptive" 
                               name = "adaptive" 
                               type = "checkbox" 
                               value = {this.state.adaptive} 
                               onChange = {this.handleChange}/>
                    <FormBlock hoverLabel = "The constant used to define the adaptive time step. Ignored if adaptive is not checked."
                               labelName = "Adaptive Constant" 
                               name = "adaptive_constant" 
                               type = "number" 
                               step = "any" 
                               placeholder = "0.1" 
                               value = {this.state.adaptive_constant} 
                               onChange = {this.handleChange}/>
                    <FormBlock hoverLabel = "The minimum time step size allowed when using an adaptive time step. Ignored if adaptive is not checked."
                               labelName = "Time Step Limit" 
                               name = "delta_lim" 
                               type = "number" 
                               step = "any" 
                               placeholder = "0.00001" 
                               value = {this.state.delta_lim} 
                               onChange = {this.handleChange}/>
                    <FormBlock hoverLabel = "The ID of the NBody which will be simulated."
                               labelName = "NBody ID"  
                               name = "nbody_id" 
                               type = "select" 
                               value = {this.state.nbody_id} 
                               data_list = {this.props.nbodyIDs} 
                               onChange = {this.handleChange}/>
                    <button type="submit" className = {buttonClass}>Set Integrator Properties</button>
                </form>
            </div>
        );
    }

}

export default IntegratorForm;