import React from "react";
import FormBlock from "./FormBlock";
import Plot from "react-plotly.js";
import {getCookie, POST_INTEGRATOR_UPDATE_URL} from "./reqResources";

class OrbitPlotter extends React.Component {
    constructor(props) {
        super(props);
        this.orbits = [];
        console.log(this.props.integratorIDs);

        // https://learnui.design/tools/data-color-picker.html#divergent
        this.colours = ["#00876c",
                        "#3d9a70",
                        "#64ad73",
                        "#89bf77",
                        "#afd17c",
                        "#d6e184",
                        "#fff18f",
                        "#fdd576",
                        "#fbb862",
                        "#f59b56",
                        "#ee7d4f",
                        "#e35e4e",
                        "#d43d51"]
        this.state = {
            btnLabel: "Plot!",
            orbitSize: 0,
            integratorID: this.props.integratorIDs[0],
            integratorIDChanged: false,
            data: [{x: [0], 
                    y: [0], 
                    type: "line",
                    mode: "lines"}],
            layout: {
                dragmode: "pan", 
                width: 500, 
                height: 500, 
                plot_bgcolor: "black",
                paper_bgcolor: "black",
                yaxis: {
                    title: {
                        text: "y"
                    },
                    color: "white",
                    gridcolor: "grey"
                },
                xaxis: {
                    title: {
                        text: "x"
                    },
                    color: "white",
                    gridcolor: "grey"
                },
                legend: {
                    font: {
                      //family: 'sans-serif',
                      size: 12,
                      color: "white"
                    }
            }
        }
        };

        this.handleChange = this.handleChange.bind(this);
        this.updatePlot = this.updatePlot.bind(this);
    }

    handleChange(e){
        const newIntegratorID = e.target.value;
        this.setState({...this.state, integratorID: newIntegratorID, integratorIDChanged: true})
    }

    /**
     * Computes the orbits using the current integrator.
     */
    async getOrbits() {

        if (this.state.integratorIDChanged === false && this.state.orbitSize !== 0) {

            return ;
        }

        const postUrl = POST_INTEGRATOR_UPDATE_URL + this.state.integratorID;
    
        var csrfToken = getCookie("csrftoken");
    
        const reqBody = {
            method: "POST",
            headers: {
                "Content-Type" : "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify({})
        };

        const response = await fetch(postUrl, reqBody);

        if (response.ok) {
            const data = await response.json();
            const newPositions = data.position_orbits;

            let orbitSize = newPositions[0].length;

            this.setState({ ...this.state, orbitSize: orbitSize });
            this.orbits = newPositions;
        }
        else {
            alert(`There was a problem when computing the orbits : ${response.statusText}`);
        }
    
    }

    getOrbitColour(i) {
        let nOrbits = this.orbits.length;
        let step = Math.floor((this.colours.length - 1) / (nOrbits - 1));
        
        return this.colours[step * i];
    }
    
    /**
     * Given the positions (as an array of arrays) of a body in the simulation, generates a list of 2 objects.
     * The first one represents the actual orbits of the body in the xy plane.
     * The second one represents the ending point of the orbit.
     * These objects are used by Plotly to plot the orbits
     * @param {*} positions positions of the body, an array of [x,y,z] coordinates
     * @param {*} bodyNumber the body within the ismulation
     * @returns a list of 2 objects, representing the motion of the body associated witht he bodyNumber
     */
    setPlot(positions, bodyNumber) {

        let orbitX = [];
        let orbitY = [];
        let orbitColour = this.getOrbitColour(bodyNumber);
    
        let x, y, z;

        for (let i = 0; i < this.state.orbitSize; i++) {
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
                mode: 'lines',
                name: `Orbit ${parseInt(bodyNumber) + 1}`,
                line : {
                    color: orbitColour
                }
            },
            {
                x: [orbitX[orbitX.length - 1]],
                y: [orbitY[orbitY.length - 1]],
                type: 'scatter',
                mode: 'marker',
                name: `Orbit ${parseInt(bodyNumber) + 1}`,
                showlegend: false,
                marker : {
                    size: 10,
                    color: orbitColour
                }
            }
            ]
        )
    
    }

    updatePlot(orbits) {

        let lineData = [];

        let line, dot;
        for (let i in orbits) {
            [line, dot] = this.setPlot(orbits[i], i);
            lineData.push(line);
            lineData.push(dot);
        }

        

        this.setState((state) => {
                        return ({...state, 
                        data: lineData,
                        integratorIDChanged: false
                    })
                });
    }

    plotOrbits() {
        this.getOrbits();
        setTimeout(() => this.updatePlot(this.orbits), 500);
    }

    render() {

        return (
            <div className="bg-form-plot">
                <h2>Plot Simulation</h2>
                <Plot data = {this.state.data} 
                      layout = {this.state.layout} 
                      config={{scrollZoom: true}}
                      useResizeHandler={true}/>
                <br/>
                <FormBlock hoverLabel = "The integrator to use for plotting."
                           labelName = "Integrator ID" 
                           name = "integratorID" 
                           type = "select" 
                           value = {this.state.integratorID} 
                           data_list = {this.props.integratorIDs} 
                           onChange = {this.handleChange}/>
                <button className = "button" onClick = {() => this.plotOrbits(this.state.integratorID)}>{this.state.btnLabel}</button>
            </div>
        );
    }


}

export default OrbitPlotter;

