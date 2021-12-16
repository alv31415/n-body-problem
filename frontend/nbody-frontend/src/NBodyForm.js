import React from "react";
import FormBlock from "./FormBlock";

class NBodyForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            body: {
                positions: "",
                velocities: "",
                masses: "",
                collision_tolerance: 0.001,
                escape_tolerance: 1000
            }
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

        const postUrl = "http://127.0.0.1:8000/api/nbody-create/";

        var csrfToken = this.getCookie("csrftoken");

        const reqBody = {
            method: "POST",
            headers: {
                "Content-Type" : "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify(this.state.body)
        };

        try {
            const response = await fetch(postUrl, reqBody)
            const data = await response.json();
            
            if (response.ok) {
                console.log(data);
                this.props.onNBodyCreate(data.id);
            }
        } 
        catch (e) {
            console.error("Error occurred during POST request", e)
        }     
    }

    handleChange(e) {
        const newBody = {...this.state.body};
        newBody[e.target.name] = e.target.value;
        this.setState({body: newBody});
    }

    render() {
        
        return (
            <div className = "n-body-form">
                <form type = "submit" onSubmit = {this.handleSubmit}>
                    <FormBlock labelName = "Positions" name = "positions" type = "text" placeholder = "[[1,2,3], [4,7,9], [2,3,4]]" value = {this.state.body.positions} onChange = {this.handleChange}/>
                    <FormBlock labelName = "Velocities" name = "velocities" type = "text" placeholder = "[[1,2,3], [4,7,9], [2,3,4]]" value = {this.state.body.velocities} onChange = {this.handleChange}/>
                    <FormBlock labelName = "Masses" name = "masses" type = "text" placeholder = "[3,1,4]" value = {this.state.body.masses} onChange = {this.handleChange}/>
                    <FormBlock labelName = "Collision Tolerance" name = "collision_tolerance" type = "number" step = "any" placeholder = "0.001" value = {this.state.body.collision_tolerance} onChange = {this.handleChange}/>
                    <FormBlock labelName = "Escape Tolerance" name = "escape_tolerance" type = "number" step = "any" placeholder = "1000" value = {this.state.body.escape_tolerance} onChange = {this.handleChange}/>       
                    <br/>
                    <button type="submit">Create NBody</button>
                </form>
            </div>
        )
    }

}

export default NBodyForm;