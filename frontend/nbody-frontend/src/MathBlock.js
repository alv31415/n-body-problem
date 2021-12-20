import React from "react";
import MathJax from 'react-mathjax';

function MathBlock(props) {
    
    return (
            <MathJax.Provider>
                <MathJax.Node formula={props.formula} />
            </MathJax.Provider>
    );

}

export default MathBlock;