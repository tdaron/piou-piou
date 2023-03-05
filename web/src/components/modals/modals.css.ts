import { style } from '@vanilla-extract/css';

export const ModalRoot = style({
    position: "absolute",
    display: "block",
    textAlign: "left",
    top: "15%",
    left: '5%',
    backgroundColor: "rgb(53,53,53)",
    borderRadius: 15,
    zIndex: 2,
    width: "90%",
    height: "70%",
})

export const ModalClose = style({
    position: "relative",
    width: "90%",
    textAlign: "right",
    padding: 15
})
