import React from "react";

class PostButton extends React.Component {
    
    constructor(props) {
        super(props)

        this.apiPost = this.apiPost.bind(this);
        this.getCookie = this.getCookie.bind(this);
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

    async apiPost() {

        let getUrl;

        if (this.props.getPk === "") {
             getUrl = "http://127.0.0.1:8000/api/nbody-create/";
        }
        else {
            getUrl = "http://127.0.0.1:8000/api/nbody-update/" + this.props.getPk;
        }

        var csrfToken = this.getCookie("csrftoken");

        const reqBody = {
            method: "POST",
            headers: {
                "Content-Type" : "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify(this.props.body)
        };

        try {
            const response = await fetch(getUrl, reqBody)
            const data = await response.json();
            
            if (response.ok) {
                console.log(data);
            }
        } 
        catch (e) {
            console.error("Error occurred during POST request", e)
        }     
    }

    render() {
        return(
            <button name = {this.props.name} type = "submit" onClick = {() => this.apiPost()}>{this.props.name}</button>
        )
    }

}

export default PostButton;