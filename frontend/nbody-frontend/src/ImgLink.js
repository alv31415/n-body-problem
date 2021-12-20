import React from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

function ImgLink (props) {
    return (  
            <div className= "icon">
                <a href={props.link} target = "_blank" rel="noreferrer" className = {props.className}>
                    <FontAwesomeIcon icon={props.icon}/>
                </a>
            </div>
        );
}
 
export default ImgLink;