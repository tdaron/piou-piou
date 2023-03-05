import {ModalClose, ModalRoot} from "./modals.css";
import {VNode} from "preact";
import {Cross1Icon} from "@radix-ui/react-icons";

interface ModalProps {
    isOpen: boolean,
    close: () => void;
    children: VNode<any>
}

export function Modal(props: ModalProps) {

    return props.isOpen ? (
        <div class={ModalRoot}>
            <div class={ModalClose}>
                <Cross1Icon onClick={props.close}/>
            </div>
            {props.children}
        </div>


    ) : (<></>)



}