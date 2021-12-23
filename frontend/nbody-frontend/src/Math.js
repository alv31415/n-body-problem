import React from "react";

import dwight from "./imgs/its-true-its-a-fact.gif";
import sweat from "./imgs/sweat.gif";
import leapfrog3 from "./imgs/leapfrog3.png";
import facepalm from "./imgs/facepalm.gif";
import MathJax from "react-mathjax";

function Math() {
    return (
    <div id = "math" style={{padding: 50}}>
        <MathJax.Provider>
        <h2>The Math</h2>
        <p>We now consider the mathematical formulation of the N Body Problem, 
        alongside the recursion which defines the integrator, and how the adaptive time step is computed.</p>
        <h3>Defining the N Body Problem</h3>
        <p>
            The N Body Problem refers to the computation of the orbits 
            of <MathJax.Node inline formula = "n"/> bodies, which interact solely via gravitational forces.
            To do this, we recall 2 key laws of physics.
        </p>
        <p>
           <b>Newton's Second Law of Motion</b> relates the net force exerted on a body with its acceleration:
            <MathJax.Node formula = "\sum \vec{F} = m\vec{a}"/>
        </p>
        <p>
            <b>Newton's Universal Law of Gravitation</b> states that the magnitude of the gravitational force 
            between 2 bodies is inversely proportional to the square of the distance between the 2 bodies. 
            In particular, the gravitational force exerted by some body <MathJax.Node inline formula = "j"/> on another 
            body <MathJax.Node inline formula = "i"/> can be described by:
            <MathJax.Node formula = "\vec{F}_{ij} = -G\frac{m_im_j}{\|\vec{r_i} - \vec{r_j}\|^3}(\vec{r}_i - \vec{r}_j)"/>
            where:
        </p>
        <ul>
            <li><MathJax.Node inline formula = "m_i, m_j"/> are the masses of the 2 bodies</li>
            <li><MathJax.Node inline formula = "\vec{r}_i, \vec{r}_j"/> are the position vectors of the 2 bodies</li>
            <li><MathJax.Node inline formula = "G = 6.67408 \times 10^{-11}m^3kg^{-1}s^{-2}"/> is the gravitational constant</li>
        </ul>
        <p>
            Hence, if we consider a system of <MathJax.Node inline formula = "n"/> bodies which interact <b>solely</b> via gravitational force, 
            we can determine the net force exerted on some body <MathJax.Node inline formula = "i"/> using:
            <MathJax.Node formula = "\vec{F}_{i} = \sum_{j = 1, j \neq i}^n \vec{F}_{ij}"/>
        </p> 
        <p>
            So how does this help? We didn't show Newton's Second Law because it looks nice, its actually useful! 
            Solving the N Body Problem ultimately reduces to taking a set of <MathJax.Node inline formula = "n"/> bodies 
            with some initial conditions (their positions, velocities and masses), 
            and then finding how these positions vary across time. And how do physicists and mathematicians finds positions of stuff in time? 
            They define <b>differential equations</b>! So now you might be wondering: where is this differential equation? 
            If <MathJax.Node inline formula = "\vec{r}_i(t)"/> is the position of the <MathJax.Node inline formula = "i"/>th body in time, 
            then notice we can rewrite Newton's Second Law as:
            <MathJax.Node formula = "\vec{F}_i = m_i\ddot{\vec{r}}_i"/>
            since acceleration is nothing but the second derivative of position with respect to time. 
            In other words, for a given body, we need to solve:
            <MathJax.Node formula = "-G\sum_{j = 1, j \neq i}^n \frac{m_im_j}{\|\vec{r_i} - \vec{r_j}\|^3}(\vec{r}_i - \vec{r}_j) = m_i\ddot{\vec{r}}_i \ \implies \ -G\sum_{j = 1, j \neq i}^n \frac{m_j}{\|\vec{r_i} - \vec{r_j}\|^3}(\vec{r}_i - \vec{r}_j) = \ddot{\vec{r}}_i"/>
            This is actually encoding 3 differential equations, one for each spatial dimension. 
            Since there are <MathJax.Node inline formula = "n"/> total bodies, this means that 
            to solve the N Body Problem, we <b>just</b> need to solve a system of <MathJax.Node inline formula = "3n"/> second-order 
            differential equations involving a measly <MathJax.Node inline formula = "n"/> variables. Piece of cake ...
            <img src = {sweat} 
                 className = "img" 
                 alt  = "Severe Sweating, taken from https://tenor.com/es/ver/sweating-intense-sweating-nervous-anxious-waiting-gif-15207841"/>
        </p>

        <h3>3-Step Leapfrog</h3>

        <p>
            So, spoiler alert, unless <MathJax.Node inline formula = "n = 2"/>, the above system can't be 
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
            In particular, for some body <MathJax.Node inline formula = "i"/>, we have to solve:
            <MathJax.Node formula = "\ddot{\vec{r}}_i = f(t, \dot{\vec{r}}_i)"/>
            <MathJax.Node formula = "\dot{\vec{r}}_i = f(t, \vec{r}_i)"/>
        </p>
        <p>
            Right now this is quite abstract, so lets go to <i>how</i> we will integrate. We use the <b>3-Step Leapfrog Method</b>. 
            Letting <MathJax.Node inline formula = "\vec{v}_i(t) = \dot{\vec{r}}_i(t), \ \vec{a}_i(t) = \ddot{\vec{r}}_i(t)"/>, we know that 
            <MathJax.Node formula = "\vec{a}_i(t) = \ddot{\vec{r}}_i(t) = -G\sum_{j = 1, j \neq i}^n \frac{m_j}{\|\vec{r_i}(t) - \vec{r_j}(t)\|^3}(\vec{r}_i(t) - \vec{r}_j(t))"/>
            The numerical method is defined recursively in 3 steps:
            <MathJax.Node formula = "\vec{v}_i\left(t + \frac{1}{2}\right) = \vec{v}_i\left(t\right) + \frac{h}{2}\vec{a}_i(t)"/>
            <MathJax.Node formula = "\vec{r}_i(t+1) = \vec{r}_i(t) + h\vec{v}_i\left(t + \frac{1}{2}\right)"/>
            <MathJax.Node formula = "\vec{v}_i\left(t + 1\right) = \vec{v}_i\left(t + \frac{1}{2}\right) + \frac{h}{2}\vec{a}_i(t+1)"/>
            where we can exploit the fact that <MathJax.Node inline formula = "\vec{a}_i(t)"/> depends <b>solely</b> on the 
            position of the body at time <MathJax.Node inline formula = "t"/>, <MathJax.Node inline formula = "\vec{r}_i(t)"/>.
            Hence, once we compute <MathJax.Node inline formula = "\vec{r}_i(t+1)"/>, we need to 
            compute <MathJax.Node inline formula = "\vec{a}_i(t+1)"/> for the final step. 
            This can be quite computationally expensive, particularly with many bodies, 
            so it is recommendable that we store the acceleration computed, since we can reuse it in the next step.

            <img src = {leapfrog3} 
                 className = "img" 
                 alt  = "Leapfrog Description, taken from https://www.researchgate.net/figure/Leap-Frog-time-integration-scheme_fig1_325968284"/>

        </p>
        <p>
            After all this, you might be wondering: given 
            that <MathJax.Node inline formula = "\texttt{scipy}"/> and <MathJax.Node inline formula = "\texttt{odeint}"/> exist, 
            why bother with complicated recursion and save-acceleration-for-the-next-step nonsense? To put it simply:
        </p>
        <ol>
            <li>It's always fun to implement your own functionality</li>
            <li>Its a second-order method, so global error varies 
                with the square of the time step, <MathJax.Node inline formula = "h^2"/>. 
                This makes this method more accurate than others, like Euler's Method.</li>
            <li>If you are attempting to simulate a physical system, 
                a slightly important aspect to consider is whether your simulation actually adheres to the laws of physics.
                As Dwight Schrute would say: <b>Fact</b>: 3-Step Leapfrog 
                is symplectic; <b>Fact</b>: <MathJax.Node inline formula = "\texttt{odeint}"/> isn't. Why does simplecticity matter? 
                For this particular application, it matters because it ensures that the energy, linear momentum and angular momentum
                    of the system are conserved (to some tolerance).
            </li>
            <img src = {dwight} 
                    className = "img" 
                    alt  = "Dwight Schrute, taken from https://tenor.com/es/ver/its-true-its-a-fact-truth-dwight-schrute-gif-14348403"/>
            <li>
                As an added bonus, this scheme is also <b>time-reversible</b>: we can find position 
                at <MathJax.Node inline formula = "t+1"/> from the position at <MathJax.Node inline formula = "t"/>, 
                but we can also find the position at <MathJax.Node inline formula = "t"/> from the 
                position at <MathJax.Node inline formula = "t+1"/>. This is a consequence of the symmetry in the recursion of the Leapfrog scheme.
                In fact, it is this time-reversibility that ensures energy conservation (thank you Frau Noether). 
                Time-reversibility is desirable, because it makes the integrator more stable and robust 
                in the long term, which is very important when considering periodic orbits which 
                oscillate for a long time. Methods like Runge-Kutta 4 don't have this nice property, 
                although they are higher order (so more accurate).
            </li>
        </ol>
        <h3>Adaptive Time Step</h3>
        <p>
            So we have differential equations. We have a way to solve them. Are we done? Yes, but actually no. 
            You could go and implement this right now, and you'll soon find that chaotic systems are named thus 
            for reasons beyond mathematicians enjoying the use of cool sounding names to describe weird phenomena. More often than not, for a set of random initial conditions, 
            you'll find that bodies either crash, or escape, or gain hundreds of Joules out of nowhere. There are 2 reasons for this:
        </p>
            <ul>
                <li>2 bodies in the simulation came too close together. Since acceleration is proportional 
                    to <MathJax.Node inline formula = "\frac{1}{\|\vec{r}_i - \vec{r}_j\|^3}"/>, if bodies get too close together, 
                    they basically accelerate infinitely, which our numerical integration scheme won't enjoy.
                </li>
                <li>a body is moving extremely fast. If this happens, then it is likely that upon integrating, 
                    it's position will change too much, taking the body out of the system (when it shouldn't)
                </li>
            </ul>
        <p>
            The cause for both of these, beyond the intricacies of the system is simple: 
            the step size, <MathJax.Node inline formula = "h"/>. This controls the accuracy of the integrator, 
            but it is flawed in the sense that we are modelling a highly dynamic system using fixed length steps. 
            This is counterproductive, since there are situations in which we might require a smaller step size 
            (for example, if a body is moving extremely fast, we might need a more accurate integrator to handle the high variability), 
            or a bigger step size (this is always nice, since it reduces the amount of computations).
            Because of this, we implemented a <b>variable/adaptive time step</b>.
        </p>
        <p>
            The idea is simple: make the time step small when bodies get too close together, 
            or when they move at high speeds, and make it larger if the system is not doing anything too crazy. 
            If we compute this adaptive time step at each time <MathJax.Node inline formula = "t"/>, we will be able to improve the performance of the integrator.
            A simple example of this is given by:
            <MathJax.Node formula = "h^*(t) = c \times \underset{1 \leq i < j \leq n}{\min}\left\{\frac{\Delta x_{ij}(t)}{\Delta v_{ij}(t)}\right\}"/>
            where at time <MathJax.Node inline formula = "t"/>:
        </p>
        <ul>
            <li>
                <MathJax.Node inline formula = "c"/> is a proportionality constant used to modulate the size of the time step
            </li>
            <li>
                <MathJax.Node inline formula = "\Delta x_{ij}(t) = \|\vec{r}_i(t) - \vec{r}_j(t)\|"/>, the distance between 2 bodies
            </li>
            <li>
                <MathJax.Node inline formula = "\Delta v_{ij}(t) = \|\vec{v}_i(t) - \vec{v}_j(t)\|"/>, the magnitude of the difference 
                in the velocities of 2 bodies
            </li>
        </ul>
        <p>
            Okay, so surely we are done now, right? Yes, but again, also no. 
            We could run this, and see that this time we observe less crashes or escapes,
            but we might notice that energy errors creep up. What is happenining is that, 
            since the time step is changing, we are breaking the time symmetry of the scheme: 
            we can't guarantee that moving forward in time leads to the same time step as moving backwards in time. 
            Great, so to solve a problem we are generating more problems!
            <img src = {facepalm} 
                 className = "img" 
                 alt  = "Face Palm, taken from https://tenor.com/view/disappointed-face-palm-seriously-exasperated-gif-7304550"/>
        </p>
        <p>
            Admittedly, this is all too dramatic, since the fix is as simple as taking the average. 
            Indeed, our <i>actual</i> adaptive time step can be made time symmetric by using:
            <MathJax.Node formula = "h(t) = \frac{h^*(t) + h^*(t+1)}{2}"/>
            With this, we get all the ebenfits of a time-symmetric integrator, whilst being able to adapt 
            our integration based on how the system is behaving. Admittedly, computing <MathJax.Node inline formula = "h(t)"/> is quite 
            involved since to perform a single integration step we need to:
        </p>
        <ol>
            <li>
                Compute <MathJax.Node inline formula = "h^*(t)"/> in the current system.
            </li>
            <li>
                Perform a (false) integration step using <MathJax.Node inline formula = "h^*(t)"/>.
            </li>
            <li>
                From the resulting system, we can compute <MathJax.Node inline formula = "h^*(t+1)"/>.
            </li>
            <li>
                Compute <MathJax.Node inline formula = "h(t) = \frac{h^*(t) + h^*(t+1)}{2}"/>.
            </li>
            <li>
                Use <MathJax.Node inline formula = "h(t)"/> to perform the actual integration step in the current system.
            </li>
        </ol>
        <p>
        However, this is well worth it, since you obtain a powerful integration scheme, which can easily integrate 
        most initial conditions, provided you modulate <MathJax.Node inline formula = "c"/> appropriately.
        </p>
        </MathJax.Provider>
    </div>
    );
}

export default Math;