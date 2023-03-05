export function sendBytes(sendMessage: any, bytes: Array<number>) {
    const buffer = new ArrayBuffer(bytes.length); // create an ArrayBuffer with 8 bytes (4 bytes for each number)
    const view = new DataView(buffer); // create a DataView for the ArrayBuffer
    bytes.forEach((n, i) => {
        view.setUint8(i, n);
    })
    sendMessage(buffer)
}