import {HeaderRoot, Stats, StatsDiv, StatsP, Status} from "./header.css";
import {useGameStore} from "../store/gameStore";
import HeartIcon, {CheckCircledIcon} from "@radix-ui/react-icons";

import {FiHeart, FiStar, RxCrossCircled} from "react-icons/all";
import {ReadyState} from "react-use-websocket";

interface HeaderProps {
    state: ReadyState,
    onStart: () => void;
}

export function Header(props: HeaderProps) {
    const [life, score] = useGameStore((state) => [state.life, state.score]);
    const connectionStatus = {
        [ReadyState.CONNECTING]: 'Connecting',
        [ReadyState.OPEN]: 'Connected',
        [ReadyState.CLOSING]: 'Closing',
        [ReadyState.CLOSED]: 'Closed',
        [ReadyState.UNINSTANTIATED]: 'Uninstantiated',
    }[props.state];
    return (
        <div className={HeaderRoot}>
            <div className={Status}>
                {connectionStatus}
                {connectionStatus == "Connected" ? <CheckCircledIcon style={{marginLeft: 8}} color={"green"}/> :  <RxCrossCircled style={{marginLeft: 8}} color={"red"}/> }
            </div>

            <div className={Stats}>
                <div className={StatsDiv}>
                    <FiHeart size={40}/> <p className={StatsP}>{life}</p>
                </div>
                <div className={StatsDiv}>
                    <FiStar size={40}/> <p className={StatsP}>{score}</p>
                </div>

                <div className={StatsDiv}>
                    <button onClick={() => {document.location.reload()}}>Connect</button>
                </div>
                <div className={StatsDiv}>
                    <button onClick={props.onStart}>Start</button>
                </div>

            </div>

        </div>
    )

}