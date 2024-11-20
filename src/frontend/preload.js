const { ipcRenderer, contextBridge } = require('electron');

// Expose a secure API to the renderer process
contextBridge.exposeInMainWorld('electronAPI', {
  navigateTo: (page) => ipcRenderer.send('navigate-to', page),
});
