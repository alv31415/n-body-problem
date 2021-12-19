import React from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

class ImgLink extends React.Component {
    constructor(props) {
        super(props);
    }
    render() { 
        return (  
            <div className= "icon">
                <a href={this.props.link} target = "_blank" className = {this.props.className}>
                    <FontAwesomeIcon icon={this.props.icon}/>
                </a>
            </div>
        );
    }
}
 
export default ImgLink;