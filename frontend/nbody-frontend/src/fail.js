async function getOrbits() {
    const postUrl = "http://localhost:8000/api/integrator-update/" + this.state.integratorID;

    var csrfToken = this.getCookie("csrftoken");

    const reqBody = {
        method: "POST",
        headers: {
            "Content-Type" : "application/json",
            "X-CSRFToken": csrfToken
        },
        body: JSON.stringify({})
    };

    try {
        const response = await fetch(postUrl, reqBody)
        const data = await response.json();
        
        if (response.ok) {
            const newPositions = data.position_orbits
            return newPositions;
        }
    } 
    catch (e) {
        console.error("Error occurred during POST request", e)
    }     

}

function setPlot(positions) {
    let orbitX = [];
    let orbitY = [];

    let x, y, z;

    for (let i = 0; i < positions.length; i++) {
        [x, y, z] = positions[i];
        orbitX.push(x);
        orbitY.push(y)
    }

    return (
        [
        {
            x: orbitX,
            y: orbitY,
            type: 'line',
            mode: 'lines'
        },
        {
            x: [orbitX[orbitX.length - 1]],
            y: [orbitY[orbitY.length - 1]],
            type: 'scatter',
            mode: 'marker',
            marker: {size: 10}
        }
        ]
    )

}

 function drawOrbits() {
    this.getOrbits().then((orbits) => {
        let lineData = [];

        let line, dot;
        for (let i in orbits) {
            [line, dot] = this.setPlot(orbits[i]);
            lineData.push(line);
            lineData.push(dot);
        }

        this.setState({...this.state, 
                        data: lineData, 
                        layout: {...this.state.layout, datarevision: this.state.layout.datarevision + 1},
                        revision: this.state.revision + 1
                    });
    });
    
}

//<Plot data = {this.state.data} layout = {this.state.layout} revision={this.state.revision} graphDiv="orbit-plotter"/>

/*
<Plot
                    data={[
                    {
                        x: [1,2,3],
                        y: [1,2,3],
                        type: 'line',
                        mode: 'lines'
                    },
                    {
                        x: [3],
                        y: [3],
                        type: 'scatter',
                        mode: 'marker',
                        marker: {size: 10}
                    }
                    ]}
                    layout={{width: 320, 
                            height: 320, 
                            plot_bgcolor:"black",
                            yaxis: {
                                title: {
                                    text: "y"
                                }
                            },
                            xaxis: {
                                title: {
                                    text: "x"
                                }
                            }}}/>
                            */