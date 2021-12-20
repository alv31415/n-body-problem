import React from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

import { faGithub } from "@fortawesome/free-brands-svg-icons";
import { faFileAlt } from "@fortawesome/free-solid-svg-icons";

function About({ aboutRef }) {

    return (
        <div ref = {aboutRef} style={{padding: 50}}>
                <h2>About</h2>
                <p>
                    This project was developed following my completion of 
                    the  <a className = "link-inline" 
                            href = "https://teaching.maths.ed.ac.uk/main/undergraduate/opportunities/vacation-scholarships">University of
                            Edinburgh School of Mathematics 2021 Summer Vacation Scholarship</a>. 
                    Under the supervision 
                    of <a className = "link-inline" href = "https://www.maths.ed.ac.uk/~mruffert/">Dr. Maximilian Ruffert</a>, I 
                    investigated the stability of the Figure of 8 configuration of the 3-Body Problem 
                    (you can check my report here <a href="https://alv31415.github.io/n-body-problem/n-body-report.pdf"
                        target = "_blank" rel = "noreferrer" className = "img-link fa-fw link-inline">
                        <FontAwesomeIcon icon={faFileAlt}/></a>).
                    This was done in Python 
                    (you can check the code here <a href="https://github.com/alv31415/n-body-problem/tree/website"
                        target = "_blank" rel = "noreferrer" className = "img-link fa-fw link-inline">
                        <FontAwesomeIcon icon={faGithub}/></a>), and was entirely numerical 
                    (although some algebraic analysis was used to derive certain initial conditions).</p>
                <p>
                    The point is, in doing this investigation, I had to do a lot of research with regards to the n body problem, 
                    and it was hard for me to find "easy to follow" resources. 
                    The objective of this site is to hopefully make it easy to understand the intricacies of the n body problem, 
                    by providing both the mathematical background of the problem, and the plots resulting from running the simulations.
                </p>
        </div>
    );
}

export default About;
