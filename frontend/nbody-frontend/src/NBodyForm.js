import React from "react";
import FormBlock from "./FormBlock";
import {getCookie, POST_NBODY_CREATE_URL} from "./reqResources";

class NBodyForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            positions: "",
            velocities: "",
            masses: "",
            collision_tolerance: "0.001",
            escape_tolerance: "1000"
        };
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleChange = this.handleChange.bind(this);
    }

    async handleSubmit(e) {

        e.preventDefault();

        if (!this.canSubmit()) {
            alert("Fill in all inputs to create an NBody!");
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

        const response = await fetch(POST_NBODY_CREATE_URL, reqBody);
            
        if (response.ok) {
            const data = await response.json();
            this.props.onNBodyCreate();
            alert(`Initial conditions set succesfully!. NBody ID: ${data.id}`);
        }
        else {
            alert(`There was a problem setting the initial conditions: ${response.statusText}`);
        }
    }

    handleChange(e) {
        const newBody = {...this.state};
        newBody[e.target.name] = e.target.value;
        this.setState(newBody);
    }

    canSubmit() {
        return !(this.state.positions === ""
                || this.state.velocities === ""
                || this.state.masses === ""
                || this.state.collision_tolerance === ""
                || this.state.escape_tolerance === "");
    }

    render() {

        let buttonClass = "button" + (this.canSubmit() ? "" : " disabled");
        
        return (
            <div className = {this.props.className}>
                <h2>Initial Conditions</h2>
                <form type = "submit" onSubmit = {this.handleSubmit}>
                    <FormBlock hoverLabel = "A list of the initial positions of the bodies in [x,y,z] coordinates."
                               labelName = "Positions" 
                               name = "positions" 
                               type = "text" 
                               placeholder = "[[1,2,3], [4,7,9], [2,3,4]]" 
                               value = {this.state.positions} 
                               onChange = {this.handleChange}/>
                    <FormBlock hoverLabel = "A list of the initial velocities of the bodies in [x,y,z] coordinates."
                               labelName = "Velocities" 
                               name = "velocities" 
                               type = "text" 
                               placeholder = "[[1,2,3], [4,7,9], [2,3,4]]" 
                               value = {this.state.velocities} 
                               onChange = {this.handleChange}/>
                    <FormBlock hoverLabel = "A list of the masses of the bodies."
                               labelName = "Masses" 
                               name = "masses" 
                               type = "text" 
                               placeholder = "[3,1,4]" 
                               value = {this.state.masses} 
                               onChange = {this.handleChange}/>
                    <FormBlock hoverLabel = "The maximum distance between 2 bodies, before they are considered to have collided."
                               labelName = "Collision Tolerance" 
                               name = "collision_tolerance" 
                               type = "number" step = "any" 
                               placeholder = "0.001" 
                               value = {this.state.collision_tolerance} 
                               onChange = {this.handleChange}/>
                    <FormBlock hoverLabel = "The maximum distance of any body away from the centre of mass, before it is considered to escape the system."
                               labelName = "Escape Tolerance" 
                               name = "escape_tolerance" 
                               type = "number" 
                               step = "any" 
                               placeholder = "1000" 
                               value = {this.state.escape_tolerance} 
                               onChange = {this.handleChange}/>       
                    <button className = {buttonClass} type="submit">Set Initial Conditions</button>
                </form>
            </div>
        );
    }

}

export default NBodyForm;