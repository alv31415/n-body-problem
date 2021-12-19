import React from "react";
import FormBlock from "./FormBlock";

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

        if (!this.canSubmit()) {
            console.log("Fill in all inputs to submit!")
            return null;
        }

        console.log(this.state)

        const postUrl = "http://127.0.0.1:8000/api/nbody-create/";

        var csrfToken = this.getCookie("csrftoken");

        const reqBody = {
            method: "POST",
            headers: {
                "Content-Type" : "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify(this.state)
        };

        try {
            const response = await fetch(postUrl, reqBody)
            const data = await response.json();
            
            if (response.ok) {
                this.props.onNBodyCreate();
            }
        } 
        catch (e) {
            console.error("Error occurred during POST request", e)
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
                || this.state.escape_tolerance === "") 
    }

    render() {
        
        return (
            <div className = {this.props.className}>
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
                    <FormBlock hoverLabel = "The minimum distance between 2 bodies, before they are considered to have collided."
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
                    <button type="submit">Create NBody</button>
                </form>
            </div>
        )
    }

}

export default NBodyForm;