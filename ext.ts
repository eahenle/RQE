import * as vscode from 'vscode';

export function activate(context: vscode.ExtensionContext) {
    let disposable = vscode.commands.registerCommand('x11.forward', () => {
        const panel = vscode.window.createWebviewPanel(
            'x11Forwarding',
            'X11 Display',
            vscode.ViewColumn.One,
            { enableScripts: true }
        );

        panel.webview.html = getWebviewContent();
    });

    context.subscriptions.push(disposable);
}

function getWebviewContent(): string {
    return `
        <!DOCTYPE html>
        <html>
        <head>
            <script src="https://xpra.org/js/xpra-html5-client.js"></script>
        </head>
        <body>
            <canvas id="xpra-canvas"></canvas>
            <script>
                const ws_url = "ws://localhost:10000";  // Match xpra WebSocket port
                const xpraClient = new XpraHTML5Client({
                    "ws": ws_url,
                    "canvas": document.getElementById("xpra-canvas")
                });
                xpraClient.start();
            </script>
        </body>
        </html>
    `;
}

export function deactivate() {}
