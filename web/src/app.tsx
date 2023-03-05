import {useEffect, useState} from 'preact/hooks'
import './app.css'

import {sendBytes} from "./scripts/websockets";
import useWebSocket, {ReadyState} from "react-use-websocket";
import {Header} from "./components/header";
import {GiFireworkRocket} from "react-icons/all";
import {useGameStore} from "./store/gameStore";

function iOS() {
    return [
            'iPhone',
        ].includes(navigator.platform)
        // iPad on iOS 13 detection
        || (navigator.userAgent.includes("Mac") && "ontouchend" in document)
}

export function App() {
    const [acceleration, setAcceleration] = useState<DeviceMotionEventAcceleration>(undefined);
    const [socketUrl, setSocketUrl] = useState('ws://192.168.83.26:8000');
    const {sendMessage, lastMessage, readyState } = useWebSocket(socketUrl, {
        shouldReconnect: (closeEvent) => true
    });
    const [setLife, setScore] = useGameStore((state) => [state.setLife, state.setScore]);
    let modifier = iOS() ? -1 : 1; //because iOS sucks
    let min = 1;

    useEffect(() => {
        if (readyState == ReadyState.OPEN) {
            setLife(3)
            setScore(0)
        }
    }, [readyState])

    const setIp = () => {
        let old = localStorage.getItem("ip")
        let ip = prompt("Ip address ?", old)
        if (ip.length < 2) {
            alert("Ip address is necessary")
            setIp()
        }
        localStorage.setItem('ip', ip)
        setSocketUrl("ws://"+ip+":8000")
    }

    useEffect(() => {
        setIp()
    }, [])
    useEffect(() => {
        if (lastMessage == undefined) {
            return
        }
        console.log("message got !")
        var reader = new FileReader();
        reader.readAsArrayBuffer(lastMessage.data);
        reader.addEventListener("loadend", function(e)
        {
            //@ts-ignore
            let buffer = new Uint8Array(e.target.result);  // arraybuffer object
            if (buffer[0] == 0) {
                setLife(buffer[1])
            }
            if (buffer[0] == 1) {
                console.log(buffer)
                var u32bytes = buffer.buffer.slice(-4); // last four bytes as a new `ArrayBuffer`
                var dv = new DataView((new Uint8Array(buffer.buffer.slice(-4))).buffer);
                //@ts-ignore
                var uint = dv.getUint32();
                setScore(uint)
            }
            if (buffer[0] == 3) {
                navigator.vibrate(100)
            }
        });
    }, [lastMessage])


    useEffect(() => {
        if (acceleration == undefined) {
            return
        }
        let [right, left] = modifier * acceleration.x > 0 ? [0, modifier * acceleration.x] : [-1 * modifier * acceleration.x, 0]
        let [up, bottom] = modifier * acceleration.y > 0 ? [0, modifier * acceleration.y] : [-1 * modifier * acceleration.y, 0]
        sendBytes(sendMessage, [
            1, //Move message type
            up > min ? up + 1 : 0,
            bottom > min ? bottom + 1: 0,
            left > min ? left + 1: 0,
            right > min ? right + 1 : 0]
        ) //+1 to make them more reactive hehe

    }, [acceleration])
    const shoot = () => {
        console.log("sent")
        sendBytes(sendMessage, [0]) //Shoot message
    }
    useEffect(() => {
        if (iOS()) {
            //@ts-ignore because typescript sucks
            DeviceMotionEvent.requestPermission().then(response => {
                if (response != 'granted') {
                    alert("Uncompatible navigator")

                }
            });
        }
        const handler = (event) => {
            setAcceleration(event.accelerationIncludingGravity);
        }
        window.addEventListener('devicemotion', handler);
    })




    return (
        <>
            <Header onStart={() => {
                sendBytes(sendMessage, [69])
            }} state={readyState}/>
            <div style={{
                display: "grid",
                placeItems: "center",
                height: "70vh",
                width: "100%",
            }}>
                <div style={{
                    padding: 110,
                    border: "1px dashed white",
                    borderRadius: 25
                }}  onClick={shoot}>
                    <GiFireworkRocket size={100}/>

                </div>

            </div>


        </>
    )
}
