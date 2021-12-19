import React from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

class ImgLink extends React.Component {
    constructor(props) {
        super(props);
    }
    render() { 
        return (  
            <div class="social-container">
                <a href={this.props.link} target = "_blank">
                    <FontAwesomeIcon icon={this.props.icon} size={this.props.size} />
                </a>
            </div>
        );
    }
}
 
export default ImgLink;