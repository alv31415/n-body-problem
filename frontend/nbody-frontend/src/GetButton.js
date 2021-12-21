import React from "react";

class GetButton extends React.Component {
    
    constructor(props) {
        super(props)

        this.apiGet = this.apiGet.bind(this);
    }

    async apiGet() {

        let getUrl;

        if (this.props.getPk === "") {
             getUrl = "https://nbody-api.herokuapp.com/api/nbody-list/";
        }
        else {
            getUrl = "https://nbody-api.herokuapp.com//api/nbody-view/" + this.props.getPk;
        }

        try {
            const response = await fetch(getUrl, {method: "GET"})
            const data = await response.json();
            
            if (response.ok) {
                console.log(data);
            }
        } 
        catch (e) {
            console.error("Error occurred during GET request", e)
        }     
    }

    render() {
        return(
            <button name = {this.props.name} type = "button" onClick = {() => this.apiGet()}>{this.props.name}</button>
        )
    }

}

export default GetButton;