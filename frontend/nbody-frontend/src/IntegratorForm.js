import React from "react";
import FormBlock from "./FormBlock";

class IntegratorForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            name: "Leapfrog3",
            steps: "",
            delta: "",
            tolerance: "",
            adaptive: false,
            adaptive_constant: "",
            delta_lim: "",
            position_orbits: [],
            nbody_id: this.props.nbodyID
        };
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleChange = this.handleChange.bind(this);
    }

    getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    async handleSubmit(e) {

        e.preventDefault()

        const postUrl = "http://127.0.0.1:8000/api/integrator-create/";

        var csrfToken = this.getCookie("csrftoken");

        const reqBody = {
            method: "POST",
            headers: {
                "Content-Type" : "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify(this.state)
        };

        console.log(this.state);

        try {
            const response = await fetch(postUrl, reqBody)
            const data = await response.json();
            
            if (response.ok) {
                console.log(data);
                this.props.onIntegratorCreate(data.id);
            }
        } 
        catch (e) {
            console.error("Error occurred during POST request", e)
        }     
    }

    handleChange(e) {

        const newIntegrator = {...this.state};
        if (e.target.name === "adaptive") {
            newIntegrator[e.target.name] = !this.state.adaptive
        }
        else {
            newIntegrator[e.target.name] = e.target.value;
        }
        
        this.setState(newIntegrator);
    }

    render() {
        
        return (
            <div className = "n-body-form">
                <form type = "submit" onSubmit = {this.handleSubmit}>
                    <FormBlock labelName = "Integration Steps" name = "steps" type = "number" step = "1" placeholder = "1000" value = {this.state.steps} onChange = {this.handleChange}/>
                    <FormBlock labelName = "Time Step" name = "delta" type = "number" step = "any" placeholder = "0.1" value = {this.state.delta} onChange = {this.handleChange}/>
                    <FormBlock labelName = "Tolerance" name = "tolerance" type = "number" step = "any" placeholder = "0.01" value = {this.state.tolerance} onChange = {this.handleChange}/>
                    <FormBlock labelName = "Adaptive" name = "adaptive" type = "checkbox" value = {this.state.adaptive} onChange = {this.handleChange}/>
                    <FormBlock labelName = "Adaptive Constant" name = "adaptive_constant" type = "number" step = "any" placeholder = "0.1" value = {this.state.adaptive_constant} onChange = {this.handleChange}/>
                    <FormBlock labelName = "Time Step Limit" name = "delta_lim" type = "number" step = "any" placeholder = "0.00001" value = {this.state.delta_lim} onChange = {this.handleChange}/>
                    <FormBlock labelName = "NBody ID" name = "nbody_id" type = "number" placeholder = "1" value = {this.state.nbody_id} onChange = {this.handleChange}/>
                    <br/>
                    <button type="submit">Create Integrator</button>
                </form>
            </div>
        )
    }

}

export default IntegratorForm;