import React from "react";
import MathJax from "react-mathjax";

function AboutSimulation() {

    return (
        
        <div id = "initial-conditions" style={{padding: 50}}>
            <MathJax.Provider>
                <h2>Setting the Initial Conditions for the Simulation</h2>
                <p>
                    The first step is to set all the initial conditions which define the simulation.
                    It is important to note that in the code, 
                    the gravitational constant <MathJax.Node inline formula = "G"/> is set to 1, 
                    whilst its real value is actually <MathJax.Node inline formula = "6.67408 \times 10^{-11}"/>. This was done so that when defining initial conditions, 
                    we could use smaller, more understandable numbers.
                    The initial conditions required are:
                </p>
                    <ul>
                        <li>
                            <b>Positions</b>: a list containing the initial position vectors of the <MathJax.Node inline formula = "n"/> bodies, in <MathJax.Node inline formula = "\mathbb{R}^3"/>. 
                            For example, if we have 2 bodies located at 
                            <MathJax.Node inline formula = "\begin{pmatrix}1 \\ 0\\ 0\end{pmatrix}, \begin{pmatrix}-1 \\ 0\\ 0\end{pmatrix}"/>, 
                            we would express this as:
                            <MathJax.Node formula = "\texttt{[[1,0,0], [-1,0,0]]}"/>
                        </li>
                        <li>
                            <b>Velocities</b>: a list containing the initial velocity vectors of the <MathJax.Node inline formula = "n"/> bodies, in <MathJax.Node inline formula = "\mathbb{R}^3"/>. 
                            For example, if we have 2 bodies moving with 
                            velocities  <MathJax.Node inline formula = "\begin{pmatrix}0 \\ -1\\ 0\end{pmatrix}, \begin{pmatrix} 0\\ 1\\ 0\end{pmatrix}"/> we would express this as:
                            <MathJax.Node formula = "\texttt{[[0,-1,0], [0,1,0]]}"/>
                        </li>
                        <li>
                            <b>Masses</b>: a list containing the masses of the <MathJax.Node inline formula = "n"/> bodies. 
                            For example, if we have 2 unit mass bodies, we would express this as:
                            <MathJax.Node formula = "\texttt{[1,1]}"/>
                        </li>
                        <li>
                            <b>Collision Tolerance</b>: the maximum distance between any of the <MathJax.Node inline formula = "n"/> bodies, 
                            before a collision is considered to have happened. The smaller the <i>collision tolerance</i>, 
                            the more "lenient" the simulation becomes, 
                            since we allow bodies to come extremely close to each other, 
                            in situations when it might not be too physically feasible.
                        </li>
                        <li>
                            <b>Escape Tolerance</b>: to avoid "uneventful" simulations in which bodies just shoot off to 
                            infinity, <i>escape tolerance</i> represents the maximum distance permitted between the centre of mass of the system and
                            any of the <MathJax.Node inline formula = "n"/> bodies, before the simulation is ended.
                        </li>
                    </ul>
                    <p>
                        Once the initial conditions are submitted, you should obtain a <b>NBody ID</b>: this is used to uniquely
                         identify the simulation associated with the initial conditions submitted.
                    </p>
            </MathJax.Provider>
        </div>
    );
}

export default AboutSimulation;
