import { render } from 'preact'
import { App } from './app'
import './index.css'


/*window.webSocket = new WebSocket("ws://127.0.0.1:8765");

window.webSocket.onclose = function(event) {
    if (event.wasClean) {
        alert(`[close] Connection closed cleanly, code=${event.code} reason=${event.reason}`);
    } else {
        // e.g. server process killed or network down
        // event.code is usually 1006 in this case
        alert('[close] Connection died');
    }
};

window.webSocket.onerror = function(error) {
    alert(`[error]`);
};
*/
render(<App />, document.getElementById('app') as HTMLElement)
