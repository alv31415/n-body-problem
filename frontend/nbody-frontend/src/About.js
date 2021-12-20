import React from "react";
import MathInline from "./MathInline";
import MathBlock from "./MathBlock";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

import { faGithub } from "@fortawesome/free-brands-svg-icons";
import { faFileAlt } from "@fortawesome/free-solid-svg-icons";

function About() {

    return <div style={{padding: 50}}>
        <div>
            <h2>About</h2>
            <p>
                This project was developed following the 
                University of Edinburgh School of Mathematics 2021 Summer Vacation Scholarship. 
                Under the supervision 
                of <a className = "link-inline" href = "https://www.maths.ed.ac.uk/~mruffert/">Dr. Maximilian Ruffert</a>, I 
                investigated the stability of the Figure of 8 configuration of the 3-Body Problem 
                (you can check my report here <a href="https://alv31415.github.io/n-body-problem/n-body-report.pdf"
                    target = "_blank" className = "img-link fa-fw link-inline">
                    <FontAwesomeIcon icon={faFileAlt}/></a>).
                This was done in Python 
                (you can check the code here <a href="https://github.com/alv31415/n-body-problem/tree/website"
                    target = "_blank" className = "img-link fa-fw link-inline">
                    <FontAwesomeIcon icon={faGithub}/></a>), and was entirely numerical 
                (although some algebraic analysis was used to derive certain initial conditions).</p>
            <p>
                The point is, in doing this investigation, I had to do a lot of research with regards to the n body problem, 
                and it was hard for me to find "easy to follow" resources. 
                The objective of this site is to hopefully make it easy to understand the intricacies of the n body problem, 
                by providing both the mathematical background of the problem, and the plots resulting from running the simulations.
            </p>
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

            <h2>Running a Simulation</h2>

            <p>
                Once the simulation has been created, we need to produce a numerical integrator, which actually computes the paths of the <MathInline formula = "n"/> bodies. 
                To do this, we employ <i>numerical integration</i>. In particular, we use 
                the <i>3-Step Leapfrog Method</i> (also known as 
                the <a className = "link-inline" href = "http://physics.ucsc.edu/~peter/242/leapfrog.pdf">Velocity Verlet Method</a>). This is a <b>second order</b>, <b>symplectic</b> method, 
                which is desirable in the context of physical simulations, as it will respect the conservation laws. 
                To geneerate the <i>Integrator</i>, you need to provide:
                <ul>
                    <li>
                        <b>Integration Steps</b>: the number of times which we integrate.
                    </li>
                    <li>
                        <b>Time Step</b>: the size of an integration step, typically denoted with <MathInline formula = "h"/>. 
                        A smaller value provides more accurate integration, at the cost of decreasing simulation time.
                    </li>
                    <li>
                        <b>Tolerance</b>: the maximum error permitted for the system properties, 
                        such as energy, angular momentum, linear momentum or centre of mass. 
                        If upon performing an integration step any of these properties changes by more than the tolerance, 
                        the simulation will terminate. 
                        We have found that setting this to <MathInline formula = "0.01"/> is enough to produce accurate enough simulations.

                    </li>
                    <li>
                        <b>Adaptive</b>: whether to use an adaptive time step of not. If this is used, 
                        the time step at each simulation step is adapted based on the positions and velocities of the bodies. 
                        In many cases, this helps avoid errors in system properties. 
                        When using an adaptive time step, the total simulation time 
                        is determined by either <MathInline formula = "integration \ steps \times time \ step"/>, 
                        or by a limit on the number of integration steps performed.
                    </li>
                    <li>
                        <b>Adaptive Constant</b>: a value used to toggle the size of the adaptive time step, 
                        with smaller adaptive constants producing smaller adaptive time steps. 
                        We have found that setting this to <MathInline formula = "0.1"/> is enough 
                        to handle most "well-behaved" simulations, 
                        although to avoid energy errors for more complicated initial 
                        conditions, <MathInline formula = "0.01"/> might be better (at the cost of much higher runtime).
                    </li>
                    <li>
                        <b>Time Step Limit</b>: the smallest permitted adaptive time step size. 
                        If the adaptive time step becomes too small, 
                        this oftentimes indicates that the bodies are moving very fast, 
                        or extremely close to each other, which might not be of interest. 
                        We have found that setting this to <MathInline formula = "10^{-5}"/> is enough to handle most simulations.
                    </li>
                    <li>
                        <b>NBody ID</b>: the ID identifying a given simulation. 
                        This means that different integration parameters can be tested on the same simulation
                    </li>
                </ul>
                Once a <i>Integrator</i> has been created, we can use its ID to plot the simulation.
            </p>
        </div>
    </div>;
}

export default About;
