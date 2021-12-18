import React from "react";

function NavItem(props) {
    return (
        <li>
            <a href = "#">
                <img src = {props.navIcon} alt = {props.alt}></img>
            </a>
        </li>
    );
} 

export default NavItem;