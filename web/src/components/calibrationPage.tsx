import {useState} from "preact/hooks";

export function CalibrationPage() {
    const [calibState, setCalibState] = useState("x");
    


    return (
        <div style={{color: "white", marginLeft: 15, textAlign:"center"}}>
            <h3>Currently calibrating {calibState}</h3>

        </div>
    )
}