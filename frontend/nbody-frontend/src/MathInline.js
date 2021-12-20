import React from "react";
import MathJax from 'react-mathjax';

function MathInline(props) {
    
    return (
            <MathJax.Provider>
                <MathJax.Node inline formula={props.formula} />
            </MathJax.Provider>
    );

}

export default MathInline;