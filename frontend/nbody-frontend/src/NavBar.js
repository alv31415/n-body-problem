import React from 'react'
import { Link } from 'react-scroll'

class NavBar extends React.Component {
    render() {
        return (
            <ul className = "navbar">
                <li><Link activeClass="active" to="about" spy={true} smooth={true}>About</Link></li>
                <li><Link to="simulation" spy={true} smooth={true}>Simulation</Link></li>
                <li><Link to="initial-conditions" spy={true} smooth={true}>Setting Initial Conditions</Link></li>
                <li><Link to="integrator" spy={true} smooth={true}>Setting Integrator</Link></li>
                <li><Link to="math" spy={true} smooth={true}>Math</Link></li>
            </ul>
        )
    }
}

export default NavBar;
