import React from "react";

function FormBlock(props) {

    if (props.type === "select") {

        return (
            <div className = "block">
                <label title = {props.hoverLabel}>{props.labelName}</label>
                <select name = {props.name} 
                        onChange = {props.onChange}>
                    {props.data_list.map((elm) => {return <option key = {elm} value = {elm} label = {elm}/>})}
                </select>
            </div>
        )
    }
    else {
        return (
            <div className = "block">
                <label title = {props.hoverLabel}>{props.labelName}</label>
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