import React from "react";
import MathBlock from "./MathBlock";
import MathInline from "./MathInline";

function Math() {
    return (
    <div style={{padding: 50}}>
        <h2>The Math</h2>
        <p>We now consider the mathematical formulation of the N Body Problem, 
        alongside the recursion which defines the integrator, and how the adaptive time step is computed.</p>
        <h3>Defining the N Body Problem</h3>
        <p>
           <b>Newton's Second Law of Motion</b> relates the net force exerted on a body with its acceleration:
            <MathBlock formula = "\sum \vec{F} = m\vec{a}"/>
        </p>
        <p>
            <b>Newton's Universal Law of Gravitation</b> states that the magnitude of the gravitational force 
            between 2 bodies is inversely proportional to the square of the distance between the 2 bodies. 
            In particular, the gravitational force exerted by some body <MathInline formula = "j"/> on another 
            body <MathInline formula = "i"/> can be described by:
            <MathBlock formula = "\vec{F}_{ij} = -G\frac{m_im_j}{\|\vec{r_i} - \vec{r_j}\|^3}(\vec{r}_i - \vec{r}_j)"/>
            where:
            <ul>
                <li><MathInline formula = "m_i, m_j"/> are the masses of the 2 bodies</li>
                <li><MathInline formula = "\vec{r}_i, \vec{r}_j"/> are the position vectors of the 2 bodies</li>
                <li><MathInline formula = "G = 6.67408 \times 10^{-11}m^3kg^{-1}s^{-2}"/> is the gravitational constant</li>
            </ul>
        </p>
        <p>
            Hence, if we consider a system of <MathInline formula = "n"/> bodies which interact <b>solely</b> via gravitational force, 
            we can determine the net force exerted on some body <MathInline formula = "i"/> using:
            <MathBlock formula = "\vec{F}_{i} = \sum_{j = 1, j \neq i}^n \vec{F}_{ij}"/>
        </p> 
        <p>
            So how does this help? We didn't show Newton's Second Law because it looks nice, its actually useful! 
            Solving the N Body Problem ultimately reduces to taking a set of <MathInline formula = "n"/> bodies 
            with some initial conditions (their positions, velocities and masses), 
            and then finding how these positions vary across time. And how do physicists and mathematicians finds positions of stuff in time? 
            They define <b>differential equations</b>! So now you might be wondering: where is this differential equation? 
            If <MathInline formula = "\vec{r}_i(t)"/> is the position of the <MathInline formula = "i"/>th body in time, 
            then notice we can rewrite Newton's Second Law as:
            <MathBlock formula = "\vec{F}_i = m_i\ddot{\vec{r}}_i"/>
            since acceleration is nothing but the second derivative of position with respect to time. 
            In other words, for a given body, we need to solve:
            <MathBlock formula = "-G\sum_{j = 1, j \neq i}^n \frac{m_im_j}{\|\vec{r_i} - \vec{r_j}\|^3}(\vec{r}_i - \vec{r}_j) = m_i\ddot{\vec{r}}_i \ \implies \ -G\sum_{j = 1, j \neq i}^n \frac{m_j}{\|\vec{r_i} - \vec{r_j}\|^3}(\vec{r}_i - \vec{r}_j) = \ddot{\vec{r}}_i"/>
            This is actually encoding 3 differential equations, one for each spatial dimension. 
            Since there are <MathInline formula = "n"/> total bodies, this means that 
            to solve the N Body Problem, we <b>just</b> need to solve a system of <MathInline formula = "3n"/> second-order 
            differential equations involving a measly <MathInline formula = "n"/> variables. Piece of cake ...
        </p>

        <h3>3-Step Leapfrog</h3>

        <p>
            So, spoiler alert, unless <MathInline formula = "n = 2"/>, the above system can't be 
            solved analytically (or at least no one has been smart enough to do so). 
            So what do frustrated scientists do when they get faced with a problem that has no apparent solution? Simplification! 
            In this case, we can resort to use a <b>numerical integrator</b> which 
            won't care about the number of variables or the number of equations (although your computer will).
        </p>
        <p>
            Now we want to use a numerical method. Can we directly apply it to our second-order set of differential equations? 
            I mean I guess you can try. Its much easier to convert each second-order differential equation 
            into a system of first-order differential equations. Since first-order differential equations 
            can be solved easily by plethora of numerical methods, this is much simpler. So what does this system look like? 
            Consider this: if we have acceleration, we can integrate numerically to get velocity; 
            if we have velocity, we can integrate numerically to get position, and this is what we want! 
            In particular, for some body <MathInline formula = "i"/>, we have to solve:
            <MathBlock formula = "\ddot{\vec{r}}_i = f(t, \dot{\vec{r}}_i)"/>
            <MathBlock formula = "\dot{\vec{r}}_i = f(t, \vec{r}_i)"/>
        </p>
        <p>
            Right now this is quite abstract, so lets go to <i>how</i> we will integrate. We use the <b>3-Step Leapfrog Method</b>. 
            Letting <MathInline formula = "\vec{v}_i(t) = \dot{\vec{r}}_i(t), \ \vec{a}_i(t) = \ddot{\vec{r}}_i(t)"/>, we know that 
            <MathBlock formula = "\vec{a}_i(t) = \ddot{\vec{r}}_i(t) = -G\sum_{j = 1, j \neq i}^n \frac{m_j}{\|\vec{r_i}(t) - \vec{r_j}(t)\|^3}(\vec{r}_i(t) - \vec{r}_j(t))"/>
            The numerical method is defined recursively in 3 steps:
            <MathBlock formula = "\vec{v}_i\left(t + \frac{1}{2}\right) = \vec{v}_i\left(t\right) + \frac{h}{2}\vec{a}_i(t)"/>
            <MathBlock formula = "\vec{r}_i(t+1) = \vec{r}_i(t) + h\vec{v}_i\left(t + \frac{1}{2}\right)"/>
            <MathBlock formula = "\vec{v}_i\left(t + 1\right) = \vec{v}_i\left(t + \frac{1}{2}\right) + \frac{h}{2}\vec{a}_i(t+1)"/>
            where we can exploit the fact that <MathInline formula = "\vec{a}_i(t)"/> depends <b>solely</b> on the 
            position of the body at time <MathInline formula = "t"/>, <MathInline formula = "\vec{r}_i(t)"/>.
            Hence, once we compute <MathInline formula = "\vec{r}_i(t+1)"/>, we need to 
            compute <MathInline formula = "\vec{a}_i(t+1)"/> for the final step. 
            This can be quite computationally expensive, particularly with many bodies, 
            so it is recommendable that we store the acceleration computed, since we can reuse it in the next step.
        </p>
        <p>
            After all this, you might be wondering: given 
            that <MathInline formula = "\texttt{scipy}"/> and <MathInline formula = "\texttt{odeint}"/> exist, 
            why bother with complicated recursion and save-acceleration-for-the-next-step nonsense? To put it simply:
            <ol>
                <li>It's always fun to implement your own functionality</li>
                <li>Its a second-order method, so global error varies 
                    with the square of the time step, <MathInline formula = "h^2"/>. 
                    This makes this method more accurate than others, like Euler's Method.</li>
                <li>If you are attempting to simulate a physical system, 
                    a slightly important aspect to consider is whether your simulation actually adheres to the laws of physics.
                    As Dwight Schrute would say: <b>Fact</b>: 3-Step Leapfrog 
                    is symplectic; <b>Fact</b>: <MathInline formula = "\texttt{odeint}"/> isn't. Why does simplecticity matter? 
                    For this particular application, it matters because it ensures that the energy, linear momentum and angular momentum
                     of the system are conserved (to some tolerance).
                </li>
                <li>
                    As an added bonus, this scheme is also <b>time-reversible</b>: we can find position 
                    at <MathInline formula = "t+1"/> from the position at <MathInline formula = "t"/>, 
                    but we can also find the position at <MathInline formula = "t"/> from the 
                    position at <MathInline formula = "t+1"/>. In fact, 
                    it is this time-reversibility that ensures energy conservation (thank you Frau Noether). 
                    Time-reversibility is desirable, because it makes the integrator more stable and robust 
                    in the long term, which is very important when considering periodic orbits which 
                    oscillate for a long time. Methods like Runge-Kutta 4 don't have this nice property, 
                    although they are higher order (so more accurate).
                </li>
            </ol>
        </p>
        <h3>Defining the Conservation Laws</h3>

        <h3>Adaptive Time Step</h3>
    </div>
    );
}

export default Math;