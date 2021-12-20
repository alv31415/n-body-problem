import React from "react";
import ImgLink from './ImgLink';
import { faGithub } from "@fortawesome/free-brands-svg-icons";
import { faFileAlt } from "@fortawesome/free-solid-svg-icons";

function SocialLinks() {
    return (
        <div className="row-icons">
          <ImgLink icon = {faGithub} 
                  className = "img-link fa-fw" 
                  link = "https://github.com/alv31415/n-body-problem/tree/website"/>
          <ImgLink icon = {faFileAlt} 
                  className = "img-link fa-fw" 
                  link = "https://alv31415.github.io/n-body-problem/n-body-report.pdf"/>
        </div>
    );
}

export default SocialLinks;