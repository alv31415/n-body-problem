import React from "react";

function FormBlock(props) {

    if (props.type === "select") {

        return (
            <div className = "block">
                <label>{props.labelName}</label>
                <select name = {props.name} style={{width: "100px"}} onChange = {props.onChange}>
                    {props.data_list.map((elm) => {return <option key = {elm} value = {elm} label = {elm}/>})}
                </select>
            </div>
        )
    }
    else {
        return (
            <div className = "block">
                <label>{props.labelName}</label>
                <input name = {props.name} 
                    type = {props.type} 
                    placeholder = {props.placeholder} 
                    value = {props.value} 
                    step = {props.step}
                    onChange = {props.onChange}/>
            </div>
        )
    }
}

export default FormBlock;