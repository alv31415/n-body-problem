import React from "react";
import FormBlock from "./FormBlock";
import Plot from "react-plotly.js"
import isEqual from "lodash/isEqual";

class OrbitPlotter extends React.Component {
    constructor(props) {
        super(props);
        this.orbits = [];
        this.state = {
            simOn: false,
            btnLabel: "Start",
            integratorID: this.props.integratorID,
            integratorIDs: [],
            orbitIndex: 1,
            orbitIndexIncrease: 1,
            continuePlot: true,
            orbitSize: 0,
            data: [{x: [1], 
                    y: [1], 
                    type: 'line',
                    mode: 'lines'}],
            layout: {datarevision: 0,
                width: 320, 
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
                }},
            revision: 0
        };

        this.handleClick = this.handleClick.bind(this);
        this.handleChange = this.handleChange.bind(this);
        this.getIntegratorIDs = this.getIntegratorIDs.bind(this);
        this.updateData = this.updateData.bind(this);
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

    handleClick() {
        const newSimOn = !this.state.simOn
        this.setState({...this.state, simOn: newSimOn, btnLabel: newSimOn ? "Stop" : "Start"});
    }

    async getIntegratorIDs() {
        const getUrl = "http://localhost:8000/api/integrator-list-ids/"

        try {
            const response = await fetch(getUrl, {method: "GET"});
            const data = await response.json();
            data.sort();
            console.log(data);
            
            if (response.ok) {
                this.setState({...this.state, integratorIDs: data, integratorID: data[0]});
            }
        } 
        catch (e) {
            console.error("Error occurred during GET request", e)
        }     
    }

    updateData() {
        const x = Math.floor(Math.random() * 10);
        const y = Math.floor(Math.random() * 10);
        let newData = this.state.data.slice(0);
        
        let newX = newData[0].x;
        let newY = newData[0].y;
        newX.push(x);
        newY.push(y);
        const data = [{...newData[0], x: newX, y:newY, name: "Orbit"}, {x: [newX[newX.length - 1]], y: [newY[newY.length - 1]], showlegend: false, type: 'marker',
        mode: 'markers', marker: {size: 10, color: "red"}}]

        this.setState({...this.state, data: data, revision: this.state.revision + 1, layout: {...this.state.layout, datarevision: this.state.revision + 1}});

    }

    async getOrbits() {

        console.log("Getting orbits")

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

                for (let i in newPositions) {
                    console.log(`${newPositions[i].length} positions calculated`)
                }

                let orbitSize = newPositions[0].length;

                console.log("Setting orbits")

                this.setState({ ...this.state, orbitSize: orbitSize });
                this.orbits = newPositions;

                console.log("Done")

                console.log(this.state.orbitSize)
                console.log(orbitSize)
                console.log(this.orbits)
                console.log(newPositions)
            }
        } 
        catch (e) {
            console.error("Error occurred during POST request", e)
        }     
    
    }
    
    setPlot(positions, bodyNumber) {

        let orbitX = [];
        let orbitY = [];
    
        let x, y, z;
    
        for (let i = 0; i < this.state.orbitIndex; i++) {
            [x, y, z] = positions[i];
            orbitX.push(x);
            orbitY.push(y)
        }

        if (orbitX.length > 100 && orbitY.length > 100) {
            let excess = orbitX.length - 100;
            orbitX.splice(0, excess);
            orbitY.splice(0, excess);
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
                        orbitIndex: state.orbitIndex + state.orbitIndexIncrease,
                        data: lineData, 
                        layout: {...state.layout, datarevision: state.layout.datarevision + 1},
                        revision: state.revision + 1
                    })
                });
        console.log(this.state.revision);
    }

    componentDidMount(){
        this.getIntegratorIDs()
    }

    componentDidUpdate() {
        console.log("Orbit Index", this.state.orbitIndex);
        console.log("Orbit Size", this.state.orbitSize);
        console.log("Component should update", this.state.orbitIndex < this.state.orbitSize)
        if (this.state.orbitIndex < this.state.orbitSize) {
            console.log("Updating plot")
            setTimeout(this.updatePlot, 1000);
        }
    }

    render() {

        return (
            <div>
                <Plot data = {this.state.data} layout = {this.state.layout}/>
                <br/>
                <FormBlock labelName = "Integrator ID" name = "integratorID" type = "select" value = {this.state.integratorIDs[0]} data_list = {this.state.integratorIDs} onChange = {this.handleChange}/>
                <br/>
                <button onClick = {() => this.getOrbits()}>{this.state.btnLabel}</button>
            </div>
        )
    }


}

export default OrbitPlotter;

