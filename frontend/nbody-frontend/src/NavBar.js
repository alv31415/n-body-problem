import React from "react";
import { Link } from "react-router-dom";

function NavBar() {
    return (
        <ul>
            <li><Link to = "/about">About</Link></li>
            <li><Link to = "/n-body-math">N Body Math</Link></li>
            <li><Link to = "/simulation">Simulation</Link></li>
        </ul>
    );
} 

export default NavBar;