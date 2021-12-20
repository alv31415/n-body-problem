// based on https://www.youtube.com/watch?v=Xz2Z8xKH-R0

import React, {useState, useEffect} from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faArrowAltCircleUp } from "@fortawesome/free-solid-svg-icons";
  
const ScrollButton = () =>{
  
  const [visible, setVisible] = useState(false)
  
  const toggleVisible = () => {
    const scrolled = window.pageYOffset;
    if (scrolled > 300){
      setVisible(true)
    } 
    else if (scrolled <= 300){
      setVisible(false)
    }
  };
  
  const scrollToTop = () =>{
    window.scrollTo({
      top: 0, 
      behavior: "smooth"
    });
  };

  useEffect(() => {
      window.addEventListener("scroll", toggleVisible);

      return () => {
          window.removeEventListener("scroll", toggleVisible)
      }
  }, []
  );
  
  window.addEventListener("scroll", toggleVisible);
  
  return (
      <button type = "button" className = "scroll-button fa-fw" onClick={scrollToTop} 
      style={{display: visible ? 'inline' : 'none'}}>
        <FontAwesomeIcon icon = {faArrowAltCircleUp}/>
      </button>
    
  );
}
  
export default ScrollButton;