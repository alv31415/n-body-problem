import React from "react";
import FormBlock from "./FormBlock";
import Plot from "react-plotly.js"

class OrbitPlotter extends React.Component {
    constructor(props) {
        super(props);
        this.orbits = [];

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
                        "#d43d51]"]
        this.state = {
            btnLabel: "Plot!",
            integratorID: this.props.integratorID,
            integratorIDs: [],
            orbitSize: 0,
            data: [{x: [0], 
                    y: [0], 
                    type: "line",
                    mode: "lines"}],
            layout: {
                dragmode: "pan", 
                width: 640, 
                height: 640, 
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
                }}
        };

        this.handleChange = this.handleChange.bind(this);
        this.getIntegratorIDs = this.getIntegratorIDs.bind(this);
        this.updatePlot = this.updatePlot.bind(this);
    }

    getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    handleChange(e){
        const newIntegratorID = e.target.value;
        this.setState({...this.state, integratorID: newIntegratorID})
    }

    /**
     * Gets the IDs of all integrators in the database
     */
    async getIntegratorIDs() {
        const getUrl = "http://localhost:8000/api/integrator-list-ids/"

        try {
            const response = await fetch(getUrl, {method: "GET"});
            const data = await response.json();
            data.sort();
            
            if (response.ok) {
                this.setState({...this.state, integratorIDs: data, integratorID: data[0]});
            }
        } 
        catch (e) {
            console.error("Error occurred during GET request", e)
        }     
    }

    /**
     * Computes the orbits using the current integrator.
     */
    async getOrbits(integratorID) {

        if (integratorID === this.state.integratorID && this.state.orbitSize !== 0) {

            return ;
        }

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

                let orbitSize = newPositions[0].length;

                this.setState({ ...this.state, orbitSize: orbitSize });
                this.orbits = newPositions;
            }
        } 
        catch (e) {
            console.error("Error occurred during POST request", e)
        }     
    
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
                name: `Orbit ${parseInt(bodyNumber) + 1}`
            },
            {
                x: [orbitX[orbitX.length - 1]],
                y: [orbitY[orbitY.length - 1]],
                type: 'scatter',
                mode: 'marker',
                marker: {size: 10},
                showlegend: false
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
                        data: lineData
                    })
                });
    }

    plotOrbits(integratorID) {
        this.getOrbits(integratorID);
        setTimeout(() => this.updatePlot(this.orbits), 500);
    }

    componentDidMount() {
        this.getIntegratorIDs()
    }

    render() {

        return (
            <div>
                <Plot data = {this.state.data} 
                      layout = {this.state.layout} 
                      config={{scrollZoom:true}}
                      useResizeHandler={true}/>;
                <br/>
                <FormBlock labelName = "Integrator ID" name = "integratorID" type = "select" value = {this.state.integratorIDs[0]} data_list = {this.state.integratorIDs} onChange = {this.handleChange}/>
                <br/>
                <button onClick = {() => this.plotOrbits(this.state.integratorID)}>{this.state.btnLabel}</button>
            </div>
        )
    }


}

export default OrbitPlotter;

