import {style} from "@vanilla-extract/css"

export const HeaderRoot = style({
    display: "flex",
    alignItems: "center",
    flexDirection: "column",
    //justifyContent: "center",
    paddingTop: 15,
    height: "20vh",
    //backgroundColor: "black",
    borderBottom: "1px solid rgba(255,255,255,0.1)",
    width: "100%"

})

export const Status = style({
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between"
})

export const Stats = style({
    marginTop: 5,
    width: "85%",
    //backgroundColor: "red",
    height: "100%",
    display: "grid",
    placeItems: "center",
    gridTemplateColumns: "1fr 1fr",
    gridTemplateRows: "1fr 1fr",
    gridTemplateAreas: `
    '. .'
    '. .'
    `,
    paddingBottom: 15

})

export const StatsDiv = style({
    display: "flex",
    alignItems: "center",
})
export const StatsP = style({
    marginLeft: 15
})