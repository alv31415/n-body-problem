import React from "react";
import MathJax from "react-mathjax";

function AboutRunSimulation() {

    return (
        <div style={{padding: 50}}>
            <MathJax.Provider>
                <h2>Running a Simulation</h2>
                <p>
                    Once the simulation has been created, we need to produce a numerical integrator, which actually computes the paths of the <MathJax.Node inline formula = "n"/> bodies. 
                    To do this, we employ <i>numerical integration</i>. In particular, we use 
                    the <i>3-Step Leapfrog Method</i> (also known as 
                    the <a className = "link-inline" href = "http://physics.ucsc.edu/~peter/242/leapfrog.pdf">Velocity Verlet Method</a>). This is a <b>second order</b>, <b>symplectic</b> method, 
                    which is desirable in the context of physical simulations, as it will respect the conservation laws. 
                    To geneerate the <i>Integrator</i>, you need to provide:
                </p>
                <ul>
                    <li>
                        <b>Integration Steps</b>: the number of times which we integrate.
                    </li>
                    <li>
                        <b>Time Step</b>: the size of an integration step, typically denoted with <MathJax.Node inline formula = "h"/>. 
                        A smaller value provides more accurate integration, at the cost of decreasing simulation time.
                    </li>
                    <li>
                        <b>Tolerance</b>: the maximum error permitted for the system properties, 
                        such as energy, angular momentum, linear momentum or centre of mass. 
                        If upon performing an integration step any of these properties changes by more than the tolerance, 
                        the simulation will terminate. 
                        We have found that setting this to <MathJax.Node inline formula = "0.01"/> is enough to produce accurate enough simulations.

                    </li>
                    <li>
                        <b>Adaptive</b>: whether to use an adaptive time step of not. If this is used, 
                        the time step at each simulation step is adapted based on the positions and velocities of the bodies. 
                        In many cases, this helps avoid errors in system properties. 
                        When using an adaptive time step, the total simulation time 
                        is determined by either <MathJax.Node inline formula = "integration \ steps \times time \ step"/>, 
                        or by a limit on the number of integration steps performed.
                    </li>
                    <li>
                        <b>Adaptive Constant</b>: a value used to toggle the size of the adaptive time step, 
                        with smaller adaptive constants producing smaller adaptive time steps. 
                        We have found that setting this to <MathJax.Node inline formula = "0.1"/> is enough 
                        to handle most "well-behaved" simulations, 
                        although to avoid energy errors for more complicated initial 
                        conditions, <MathJax.Node inline formula = "0.01"/> might be better (at the cost of much higher runtime).
                    </li>
                    <li>
                        <b>Time Step Limit</b>: the smallest permitted adaptive time step size. 
                        If the adaptive time step becomes too small, 
                        this oftentimes indicates that the bodies are moving very fast, 
                        or extremely close to each other, which might not be of interest. 
                        We have found that setting this to <MathJax.Node inline formula = "10^{-5}"/> is enough to handle most simulations.
                    </li>
                    <li>
                        <b>NBody ID</b>: the ID identifying a given simulation. 
                        This means that different integration parameters can be tested on the same simulation
                    </li>
                </ul>
                <p>
                    Once a <i>Integrator</i> has been created, we can use its ID to plot the simulation.
                </p>
            </MathJax.Provider>
        </div>
    );
}

export default AboutRunSimulation;
