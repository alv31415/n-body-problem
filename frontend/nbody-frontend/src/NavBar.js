import React from "react";

function NavBar(props) {
    return (
        <ul>{props.children}</ul>
    );
} 

export default NavBar;