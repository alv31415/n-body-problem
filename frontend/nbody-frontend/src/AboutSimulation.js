import React from "react";
import MathInline from "./MathInline";
import MathBlock from "./MathBlock";

function AboutSimulation() {

    return (
        <div style={{padding: 50}}>
                <h2>Creating a Simulation</h2>
                <p>
                    To create a simulation, you need to produce an <i>NBody</i>, which holds all the simulation data, 
                    such as the position, velocity and mass of each body in the simulation, 
                    alongside the physical information of the system, like energy, angular momentum or linear momentum. 
                    It is important to note that in the code, the gravitational constant <MathInline formula = "G"/> is set to 1, 
                    whilst its real value is actually <MathInline formula = "6.67408 \times 10^{-11}"/>. This was done so that when defining initial conditions, 
                    we could use smaller, more understandable numbers.
                    To create the simulation, you need to provide:
                    <ul>
                        <li>
                            <b>Positions</b>: a list containing the initial position vectors of the <MathInline formula = "n"/> bodies, in <MathInline formula = "\mathbb{R}^3"/>. 
                            For example, if we have 2 bodies located at 
                            <MathInline formula = "\begin{pmatrix}1 \\ 0\\ 0\end{pmatrix}, \begin{pmatrix}-1 \\ 0\\ 0\end{pmatrix}"/>, 
                            we would express this as:
                            <MathBlock formula = "\texttt{[[1,0,0], [-1,0,0]]}"/>
                        </li>
                        <li>
                            <b>Velocities</b>: a list containing the initial velocity vectors of the <MathInline formula = "n"/> bodies, in <MathInline formula = "\mathbb{R}^3"/>. 
                            For example, if we have 2 bodies moving with 
                            velocities  <MathInline formula = "\begin{pmatrix}0 \\ -1\\ 0\end{pmatrix}, \begin{pmatrix} 0\\ 1\\ 0\end{pmatrix}"/> we would express this as:
                            <MathBlock formula = "\texttt{[[0,-1,0], [0,1,0]]}"/>
                        </li>
                        <li>
                            <b>Masses</b>: a list containing the masses of the <MathInline formula = "n"/> bodies. 
                            For example, if we have 2 unit mass bodies, we would express this as:
                            <MathBlock formula = "\texttt{[1,1]}"/>
                        </li>
                        <li>
                            <b>Collision Tolerance</b>: the maximum distance between any of the <MathInline formula = "n"/> bodies, 
                            before a collision is considered to have happened. The smaller the <i>collision tolerance</i>, 
                            the more "lenient" the simulation becomes, 
                            since we allow bodies to come extremely close to each other, 
                            in situations when it might not be too physically feasible.
                        </li>
                        <li>
                            <b>Escape Tolerance</b>: to avoid "uneventful" simulations in which bodies just shoot off to 
                            infinity, <i>escape tolerance</i> represents the maximum distance permitted between the centre of mass of the system and
                            any of the <MathInline formula = "n"/> bodies, before the simulation is ended.
                        </li>
                    </ul>
                </p>
        </div>
    );
}

export default AboutSimulation;
