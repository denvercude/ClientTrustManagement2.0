const { app, BrowserWindow } = require('electron');
const path = require('path');

let mainWindow;

app.on('ready', () => {
  mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'), // Enable preload for secure communication
      contextIsolation: true,
      nodeIntegration: false,
    },
  });

  mainWindow.loadFile(path.join(__dirname, 'index.html'));
});

// Function to navigate between pages
function loadPage(page) {
  mainWindow.loadFile(path.join(__dirname, page));
}

// Export the `loadPage` function for use in the preload script
module.exports = { loadPage };

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

const { ipcMain } = require('electron');

// Handle navigation requests from the renderer process
ipcMain.on('navigate-to', (event, page) => {
  loadPage(page);
});
